import sys

from PyQt4.QtGui import QApplication, QMainWindow, QDirModel, QColumnView
from PyQt4.QtGui import QFrame
from PyQt4.QtCore import SIGNAL
from PyQt4.phonon import Phonon

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.m_media = None

    def play(self):
        self.delayedInit()
        #self.m_media.setCurrentSource(self.m_model.filePath(index))
        self.m_media.setCurrentSource(
            Phonon.MediaSource("music.mp3"))
        self.m_media.play()

    def delayedInit(self):
        if not self.m_media:
            self.m_media = Phonon.MediaObject(self)
            audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
            Phonon.createPath(self.m_media, audioOutput)

def main():
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Phonon Tutorial 2 (Python)")
    mw = MainWindow()
    mw.play()
    #sys.exit(app.exec_())

if __name__ == '__main__':
    main()

