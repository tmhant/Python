import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s',)
def producer(cond):
    logging.debug('Starting producer thread')
    with cond:
        logging.debug('Making producer available')
        cond.notifyAll()

def consumer(cond):
    logging.debug('Starting consumer thread')
    t=threading.currentThread()
    with cond:
        cond.wait()
        logging.debug('Resource is available to consumer')

condition = threading.Condition()
cu1 = threading.Thread(name='consumer_1', target=consumer, args=(condition,))
cu2 = threading.Thread(name='consumer_2', target=consumer, args=(condition,))
proc = threading.Thread(name='Producer', target=producer, args=(condition,))
cu1.start()
time.sleep(2)
cu2.start()
time.sleep(2)
proc.start()
