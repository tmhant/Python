import multiprocessing as mp
import os

class running:
    def __init__(self):
        self.__lists=[]

    def job(self,i):
        print('第',str(i))
        print('Thread ID:',os.getpid())

    def run(self):
        for i in range(5):
            self.__lists.append(mp.Process(target=self.job,args=(str(i))))
            self.__lists[i].start()

        for i in self.__lists:
            i.join()
if __name__ == '__main__':
    r = running()
    r.run()