import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import json

def clean(data):
    soup = BeautifulSoup(data, "html.parser")
    return soup.get_text().replace("\n", " ")

def shortener(url):
    return url

def Tiktok(query):
    url = "https://lovetik.com/api/ajax/search"
    data = {"query": query}

    kampret = requests.post(url, data=urlencode(data), headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })
    
    if kampret.status_code != 200:
        return json.dumps({
            "creator": "maschyodjin",
            "status": kampret.status_code,
            "message": "Error fetching data from API"
        }, indent=4)
    
    kampret_data = kampret.json()
    result = {
        "creator": "maschyodjin",
        "title": clean(kampret_data.get("desc", "")),
        "author": clean(kampret_data.get("author", "")),
        "nowm": shortener(kampret_data.get("links", [{}])[0].get("a", "").replace("https", "http")),
        "watermark": shortener(kampret_data.get("links", [{}])[1].get("a", "").replace("https", "http")),
        "audio": shortener(kampret_data.get("links", [{}])[2].get("a", "").replace("https", "http")),
        "thumbnail": shortener(kampret_data.get("cover", ""))
    }
    
    return json.dumps(result, indent=4)

result = Tiktok("https://vm.tiktok.com/ZSjFP3Lrx/")
print(result)
