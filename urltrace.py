import urllib.request as ur
from bottle import route, run
import webbrowser
import requests
from bs4 import BeautifulSoup as soup, element
url="https://www.mycard.com.tw/contact.php"
#conn=ur.urlopen(url)
#print(conn)
#mydata=conn.read().decode('utf-8')
#print(mydata)
#print(conn.status)
#print(conn.getheader('Content-Type'))
#for key,value in conn.getheaders():
    #print(key,value) 
#@route('/')
#def home():
    #return 'home'
#run(host='localhost',port='9999')

#webbrowser.open_new(url)

result = requests.get(url)
page = result.text
doc = soup(page)
links = [element.get('href') for element in doc.find_all('a')]
for value in links:
    print(value)
