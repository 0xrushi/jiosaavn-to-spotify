import json
import os
import logger
import requests
import urllib3.request
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from pyDes import *

# Pre Configurations
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
unicode = str
raw_input = input


def setProxy():
    base_url = 'http://h.saavncdn.com'
    proxy_ip = ''
    if ('http_proxy' in os.environ):
        proxy_ip = os.environ['http_proxy']
    proxies = {
        'http': proxy_ip,
        'https': proxy_ip,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
    }
    return proxies, headers


def getPlayList(listId):
    songs_json = []
    respone = requests.get(
        'https://www.saavn.com/api.php?listid={0}&_format=json&__call=playlist.getDetails'.format(listId), verify=False)
    if respone.status_code == 200:
        songs_json = list(filter(lambda x: x.startswith("{"), respone.text.splitlines()))[0]
        songs_json = json.loads(songs_json)
    return songs_json

pp="fff"
tracks=[]
artists=[]
def processPlaylist(url):
    input_url = url.strip()
    try:
        proxies, headers = setProxy()
        res = requests.get(input_url, proxies=proxies, headers=headers)
    except Exception as e:
        logger.error('Error accessing website error: ' + e)

    soup = BeautifulSoup(res.text, "lxml")

    try:
        getPlayListID = soup.select(".flip-layout")[0]["data-listid"]
        if getPlayListID is not None:
            print("Initiating PlayList Downloading")
            #downloadSongs(getPlayList(getPlayListID))
            #print(getPlayList(getPlayListID))
            pp=getPlayList(getPlayListID)
            #print(pp['songs'])
            for so in pp['songs']:
                # print(so['song']+"--"+so['primary_artists'])
                tracks.append(so['song'])
                artists.append(so['primary_artists'])
            return tracks, artists
            sys.exit()
    except Exception as e:
        return NULL
        print('...')
