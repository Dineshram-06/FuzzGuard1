import argparse
import sys
import time
from datetime import datetime
from modules.scanner import WebFuzzer
from modules.detector import TechDetector
from modules.reporter import ReportEngine
from modules.utils import load_wordlist, check_robots, rotate_ua, setup_logger
import logging
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SIH1750 Web Fuzzer: Ethical vulnerability scanner for web applications."
    )
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., https://example.com)")
    parser.add_argument("-w", "--wordlist", default="wordlists/common.txt", help="Path to wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of concurrent threads")
    parser.add_argument("-o", "--output", choices=["json", "md", "csv"], default="json", help="Output format")
    parser.add_argument("--rate-limit", type=int, default=10, help="Max requests per second")
    parser.add_argument("--user-agent", help="Custom User-Agent string")
    parser.add_argument("--proxy", help="Proxy URL (e.g., http://proxy:8080)")
    parser.add_argument("--ignore-robots", action="store_true", help="Bypass robots.txt check")
    parser.add_argument("--demo", action="store_true", help="Enable demo mode for presentations")
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logger()
    
    print(f"{Fore.CYAN}🚀 SIH1750 Web Application Fuzzer v1.0{Style.RESET_ALL}")
    print("=" * 40)
    print(f"{Fore.RED}⚠️ LEGAL NOTICE: Only scan targets you have explicit permission to test.{Style.RESET_ALL}")
    print(f"{Fore.RED}Ensure compliance with responsible disclosure practices.{Style.RESET_ALL}")
    print("=" * 40 + "\n")
    
    start_time = time.time()
    target_url = args.url.rstrip("/")
    wordlist = load_wordlist(args.wordlist)
    
    if not args.ignore_robots:
        if not check_robots(target_url):
            print(f"{Fore.RED}[ERROR] Robots.txt disallows scanning. Use --ignore-robots to proceed.{Style.RESET_ALL}")
            sys.exit(1)
    
    print(f"Target: {target_url}")
    print(f"Threads: {args.threads} | Rate Limit: {args.rate_limit} req/s")
    print(f"Wordlist: {args.wordlist} ({len(wordlist)} entries)\n")
    
    if args.demo:
        print(f"{Fore.MAGENTA}[DEMO] Running in demo mode with enhanced visuals.{Style.RESET_ALL}")
        time.sleep(1)
    
    print(f"{Fore.BLUE}[INFO] Detecting technologies...{Style.RESET_ALL}")
    detector = TechDetector(target_url, proxy=args.proxy)
    tech_stack = detector.identify_tech()
    print(f"{Fore.GREEN}[TECH] Detected: {', '.join(tech_stack or ['None'])} {Style.RESET_ALL}\n")
    
    if "WordPress" in tech_stack:
        wordlist.extend(load_wordlist("wordlists/wordpress.txt"))
    if "Django" in tech_stack:
        wordlist.extend(load_wordlist("wordlists/django.txt"))
    wordlist.extend(load_wordlist("wordlists/api.txt"))
    
    if args.demo:
        print(f"{Fore.MAGENTA}[DEMO] Tailoring wordlist based on detected tech to optimize scan.{Style.RESET_ALL}")
        time.sleep(1)
    
    fuzzer = WebFuzzer(
        target_url=target_url,
        wordlist=wordlist,
        threads=args.threads,
        rate_limit=args.rate_limit,
        user_agent=args.user_agent,
        proxy=args.proxy,
        demo_mode=args.demo
    )
    findings = fuzzer.run_scan()
    
    print("\n" + "=" * 40)
    print(f"{Fore.GREEN}🎯 Scan Completed{Style.RESET_ALL}")
    total_scanned = len(wordlist)
    found = len(findings)
    high_risk = sum(1 for f in findings if f.get("risk") == "High")
    elapsed = time.time() - start_time
    print(f"Total Scanned: {total_scanned} | Found: {found} | High Risk: {high_risk}")
    print(f"Time: {elapsed // 60:.0f}m {elapsed % 60:.1f}s | Avg Speed: {total_scanned / elapsed:.1f} req/s")
    print("=" * 40 + "\n")
    
    reporter = ReportEngine(findings, target_url, tech_stack, elapsed)
    output_file = f"reports/scan.{args.output}"
    if args.output == "json":
        reporter.save_json(output_file)
    elif args.output == "md":
        reporter.save_markdown(output_file)
    elif args.output == "csv":
        reporter.save_csv(output_file)
    
    if args.demo:
        print(f"{Fore.MAGENTA}[DEMO] Reports generated. These findings could indicate critical vulnerabilities like exposed admin panels.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()