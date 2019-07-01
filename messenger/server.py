# -*- coding: utf8 -*-
# Продолжаем работу над проектом «Мессенджер»:
# Реализовать обработку нескольких клиентов на сервере, используя функцию select.
# Клиенты должны общаться в «общем чате»: каждое сообщение участника отправляется всем,
# подключенным к серверу.
# Реализовать функции отправки/приема данных на стороне клиента. Чтобы упростить разработку
# на данном этапе, пусть клиентское приложение будет либо только принимать, либо только
# отправлять сообщения в общий чат. Эти функции надо реализовать в рамках отдельных скриптов.


import argparse
import json
import select
import time
import traceback
from socket import *
from server_log_config import serv_log


def server_response(incoming_msg):
    # парсим сообщение клиента и формируем ответ сервера
    # ответ вида:
    # presence = клиент ... вошел в чат
    # msg = сообщение от клиента ...
    json_resp = {}
    json_resp_error = {
        'response': 400,
        'time': time.time(),
        'alert': 'Could not parse message'
    }
    if not incoming_msg:
        msg = json.dumps(json_resp_error)
        return msg
    try:
        client_msg = json.loads(incoming_msg)
        serv_log.info('Msg: Action={} , {} bytes'.format(str(client_msg['action']),
                                                         str(len(incoming_msg))))
    except json.decoder.JSONDecodeError:
        serv_log.critical('Message not parsed {}'.format(incoming_msg))
        msg = json.dumps(json_resp_error)
        return msg
    if client_msg['action'] == 'presence':
        json_resp = {
            'response': 200,
            'time': time.time(),
            'alert': 'Connected'
        }
        print('{} is online'.format(client_msg['user']['account_name']))
    elif client_msg['action'] == 'msg':
        json_resp = {
            'response': 200,
            'time': time.time(),
            'alert': 'Message "{}" from {} sent to {}'.format(client_msg['message'], client_msg['from'],
                                                              client_msg['to'])
        }
        print('Message from {}: {}'.format(client_msg['from'], client_msg['message']))
    msg = json.dumps(json_resp)
    return msg


def read_requests(r_clients, all_clients):
    # Чтение запросов из списка клиентов
    # может быть сообщение о входе в чат (presence)
    # или текстовое сообщение всем в чате
    # на прочитанное сообщение формируем ответ и сохраняем в списке
    requests = {}  # Список запросов от клиентов  вида {сокет: запрос}
    responses = {}  # Список ответов вида {сокет: запрос}
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            requests[sock] = data
            responses[sock] = server_response(data)
        except ConnectionAbortedError:
            tb = traceback.format_exc()
            print('{} {} disconnected in read_requests with traceback {}'.format(sock.fileno(), sock.getpeername(), tb))
            all_clients.remove(sock)
    return requests, responses


def write_responses(responses, w_clients, all_clients):
    # ответ сервера клиентам, от которых были запросы
    for sock in w_clients:
        if sock in responses:
            try:
                # Подготовить и отправить ответ сервера
                resp = responses[sock].encode('utf-8')
                # рассылаем сообщения всем клиентам
                for client in all_clients:
                    client.send(resp)
            except ConnectionAbortedError:  # Сокет недоступен, клиент отключился
                tb = traceback.format_exc()
                print(
                    '{} {} disconnected in write_responses with traceback {}'.format(sock.fileno(), sock.getpeername(),
                                                                                     tb))
                sock.close()
                all_clients.remove(sock)


def new_listen_socket(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    # Таймаут для операций с сокетом
    # Таймаут необходим, чтобы не ждать появления данных в сокете
    sock.settimeout(0.2)
    serv_log.info('Listening port {}'.format(str(address[1])))
    return sock


def parse_args():
    parser = argparse.ArgumentParser(description='Server App')
    parser.add_argument('-p', action='store', dest='port', type=int, default=7777,
                        help='enter port number, default is 7777')
    parser.add_argument('-a', action='store', dest='addr', type=str, default='0.0.0.0',
                        help='enter IP address, default is 0.0.0.0')
    return parser.parse_args()


def mainloop():
    # Основной цикл обработки запросов клиентов
    args = parse_args()
    address = ('', args.port)
    clients = []
    sock = new_listen_socket(address)

    while True:
        try:
            conn, addr = sock.accept()  # Проверка подключений
        except OSError:
            pass  # timeout вышел
        else:
            print('Incoming connection {}'.format(str(addr)))
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 0
            r = []
            w = []
            # r, w, e = select.select(clients, clients, [], wait)
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except OSError:
                pass  # Ничего не делать, если какой-то клиент отключился
            requests, responses = read_requests(r, clients)  # Сохраним запросы клиентов
            # if requests:
            #     print('requests=', requests)
            # if responses:
            #     print('responses=', responses)
            # отправляем 3 вида сообщений
            # 1 - подтвердждение клиенту
            # 2 - сообщение из чата либо от другого клиента
            write_responses(responses, w, clients)  # Выполним отправку ответов клиентам


# Entry point
if __name__ == '__main__':
    mainloop()