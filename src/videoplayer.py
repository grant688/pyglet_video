#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function

__docformat__ = 'restructuredtext'
__version__ = '$Id$'

import os
#system imports
import sys

#pyqt imports
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pyglet

from win32api import GetSystemMetrics

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

# Disable error checking for increased performance
pyglet.options['debug_gl'] = False


pyglet.lib.load_library('../lib/avbin64.dll')
pyglet.have_avbin=True

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # set background
        palette=QtGui.QPalette()
        icon=QtGui.QPixmap('../res/background.jpg')
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(icon)) #添加背景图片
        self.setPalette(palette)
        self.color=QtGui.QColor(0, 0, 255)
        # self.setStyleSheet("background-color:black")




        # set title
        self.title = QLabel()
        self.title.setText("Welcome to Python GUI Programming")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedWidth(600)
        self.title.setFixedHeight(80)
        self.title.setStyleSheet("QLabel{background:yellow;}"
                   "QLabel{color:rgb(100,100,100,250);font-size:32px;font-weight:bold;font-family:Roman times;}"
                   "QLabel:hover{color:rgb(100,100,100,120);}")

        self.title.move(200,200)

        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.addWidget(self.title)
        self.vboxLayout.addStretch()
        self.setLayout(self.vboxLayout)

        self.qbtn_1=QtGui.QPushButton(u"",self)
        self.qbtn_1.setGeometry(400,360,80,80)
        self.qbtn_1.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                               "QPushButton:hover{background-color:#333333;}")
        self.qbtn_1.setIcon(QtGui.QIcon("../res/btn1.jpg"));
        self.qbtn_1.setIconSize(QSize(80, 80));
        self.qbtn_1.clicked.connect(lambda:self.whichbtn(self.qbtn_1))

        self.qbtn_2 = QPushButton(u"",self)
        self.qbtn_2.setGeometry(400,460,80,80)
        self.qbtn_2.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                "QPushButton:hover{background-color:#333333;}")
        self.qbtn_2.setIcon(QtGui.QIcon("../res/btn2.png"))
        self.qbtn_2.setIconSize(QSize(80, 80));
        self.qbtn_2.clicked.connect(lambda:self.whichbtn(self.qbtn_2))

        self.qbtn_3 = QPushButton(u"",self)
        self.qbtn_3.setGeometry(400,560,80,80)
        self.qbtn_3.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                "QPushButton:hover{background-color:#333333;}")
        self.qbtn_3.setIcon(QtGui.QIcon("../res/btn3.png"))
        self.qbtn_3.setIconSize(QSize(80, 80));
        self.qbtn_3.clicked.connect(lambda:self.whichbtn(self.qbtn_3))

        self.qbtn_4 = QPushButton(u"",self)
        self.qbtn_4.setGeometry(400,660,80,80)
        self.qbtn_4.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                "QPushButton:hover{background-color:#333333;}")
        self.qbtn_4.setIcon(QtGui.QIcon("../res/btn4.jpg"))
        self.qbtn_4.setIconSize(QSize(80, 80));
        self.qbtn_4.clicked.connect(lambda:self.whichbtn(self.qbtn_4))

        qbtn_close=QtGui.QPushButton(u"关闭此窗口",self)
        qbtn_close.setGeometry(800,360,120,80)
        qbtn_close.setStyleSheet("QPushButton{background-color:#D35400;border:none;color:#ffffff;font-size:20px;}"
                                 "QPushButton:hover{background-color:#333333;}")

        #注册事件
        self.connect(qbtn_close,QtCore.SIGNAL("clicked()"),QtGui.qApp,QtCore.SLOT("quit()"))

        self.showFullScreen()

    def whichbtn(self,b):
        print("clicked button is b2")
        video_path = "../res/a.wmv"
        if b == self.qbtn_1:
            video_path = "../res/a.wmv"
        elif b == self.qbtn_2:
            video_path = "../res/b.wmv"

        self.player_window = PlayerWindow(video_path)
        pyglet.app.run()

    def handlePlay(self):
        video_path = "../res/a.wmv"
        self.player_window = PlayerWindow(video_path)
        pyglet.app.run()

    def keyPressEvent(self, event):
        print("MainWindow(): keyPressEvent = ", event)
        if event.key() == QtCore.Qt.Key_A:
            self.showFullScreen()
        if event.key() == QtCore.Qt.Key_Escape:
            quit()


# class PlayerWindow(pyglet.window.Window):
class PlayerWindow(pyglet.window.Window):
    def __init__(self, video_path):
        super(PlayerWindow, self).__init__(caption='Media Player',
                                           visible=False,
                                           resizable=True)
        # video_path = "../res/a.wmv"
        source = pyglet.media.load(video_path)
        print("video_path = ", video_path)

        format = source.video_format
        print("format = ", format)
        if not format:
            print('No video track in this source.')
            sys.exit(1)

        self.player = pyglet.media.Player()
        print("get player ...")
        self.player.queue(source)
        self.player.play()
        print("player play...")

        video_width = format.width;
        video_height = format.height;


        window = pyglet.window.Window(width=screen_width, height=screen_height)

        window.set_fullscreen(True)

        window.push_handlers(pyglet.window.event.WindowEventLogger())

        @window.event
        def on_draw():
            window.clear()
            self.player.get_texture().blit((screen_width-format.width)/2, (screen_height-format.height)/2, width=format.width, height=format.height)

        @window.event
        def on_close():
            print("PlayerWindow(): on_close.")
            self.player.pause()
            self.close()

        @window.event
        def on_key_press(symbol,modifiers):
            print("PlayerWindow(): on_key_press, symbol = ", symbol)
            print("PlayerWindow(): on_key_press, ESCAPE = ", pyglet.window.key.ESCAPE)
            print("PlayerWindow(): on_key_press, A = ", pyglet.window.key.A)
            if symbol == pyglet.window.key.ESCAPE:
                print("PlayerWindow(): on_key_press,000000000000000")
                # self.dispatch_event('on_close')
                window.set_fullscreen(False)
            if symbol == pyglet.window.key.A:
                print("PlayerWindow(): on_key_press,111111111111111")


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Video Player")
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

