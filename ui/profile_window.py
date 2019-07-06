import os.path
import sys

from PyQt5.QtGui import QPixmap, QIcon, QPalette
from PyQt5.QtWidgets import (QLabel, QPushButton, QSizePolicy, QScrollArea,
                             QDialogButtonBox, QVBoxLayout, QHBoxLayout,
                             QFileDialog, QApplication, QInputDialog, QLineEdit, QFormLayout,
                             QDialog, QGroupBox)

from definitions import IMAGES_PATH
from image_editor import ImageEditor


class ProfileWindow(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(ProfileWindow, self).__init__()
        self.currentImage = ''
        self.init_ui()

    def init_ui(self):
        self.formGroupBox = QGroupBox()
        layout = QFormLayout()
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        load_button = QPushButton('Load image')
        load_button.clicked.connect(self.dialog_open)
        layout.addRow(QLabel('Name:'), self.username_edit)
        layout.addRow(QLabel('Password:'), self.password_edit)
        layout.addRow(QLabel('Profile picture:'), load_button)

        self.formGroupBox.setLayout(layout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.image_label = QLabel()
        group_image_buttons = self.init_image_buttons()
        self.image_label.setBackgroundRole(QPalette.Dark)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setScaledContents(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setWidget(self.image_label)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(group_image_buttons)
        mainLayout.addWidget(self.scroll_area)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.init_image_buttons()
        app_icon = QIcon(os.path.join(IMAGES_PATH, 'id-card-4.png'))
        self.setWindowTitle('Profile')
        self.setWindowIcon(app_icon)
        self.move(300, 200)

    def init_image_buttons(self):
        groupBox = QGroupBox('Image tools')
        push_bw = QPushButton('Black and White')
        push_inv = QPushButton('Inverted')
        push_gray = QPushButton('Grayscale')
        push_scale = QPushButton('Resize')
        gray_icon = QIcon(os.path.join(IMAGES_PATH, 'picture-gray.png'))
        bw_icon = QIcon(os.path.join(IMAGES_PATH, 'picture_bw.png'))
        inv_icon = QIcon(os.path.join(IMAGES_PATH, 'picture_inv.png'))
        scale_icon = QIcon(os.path.join(IMAGES_PATH, '020 - scale.png'))
        push_bw.setIcon(bw_icon)
        push_gray.setIcon(gray_icon)
        push_inv.setIcon(inv_icon)
        push_scale.setIcon(scale_icon)
        vbox = QHBoxLayout()
        vbox.addWidget(push_bw)
        vbox.addWidget(push_inv)
        vbox.addWidget(push_gray)
        vbox.addWidget(push_scale)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        push_bw.clicked.connect(self.set_bw)
        push_inv.clicked.connect(self.set_inverted)
        push_gray.clicked.connect(self.set_gray)
        push_scale.clicked.connect(self.scale)
        return groupBox

    def enable_actions(self, state):
        pass
        # for action in self.toolbar.actions():
        #     action.setEnabled(state)

    def dialog_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser(''),
                                            'Images (*.png *.xpm *.jpg);;All files (*.*)')[0]
        if fname:
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
        self.resize(self.image_label.width() + 30, self.image_label.height() + 210)

    def crop(self):
        if os.path.isfile(self.currentImage):
            self.pixmap = ImageEditor(self.currentImage).crop()
            self.image_label.setPixmap(self.pixmap)
            self.adjust_size()

    def scale(self):
        if os.path.isfile(self.currentImage):
            items = ('0.5', '0.7', '1.5')
            item, okPressed = QInputDialog.getItem(self, 'Resize image', 'Scale factor:', items, 0, False)
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


def main():
    app = QApplication(sys.argv)
    dialog = ProfileWindow()
    sys.exit(dialog.exec_())


if __name__ == '__main__':
    main()
