from bs4 import BeautifulSoup
import os
from os import path
import requests
import sys
from colorama import Fore, Style, init
import urllib.parse
import re
import ctypes


init()

VERSION = "1.2"
homesite = "https://www.zerochan.net"
outdir = "IMAGES"

last_filename = None

ctypes.windll.kernel32.SetConsoleTitleW(f"Zerocrawner v{VERSION}")

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
        return sys.maxsize
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
        print(Fore.YELLOW + "[*] File with same name exist, the program will skip this step." + Fore.RESET)
        return
    with open(outdir + "/" + filename, "wb") as f:
        last_filename = filename
        f.write(requests.get(url).content)
    print(Fore.LIGHTGREEN_EX + "[*] Download completed" + Fore.RESET)
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

def search_tag(tag_query):
    file_downloaded = 0
    try:
        last_page = getPages()
        if last_page == 0:
            print(f"{Fore.RED}[!] Images are not found.{Fore.RESET}")
            return
        print(f"{Fore.BLUE}[*] Proceeds to download images.{Fore.RESET}") 
        print(f"{Fore.YELLOW}[~] Press <Ctrl> + C to stop the program.{Fore.RESET}")
        for i in range(1, last_page + 1):
            list_link = getImageLink(homesite + "/" + tag_query.strip() + "?p=" + str(i))
            if len(list_link) < 1:
                if file_downloaded == 0: print(f"{Fore.RED}[!] Images are not found.{Fore.RESET}")
                return
            for i in list_link:
                file_downloaded = file_downloaded + 1
                getImageUrl(i)
    except KeyboardInterrupt:
        if last_filename != None and path.exists("images/"+last_filename) and path.isfile("images/"+last_filename):
            os.remove("images/" + last_filename)
        print(f"{Fore.LIGHTYELLOW_EX}[!] Quitting the progress.{Fore.RESET}")
    except:
        print(f"{Fore.RED}[!] Unexpexted error occured, progress will automatically stop.{Fore.RESET}")

print(f"{Style.DIM}[ {Fore.LIGHTCYAN_EX}ZEROchan CRAWLER{Fore.RESET} by {Fore.LIGHTGREEN_EX}Adhya Adam {Fore.RESET}]{Style.RESET_ALL} v{VERSION}")
print(f"{Fore.LIGHTYELLOW_EX}A program that will download wallpaper with given query from zerochan.{Fore.RESET}")

        
while True:
    try:
        print("")
        tag = input("Insert your search tag: ")
        s_query = urllib.parse.quote(tag)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Quitting the program.{Fore.RESET}")
        break
    search_tag(s_query)