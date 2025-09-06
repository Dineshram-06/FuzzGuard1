import random
import requests
from typing import List, Dict, Optional
from urllib.parse import urljoin
import logging

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/17.2",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

def load_wordlist(filename: str) -> List[str]:
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error(f"Wordlist {filename} not found")
        return []

def check_robots(target_url: str) -> bool:
    try:
        response = requests.get(urljoin(target_url, "/robots.txt"), timeout=5)
        if response.status_code == 200 and "Disallow: /" in response.text:
            return False
        return True
    except:
        return True

def rotate_ua(custom_ua: Optional[str] = None) -> str:
    return custom_ua or random.choice(USER_AGENTS)

def classify_response(result: Dict) -> Dict:
    path = result["url"].split("/")[-1].lower()
    if any(kw in path for kw in ["admin", "dashboard", "login"]):
        result["type"] = "Admin Panel"
        result["risk"] = "High"
    elif any(kw in path for kw in ["config", "backup", ".bak"]):
        result["type"] = "Configuration File"
        result["risk"] = "High"
    elif "api" in path or "graphql" in path:
        result["type"] = "API Endpoint"
        result["risk"] = "Medium"
    else:
        result["type"] = "Directory/File"
        result["risk"] = "Low"
    return result

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )