# -*- coding: utf8 -*-
# Продолжаем работу над проектом «Мессенджер»:
# Реализовать обработку нескольких клиентов на сервере, используя функцию select.
# Клиенты должны общаться в «общем чате»: каждое сообщение участника отправляется всем,
# подключенным к серверу.
# Реализовать функции отправки/приема данных на стороне клиента. Чтобы упростить разработку
# на данном этапе, пусть клиентское приложение будет либо только принимать, либо только
# отправлять сообщения в общий чат. Эти функции надо реализовать в рамках отдельных скриптов.


import argparse
import inspect
import json
import time
import sys
from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtNetwork import QTcpSocket

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


class Jim_client:
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

    def message_chat(self, room_name, msg):  # сформировать сообщение;
        msg = {
            'action': 'msg',
            'time': time.time(),
            'to': room_name,
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

    @log
    def parse_server_message(self, str1):  # разобрать сообщение сервера;
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

