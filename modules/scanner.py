import requests
import threading
import queue
import time
from urllib.parse import urljoin
from typing import List, Dict, Optional
from modules.utils import rotate_ua, classify_response
from colorama import Fore, Style
import logging

class WebFuzzer:
    def __init__(self, target_url: str, wordlist: List[str], threads: int, rate_limit: int,
                 user_agent: Optional[str] = None, proxy: Optional[str] = None, demo_mode: bool = False):
        self.target_url = target_url
        self.wordlist = wordlist
        self.threads = min(threads, 50)  # Cap for safety
        self.rate_limit = max(1, min(rate_limit, 50))  # Enforce ethical limits
        self.user_agent = user_agent
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        self.demo_mode = demo_mode
        self.findings: List[Dict] = []
        self.lock = threading.Lock()
        self.last_request = 0
        self.task_queue = queue.Queue()
        for path in wordlist:
            self.task_queue.put(path)
        self.session = requests.Session()

    def _send_request(self, path: str) -> Optional[Dict]:
        url = urljoin(self.target_url, path)
        headers = {"User-Agent": rotate_ua(self.user_agent)}
        try:
            response = self.session.get(url, headers=headers, proxies=self.proxy, timeout=10, verify=False)
            return {
                "url": url,
                "status": response.status_code,
                "length": len(response.content),
                "headers": dict(response.headers),
                "content_snippet": response.text[:200]
            }
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch {url}: {str(e)}")
            return None

    def _worker(self):
        while not self.task_queue.empty():
            with self.lock:
                elapsed = time.time() - self.last_request
                delay = (1 / self.rate_limit) - elapsed
                if delay > 0:
                    time.sleep(delay)
                self.last_request = time.time()
            
            path = self.task_queue.get()
            result = self._send_request(path)
            if result and result["status"] in (200, 301, 302):
                finding = classify_response(result)
                with self.lock:
                    self.findings.append(finding)
                    color = Fore.GREEN if finding["status"] == 200 else Fore.YELLOW
                    print(f"{color}[✓] {finding['status']} {finding['url']} \t[{finding['type']}] {Style.RESET_ALL}")
                    if self.demo_mode:
                        print(f"{Fore.MAGENTA}[DEMO] {finding['type']} found. Potential security risk if unprotected.{Style.RESET_ALL}")
                        time.sleep(0.5)
            self.task_queue.task_done()

    def run_scan(self) -> List[Dict]:
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self._worker)
            t.start()
            threads.append(t)
        self.task_queue.join()
        for t in threads:
            t.join()
        return self.findings