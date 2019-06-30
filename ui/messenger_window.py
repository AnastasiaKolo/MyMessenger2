# -*- coding: utf-8 -*-
# 2. Добавить форматирование в сообщения в вашем мессенджере.
# 3. Реализовать возможность добавления фотографии в ваш профиль.
# 4. *Нужно сделать предыдущее задание и добавить смайлы в мессенджер.
# 5. *Нужно сделать предыдущее задание и применить разные эффекты к изображению в профиле.

import datetime
import os.path
import sys

# import random
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QMainWindow, QToolBar,
                             QAction, QFileDialog, QApplication, QTextEdit, QSplitter)

from definitions import IMAGES_PATH
from profile_window import Dialog


class Messenger_Window(QMainWindow):

    # noinspection PyArgumentList
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        myFont = QFont('Arial', pointSize=14, weight=400)
        self.font = myFont
        self.chat_area = QTextEdit('В чат пока ничего не написали', readOnly=True, )
        self.message_area = QTextEdit('Введите сообщение', )
        self.message_area.setFont(myFont)
        self.chat_area.setFont(myFont)
        # h_splitter = QSplitter(Qt.Horizontal)
        # h_splitter.addWidget(self.text_edit)
        # h_splitter.addWidget(self.plain_text_edit)

        v_splitter = QSplitter(Qt.Vertical)
        v_splitter.addWidget(self.chat_area)
        v_splitter.addWidget(self.message_area)
        self.setCentralWidget(v_splitter)
        self.setGeometry(300, 300, 600, 600)
        self.create_actions()
        self.init_tool_bar()
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        app_icon = QIcon(os.path.join(IMAGES_PATH, 'worldwide.png'))
        self.setWindowIcon(app_icon)
        self.enable_actions(True)
        self.setWindowTitle('My awesome client')
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
        self.save_action = QAction(save_icon, 'Save chat as...', self, shortcut='Ctrl+S', triggered=self.dialog_save)
        self.send_action = QAction(send_icon, 'Send message', self, shortcut='Ctrl+Enter', triggered=self.send)
        self.edit_profile_action = QAction(profile_icon, 'Edit profile', self, triggered=self.edit_profile)
        self.bold_action = QAction(bold_icon, 'Bold', self, shortcut='Ctrl+S', triggered=self.make_bold)
        self.italic_action = QAction(italic_icon, 'Italic', self, shortcut='Ctrl+Enter', triggered=self.make_italic)
        self.underline_action = QAction(underline_icon, 'Underlined', self, triggered=self.make_underline)
        self.smile_action = QAction(smile_icon, 'Smile!', self, triggered=self.insert_smile)

    def init_tool_bar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(50, 50))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon | Qt.AlignLeading)  # <= Toolbuttonstyle
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        self.toolbar = toolbar
        self.toolbar.addAction(self.edit_profile_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.save_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.send_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.bold_action)
        self.toolbar.addAction(self.italic_action)
        self.toolbar.addAction(self.underline_action)

        self.toolbar.addAction(self.smile_action)

    def enable_actions(self, state):
        for action in self.toolbar.actions():
            action.setEnabled(state)

    def insert_smile(self):
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

    def send(self):
        self.chat_area.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.chat_area.append(self.message_area.toHtml())
        print(self.message_area.toHtml())

    def edit_profile(self):
        dlg = Dialog(self)
        dlg.exec_()


def main():
    app = QApplication(sys.argv)
    window = Messenger_Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
