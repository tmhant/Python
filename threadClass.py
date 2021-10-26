import threading
import time

# class MyThread(threading.Thread):
#     def __init__(self,num):
#         threading.Thread.__init__(self)
#         self.num = num

#     def run(self):
#         print('Thread',self.num)
#         time.sleep(1)

# threads=[]
# for i in range(5):
#     threads.append(MyThread(i))
#     threads[i].start()

# for i in range(3):
#     threads[i].join()

class runner(object):
    def __init__(self,name):
        self.name=name
        self.thread_job()

    def job(self,name):
        print('HI,', name)

    def thread_job(self):
        self.threads=[]
        t = threading.Thread(target=self.job, args=(self.name,))
        self.threads.append(t)

    def thread_start(self):
        for t in self.threads:
            t.start()

        for t in self.threads:
            t.join()

        self.thread_job()


r = runner('John')
r.thread_start()
