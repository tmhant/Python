from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import sys
from multiprocessing import Process

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None

    try:
        Obj = soup(html,'html.parser')
        title = Obj.body.a
    except AttributeError:
        return None
    print(title)


if __name__ == '__main__':
    #title = getTitle("https://www.mycard.com.tw")
    p = Process(target=getTitle, args=('https://www.mycard.com.tw',))
    p.start()
    p.join()
    #if title == None:
        #print('找不到')
    #else:
        #print(title)
