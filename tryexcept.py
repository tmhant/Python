from os import read
import sys
try:
    f=open("stepsa.txt","r", encoding="utf-8")
    s=f.readlines()
    print(s)
except FileNotFoundError as err:
    print("找不到檔案",format(err))
except:
    print(sys.exc_info())
