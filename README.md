# WEBCHOMPA: Comprehensive Web Recon & Fuzzing Script

WEBCHOMPA is an automated reconnaissance and fuzzing tool specifically designed for web applications. It combines powerful open-source security tools to efficiently perform information gathering, vulnerability scanning, and enumeration, organizing the results clearly and logically.

## Features
- **Nmap scanning** for comprehensive port and service enumeration.
- **FFUF fuzzing** for discovering directories and parameters.
- **WPScan integration** for detecting WordPress vulnerabilities.
- **Nikto** for identifying web server vulnerabilities.
- **SearchSploit and Vulners** for vulnerability matching.
- **OSINT collection** with theHarvester.
- **Wayback URLs** extraction for historical URLs.
- **WhatWeb** for website fingerprinting.
- **Automatic suggestions** for follow-up exploitation commands.
- Structured output in **Markdown** or **CSV** format.

## Installation

### Dependencies
Ensure the following tools are installed:

```bash
sudo apt install nmap ffuf wpscan nikto theharvester whatweb golang-go
sudo apt install seclists
```

### Optional Tools
```bash
go install github.com/tomnomnom/waybackurls@latest
searchsploit -u
```

Clone the repository:
```bash
git clone https://github.com/yourusername/webchompa.git
cd webchompa
```

## Usage

Basic usage:
```bash
python3 webchompa.py https://example.com
```

Full options:
```bash
python3 webchompa.py <target> [--stealth] [--company COMPANY_NAME] [--output {markdown,csv}]
```

### Examples
Perform a comprehensive scan in stealth mode:
```bash
python3 webchompa.py https://example.com --stealth
```

Include OSINT information about a company:
```bash
python3 webchompa.py https://example.com --company "ExampleCorp"
```

Set CSV as output format:
```bash
python3 webchompa.py https://example.com --output csv
```

## Output
Results are automatically saved to an organized folder named after the target hostname or IP:

```
example.com/
├── ffuf_dirs.json
├── ffuf_params.json
├── nikto_scan.txt
├── nmap_scan.txt
├── osint_results.* (if OSINT enabled)
├── searchsploit_results.txt
├── suggestions.txt
├── vulners_results.json
├── wayback_results.txt
├── whatweb_results.txt
└── wpscan_results.json
```

## Customization
Replace the placeholder API keys in the script:
```python
BURP_API_KEY = "YOUR_BURP_API_KEY"
VULNERS_API_KEY = "YOUR_VULNERS_API_KEY"
WPSCAN_API_KEY = "YOUR_WPSCAN_API_KEY"
```

## Contribution
Feel free to submit pull requests or issues to help enhance WEBCHOMPA.

## Disclaimer
Use this script responsibly and only against targets for which you have explicit permission. The author is not responsible for misuse or any damages caused by the script.

## License
WEBCHOMPA is licensed under the MIT License.
