############ @ Modules ############ 
from pytube import YouTube
import re
import urllib.request as urllib
import os
import pyfiglet
################################### 

def utilsYoutube(chs):
    u = {
        "link": "https://www.youtube.com/watch?v=",
        "search": "https://www.youtube.com/results?search_query=",
        "id": 0,
        "path": os.getcwd()
    }
    return (u[chs])


banner = pyfiglet.figlet_format("Y DOWNLOADER")
print(banner)

def downloadVideo(link):
    print("Downloading...")
    try:
        youtube = YouTube(link).streams.first()
        youtube.download(utilsYoutube("path"))
        print("Music: " + youtube.title + " download succesfull!")
    except:
        print("Try again...")
   
def getID():
    answer = input("Video Name: ")
    if " " in answer: answer = answer.replace(" ", "+")
    elif answer.endswith(" "): answer = answer.replace(" ", str())

    search = urllib.urlopen(utilsYoutube("search") + answer)
    
    compiles = re.compile(r"watch\?v=(\S{11})")
    findAll = compiles.findall(search.read().decode())
    
    return findAll[utilsYoutube("id")]
    
def getVideo():
    return downloadVideo(utilsYoutube("link") + getID())


getVideo()
