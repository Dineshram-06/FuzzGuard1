import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from modules.utils import get_logger

logger = get_logger(__name__)

class WebApplicationFuzzer:
    def __init__(self, base_url, threads=5, rate=10):
        self.base_url = base_url.rstrip('/')
        self.threads = threads
        self.rate = rate  # Requests per second
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
        ]
        self.ua_index = 0
        self.lock = threading.Lock()
        self.last_request_time = time.time()

    def get_next_ua(self):
        with self.lock:
            ua = self.user_agents[self.ua_index]
            self.ua_index = (self.ua_index + 1) % len(self.user_agents)
            return ua

    def safe_request(self, path, callback):
        # Rate limiting: ensure at least 1/rate seconds between requests
        with self.lock:
            elapsed = time.time() - self.last_request_time
            wait_time = (1.0 / self.rate) - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_request_time = time.time()

        url = f"{self.base_url}{path}"
        headers = {'User-Agent': self.get_next_ua()}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            callback(path, response)
        except requests.RequestException as e:
            logger.warning(f"Request failed for {path}: {e}")
            callback(path, None)

    def fuzz(self, wordlist, callback):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.safe_request, path, callback) for path in wordlist]
            for future in as_completed(futures):
                future.result()  # Ensure exceptions are raised

                