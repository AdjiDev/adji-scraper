"""
Real Source https://github.com/adjidev/adji-scraper
Licensed By GNU 3.0 License see https://github.com/AdjiDev/adji-scraper/blob/main/LICENSE
Selling this script without permission from adjisan will violate the humanity laws
"""

import dataclasses
import random
import requests
from bs4 import BeautifulSoup
import json

def IpSpoof():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

#+----------------------------+
#| Other headers are blocked  |
#| Header yang lain di blokir |
#+----------------------------+
def Header():
    return {
        #"X-Forwarded-For": IpSpoof(),
        #"X-Forwarded-Host": "bing.com",
        #"X-Real-Ip": IpSpoof(),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        #"Accept-Language": "en-US,en;q=0.5",
        #"Accept-Encoding": "gzip, deflate, br",
        #"Referer": "https://www.bing.com",
        #"Upgrade-Insecure-Requests": "1",
        #"Cache-Control": "no-cache",
        #"Pragma": "no-cache",
        #"Connection": "keep-alive",
        #"DNT": "1"
    }

@dataclasses.dataclass
class BingSearch:
    creator: str
    status: str = "initialized"
    message: str = ""
    query: str = ""
    total_result: int = 0
    data: list = dataclasses.field(default_factory=list)

    def RunSearch(self):
        try:
            url = f"https://www.bing.com/search?q={self.query}"
            adjisan = requests.get(url, headers=Header())
            if adjisan.status_code == 200:
                self.status = "success"
                self.message = "Search successful"
                ambatukam = BeautifulSoup(adjisan.text, 'html.parser')
                results = ambatukam.find_all('li', {'class': 'b_algo'})
                self.data = [
                    {
                        "title": result.h2.text.strip() if result.h2 else "",
                        "url": result.a['href'] if result.a else "",
                        "description": result.p.text.strip() if result.p else ""
                    }
                    for result in results if result.h2 and result.a and result.p
                ]
                self.total_result = len(self.data)
            else:
                self.status = "failed"
                self.message = f"status code {adjisan.status_code}."
        except Exception as e:
            self.status = "error"
            self.message = str(e)

    def to_json(self):
        result = {
            "creator": self.creator,
            "status": self.status,
            "message": self.message,
            "total_result": self.total_result,
            "data": self.data
        }
        return json.dumps(result, indent=4)

if __name__ == "__main__":
    kontol = BingSearch(creator="adjisan", query="python")
    kontol.RunSearch()

    print(kontol.to_json())
