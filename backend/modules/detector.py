import re
from modules.utils import get_logger

logger = get_logger(__name__)

class TechnologyDetector:
    def __init__(self):
        self.patterns = {
            'Server': r'Server: (.*)',
            'X-Powered-By': r'X-Powered-By: (.*)',
            'Cookie': r'Set-Cookie: (.*)'
        }

    def detect(self, response):
        tech = []
        for header, pattern in self.patterns.items():
            value = response.headers.get(header)
            if value:
                match = re.search(pattern, value)
                if match:
                    tech.append(match.group(1))
        # Simple HTML check if needed
        if 'wordpress' in response.text.lower():
            tech.append('WordPress')
        return tech