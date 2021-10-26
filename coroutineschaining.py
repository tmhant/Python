import asyncio
import time
import random

now = lambda : time.time()
async def step_1(num,n):
    time_sleep=random.randint(0,1)
    print('task {}, step one, sleep {}'.format(n,time_sleep))
    await asyncio.sleep(time_sleep)
    print('task {}, step one, wakeup'.format(n))
    num += 1
    return num

async def step_2(num, n):
    time_sleep = random.randint(0, n)
    print('task {}, step two, sleep {}'.format(n, time_sleep))
    await asyncio.sleep(time_sleep)
    print('task {}, step two, wakeup'.format(n))
    num += 2
    return num

async def step_3(num, n):
    time_sleep = random.randint(0, n)
    print('task {}, step three, sleep {}'.format(n, time_sleep))
    await asyncio.sleep(time_sleep)
    print('task {}, step three, wakeup'.format(n))
    num += 3
    return [n,num]

async def asyncio_chain(n):
    s1 = await step_1(n,n)
    s2 = await step_2(s1,n)
    s3 = await step_3(s2, n)
    return s3

async def main():
    tasks = [asyncio_chain(n) for n in range(3)]
    result = await asyncio.gather(*tasks)
    print(result)

if __name__ == '__main__':
    start=now()
    asyncio.run(main())
    print('time: ', now()-start)
