import asyncio

async def hello_world(x):
    print('hello world {}'.format(x))
    await asyncio.sleep(2)

asyncio.run(hello_world(2))