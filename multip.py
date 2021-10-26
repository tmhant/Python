from multiprocessing import Pool, Process
import os

def f(x):
    return x*x

def N(name):
    print('Hello ', os.getpid())

if __name__ == '__main__':
    p = Pool(5)
    print(os.getpid(), p.map(f, [1, 3, 5]))
    p = Process(target=N, args=('bob',))
    p.start()
    p.join()
