import threading
import time
import queue

class MyThread(threading.Thread):
    def __init__(self, queue, num):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num

    def run(self):
        while self.queue.qsize() > 0:
            msg = self.queue.get()
            print('Thread %d: %s' % (self.num, msg))
            time.sleep(1)


mqueue = queue.Queue()
for i in range(10):
    mqueue.put("Data %d" % i)

mythread1 = MyThread(mqueue,1)
mythread2 = MyThread(mqueue, 2)
mythread1.start()
mythread2.start()

mythread1.join()
mythread2.join()

