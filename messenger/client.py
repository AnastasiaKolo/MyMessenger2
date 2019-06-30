# -*- coding: utf8 -*-
# Продолжаем работу над проектом «Мессенджер»:
# Реализовать обработку нескольких клиентов на сервере, используя функцию select.
# Клиенты должны общаться в «общем чате»: каждое сообщение участника отправляется всем,
# подключенным к серверу.
# Реализовать функции отправки/приема данных на стороне клиента. Чтобы упростить разработку
# на данном этапе, пусть клиентское приложение будет либо только принимать, либо только
# отправлять сообщения в общий чат. Эти функции надо реализовать в рамках отдельных скриптов.


from socket import *
import threading
import time
import argparse
import json
import inspect
from client_log_config import cli_log

enable_tracing = False


def log(func):
    # print('decorator working')
    if enable_tracing:
        def callf(*args, **kwargs):
            cli_log.info('Функция {}: вызвана из функции  {}'.format(func.__name__, inspect.stack()[1][3]))
            r = func(*args, **kwargs)
            cli_log.info('{} вернула {}'.format(func.__name__, r))
            return r

        return callf
    else:
        return func


class Parser:
    @log
    def parse_message(str1):  # разобрать сообщение сервера;
        try:
            serv_message = json.loads(str1)
            if serv_message['response'] in (100, 101, 102, 200, 201, 202):
                cli_log.info('Message delivered to server, return code is {}, {}'.format(
                    str(serv_message['response']), serv_message['alert']))
                return serv_message
        except json.decoder.JSONDecodeError:
            cli_log.critical('Server message not parsed: {}'.format(str1))
            return {
                'response': 400,
                'time': time.time(),
                'alert': 'Server message not parsed: {}'.format(str1)
            }


class Client:
    def __init__(self, user_login: str):
        self.username = user_login
        self.status = 'online'
        self.encoding = 'utf8'

    @log
    def presence(self):  # сформировать presence-сообщение;
        msg = {
            'action': 'presence',
            'time': time.time(),
            'type': self.status,
            'user': {
                'account_name': self.username,
                'status': self.status
            }
        }
        return self.pack(msg)

    @log
    def message_to_user(self, to_user, msg):  # сформировать сообщение;
        msg = {
            'action': 'msg',
            'time': time.time(),
            'to': to_user,
            'from': self.username,
            'encoding': 'utf-8',
            'message': msg
        }
        return self.pack(msg)

    def message_chat(self, msg):  # сформировать сообщение;
        msg = {
            'action': 'msg',
            'time': time.time(),
            'to': 'ALL',  # вообще-то здесь указывается room name,
            # пока упрощенный чат в котором участвуют все подключенные
            'from': self.username,
            'encoding': 'utf-8',
            'message': msg
        }
        return self.pack(msg)

    def join_chat(self, room_name):  # Присоединиться к чату
        msg = {
            'action': 'join',
            'time': time.time(),
            'from': self.username,
            'room': room_name
        }
        return self.pack(msg)

    def leave_chat(self, room_name):  # Покинуть чат
        msg = {
            'action': 'leave',
            'time': time.time(),
            'from': self.username,
            'room': room_name
        }
        return self.pack(msg)

    def pack(self, dict_msg):
        str_msg = json.dumps(dict_msg)
        return str_msg.encode(self.encoding)

    def unpack(self, bt_str):
        str_decoded = bt_str.decode(self.encoding)
        return json.loads(str_decoded)


class Messenger(Client):
    def __init__(self, user_login, sock):
        self.sock = sock
        super().__init__(user_login)

    def read_messages(self, event_for_wait):
        while not event_for_wait.wait(1):  # дальше в цикле получаем сообщения
            # print('receiving msg')
            data = self.sock.recv(1024).decode('utf-8')
            if data:
                server_resp = Parser.parse_message(str1=data)
                print('\n' + server_resp['alert'])
            else:
                print('Server message empty')
                break

    def send_messages(self, event_for_set):
        while True:  # дальше в цикле отправляем сообщения
            time.sleep(0.2)
            msg_input = input('input message: ')
            if msg_input == 'exit':
                event_for_set.set()
                print('exiting...')
                msg = self.message_chat('exiting...')
                self.sock.send(msg)  # Отправить!
                break
            msg = self.message_chat(msg_input)
            self.sock.send(msg)  # Отправить!


def client_loop(host, port):  # отправляет сообщения в чат
    # и читает из него в отдельном потоке
    # Начиная с Python 3.2 сокеты имеют протокол менеджера контекста
    # При выходе из оператора with сокет будет авторматически закрыт
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        print('Connecting to %s:%s' % (host, port))
        cli_log.info('Connecting to %s:%s' % (host, port))
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            cli_log.critical('Unable to connect to %s:%s' % (host, port))
            return
        except OSError as err:
            cli_log.critical('OS error: {0}'.format(err))
            return
        else:
            cli_log.info('Connected to %s:%s' % (host, port))
        clnt = Messenger(input('Username: '), sock)
        msg = clnt.presence()
        clnt.sock.send(msg)  # Отправить сообщение presence
        # print('presence message sent')
        data = clnt.sock.recv(1024).decode('utf-8')  # Получить ответ на него
        # print('data=', data)
        server_resp = Parser.parse_message(str1=data)
        print(server_resp['alert'])

        # создаем эвент окончания работы
        evt_exit = threading.Event()

        # в отдельном потоке шлем сообщения из консоли
        th_sender = threading.Thread(target=clnt.send_messages, args=(evt_exit,))
        th_sender.daemon = True

        th_reader = threading.Thread(target=clnt.read_messages, args=(evt_exit,))
        th_reader.daemon = True

        th_sender.start()
        th_reader.start()

        th_sender.join()
        th_reader.join()


# получить и обработать параметры командной строки
def parse_args():
    parser = argparse.ArgumentParser(description='Client App')
    parser.add_argument('-a', action='store', dest='addr', type=str, default='localhost',
                        help='enter IP address, default is localhost')
    parser.add_argument('-p', action='store', dest='port', type=int, default=7777,
                        help='enter port number, default is 7777')
    # parser.add_argument('-t', action='store', dest='trace', type=str, default='false',
    #                    help='enter 'true' to enable tracing, default is 'false'')
    return parser.parse_args()


def main():
    # print('main working')
    cli_log.debug('Старт приложения')
    args = parse_args()
    port = args.port
    host = args.addr
    # enable_tracing = args.trace
    client_loop(host, port)
    # resp = ''
    # msg = json.dumps(presence('Nastya', 'Yep, I am here!'))
    # communicate(msg, resp, host, port)
    # msg = json.dumps(message_from_user('Nastya'))
    # communicate(msg, resp, host, port)


# Entry point
if __name__ == '__main__':
    main()
