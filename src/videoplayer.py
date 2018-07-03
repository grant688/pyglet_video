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
        self.connect(qbtn_one,QtCore.SIGNAL("clicked()"),self.handlePlay)
        self.connect(qbtn_close,QtCore.SIGNAL("clicked()"),QtGui.qApp,QtCore.SLOT("quit()"))

    def handlePlay(self):
        self.player_window = PlayerWindow()
        pyglet.app.run()

    def keyPressEvent(self, event):
        print("MainWindow(): keyPressEvent = ", event)
        if event.key() == QtCore.Qt.Key_A:
            self.showFullScreen()
        if event.key() == QtCore.Qt.Key_Escape:
            self.showNormal()


# class PlayerWindow(pyglet.window.Window):
class PlayerWindow(pyglet.window.Window):
    def __init__(self):
        super(PlayerWindow, self).__init__(caption='Media Player',
                                           visible=False,
                                           resizable=True)
        video_path = "../res/a.wmv"
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

        # video_width = screen_width
        # video_height = screen_height

        window = pyglet.window.Window(width=screen_width, height=screen_height)

        # self.window.set_fullscreen(True)

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
            if symbol == pyglet.window.key.A:
                print("PlayerWindow(): on_key_press,111111111111111")
                window.set_fullscreen(True)

    # def keyPressEvent(self, event):
    #     print("PlayerWindow(): keyPressEvent = ", event)
    #     if event.key() == QtCore.Qt.Key_A:
    #         self.MainWindow.set_fullscreen(True)
    #     if event.key() == QtCore.Qt.Key_Escape:
    #         self.on_close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Video Player")
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

