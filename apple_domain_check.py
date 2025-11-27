import requests
from bs4 import BeautifulSoup
import re
import sys


def fetch_page_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as error:
        print(f"[!] Network Error: {error}")
        return None


def check_if_domain(text):
    if not text: return False
    domains = text.strip()
    if '.' not in domains: return False
    if len(domains) < 4 or len(domains) > 60: return False
    if ' ' in domains: return False
    if any(k in domains for k in ['apple', 'icloud', 'mzstatic', 'cdn', 'digicert', 'symcb']):
        return True
    if re.match(r'^[\w\-.*]+\.[a-z]+$', domains):
        return True
    return False


def extract_ports_from_text(text):
    if not text: return []
    objects = re.findall(r'\b\d+\b', text)
    valid_ports = []
    for port_objects in objects:
        try:
            port = int(port_objects)
            if 0 < port < 65535:
                valid_ports.append(port)
        except ValueError:
            pass
    return valid_ports

def scrape_by_pattern(soup):
    found_domains = set()
    found_ports = set()
    rows = soup.find_all('tr')
    print(f"Scanning {len(rows)} rows for data patterns...")
    for row in rows:
        cells = row.find_all(['td', 'th'])
        row_text = [c.get_text(strip=True) for c in cells]
        domain_found_in_row = False
        row_domains = []
        for text in row_text:
            parts = text.replace('\n', ' ').split()
            for part in parts:
                if check_if_domain(part):
                    clean_domain = part.rstrip('.')
                    row_domains.append(clean_domain)
                    domain_found_in_row = True
        if domain_found_in_row:
            for d in row_domains:
                found_domains.add(d)
            for text in row_text:
                if check_if_domain(text):
                    continue
                ports = extract_ports_from_text(text)
                for p in ports:
                    found_ports.add(p)
    return sorted(list(found_domains)), sorted(list(found_ports))


def save_info_to_txt_files(data_list, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for item in data_list:
                f.write(f"{item}\n")
        print(f"[+] Saved {len(data_list)} items to {filename}")
    except IOError as error:
        print(f"[!] Error writing to {filename}: {error}")


def main():
    apple_url = "https://support.apple.com/en-us/101555"
    print("1. Fetching page...")
    soup = fetch_page_content(apple_url)
    if not soup:
        sys.exit(1)
    print("2. Scraping using Pattern Matching (Header-Free)...")
    domains, ports = scrape_by_pattern(soup)
    print("3. Saving files...")
    save_info_to_txt_files(domains, 'domains.txt')
    save_info_to_txt_files(ports, 'ports.txt')
    print("Done.")


if __name__ == "__main__":
    main()