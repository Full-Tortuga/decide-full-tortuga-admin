from bs4 import BeautifulSoup as bs
import urllib.request as request
from urllib.parse import  urlparse

#returns images of a voting
def get_graphs(link):
    file=request.urlopen(link)
    s=bs(file, "lxml")
    images=s.find_all("img")
    urls=[]
    for img in images:
        img_url=img.attrs.get("src")
        if not img_url:
            continue
    if len(urls) == 0:
        urls=False
    return urls