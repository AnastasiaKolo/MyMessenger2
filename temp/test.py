import asyncio
import functools
from time import sleep
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
    sleep(random.randint(0, 3) * 0.005)
    p('Задача %s выполнена' % pid)


async def taskCoro(pid):
    """Асинхронная задача с помощью корутины
    """
    await asyncio.sleep(random.randint(0, 3) * 0.005)
    p('Задача %s выполнена' % pid)


def synchronousTask():
    for i in range(1, 10):
        task(i)


async def asynchronousTask():
    tasks = [asyncio.ensure_future(taskCoro(i)) for i in range(1, 10)]
    await asyncio.wait(tasks)


p('Синхронно:')
synchronousTask()

def mainLoopAsync():
    loop = asyncio.get_event_loop()
    p('Асинхронно:')
    loop.run_until_complete(asynchronousTask())
    loop.close()

if __name__ == '__main__':
    mainLoopAsync()