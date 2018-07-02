import time
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon


class PollTimeThread(QtCore.QThread):
  """
  This thread works as a timer.
  """
  update = QtCore.pyqtSignal()

  def __init__(self, parent):
    super(PollTimeThread, self).__init__(parent)

  def run(self):
    while True:
      time.sleep(1)
      if self.isRunning():
        # emit signal
        self.update.emit()
      else:
        return

class Window(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)

    # media
    self.media = Phonon.MediaObject(self)
    self.media.stateChanged.connect(self.handleStateChanged)
    self.video = Phonon.VideoWidget(self)
    self.video.setMinimumSize(200, 200)
    self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self)
    Phonon.createPath(self.media, self.audio)
    Phonon.createPath(self.media, self.video)

    # control button
    self.button = QtGui.QPushButton('Chose File', self)
    self.button.clicked.connect(self.handleButton)

    # for display of time lapse
    self.info = QtGui.QLabel(self)

    # layout
    layout = QtGui.QGridLayout(self)
    layout.addWidget(self.video, 1, 1, 3, 3)
    layout.addWidget(self.info, 4, 1, 1, 3)
    layout.addWidget(self.button, 5, 1, 1, 3)

    # signal-slot, for time lapse
    self.thread = PollTimeThread(self)
    self.thread.update.connect(self.update)

  def update(self):
    # slot
    lapse = self.media.currentTime()/1000.0
    self.info.setText("%4.2f second" % lapse)

  def startPlay(self):
    if self.path:
      self.media.setCurrentSource(Phonon.MediaSource(self.path))

      # use a thread as a timer
      self.thread = PollTimeThread(self)
      self.thread.update.connect(self.update)
      self.thread.start()
      self.media.play()

  def handleButton(self):
    if self.media.state() == Phonon.PlayingState:
      self.media.stop()
      self.thread.terminate()
    else:
      self.path = QtGui.QFileDialog.getOpenFileName(self, self.button.text())
      self.startPlay()

  def handleStateChanged(self, newstate, oldstate):
    if newstate == Phonon.PlayingState:
      self.button.setText('Stop')
    elif (newstate != Phonon.LoadingState and
       newstate != Phonon.BufferingState):
      self.button.setText('Chose File')
      if newstate == Phonon.ErrorState:
        source = self.media.currentSource().fileName()
        print ('Error:can not play:', source.toLocal8Bit().data())
        print (' %s' % self.media.errorString().toLocal8Bit().data())


if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  app.setApplicationName('video play')
  window = Window()
  window.show()
  sys.exit(app.exec_())