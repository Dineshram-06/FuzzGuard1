import requests
import re
from typing import List, Optional
from modules.utils import rotate_ua

class TechDetector:
    def __init__(self, target_url: str, proxy: Optional[str] = None):
        self.target_url = target_url
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        self.session = requests.Session()

    def identify_tech(self) -> List[str]:
        tech = []
        headers = {"User-Agent": rotate_ua()}
        try:
            response = self.session.get(self.target_url, headers=headers, proxies=self.proxy, timeout=10, verify=False)
            server = response.headers.get("Server", "").lower()
            powered_by = response.headers.get("X-Powered-By", "").lower()
            content = response.text.lower()
            
            if "wordpress" in content or "wp-content" in content:
                version = re.search(r'wordpress (\d+\.\d+)', content)
                tech.append(f"WordPress {version.group(1) if version else ''}")
            
            if "django" in powered_by or "django" in content:
                tech.append("Django")
            
            if "apache" in server:
                version = re.search(r'apache/(\d+\.\d+)', server)
                tech.append(f"Apache {version.group(1) if version else ''}")
            
            if "php" in powered_by:
                version = re.search(r'php/(\d+\.\d+)', powered_by)
                tech.append(f"PHP {version.group(1) if version else ''}")
        
        except requests.exceptions.RequestException:
            pass
        
        return tech if tech else ["Unknown"]