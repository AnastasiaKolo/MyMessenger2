# -*- coding: utf8 -*-
# Продолжаем работу над проектом «Мессенджер»:
# Реализовать обработку нескольких клиентов на сервере, используя функцию select.
# Клиенты должны общаться в «общем чате»: каждое сообщение участника отправляется всем,
# подключенным к серверу.
# Реализовать функции отправки/приема данных на стороне клиента. Чтобы упростить разработку
# на данном этапе, пусть клиентское приложение будет либо только принимать, либо только
# отправлять сообщения в общий чат. Эти функции надо реализовать в рамках отдельных скриптов.


import argparse
import select
import time
import traceback
from socket import *

import datetime
import asyncio
from definitions import IMAGES_PATH
from server_log_config import serv_log
from jim import Jim_server



class Server(Jim_server):
    def __init__(self):
        def parse_args():
            parser = argparse.ArgumentParser(description='Server App')
            parser.add_argument('-p', action='store', dest='port', type=int, default=7777,
                                help='enter port number, default is 7777')
            parser.add_argument('-a', action='store', dest='addr', type=str, default='0.0.0.0',
                                help='enter IP address, default is 0.0.0.0')
            return parser.parse_args()

        def new_listen_socket(address):
            sock = socket(AF_INET, SOCK_STREAM)
            sock.bind(address)
            sock.listen(5)
            # Таймаут для операций с сокетом
            # Таймаут необходим, чтобы не ждать появления данных в сокете
            sock.settimeout(0.2)
            serv_log.info('Listening port {}'.format(str(address[1])))
            print('Listening port {}'.format(str(address[1])))
            return sock

        super().__init__()
        # self.client_list = []
        # self.chat_list = []
        args = parse_args()
        address = ('', args.port)
        self.clients = []
        self.sock = new_listen_socket(address)





    def read_requests(self, r_clients, all_clients):
        # Чтение запросов из списка клиентов
        # может быть сообщение о входе в чат (presence)
        # или текстовое сообщение всем в чате
        # на прочитанное сообщение формируем ответ и сохраняем в списке
        requests = {}  # Список запросов от клиентов  вида {сокет: запрос}
        responses = {}  # Список ответов вида {сокет: запрос}
        for sock in r_clients:
            try:
                data = sock.recv(1024)
                requests[sock] = data
                responses[sock] = self.parse_client_message(data)
            except ConnectionError:
                tb = traceback.format_exc()
                # TODO print disconnected client name
                print('{} disconnected in read_requests '.format(sock.getpeername()))
                all_clients.remove(sock)
        return requests, responses


    def write_responses(self, responses, w_clients, all_clients):
        # ответ сервера клиентам, от которых были запросы
        for sock in w_clients:
            if sock in responses:
                try:
                    # Подготовить и отправить ответ сервера
                    resp = responses[sock]
                    # рассылаем сообщения всем клиентам
                    for client in all_clients:
                        client.send(resp)
                except ConnectionAbortedError:  # Сокет недоступен, клиент отключился
                    tb = traceback.format_exc()
                    print('{} disconnected in write_responses'.format(sock.getpeername()))
                    sock.close()
                    all_clients.remove(sock)

    def mainloop(self):
        while True:
            try:
                conn, addr = self.sock.accept()  # Проверка подключений
            except OSError:
                pass  # timeout вышел
            else:
                print('Incoming connection {}'.format(str(addr)))
                self.clients.append(conn)
            finally:
                # Проверить наличие событий ввода-вывода
                wait = 0
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)
                except OSError:
                    pass  # Ничего не делать, если какой-то клиент отключился
                requests, responses = self.read_requests(r, self.clients)  # Сохраним запросы клиентов
                # if requests:
                #     print('requests=', requests)
                # if responses:
                #     print('responses=', responses)
                # отправляем 3 вида сообщений
                # 1 - подтвердждение клиенту
                # 2 - сообщение из чата либо от другого клиента
                self.write_responses(responses, w, self.clients)  # Выполним отправку ответов клиентам


# Entry point
if __name__ == '__main__':
    new_server = Server()
    new_server.mainloop()
