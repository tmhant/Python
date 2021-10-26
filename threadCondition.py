import threading

def firstJob():
    global a,cond
    cond.acquire()
    print('Acquire the condition lock')

    if a == 0:
        print('Wait...')
        cond.wait()

    cond.notify()
    print('notify the condition')

    for _ in range(3):
        a += 1
        print('This is the first thread', a)

    cond.release()


def secondJob():
    global a,cond
    cond.acquire()

    cond.notify()
    a += 1

    cond.release()

cond = threading.Condition()
a=0
thread1 = threading.Thread(target=firstJob)
thread2 = threading.Thread(target=secondJob)

thread1.start()
thread2.start()
thread1.join()
thread2.join()
