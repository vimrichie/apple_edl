# Apple Enterprise Networks External Dynamic List

## Overview

This tool automates the extraction of required network hosts (domains) and ports from the official [Apple Support Enterprise Network Requirements (Article 101555)](https://support.apple.com/en-us/101555).

It is designed to help Network Engineers and System Administrators maintain accurate firewall allowlists by programmatically tracking Apple's infrastructure changes.

## How It Works

Apple's support pages frequently change their HTML structure (nested tables, mobile-responsive layouts, header visibility), which breaks traditional DOM-based web scrapers.

Instead of looking for specific HTML tags (like `<th>` or specific column indices), this tool uses **Context-Aware Pattern Matching**:

1. **Row Scanning:** It iterates through every row of data on the page.

2. **Heuristic Detection:** It identifies "Domain-like" strings based on DNS syntax and Apple-specific keywords.

3. **Proximity Association:** It only accepts integer "Ports" if they appear in the *same visual row* as a valid Domain.

This makes the scraper resilient to layout changes, column reordering, or dirty HTML data.

## Output

The script generates two clean, sorted, line-separated text files:

* **`domains.txt`**: A deduplicated list of all required FQDNs and wildcards (e.g., `*.apple.com`, `gs.apple.com`).

* **`ports.txt`**: A deduplicated list of all required TCP/UDP ports (e.g., `443`, `5223`, `2197`).

## Usage

### Local Execution

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/vimrichie/apple_edl.git](https://github.com/vimrichie/apple_edl.git)
   cd apple_edl
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Scraper:**

   ```bash
   python applescrape.py
   ```

### Automation (GitHub Actions)

This repository includes a GitHub Actions workflow (`.github/workflows/check_apple_change.yml`) that runs the scraper automatically.

* **Schedule:** Runs daily at **10:00 AM PST** (18:00 UTC).

* **Logic:** 1. Spins up an Ubuntu runner.
  2. Executes the python script.
  3. Compares the new output against the existing files.
  4. **Commits and Pushes** only if changes are detected. If the data hasn't changed, the workflow exits cleanly without creating empty commits.

## 🔧 Technical Notes

### Requirements

* Python 3.10+
* `requests`
* `beautifulsoup4`

## 📜 License

This project is licensed under the **GNU General Public License v3.0**.