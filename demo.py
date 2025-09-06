import subprocess
import time
import os

def run_demo():
    print(f"{Fore.CYAN}SIH1750 Web Fuzzer: Hackathon Demo{Style.RESET_ALL}")
    print("Step 1: Starting vulnerable test application...")
    test_proc = subprocess.Popen(["python", "demo/test_app.py"])
    time.sleep(3)  # Wait for server
    
    print("\nStep 2: Fuzzing for vulnerabilities...")
    os.system("python fuzzer.py -u http://localhost:5000 -w wordlists/common.txt -t 10 -o md --demo --rate-limit 5")
    
    print("\nStep 3: Security Implications")
    print("- Exposed /admin/: Could allow unauthorized access to sensitive controls.")
    print("- Exposed /backup/config.txt: Leaked credentials lead to data breaches.")
    print("Value: Automates discovery, saving hours of manual testing.")
    
    print("\nStep 4: Report Generation")
    print("Check reports/scan.md for client-ready output.")
    
    print("\nDemo Complete: Ethical, efficient, and impactful vulnerability scanning.")
    test_proc.terminate()

if __name__ == "__main__":
    run_demo()