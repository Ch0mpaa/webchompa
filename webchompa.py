import subprocess
import requests
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import os

# === User Configuration ===
BURP_API_KEY = "your key here"
BURP_API_URL = "http://127.0.0.1:1337/"
VULNERS_API_KEY = "YOUR_VULNERS_API_KEY"
WPSCAN_API_KEY = "YOUR_WPSCAN_API_KEY"

THREADS_FAST = 10
THREADS_STEALTH = 2
def print_banner():
    print(r"""
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓██████████████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█████████████▓▒░░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░
    """)
    
    print_banner()
    print("[+] Starting Comprehensive Web Recon")


parser = argparse.ArgumentParser(description="Comprehensive Web Recon & Fuzzing Script")
parser.add_argument("target", help="Target URL/IP (include http:// or https:// if URL)")
parser.add_argument("--stealth", action="store_true", help="Stealth mode (slow)")
parser.add_argument("--company", help="Company name for OSINT")
parser.add_argument("--output", choices=["markdown", "csv"], default="markdown", help="Output format")
args = parser.parse_args()

threads = THREADS_STEALTH if args.stealth else THREADS_FAST

parsed_target = urlparse(args.target)
target_host = parsed_target.netloc if parsed_target.netloc else args.target
base_url = f"{parsed_target.scheme}://{target_host}" if parsed_target.scheme else f"http://{target_host}"

# Create and navigate to output directory
output_folder = target_host.replace(':', '_')
os.makedirs(output_folder, exist_ok=True)
os.chdir(output_folder)

# Recon Functions
def run_nmap(target):
    cmd = f"nmap -p- --min-rate 1000 -sV -sC -Pn -O -sS -oN nmap_scan.txt {target}"
    subprocess.run(cmd, shell=True)

def run_ffuf_directories(url):
    cmd = f"ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -u {url}/FUZZ -t {threads} -o ffuf_dirs.json"
    subprocess.run(cmd, shell=True)

def run_ffuf_parameters(url):
    cmd = f"ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u {url}/?FUZZ=test -mc all -t {threads} -o ffuf_params.json"
    subprocess.run(cmd, shell=True)

def run_wpscan(url):
    cmd = f"wpscan --url {url} --enumerate vp --api-token {WPSCAN_API_KEY} -o wpscan_results.json"
    subprocess.run(cmd, shell=True)

def run_nikto(url):
    cmd = f"nikto -h {url} -o nikto_scan.txt"
    subprocess.run(cmd, shell=True)

def run_searchsploit(target):
    cmd = f"searchsploit {target} -w > searchsploit_results.txt"
    subprocess.run(cmd, shell=True)

def run_vulners(target):
    url = f"https://vulners.com/api/v3/search/lucene/?query={target}"
    headers = {'API-Key': VULNERS_API_KEY}
    response = requests.get(url, headers=headers)
    with open("vulners_results.json", "w") as file:
        file.write(response.text)

def run_osint(company):
    cmd = f"theHarvester -d {company} -l 100 -b all -f osint_results"
    subprocess.run(cmd, shell=True)

def run_waybackurls(target):
    cmd = f"waybackurls {target} > wayback_results.txt"
    subprocess.run(cmd, shell=True)

def run_whatweb(url):
    cmd = f"whatweb {url} > whatweb_results.txt"
    subprocess.run(cmd, shell=True)

# Suggestion Generator
def generate_suggestions():
    suggestions = [
        f"gobuster dir -u {base_url} -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt",
        f"searchsploit -m <exploit-id>",
        f"sqlmap -u '{base_url}/page?id=1'",
        f"hydra -l admin -P /usr/share/seclists/Passwords/Common-Credentials/best110.txt http-get://{target_host}"
    ]
    with open("suggestions.txt", "w") as file:
        file.write("\n".join(suggestions))

# Main Execution
print("[+] Starting Comprehensive Web Recon")

with ThreadPoolExecutor(max_workers=threads) as executor:
    executor.submit(run_nmap, target_host)
    executor.submit(run_ffuf_directories, base_url)
    executor.submit(run_ffuf_parameters, base_url)
    executor.submit(run_nikto, base_url)
    executor.submit(run_wpscan, base_url)
    executor.submit(run_searchsploit, target_host)
    executor.submit(run_vulners, target_host)
    executor.submit(run_waybackurls, target_host)
    executor.submit(run_whatweb, base_url)

    if args.company:
        executor.submit(run_osint, args.company)

generate_suggestions()

print(f"[+] Recon complete. Results saved in folder: {output_folder}")
