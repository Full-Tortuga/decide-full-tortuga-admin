from bs4 import BeautifulSoup as bs
import lxml
import urllib.request as request
from urllib.parse import  urlparse

#returns images of a voting (FOR NOW)
def get_graphs(link):
    file=request.urlopen(link)
    s=bs(file, "lxml")
    images=s.find_all("img")
    urls=[]
    for img in images:
        img_url=img.attrs.get("src")
        if not img_url:
            continue
        if validate_url(img_url):
            urls.append(img_url)
    if len(urls) == 0:
        urls=False
    return urls

#checks whether url is valid or not (Might be removed in a near future)
def validate_url(link):
    parse=urlparse(link)
    return bool(parse.netloc) and bool(parse.scheme) 