import threading
import time
import queue

class MyThread(threading.Thread):
    def __init__(self, queue, num, lock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num
        self.lock = lock

    def run(self):
        while self.queue.qsize() > 0:
            msg = self.queue.get()

            # 取得lock
            self.lock.acquire()
            print('lock acquired by worker %d' % self.num)

            print('Thread %d: %s' % (self.num, msg))
            time.sleep(1)

            # 釋放lock
            self.lock.release()
            print('lock release by worker %d' % self.num)


mqueue = queue.Queue()
for i in range(10):
    mqueue.put("Data %d" % i)

lock = threading.Lock()
mythread1 = MyThread(mqueue, 1, lock)
mythread2 = MyThread(mqueue, 2, lock)
mythread1.start()
mythread2.start()

mythread1.join()
mythread2.join()
