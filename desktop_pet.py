# *_* coding : UTF-8 *_*
# author : Rick.Liang
# time : 20230204
import os
import sys
# import random
import win32api
import cv2
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

# print(QT_VERSION_STR)
# print(PYQT_VERSION_STR)

class Pet():
    def __init__(self, img_pth):
        self.screen_size = tuple(map(win32api.GetSystemMetrics, [0, 1]))
        
        self.img_id = 1
        self.img_num = 20
        self.img_pth = img_pth
        self.img = cv2.imread(self.img_pth)
        self.img_height, self.img_width = self.img.shape[:2]

        self.birth_pos = (
            self.screen_size[0] - 1.25 * self.img_width, 
            self.screen_size[1] - 1.35 * self.img_height
        )
        self.birth_pos = tuple(map(int, self.birth_pos))
        self.cur_pos = self.birth_pos

    def gif(self):
        if self.image_id < 61:
            self.image_id += 1
        else:
            self.image_id = 1
        self.image = self.image_url + str(self.image_id) + ').png'


class MyLabel(QLabel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        #声明
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # 开放右键策略
        self.customContextMenuRequested.connect(self.rightMenuShow)

    # 添加右键菜单
    def rightMenuShow(self, pos):
        menu = QMenu(self)
        menu.addAction(QAction(QIcon('data/icon/percent-outline.png'), '计算器', self, triggered=self.calc))
        menu.addAction(QAction(QIcon('data/icon/eye-off-outline.png'), '隐藏', self, triggered=self.hide))
        menu.addAction(QAction(QIcon('data/icon/power-outline.png'), '退出', self, triggered=self.quit))
        # menu.addAction(QAction(QIcon('image/exit.png'), '打开网易云', self, triggered=self.music))
        menu.exec(QCursor.pos())

    def calc(self):
        try:
            os.system("calc.exe")        
        except:
            print('error')

    def hide(self):
        self.setVisible(False)

    def quit(self):
        self.close()
        sys.exit()


class Puppy(QWidget):
    def __init__(self, *args, **kw):
        super(Puppy, self).__init__()

        self.puppy=Pet(img_pth='data/doge/Doge-Picture-x240.png')

        self.is_follow_mouse = False

        self.initUi()
        self.tray()

        # 每隔一段时间执行
        # timer_puppy = QTimer(self)
        # timer_puppy.timeout.connect(self.gem)
        # timer_puppy.start(250)

    def initUi(self):

        ##窗口大小
        self.setGeometry(0, 0, *self.puppy.screen_size)

        ##标签
        self.lb_puppy = MyLabel(self)
        self.pm_puppy= QPixmap(self.puppy.img_pth)
        self.lb_puppy.setPixmap(self.pm_puppy)
        self.lb_puppy.move(*self.puppy.birth_pos)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.SubWindow
        )
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.showMaximized()


    def mouseDoubleClickEvent(self, QMouseEvent):
        self.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_follow_mouse = True

            event.accept()
            self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton and self.is_follow_mouse:
            self.puppy.cur_pos = (
                QCursor.pos().x() - int(self.puppy.img_width / 2),
                QCursor.pos().y() - int(self.puppy.img_height / 2),
            )
            self.lb_puppy.move(*self.puppy.cur_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    # 系统托盘
    def tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('data/doge/Doge-Head-x200.png'))
        display = QAction(QIcon('data/icon/eye-outline.png'), '显示', self, triggered=self.display)
        quit = QAction(QIcon('data/icon/power-outline.png'), '退出', self, triggered=self.quit)
        menu = QMenu(self)
        menu.addAction(display)
        menu.addAction(quit)
        self.tray.setContextMenu(menu)
        self.tray.show()

    def hide(self):
        self.lb_puppy.setVisible(False)

    def display(self):
        self.lb_puppy.setVisible(True)

    def quit(self):
        self.close()
        sys.exit()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    puppy = Puppy()
    sys.exit(app.exec())
