import asyncio
import functools
import time
import  random

# async def function1():
#     print('Загрузка функции function 1')
#     await asyncio.sleep(3)
#     print('Возвращаемся в функцию function 1 снова')
#
# async def function2():
#     print('Начинаем выполнять функцию function 2')
#     await asyncio.sleep(3)
#     print('Выполняем функцию function 2 снова')
#
# def mainLoop():
#     eloop = asyncio.get_event_loop()
#     tasks = [eloop.create_task(function1()), eloop.create_task(function2())]
#     wait_tasks = asyncio.wait(tasks)
#     eloop.run_until_complete(wait_tasks)
#     eloop.close()
#
# mainLoop()
def p(txt):
    print(txt)

def task(pid):
    """Синхронная задача
    """
    time.sleep(random.randint(0, 3) * 0.005)
    p('Задача %s выполнена' % pid)

def random_delay():
    return random.random() * 5

def random_countdown():
    return random.randrange(5)

def launch_rocket(delay, countdown):
    time.sleep(delay)
    for i in reversed(range(countdown)):
        print(f'{i+1}...')
        time.sleep(1)
    print('Rocket launched')

def rockets():
    N = 100
    return {
        (random_delay(), random_countdown())
        for _ in range(N)
    }

async def taskCoro(pid):
    """Асинхронная задача с помощью корутины
    """
    await asyncio.sleep(random.randint(0, 3) * 0.005)
    p('Задача %s выполнена' % pid)

async def async_launch_rocket(delay, countdown):
    await asyncio.sleep(delay)
    for i in reversed(range(countdown)):
        print(f'{i+1}...')
        await asyncio.sleep(1)
    print('Rocket launched')


def synchronousTask():
    for i in range(1, 10):
        task(i)


async def asynchronousTask():
    tasks = [asyncio.ensure_future(taskCoro(i)) for i in range(1, 10)]
    await asyncio.wait(tasks)


async def asynchronous_rockets():
    tasks = [asyncio.ensure_future(async_launch_rocket(d, c)) for d, c in rockets()]
    await asyncio.wait(tasks)

# p('Синхронно:')
# synchronousTask()

def mainLoopAsync():
    loop = asyncio.get_event_loop()
    p('Асинхронно:')
    # loop.run_until_complete(asynchronousTask())
    loop.run_until_complete(asynchronous_rockets())
    loop.close()

if __name__ == '__main__':
    mainLoopAsync()
    # for d, c in rockets():
    #     launch_rocket(d, c)