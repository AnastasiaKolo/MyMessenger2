# -*- coding: utf8 -*-

import inspect
import json
import time
import html2text

from client_log_config import cli_log
from server_log_config import serv_log
from mongo_client import AwesomDBClient

enable_tracing = False
DELIMITER = '\n\r'


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


class Jim:
    '''
    Parent class for Jim Client and Jim Server
    packs json messages to bytes string
    '''
    SERVER_RESPONSES = {
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'User is online',
        204: 'User has joined chat',
        215: 'Sending chat list',
        216: 'Sending users list',
        400: 'Could not parse message',
        401: 'Not authorised',
        402: 'Wrong username or password',
        403: 'The account is locked',
        404: 'Not found',
        409: 'Someone is already connected with the given user name',
        410: 'Offline',
        500: 'Internal server error',
        501: 'Not implemented'
    }

    def __init__(self, encoding='utf8'):
        super().__init__()
        self.encoding = encoding

    def server_response(self, msg_code):
        '''returns packed server response for given code'''
        msg = {
            'response': msg_code,
            'time': time.time(),
            'alert': self.SERVER_RESPONSES[msg_code]
        }
        return msg

    def pack(self, json_list):
        str_msg = ''
        for json_msg in json_list:
            # print('pack json_msg', json_msg)
            dumped_json = json.dumps(json_msg)
            str_msg += dumped_json + DELIMITER
            # print('pack ok')
        # print('packing ( {} )'.format(str_msg))
        return str_msg.encode(self.encoding)

    def unpack(self, bt_str):
        json_list = []
        try:
            str_decoded = bt_str.decode(self.encoding)
            list_strings = list(filter(None, str_decoded.split(DELIMITER)))
            json_list = list(map(json.loads, list_strings))
        except json.decoder.JSONDecodeError:
            json_list.append(self.server_response(400))
            serv_log.critical('Message not parsed {}'.format(bt_str))
        return json_list


class JimClient(Jim):
    '''Creates and packs json messages for all client actions
    also parses server messages'''

    def __init__(self, user_login: str):
        super().__init__()
        self.username = user_login
        self.status = 'online'

    @log
    def presence(self):  # сформировать presence-сообщение;
        json_message = {
            'action': 'presence',
            'time': time.time(),
            'type': self.status,
            'user': {
                'account_name': self.username,
                'status': self.status
            }
        }
        return self.pack([json_message])

    @log
    def auth(self, password):
        json_message = {
            'action': 'authenticate',
            'time': time.time(),
            'user': {
                'account_name': self.username,
                'password': password
            }
        }
        return self.pack([json_message])

    def request_chat_list(self):  # сформировать presence-сообщение;
        json_message = {
            'action': 'request_chat_list',
            'time': time.time(),
        }
        return self.pack([json_message])

    def message(self, user_or_chat, msg):
        json_message = {
            'action': 'msg',
            'time': time.time(),
            'to': user_or_chat,
            'from': self.username,
            'encoding': 'utf-8',
            'message': msg
        }
        return self.pack([json_message])

    def join_chat(self, chat_name):
        json_message = {
            'action': 'join',
            'time': time.time(),
            'from': self.username,
            'chat': chat_name
        }
        return self.pack([json_message])

    def leave_chat(self, chat_name):
        json_message = {
            'action': 'leave',
            'time': time.time(),
            'from': self.username,
            'chat': chat_name
        }
        return self.pack([json_message])

    def quit(self):
        json_message = {
            'action': 'quit',
            'time': time.time(),
            'from': self.username
        }
        return self.pack([json_message])

    @log
    def parse_server_message(self, serv_message):  # разобрать сообщение сервера;
        parsing_error = {
            'response': 500,
            'time': time.time(),
            'alert': 'Server message not valid: {}'.format(json.dumps(serv_message))
        }
        if 'response' in serv_message.keys():
            if serv_message['response'] in self.SERVER_RESPONSES.keys():
                cli_log.info('Message delivered to server, return code is {}, {}'.format(
                    str(serv_message['response']), serv_message['alert']))
                return serv_message
            else:
                return parsing_error
        elif 'message' in serv_message.keys():
            # message from user or chat
            return serv_message
        else:
            return parsing_error


class JimServer(Jim):
    '''Parses client messages
    Creates and packs json messages for all server responses'''

    def __init__(self):
        super().__init__()

        self.chats = {}
        self.username_clients = {}  # dictionary for translating usernames into client sockets
        self.dbclient = AwesomDBClient('mongodb://localhost:27017/')
        self.chats = self.dbclient.get_chats()


    def add_chat(self, chat_name):
        if len(self.chats.keys()) == 20:
            NameError('More than 20 chats are not supported')
        if chat_name in self.chats.keys():
            NameError('Chat already exists')
        self.chats[chat_name] = []
        self.dbclient.add_chat({'chat': chat_name, 'userlist': []})

    def send_chat_list(self):
        '''returns packed server response with chat list'''
        msg = {
            'response': 215,
            'time': time.time(),
            'alert': self.SERVER_RESPONSES[215],
            'chat_list': ','.join(self.chats.keys())
        }
        return msg

    def send_user_list(self):
        '''returns packed server response with online users list'''
        msg = {
            'response': 216,
            'time': time.time(),
            'alert': self.SERVER_RESPONSES[216],
            'user_list': ','.join(self.username_clients.keys())
        }
        # print('online user list: {}'.format(','.join(self.username_clients.keys())))
        return msg

    # 203: 'User is online',
    def info_user_online(self, username):
        msg = {
            'response': 203,
            'time': time.time(),
            'alert': self.SERVER_RESPONSES[203],
            'username': username
        }
        return msg

    # 204: 'User has joined chat',
    def info_user_in_chat(self, username, chat):
        msg = {
            'response': 204,
            'time': time.time(),
            'alert': self.SERVER_RESPONSES[204],
            'username': username,
            'chat': chat
        }
        return msg

    def parse_client_message(self, incoming_msg):
        '''returns packed server response for given incoming msg'''
        if not incoming_msg:
            return self.server_response(400)
        try:
            if incoming_msg['action'] == 'presence':
                print(f'{incoming_msg["user"]["account_name"]} is online')
                return self.server_response(200)
            elif incoming_msg['action'] == 'msg':  # sent message_to_user or message_chat
                message_txt = html2text.html2text(incoming_msg['message']).strip()
                print(f'message "{message_txt}" from {incoming_msg["from"]} to {incoming_msg["to"]}')
                self.dbclient.add_message(incoming_msg)
                return self.server_response(200)
            elif incoming_msg['action'] == 'join':  # join chat
                if incoming_msg['chat'] in self.chats.keys():
                    if not incoming_msg['from'] in self.chats[incoming_msg['chat']]:
                        self.chats[incoming_msg['chat']].append(incoming_msg['from'])
                        self.dbclient.add_users_to_chat(incoming_msg['chat'], incoming_msg['from'])
                    return self.server_response(202)
                else:
                    return self.server_response(404)
            elif incoming_msg['action'] == 'quit':  # went offline
                print(f'{incoming_msg["from"]} logged off')
                return self.server_response(200)
            elif incoming_msg['action'] == 'leave':  # left chat
                # # remove user from all chats
                # for client_list in self.chats.items():
                #     client_list.remove(incoming_msg['from'])
                return self.server_response(501)
            elif incoming_msg['action'] == 'request_chat_list':  # send chat list
                return self.send_chat_list()
            else:
                return self.server_response(500)
        except KeyError:
            serv_log.critical('Message format not recognized {}'.format(incoming_msg))
            return self.server_response(400)
