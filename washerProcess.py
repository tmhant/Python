import multiprocessing as mp

def washer(dishes, output):
    for dish in dishes:
        print('洗', dish+'\n')
        output.put(dish)


def dryer(input):
    while True:
        dish = input.get()
        print('擦乾', dish+'\n')
        input.task_done()

if __name__ == '__main__':
    dish_queue = mp.JoinableQueue()
    dry_proc = mp.Process(target=dryer, args=(dish_queue,))
    dry_proc.daemon = True
    dishes = ['大碗', '小碗', '鍋子', '筷子', '湯匙']
    washer(dishes, dish_queue)
    dry_proc.start()
    dish_queue.join()
