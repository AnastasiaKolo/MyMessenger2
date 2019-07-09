# -*- coding: utf8 -*-


import argparse
import select
import time
import traceback
from socket import *

import datetime
import asyncio
from definitions import IMAGES_PATH
from server_log_config import serv_log
from jim import JimServer


class Worker:
    '''manages client messages'''

    def __init__(self, sock):
        self.client_name = None
        self.queue_out = []  # queue for outgoing json messages to this client
        self.raw_in = b''
        # self.raw_out = b''
        self.sock = sock
        self.active = False

    def __str__(self):
        return '(client_name {}, queue_out {}), raw_in {})'.format(self.client_name, self.queue_out,
                                                                   self.raw_in)

    def work(self, messaging_server):
        if self.raw_in:
            # split raw data into messages
            messages = messaging_server.unpack(self.raw_in)
            # process messages
            for message in messages:
                response = messaging_server.parse_client_message(message)
                self.queue_out.append(response)
                if response['response'] >= 400:
                    break
                # if presence then save username
                if message['action'] == 'presence':
                    self.client_name = message['user']['account_name']
                    messaging_server.username_clients[self.client_name] = self.sock
                elif message['action'] == 'msg':
                    # if message to user then find the user and put message in user's messages queue
                    # if message to chat then find all users of the chat and put message in their queues
                    destination = message['to']
                    users_list = []
                    if destination in messaging_server.chats.keys():
                        users_list = messaging_server.chats[destination]
                    elif destination in messaging_server.username_clients.keys():
                        users_list = [destination]
                    for receiver in users_list:
                        sock = messaging_server.username_clients[receiver]
                        messaging_server.workers[sock].queue_out.append(message)
            # clear raw data
            self.raw_in = b''


class Server(JimServer):
    def __init__(self):
        def parse_args():
            parser = argparse.ArgumentParser(description='Server App')
            parser.add_argument('-p', action='store', dest='port', type=int, default=7777,
                                help='enter port number, default is 7777')
            parser.add_argument('-a', action='store', dest='addr', type=str, default='0.0.0.0',
                                help='enter IP address, default is 0.0.0.0')
            return parser.parse_args()

        def new_listen_socket(addr):
            # https://docs.python.org/3.7/howto/sockets.html
            sock = socket(AF_INET, SOCK_STREAM)
            sock.bind(addr)
            sock.listen(5)
            # Таймаут для операций с сокетом
            # Таймаут необходим, чтобы не ждать появления данных в сокете
            sock.settimeout(0.2)
            serv_log.info('Listening port {}'.format(str(address[1])))
            print('Listening port {}'.format(str(address[1])))
            return sock

        super().__init__()
        args = parse_args()
        # socket.gethostname()
        address = ('', args.port)
        self.clients = []  # list of currently connected client sockets
        self.workers = {}  # dictionary, key = client, value = worker workers for each socket
        self.username_clients = {}  # dictionary for translating usernames into client sockets
        self.sock = new_listen_socket(address)

    def disconnect_client(self, client_socket):
        client_socket.close()
        self.clients.remove(client_socket)
        self.username_clients.pop(self.workers[client_socket].client_name)
        self.workers.pop(client_socket)

    def process_data(self, client_socket):
        if self.workers[client_socket].raw_in:
            self.workers[client_socket].work(self)

    def receive_data(self, client_socket):
        try:
            total_data = b''
            while True:
                data = client_socket.recv(1024)
                total_data += data
                if not data or len(data) < 1024:
                    break
            if total_data:
                self.workers[client_socket].raw_in = total_data
        except ConnectionError:
            print('{} disconnected in receive_data '.format(self.workers[client_socket].client_name))
            self.disconnect_client(client_socket)
        return

    def send_data(self, client_socket):
        try:
            worker = self.workers[client_socket]
        except KeyError:
            # client has already disconnected, nobody to send data
            print('worker not found for {} '.format(client_socket))
            return
        if worker.queue_out:
            raw_out = self.pack(worker.queue_out)
            worker.queue_out = []
            try:
                client_socket.send(raw_out)
            except ConnectionError:  # Сокет недоступен, клиент отключился
                print('{} disconnected in send_data'.format(self.workers[client_socket].client_name))
                self.disconnect_client(client_socket)

    def listen_connections(self):
        try:
            while True:
                try:
                    client, addr = self.sock.accept()  # connect new clients
                except OSError:
                    pass  # timeout expired
                else:
                    print('Incoming connection {}'.format(str(addr)))
                    self.clients.append(client)
                    self.workers[client] = Worker(client)

                finally:
                    r = []
                    w = []
                    try:
                        r, w, e = select.select(self.clients, self.clients, [], 0)
                    except OSError:
                        pass  # Ничего не делать, если какой-то клиент отключился
                    for sock in r:  # sockets that can be read
                        self.receive_data(sock)
                    for sock in self.clients:
                        if self.workers[sock].raw_in or self.workers[sock].queue_out:
                            print('-------{}'.format(self.workers[sock]))
                    for sock in self.clients:
                        self.process_data(sock)
                    for sock in self.clients:
                        if self.workers[sock].raw_in or self.workers[sock].queue_out:
                            print('+++++++{}'.format(self.workers[sock]))
                    for sock in w:  # sockets that can be written to
                        self.send_data(sock)
        except KeyboardInterrupt:
            serv_log.critical('Shutting down')


# Entry point
if __name__ == '__main__':
    new_server = Server()
    new_server.listen_connections()
