# Apple Enterprise Networks External Dynamic List

> ** Quick Start / Status**
> 
> **You likely do not need to run this script manually.**
> 
> This repository is automated via GitHub Actions to scan Apple's requirements daily. The **[`domains.txt`](domains.txt)** and **[`ports.txt`](ports.txt)** files in this repository are already up-to-date and ready for use in your firewalls or EDLs.

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

## Usage (Manual Execution)

*Follow these steps only if you wish to fork the project or force a manual update.*

This project uses **[uv](https://github.com/astral-sh/uv)** for dependency management and Python version control. This ensures you run the script with the exact correct version of Python and OpenSSL, regardless of your system defaults.

### 1. Install uv
If you don't have `uv` installed, get it via Homebrew or the official installer:

```bash
# macOS / Linux
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

### 2. Clone and Sync
Clone the repo and instruct `uv` to build the environment. This will automatically fetch the correct Python version and install dependencies defined in `uv.lock`.

```bash
git clone [https://github.com/vimrichie/apple_edl.git](https://github.com/vimrichie/apple_edl.git)
cd apple_edl
uv sync
```

### 3. Run the Scraper
Use `uv run` to execute the script inside the managed environment automatically.

```bash
uv run applescrape.py
```

## Automation (GitHub Actions)

This repository includes a GitHub Actions workflow (`.github/workflows/check_apple_change.yml`) that runs the scraper automatically.

* **Schedule:** Runs daily at **10:00 AM PST** (18:00 UTC).
* **Logic:**
  1. Spins up an Ubuntu runner.
  2. Sets up `uv` for fast environment caching.
  3. Executes the extraction script.
  4. **Commits and Pushes** only if changes are detected. If the data hasn't changed, the workflow exits cleanly without creating empty commits.

## Technical Notes

### Requirements
* **uv** (Package & Project Manager)
* Python 3.12+ (Managed automatically by `uv` via `.python-version`)

### Dependencies
* `requests`
* `beautifulsoup4`
* `urllib3` (Secure OpenSSL backend)

## License

This project is licensed under the GNU General Public License v3.0.
