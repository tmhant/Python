import threading
import time

def job(num):
        print('Child Thread:',num)
        time.sleep(1)

threads = []
for i in range(5):
    threads.append(threading.Thread(target=job, args=(i,)))
    threads[i].start()


for i in range(3):
    threads[i].join()
    print("Main Thread:",i)
    time.sleep(1)

print("Done")
