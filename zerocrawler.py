from bs4 import BeautifulSoup
import os
from os import path
import requests
import sys
import urllib.parse
import re

homesite = "https://www.zerochan.net"
outdir = "IMAGES"

last_filename = None

def is_exist(fn):
    return path.exists(fn) and path.isfile(fn)

def getPages():
    global s_query
    num = ""
    site = getSite(homesite + "/" + s_query)
    p = site.find("p", class_="pagination")
    if not p:
        return 0
    try:
        digit = p.get_text("|").split("|")[0].strip().split(" ")[3].split(",")
    except:
        print("[*] No image found.")
        exit()
    for i in digit:
        num += i
    return int(num)

def getSite(url):
    return BeautifulSoup(requests.get(url).text, "lxml")

def downloadFile(url,name):
    global last_filename
    if not (path.exists(outdir) and path.isdir(outdir)):
        os.mkdir(outdir)
    filename = path.basename(url)
    print("[*] Downloading \"" + name + "\" image...")
    if is_exist(outdir + "/" + filename):
        print("[*] File with same name exist, the program will skip this step.")
        return
    with open(outdir + "/" + filename, "wb") as f:
        last_filename = filename
        f.write(requests.get(url).content)
    print("[*] Download completed")
    last_filename = None

def getImageUrl(code):
    site = getSite(homesite + "/" + code)
    try:
        int(code)
    except:
        return
    if site.find("a", class_="preview") == None:
        img_src = site.select_one("div#large > img")["src"]
    else:
        img_src = site.find("a", class_="preview")["href"]
    img_name = site.find("div",attrs={"id":"content"}).find("h1").get_text()
    downloadFile(img_src,img_name)

def getImageLink(url):
    links = []
    site = getSite(url)
    list_a = site.select("ul#thumbs2 > li > a")
    for i in list_a:
        links.append(i["href"].replace("/",""))
    return links

print("[ ZEROchan CRAWLER by Adhya Adam ]")
print("A program that will download wallpaper with given query from zerochan.")
print("")

try:
    s_query = urllib.parse.quote(input("Insert your search tag: "))
    last_page = getPages()
    if last_page == 0:
        print("[!] Images are not found.")
        exit()
    print("[*] Proceeds to download images.") 
    print("[~] Press <Ctrl> + C to stop thr program")
    for i in range(1, last_page + 1):
        list_link = getImageLink(homesite + "/" + s_query.strip() + "?p=" + str(i))
        if len(list_link) < 1:
            print("[!] No image found.")
            exit()
        for i in list_link:
            getImageUrl(i)
except KeyboardInterrupt:
    if last_filename != None and path.exists("images/"+last_filename) and path.isfile("images/"+last_filename):
        os.remove("images/"+last_filename)
    print("[!] Quitting the program.")
except:
    print("[!] Unexpexted error occured, program will automatically quit.")