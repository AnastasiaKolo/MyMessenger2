# -*- coding: utf-8 -*-

import time
import os.path
import sys

import random
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtWidgets import (QMainWindow, QToolBar, QLineEdit, QErrorMessage, QInputDialog, QLabel,
                             QAction, QFileDialog, qApp, QApplication, QTextEdit, QSplitter)
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtCore import QIODevice
from definitions import IMAGES_PATH
from profile_window import ProfileWindow

from jim import JimClient


class Messenger_Window(QMainWindow):

    # noinspection PyArgumentList
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        myFont = QFont('Arial', pointSize=14, weight=400)
        self.font = myFont
        self.errorMessageDialog = QErrorMessage(self)
        self.errorMessageDialog.setWindowModality(Qt.WindowModal)
        self.chat_area = QTextEdit('В чат пока ничего не написали', readOnly=True, )
        self.chat_area.setFont(myFont)
        self.chat_label = QLabel()
        self.chat_label.setFont(myFont)
        self.message_area = QTextEdit('Введите сообщение')
        self.message_area.setFont(myFont)
        self.message_area.setMaximumHeight(100)

        v_splitter = QSplitter(Qt.Vertical)
        v_splitter.addWidget(self.chat_label)
        v_splitter.addWidget(self.chat_area)
        v_splitter.addWidget(self.message_area)
        self.setCentralWidget(v_splitter)
        self.setGeometry(200, 50, 500, 900)
        self.create_actions()
        self.init_tool_bar()
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        app_icon = QIcon(os.path.join(IMAGES_PATH, 'worldwide.png'))
        self.setWindowIcon(app_icon)
        self.enable_actions(True)
        self.setWindowTitle('My awesome client')

        self.message_area.setFocus()
        self.statusBar().showMessage('Ready')

    # noinspection PyArgumentList
    def create_actions(self):
        send_icon = QIcon(os.path.join(IMAGES_PATH, 'paper-plane-1.png'))
        save_icon = QIcon(os.path.join(IMAGES_PATH, 'save.png'))
        profile_icon = QIcon(os.path.join(IMAGES_PATH, 'emoji.png'))
        bold_icon = QIcon(os.path.join(IMAGES_PATH, '012-bold.png'))
        italic_icon = QIcon(os.path.join(IMAGES_PATH, '057-italic.png'))
        underline_icon = QIcon(os.path.join(IMAGES_PATH, '093-underline.png'))
        smile_icon = QIcon(os.path.join(IMAGES_PATH, 'croco.png'))
        logon_icon = QIcon(os.path.join(IMAGES_PATH, 'key.png'))
        random_icon = QIcon(os.path.join(IMAGES_PATH, 'magic-wand.png'))
        exit_icon = QIcon(os.path.join(IMAGES_PATH, 'exit.png'))
        join_chat_icon = QIcon(os.path.join(IMAGES_PATH, 'users-1.png'))
        contact_user_icon = QIcon(os.path.join(IMAGES_PATH, 'user-4.png'))
        debug_icon = QIcon(os.path.join(IMAGES_PATH, 'settings-1'))
        self.save_action = QAction(save_icon, 'Save chat as...', self, shortcut='Ctrl+S', triggered=self.dialog_save)
        self.send_action = QAction(send_icon, 'Send message', self, shortcut='Ctrl+Enter', triggered=self.send)
        self.edit_profile_action = QAction(profile_icon, 'Edit profile', self, triggered=self.edit_profile)
        self.bold_action = QAction(bold_icon, 'Bold', self, shortcut='Ctrl+S', triggered=self.make_bold)
        self.italic_action = QAction(italic_icon, 'Italic', self, shortcut='Ctrl+Enter', triggered=self.make_italic)
        self.underline_action = QAction(underline_icon, 'Underlined', self, triggered=self.make_underline)
        self.smile_action = QAction(smile_icon, 'Smile!', self, triggered=self.insert_smile)
        self.logon_action = QAction(logon_icon, 'Logon', self, triggered=self.logon)
        self.random_action = QAction(random_icon, 'Random message!', self, triggered=self.random_message)
        self.exit_action = QAction(exit_icon, 'Exit', self, triggered=self.exit)
        self.join_chat_action = QAction(join_chat_icon, 'Select chat', self, triggered=self.dialog_join_chat)
        self.contact_user_action = QAction(contact_user_icon, 'Select user', self, triggered=self.dialog_contact_user)
        self.debug_action = QAction(debug_icon, 'Debug', self, triggered=self.debug)

    def exit(self):
        self.before_exit()
        qApp.quit()

    def init_tool_bar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(30, 30))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon | Qt.AlignLeading)  # <= Toolbuttonstyle
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        self.toolbar = toolbar
        self.toolbar.addAction(self.logon_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.join_chat_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.contact_user_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.edit_profile_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.save_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.send_action)
        self.toolbar.addAction(self.random_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.bold_action)
        self.toolbar.addAction(self.italic_action)
        self.toolbar.addAction(self.underline_action)
        self.toolbar.addAction(self.smile_action)
        self.toolbar.addAction(self.exit_action)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.debug_action)
        self.toolbar.setMovable(False)

    def enable_actions(self, state):
        for action in self.toolbar.actions():
            action.setEnabled(state)

    def enable_server_buttons(self, state):
        self.send_action.setEnabled(state)
        self.edit_profile_action.setEnabled(state)
        self.join_chat_action.setEnabled(state)
        self.contact_user_action.setEnabled(state)

    def enable_communication_buttons(self, state):
        self.send_action.setEnabled(state)
        self.random_action.setEnabled(state)
        self.smile_action.setEnabled(state)
        self.bold_action.setEnabled(state)
        self.italic_action.setEnabled(state)
        self.underline_action.setEnabled(state)
        self.message_area.setEnabled(state)


    def insert_smile(self):
        # TODO insert smiles in unicode
        url = os.path.join(IMAGES_PATH, 'croco-small.png')
        self.message_area.insertHtml('<img src="%s" />' % url)

    def make_bold(self):
        self.font.setBold(True)
        self.message_area.setFont(self.font)

    def make_italic(self):
        self.font.setItalic(True)
        self.message_area.setFont(self.font)

    def make_underline(self):
        self.font.setUnderline(True)
        self.message_area.setFont(self.font)

    def dialog_save(self):
        fname = QFileDialog.getSaveFileName(self, 'Save as', os.path.expanduser(''),
                                            'Html (*.html);;Txt (*.txt);;All files (*.*)')[0]
        if fname:
            self.statusBar().showMessage('Saved file as: {}'.format(fname))
            print(fname)
            html_str = self.chat_area.toHtml()
            Html_file = open(fname, "w")
            Html_file.write(html_str)
            Html_file.close()

    def edit_profile(self):
        dlg = ProfileWindow()
        dlg.exec_()


class Messenger(Messenger_Window):
    RANDOM_MESSAGES = (
        'Hello',
        'How are you?',
        'Hi there!',
        'I’m fine, and you?',
        'Your problems – my problems.',
        'Hello, I’m awesome. How can I help you?',
        'What’s up?',
        'I was so bored. Thank you for saving me!',
        'I’ve been expecting you!'
    )

    def __init__(self, host, port):
        super().__init__()
        self.tcpSocket = QTcpSocket()
        self.blockSize = 0
        self.host = host
        self.port = port
        self.jim = None
        self.connected = False
        self.chat_list = []
        self.online_users = []
        self.active_chat = ''
        self.logon()

        # self.last_sent_message = ''

    def reset_connection(self):
        if self.connected:
            self.tcpSocket.disconnect()
        self.jim = None
        self.connected = False
        self.chat_list = []
        self.online_users = []
        self.active_chat = ''
        self.enable_server_buttons(False)
        self.enable_communication_buttons(False)
        self.setWindowTitle('My awesome client: disconnected')
        self.chat_label.setText('Disconnected')


    def debug(self):
        print('chat_list='+','.join(self.chat_list))
        print('online_users=' + ','.join(self.online_users))
        print('active_chat={}'.format(self.active_chat))
        try:
            print('username={}'.format(self.jim.username))
        except:
            print('username is none')
        print('connected={}'.format(self.connected))


    def logon(self):
        if self.connected:
            self.tcpSocket.disconnect()
        username, ok = QInputDialog.getText(self, 'Logon to chat', 'Enter your name:', QLineEdit.Normal, 'Nastya')
        if ok:
            self.jim = JimClient(username)
            self.enable_server_buttons(True)
            self.enable_communication_buttons(False)
            self.setWindowTitle('My awesome client: connected as {}'.format(username))
            self.tcpSocket.connectToHost(self.host, self.port, QIODevice.ReadWrite)
            # self.tcpSocket.waitForConnected()
            self.chat_label.setText('Please join chat...')
            self.tcpSocket.readyRead.connect(self.read_messages)
            self.tcpSocket.error.connect(self.display_error)
            # self.tcpSocket.write(self.jim.auth())
            self.tcpSocket.write(self.jim.presence())
            self.connected = True
            # self.tcpSocket.write(self.jim.request_chat_list())
            self.chat_area.clear()
        else:
            self.reset_connection()

    def before_exit(self):
        print('Exiting!')
        if self.jim:
            msg = self.jim.quit()
            self.tcpSocket.write(msg)
            time.sleep(5)
            print('Exiting! Message length is {}, message={}'.format(len(msg), msg))
        if self.connected:
            self.tcpSocket.disconnectFromHost()

    def dialog_join_chat(self):
        # print(self.chat_list)
        if self.connected:
            chat, ok = QInputDialog.getItem(self, 'Доступные чаты', 'Выберите чат', self.chat_list, 0, False)
            if ok and chat:
                self.chat_label.setText('Active Chat: ' + chat)
                msg = self.jim.join_chat(chat)
                self.tcpSocket.write(msg)
                self.chat_area.clear()
                self.enable_communication_buttons(True)
                self.active_chat = chat

    def dialog_contact_user(self):
        # print(self.chat_list)
        if self.connected:
            user, ok = QInputDialog.getItem(self, 'Пользователи онлайн', 'Выберите пользователя', self.online_users, 0,
                                            False)
            if ok and user:
                self.chat_label.setText('Dialog with ' + user)
                self.chat_area.clear()
                self.enable_communication_buttons(True)
                self.active_chat = user

    def random_message(self):
        message = self.RANDOM_MESSAGES[random.randint(0, len(self.RANDOM_MESSAGES) - 1)]
        self.message_area.clear()
        self.message_area.setText(message)
        self.send()

    def read_messages(self):
        data = self.tcpSocket.readAll().data()
        if data:
            received_messages = self.jim.unpack(data)
            for msg in received_messages:
                server_resp = self.jim.parse_server_message(msg)
                if 'response' in server_resp:
                    print('received server message {} "{}"'.format(server_resp['response'], server_resp['alert']))
                    if server_resp['response'] in (200, 201):  # everything OK
                        # self.chat_area.append(time.strftime("%Y-%m-%d %H:%M", time.localtime(server_resp['time'])))
                        # self.chat_area.append('{}: {}'.format(self.jim.username, self.last_sent_message))
                        pass
                    elif server_resp['response'] == 203:  # a user is online
                        if not server_resp['username'] in self.online_users:
                            self.online_users.append(server_resp['username'])
                    elif server_resp['response'] == 204:  # a user has joined chat
                        if self.active_chat == server_resp['chat']:
                            # redColor = QColor(255, 0, 0)
                            # blackColor = QColor(0, 0, 0)
                            # tmpFont = QFont('Arial', pointSize=10, weight=400)
                            # self.chat_area.setTextColor(redColor)
                            # self.chat_area.setFont(tmpFont)
                            self.chat_area.append(time.strftime("%Y-%m-%d %H:%M", time.localtime(server_resp['time'])))
                            self.chat_area.append('{} has joined this chat'.format(server_resp['username']))
                            # self.chat_area.setFont(self.font)
                            # self.chat_area.setTextColor(blackColor)
                    elif server_resp['response'] == 215:
                        # received chat list
                        self.chat_list = server_resp['chat_list'].split(',')
                    elif server_resp['response'] == 216:
                        # received users list
                        self.online_users = server_resp['user_list'].split(',')
                    elif server_resp['response'] >= 400:
                        # received an error
                        self.chat_area.append(time.strftime("%Y-%m-%d %H:%M", time.localtime(server_resp['time'])))
                        self.chat_area.append(server_resp['alert'])
                elif 'message' in server_resp:
                    # received a message
                    if self.chat_area.toPlainText() == 'В чат пока ничего не написали':
                        self.chat_area.clear()
                    # if message to current chat or dialog then display it
                    if (server_resp['from'] == self.active_chat and server_resp['to'] == self.jim.username) or \
                            (self.active_chat == server_resp['to']) or \
                            (server_resp['from'] == self.jim.username and server_resp['to'] == self.active_chat):
                        self.display_message(server_resp)
                    print('received message {}'.format(server_resp))
                else:
                    print('something wrong in read_messages {}'.format(msg))

    def display_message(self, server_resp):
        self.chat_area.append(time.strftime("%Y-%m-%d %H:%M", time.localtime(server_resp['time'])))
        self.chat_area.append('{}: {}'.format(server_resp['from'], server_resp['message']))

    def display_error(self):
        self.chat_area.append(time.strftime("%Y-%m-%d %H:%M", time.localtime()))
        self.chat_area.append('Connection error')
        self.reset_connection()


    def send(self):
        # message_html = self.message_area.toHtml()
        message_txt = self.message_area.toPlainText()
        msg_len = len(message_txt)
        if msg_len > 512:
            self.errorMessageDialog.showMessage('Warning: Message {} bytes too long, max 512'.format(msg_len))
        elif not message_txt:
            pass
        else:
            message_json_packed = self.jim.message(self.active_chat, message_txt)
            self.tcpSocket.write(message_json_packed)
            self.message_area.clear()
            self.message_area.setFocus()


def main():
    app = QApplication(sys.argv)
    # TODO сделать настройку коннекта на указанныйс пользователем хост/порт
    messenger = Messenger('localhost', 7777)
    messenger.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
