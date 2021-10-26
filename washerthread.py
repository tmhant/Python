import threading, queue
import time

def washer(dishes, dish_queue):
    for dish in dishes:
        print('洗',dish+'\n')
        time.sleep(1)
        dish_queue.put(dish)

def dryer(dish_queue):
    while True:
        dish = dish_queue.get()
        print('擦乾', dish+'\n')
        time.sleep(2)
        dish_queue.task_done()

dish_queue = queue.Queue()
for n in range(2):
    dryer_thread = threading.Thread(target=dryer, args=(dish_queue,))
    dryer_thread.start()
dishes=['大碗', '小碗', '鍋子', '筷子', '湯匙']
washer(dishes, dish_queue)
print(dish_queue.join())