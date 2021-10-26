f=open('test.txt','w')
if f != None:
    print('檔案開啟成功')
f.close()

f = open('test.txt', 'w', encoding='utf-8')
if f != None:
    f.write('小白')
f.close()

f = open('test.txt', 'r', encoding='utf-8')
if f != None:
    s=f.read()
    print(s)
f.close()

f = open('test.txt', 'a', encoding='utf-8')
if f != None:
    f.write('小黑')
f.close()

f = open('test.txt', 'r', encoding='utf-8')
if f != None:
    s = f.readlines()
    print(s)
f.close()
