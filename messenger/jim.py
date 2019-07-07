# -*- coding: utf8 -*-

import inspect
import json
import time

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


class Json_coder:
    '''
    Parent class for Jim Client and Jim Server
    packs json messages to bytes string
    '''

    def __init__(self):
        super().__init__()
        self.encoding = 'utf8'

    def pack(self, dict_msg):
        str_msg = json.dumps(dict_msg)
        return str_msg.encode(self.encoding)

    def unpack(self, bt_str):
        str_decoded = bt_str.decode(self.encoding)
        return json.loads(str_decoded)


class Jim_client(Json_coder):
    '''Creates and packs json messages for all client actions
    also parses server messages'''

    def __init__(self, user_login: str):
        super().__init__()
        self.username = user_login
        self.status = 'online'

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

    @log
    def auth(self, password):
        msg = {
            'action': 'authenticate',
            'time': time.time(),
            'user': {
                'account_name': self.username,
                'password': password
            }
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

    def quit(self):
        msg = {
            'action': 'quit',
            'time': time.time(),
            'from': self.username
        }
        return self.pack(msg)

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


class Jim_server(Json_coder):
    '''Creates and packs json messages for all server actions'''

    def __init__(self):
        super().__init__(self)
