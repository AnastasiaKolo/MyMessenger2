# -*- coding: utf-8 -*-
# Все задания делать локально, без использования базы данных. Сохранять можно в обычный текстовый файл.
#
# 1. Сделать программу, которая будет загружать изображения с компьютера и добавлять к ним эффекты.
# 2. Добавить форматирование в сообщения в вашем мессенджере.
# 3. Реализовать возможность добавления фотографии в ваш профиль.
# 4. *Нужно сделать предыдущее задание и добавить смайлы в мессенджер.
# 5. *Нужно сделать предыдущее задание и применить разные эффекты к изображению в профиле.


import os.path
import sys

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QIcon, QPalette
from PyQt5.QtWidgets import (QMainWindow, QLabel, QDesktopWidget, QSizePolicy, QScrollArea,
                             QAction, QFileDialog, QApplication, QInputDialog)

from definitions import IMAGES_PATH

class MainWindow(QMainWindow):

    # noinspection PyArgumentList
    def __init__(self):
        super().__init__()
        self.currentImage = ''

        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 350, 300)
        self.center()

        self.image_label = QLabel()
        self.image_label.setBackgroundRole(QPalette.Dark)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setScaledContents(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setWidget(self.image_label)
        self.setCentralWidget(self.scroll_area)
        self.create_actions()
        self.init_tool_bar()
        app_icon = QIcon(os.path.join(IMAGES_PATH, 'photos.png'))
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction(self.open_file)
        file_menu.addAction(self.save_file)
        self.enable_actions(False)
        self.setWindowTitle('Image processing')
        self.setWindowIcon(app_icon)
        self.statusBar().showMessage('Ready')

    # noinspection PyArgumentList
    def create_actions(self):
        open_icon = QIcon(os.path.join(IMAGES_PATH, 'folder-10.png'))
        save_icon = QIcon(os.path.join(IMAGES_PATH, 'save.png'))
        gray_icon = QIcon(os.path.join(IMAGES_PATH, 'picture-gray.png'))
        sepia_icon = QIcon(os.path.join(IMAGES_PATH, 'picture-sepia.png'))
        bw_icon = QIcon(os.path.join(IMAGES_PATH, 'picture_bw.png'))
        bw_icon_2 = QIcon(os.path.join(IMAGES_PATH, 'picture_bw_2.png'))
        inv_icon = QIcon(os.path.join(IMAGES_PATH, 'picture_inv.png'))
        orig_icon = QIcon(os.path.join(IMAGES_PATH, 'picture.png'))
        scale_icon = QIcon(os.path.join(IMAGES_PATH, '020-scale.png'))
        crop_icon = QIcon(os.path.join(IMAGES_PATH, '018-crop.png'))
        self.open_file = QAction(open_icon, '&Open...', self, shortcut='Ctrl+O', triggered=self.dialog_open, )
        self.save_file = QAction(save_icon, '&Save as...', self, shortcut='Ctrl+S', triggered=self.dialog_save)
        self.set_gray_action = QAction(gray_icon, 'Gray tones', self, triggered=self.set_gray)
        self.set_bw_action = QAction(bw_icon, 'Black and white', self, triggered=self.set_bw)
        self.set_bw2_action = QAction(bw_icon_2, 'Black and white method 2', self, triggered=self.set_bw2)
        self.set_sepia_action = QAction(sepia_icon, 'Sepia', self, triggered=self.set_sepia)
        self.set_inverted_action = QAction(inv_icon, 'Inverted', self, triggered=self.set_inverted)
        self.set_original_action = QAction(orig_icon, 'Original', self, triggered=self.set_original)
        self.scale_action = QAction(scale_icon, 'Scale', self, triggered=self.scale)
        self.crop_action = QAction(crop_icon, 'Crop', self, triggered=self.crop)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_tool_bar(self):

        self.toolbar = self.addToolBar('Image tools')
        self.toolbar.addAction(self.set_original_action)
        self.toolbar.addAction(self.set_gray_action)
        self.toolbar.addAction(self.set_bw_action)
        self.toolbar.addAction(self.set_bw2_action)
        self.toolbar.addAction(self.set_sepia_action)
        self.toolbar.addAction(self.set_inverted_action)
        self.toolbar.addAction(self.scale_action)
        self.toolbar.addAction(self.crop_action)

    def enable_actions(self, state):
        for action in self.toolbar.actions():
            action.setEnabled(state)

    def dialog_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser(''),
                                            'Images (*.png *.xpm *.jpg);;All files (*.*)')[0]
        if fname:
            self.statusBar().showMessage('Selected file: {}'.format(fname))
            print(fname)
        if os.path.isfile(fname):
            self.pixmap = QPixmap(fname)
            self.currentImage = fname
            self.image_label.setPixmap(self.pixmap)
            self.adjust_size()
            self.enable_actions(True)


    def dialog_save(self):
        fname = QFileDialog.getSaveFileName(self, 'Save as', os.path.expanduser(''),
                                            'Images (*.png *.xpm *.jpg);;All files (*.*)')[0]
        if fname:
            self.statusBar().showMessage('Saved file as: {}'.format(fname))
            print(fname)
            self.pixmap.save(fname)
            self.currentImage = fname

    def adjust_size(self):
        self.image_label.adjustSize()
        self.resize(self.image_label.width()+25, self.image_label.height()+60)


    def crop(self):
        if os.path.isfile(self.currentImage):
            self.pixmap = ImageEditor(self.currentImage).crop()
            self.image_label.setPixmap(self.pixmap)
            self.adjust_size()

    def scale(self):
        if os.path.isfile(self.currentImage):
            items = ('0.5','0.7','1.5')
            item, okPressed = QInputDialog.getItem(self, 'Resize image', 'Scale factor:', items, 0 ,False)
            if okPressed and item:
                print(item)
                self.pixmap = ImageEditor(self.currentImage).resize(item)
                self.image_label.setPixmap(self.pixmap)
                self.adjust_size()

    def set_bw(self):
        if os.path.isfile(self.currentImage):
            self.pixmap = ImageEditor(self.currentImage).bw()
            self.image_label.setPixmap(self.pixmap)
            self.adjust_size()

    def set_bw2(self):
        if os.path.isfile(self.currentImage):
            self.pixmap = ImageEditor(self.currentImage).bw2()
            self.image_label.setPixmap(self.pixmap)
            self.adjust_size()

    def set_inverted(self):
        if os.path.isfile(self.currentImage):
            self.pixmap = ImageEditor(self.currentImage).inverted()
            self.image_label.setPixmap(self.pixmap)
            self.adjust_size()

    def set_sepia(self):
        if os.path.isfile(self.currentImage):
            self.pixmap = ImageEditor(self.currentImage).sepia()
            self.image_label.setPixmap(self.pixmap)
            self.adjust_size()

    def set_original(self):
        if os.path.isfile(self.currentImage):
            self.pixmap = QPixmap(self.currentImage)
            self.image_label.setPixmap(self.pixmap)
            self.adjust_size()

    def set_gray(self):
        if os.path.isfile(self.currentImage):
            self.pixmap = ImageEditor(self.currentImage).gray()
            self.image_label.setPixmap(self.pixmap)
            self.adjust_size()





class ImageEditor:
    def __init__(self, path):
        self.image = Image.open(path)
        self.draw = ImageDraw.Draw(self.image)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pix = self.image.load()

    def crop(self):
        self.image = self.image.crop((0, 0, 300, 300))
        img_tmp = ImageQt(self.image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)
        return pixmap

    def resize(self, factor):
        if (self.width > 4000 or self.height > 4000) and factor == '1.5':
            raise ValueError('Too large image to resize: {}x{} factor {}'.format(self.width, self.height, factor))
        factor_to_num = {
            '0.5': 0.5,
            '0.7': 0.7,
            '1.5': 1.5
        }
        try:
            self.width = int(factor_to_num[factor] * self.width)
            self.height = int(factor_to_num[factor] * self.height)
            print('new width {} new heigth {}'.format(self.width, self.height))
        except KeyError:
            raise ValueError('Not found factor {}'.format(factor))
        self.image = self.image.resize((self.width, self.height), Image.NEAREST)
        img_tmp = ImageQt(self.image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)
        return pixmap

    def gray(self):
        img_tmp = ImageQt(self.image.convert('L'))
        pixmap = QPixmap.fromImage(img_tmp)
        return pixmap

    def bw(self) -> object:
        factor = 30
        for i in range(self.width):
            for j in range(self.height):
                a = self.pix[i, j][0]
                b = self.pix[i, j][1]
                c = self.pix[i, j][2]
                s = a + b + c
                if s > (((255 + factor) // 2) * 3):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0
                self.draw.point((i, j), (a, b, c))
        img_tmp = ImageQt(self.image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)
        return pixmap
    
    def bw2(self):
        img_tmp = ImageQt(self.image.convert('1'))
        pixmap = QPixmap.fromImage(img_tmp)
        return pixmap
    
    def inverted(self):
        for i in range(self.width):
            for j in range(self.height):
                a = self.pix[i, j][0]
                b = self.pix[i, j][1]
                c = self.pix[i, j][2]
                self.draw.point((i, j), (255 - a, 255 - b, 255 - c))

        img_tmp = ImageQt(self.image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)
        return pixmap

    def sepia(self):
        # faster sepia filter here https://yabirgb.com/blog/creating-a-sepia-filter-with-python/
        # another sepia filter using palette http://effbot.org/zone/pil-sepia.htm
        for i in range(self.width):
            for j in range(self.height):
                r = self.pix[i, j][0]
                g = self.pix[i, j][1]
                b = self.pix[i, j][2]

                sep_r = int(r * .393 + g * .769 + b * .189)
                sep_g = int(r * .349 + g * .686 + b * .168)
                sep_b = int(r * .272 + g * .534 + b * .131)

                if sep_r > 255:
                    sep_r = 255
                if sep_g > 255:
                    sep_g = 255
                if sep_b > 255:
                    sep_b = 255
                self.draw.point((i, j), (sep_r, sep_g, sep_b))
        img_tmp = ImageQt(self.image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)
        return pixmap




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
