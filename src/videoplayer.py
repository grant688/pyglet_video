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
from PyQt4.QtCore import Qt

import pyglet

from win32api import GetSystemMetrics

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

# Disable error checking for increased performance
pyglet.options['debug_gl'] = False
# pyglet.options['debug_gl'] = True
# from pyglet.gl import *

pyglet.lib.load_library('../lib/avbin64.dll')
pyglet.have_avbin=True

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        #QtGui.QWidget.__init__(self)
        super(MainWindow, self).__init__(parent)

        #self.resize(600, 400)
        self.setStyleSheet("background-color:black")

        #按钮一
        qbtn_one=QtGui.QPushButton(u"开始测试",self)
        qbtn_one.setGeometry(400,360,120,80)
        qbtn_one.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                               "QPushButton:hover{background-color:#333333;}")

        qbtn_close=QtGui.QPushButton(u"关闭此窗口",self)
        qbtn_close.setGeometry(600,360,120,80)
        qbtn_close.setStyleSheet("QPushButton{background-color:#D35400;border:none;color:#ffffff;font-size:20px;}"
                                 "QPushButton:hover{background-color:#333333;}")

        #注册事件
        self.connect(qbtn_one,QtCore.SIGNAL("clicked()"),QtGui.qApp,QtCore.SLOT("quit()"))
        self.connect(qbtn_close,QtCore.SIGNAL("clicked()"),QtGui.qApp,QtCore.SLOT("quit()"))

        # video_path = "../res/a.wmv"
        # source = pyglet.media.load(video_path)
        # print("video_path = ", video_path)

        # format = source.video_format
        # print("format = ", format)
        # if not format:
        #     print('No video track in this source.')
        #     sys.exit(1)

        # self.player = pyglet.media.Player()
        # self.player.queue(source)
        # self.player.play()

        # self.showFullScreen()    #全屏显示必须放在所有组件画完以后执行

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_A:
            # self.showFullScreen()
            player_window = PlayerWindow()
            # pyglet.app.run()
        if event.key() == QtCore.Qt.Key_Escape:
            self.showNormal()

    # def on_draw(self):
    #     #self.clear()
    #     self.player.get_texture().blit((self.width-self.player.width)/2, self.player.y, width=self.player.width, height=self.player.height)

# class PlayerWindow(pyglet.window.Window):
class PlayerWindow():
    def __init__(self):
        # super(PlayerWindow, self).__init__(caption='Media Player',
        #                                    visible=False,
        #                                    resizable=True)
        video_path = "../res/a.wmv"
        source = pyglet.media.load(video_path)
        print("video_path = ", video_path)

        format = source.video_format
        print("format = ", format)
        if not format:
            print('No video track in this source.')
            sys.exit(1)

        player = pyglet.media.Player()
        print("get player ...")
        player.queue(source)
        player.play()
        print("player play...")

        # video_width = format.width;
        # video_height = format.height;

        video_width = screen_width
        video_height = screen_height

        window = pyglet.window.Window(width=screen_width, height=screen_height)

        # window.set_visible(True)
        window.set_fullscreen(True)

        # window = mainwindow
        # window.showFullScreen()

        @window.event
        def on_draw():
            window.clear()
            player.get_texture().blit((screen_width-format.width)/2, (screen_height-format.height)/2, width=format.width, height=format.height)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Video Player")
    # window = MainWindow()
    window = PlayerWindow()

    # window.show()
    pyglet.app.run()
    sys.exit(app.exec_())

