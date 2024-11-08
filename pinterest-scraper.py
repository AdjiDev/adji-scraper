"""
Forbidden to the watermark
telegram: t.me/adjidev
Github: github.com/adjidev
"""

import requests
from bs4 import BeautifulSoup
import os
import hashlib
import json
import random

def IpSpoof():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

def Header():
    return {
        #"X-Forwarded-For": IpSpoof(),
        #"X-Forwarded-Host": "pinterest.com",
        #"X-Real-Ip": IpSpoof(),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        #"Accept-Language": "en-US,en;q=0.5",
        #"Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.pinterest.com/",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Connection": "keep-alive",
        #"DNT": "1"
    }


class PinterestScraper:
    
    def __init__(self):
        self.base_url = "https://id.pinterest.com/search/pins/?autologin=true&q="
        self.session_cookie = os.getenv("PINTEREST_SESSION")
        if not self.session_cookie:
            raise ValueError("PINTEREST_SESSION cookie is not set in environment variables.")
        
        self.headers = Header()
        self.headers["cookie"] = self.session_cookie

    def search(self, query):
        try:
            response = requests.get(f"{self.base_url}{query}", headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            for element in soup.select('div > a img'):
                url = element.get('src')
                if url:
                    url = url.replace("236", "736")
                    img_id = hashlib.md5(url.encode()).hexdigest()
                    
                    results.append({
                        "id": img_id,
                        "url": url
                    })

            if results:
                results.pop(0)

            return {
                "creator": "adjisan",
                "status": 200,
                "query": query,
                "total_result": len(results),
                "data": results
            }

        except requests.HTTPError as http_err:
            return {
                "creator": "adjisan",
                "status": response.status_code,
                "message": f"HTTP error occurred: {http_err}"
            }
        except requests.RequestException as req_err:
            return {
                "creator": "adjisan",
                "status": 500,
                "message": f"Request error occurred: {req_err}"
            }
        except Exception as e:
            return {
                "creator": "adjisan",
                "status": 500,
                "message": f"An unexpected error occurred: {e}"
            }

def test():
    scraper = PinterestScraper()
    result = scraper.search("anime")
    print(json.dumps(result, indent=4))

test()
