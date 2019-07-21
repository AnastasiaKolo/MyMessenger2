import asyncio
from aioconsole import ainput

async def send(writer):
    while True:
        try:
            message = await ainput('Введите сообщение:')
            print(f'Send: {message!r}')
            writer.write(message.encode())
            await writer.drain()
        except KeyboardInterrupt:
            break
        except ConnectionError:
            break

async def read(reader):
    while True:
        try:
            data = await reader.read(100)
            print(f'Received: {data.decode()!r}')
        except KeyboardInterrupt:
            break
        except ConnectionError:
            break


async def main():
    try:
        reader, writer = await asyncio.open_connection(
        '127.0.0.1', 5000)
        task_write = asyncio.create_task(send(writer))
        task_read = asyncio.create_task(read(reader))
        await asyncio.gather(task_write, task_read)
        print('Close the connection')
        writer.close()
        await writer.wait_closed()
    except OSError:
        print('Could not connect')

asyncio.run(main())