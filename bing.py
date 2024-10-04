import requests as kontol
from bs4 import BeautifulSoup as skrep

class BingSearchScraper:
    def __init__(self):
        self.url = "https://www.bing.com/search"

    def Pencarian(self, query, hasil):
        a = {
            'q': query,
            'count': hasil
        }

        c = kontol.get(self.url, params=a)

        if c.status_code != 200:
            print(f"[!] {c.status_code} [!]")
            return []

        o = skrep(c.text, 'html.parser')
        rsl = []
        for hitam in o.find_all('li', class_="b_algo")[:hasil]:
            tlt = hitam.find('h2').text
            link = hitam.find('a')['href']
            snp = hitam.find('p').text if hitam.find('p') else "undefined"
            rsl.append({
                'title': tlt,
                'link': link,
                'description': snp
            })
        return rsl
