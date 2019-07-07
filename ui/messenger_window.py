# -*- coding: utf-8 -*-
# 2. Добавить форматирование в сообщения в вашем мессенджере.
# 3. Реализовать возможность добавления фотографии в ваш профиль.
# 4. *Нужно сделать предыдущее задание и добавить смайлы в мессенджер.
# 5. *Нужно сделать предыдущее задание и применить разные эффекты к изображению в профиле.

import datetime
import os.path
import sys

import random
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QMainWindow, QToolBar, QLineEdit, QErrorMessage, QInputDialog,
                             QAction, QFileDialog, qApp, QApplication, QTextEdit, QSplitter)
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtCore import QIODevice
from definitions import IMAGES_PATH
from profile_window import ProfileWindow

from jim import Jim_client


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
        self.message_area = QTextEdit('Введите сообщение')
        self.message_area.setFont(myFont)
        self.message_area.setMaximumHeight(100)

        v_splitter = QSplitter(Qt.Vertical)
        v_splitter.addWidget(self.chat_area)
        v_splitter.addWidget(self.message_area)
        self.setCentralWidget(v_splitter)
        self.setGeometry(200, 50, 700, 900)
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




    def exit(self):
        qApp.quit()

    def init_tool_bar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(50, 50))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon | Qt.AlignLeading)  # <= Toolbuttonstyle
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        self.toolbar = toolbar
        self.toolbar.addAction(self.logon_action)
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

    def enable_actions(self, state):
        for action in self.toolbar.actions():
            action.setEnabled(state)

    def enable_chat_buttons(self, state):
        self.send_action.setEnabled(state)
        self.edit_profile_action.setEnabled(state)

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
        self.logon()

    def logon(self):
        if self.connected:

            self.tcpSocket.disconnect()
        username, ok = QInputDialog.getText(self, 'Logon to chat', 'Enter your name:', QLineEdit.Normal, 'Nastya')
        if ok:
            self.jim = Jim_client(username)
            self.enable_chat_buttons(True)
            self.setWindowTitle('My awesome client: connected as {}'.format(username))
            self.tcpSocket.connectToHost(self.host, self.port, QIODevice.ReadWrite)
            self.tcpSocket.write(self.jim.presence())
            self.tcpSocket.readyRead.connect(self.read_messages)
            self.tcpSocket.error.connect(self.display_error)
            self.connected = True
        else:
            self.enable_chat_buttons(False)
            self.setWindowTitle('My awesome client: disconnected')
            self.connected = False

    def random_message(self):
        message = self.RANDOM_MESSAGES[random.randint(0, len(self.RANDOM_MESSAGES) - 1)]
        self.message_area.clear()
        self.message_area.setText(message)
        self.send()

    def read_messages(self):
        data = self.tcpSocket.readLine().data().decode("utf-8")
        if data:
            # print(data)
            server_resp = self.jim.parse_server_message(str1=data)
            if self.chat_area.toPlainText() == 'В чат пока ничего не написали':
                self.chat_area.clear()
            self.chat_area.append(server_resp['alert'])
            # print('\n' + server_resp['alert'])

    def display_error(self):
        self.chat_area.append("Connection error")

    def send(self):
        # self.chat_area.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # TODO refuse empty messages
        # self.chat_area.append(self.message_area.toHtml())
        message_html = self.message_area.toHtml()
        msg_len = len(message_html)
        if msg_len > 512:
            self.errorMessageDialog.showMessage('Warning: Message {} bytes too long, max 512'.format(msg_len))
        elif len(self.message_area.toPlainText()) == 0:
            pass  # self.errorMessageDialog.showMessage('Warning: Message is empty')
        else:
            # message_txt = self.message_area.toPlainText()
            message_json_packed = self.jim.message_chat('ALL', message_html)
            # print(message_json_packed)
            print("Message length is {}".format(len(message_json_packed)))
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
