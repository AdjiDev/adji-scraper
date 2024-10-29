import requests
from bs4 import BeautifulSoup
import os
import hashlib
import json

class PinterestScraper:
    
    def __init__(self):
        self.base_url = "https://id.pinterest.com/search/pins/?autologin=true&q="
        self.session_cookie = os.getenv("PINTEREST_SESSION")
        if not self.session_cookie:
            raise ValueError("PINTEREST_SESSION cookie is not set in environment variables.")
        
        self.headers = {
            "cookie": self.session_cookie
        }

    def search(self, query):
        try:
            kampret = requests.get(f"{self.base_url}{query}", headers=self.headers)
            kampret.raise_for_status()

            soup = BeautifulSoup(kampret.text, "html.parser")
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
                "creator": "maschyodjin",
                "status": 200,
                "query": query,
                "total_result": len(results),
                "data": results
            }

        except requests.HTTPError as http_err:
            return {
                "creator": "maschyodjin",
                "status": kampret.status_code,
                "message": f"HTTP error occurred: {http_err}"
            }
        except requests.RequestException as req_err:
            return {
                "creator": "maschyodjin",
                "status": 500,
                "message": f"Request error occurred: {req_err}"
            }
        except Exception as e:
            return {
                "creator": "maschyodjin",
                "status": 500,
                "message": f"An unexpected error occurred: {e}"
            }

def test():
    scraper = PinterestScraper()
    result = scraper.search("loli anime")
    print(json.dumps(result, indent=4))

test()
