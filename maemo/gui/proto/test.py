#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
import sys
import sip
import time
import gobject
import dbus
import dbus.service
import dbus.mainloop.qt
from PyQt4 import QtGui
from PyQt4 import QtCore
#from tricksimulator import *


# class DemoException(dbus.DBusException):
#     _dbus_error_name = 'net.prometoys.solderinskater.DemoException'

class DbusTrickObject(dbus.service.Object):
    def __init__(self, bus_name,method,gui):

        # Here the object path
        dbus.service.Object.__init__(self, bus_name, method)
        self.gui = gui

    @dbus.service.method("net.prometoys.solderinskater.TrickService",
                         in_signature='s', out_signature='')
    def TrickCommit(self, hello_message):
        gui.trick_commit(str(hello_message))
        

    @dbus.service.method("net.prometoys.solderinskater.TrickService",
                         in_signature='', out_signature='')
    def RaiseException(self):
        raise DemoException('The RaiseException method does what you might '
                            'expect')

    # Signal senden
    @dbus.service.signal('net.prometoys.solderinskater.TrickService')
    def ShoutSignal(self, message):
        # The signal is emitted when this method exits
        # You can have code here if you wish
        pass

    # Musik senden
    @dbus.service.signal('net.prometoys.solderinskater.TrickService')
    def MusicSignal(self, message):
        # The signal is emitted when this method exits
        # You can have code here if you wish
        pass

    # Level senden
    @dbus.service.signal('net.prometoys.solderinskater.TrickService')
    def LevelSignal(self, message):
        # The signal is emitted when this method exits
        # You can have code here if you wish
        pass

    # dirty trick um signal senden zu triggern, dient als beispiel
    @dbus.service.method('net.prometoys.solderinskater.TrickService')
    def emitHelloSignal(self):
        # liste an shout samples die abgespielt werden soll
        self.ShoutSignal(['ollie','500p','awesome'])
        # level
        self.LevelSignal(1)
        # music
        self.MusicSignal(['electro','guitar','hiphop'])
        return 'Signal emitted'


class MainGui(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Solderin Skater TestApp')
        
        self.frame = QtGui.QFrame(self)
        self.frame.setGeometry(0, 0, 800, 480)

        self.setStyleSheet("QFrame {background-image: url(./startscreen.jpg);} \
            QLabel {background-image: url(./transp.png);} \
            QPushButton {height: 50px; background-color: black; \
            background-repeat:no-repeat; background-position: center;}")

        self.layout = QtGui.QVBoxLayout()
        
        self.buttonPlay = QtGui.QPushButton("")
        self.buttonPlay.setStyleSheet("background-image: url(./play.png);")
        self.buttonPlay.setFlat(True)
        
        self.buttonSettings = QtGui.QPushButton("")
        self.buttonSettings.setStyleSheet("background-image: url(./settings.png);")
        self.buttonSettings.setFlat(True)
        
        self.buttonQuit = QtGui.QPushButton("")
        self.buttonQuit.setStyleSheet("background-image: url(./quit.png);")
        self.buttonQuit.setFlat(True)

        self.spaceLabel1 = QtGui.QLabel("")
        self.spaceLabel2 = QtGui.QLabel("")
        self.spaceLabel3 = QtGui.QLabel("")

        self.connect(self.buttonPlay, QtCore.SIGNAL("clicked()"), self.play);
        self.connect(self.buttonSettings, QtCore.SIGNAL("clicked()"), self.settings);
        self.connect(self.buttonQuit, QtCore.SIGNAL("clicked()"), sys.exit);
                                            
        self.layout.addWidget(self.spaceLabel1)
        self.layout.addWidget(self.spaceLabel2)
        self.layout.addWidget(self.buttonPlay)
        self.layout.addWidget(self.buttonSettings)
        self.layout.addWidget(self.buttonQuit)
        self.layout.addWidget(self.spaceLabel3)
         
        self.frame.setLayout(self.layout)
        #self.showFullScreen()
        
        self

    def play(self):
        print "Open play window"
        self.setStyleSheet("QFrame {background-image: url(./PLAYERZ.jpg);} \
            QLabel {background-image: url(./transp.png);} \
            QPushButton {height: 50px; background-color: black; \
            background-repeat:no-repeat; background-position: center;}")
    # remove old buttons - del buttons if not needed again
        self.layout.removeWidget(self.spaceLabel1)
        self.spaceLabel1.setParent(None)
        self.layout.removeWidget(self.spaceLabel2)
        self.spaceLabel2.setParent(None)
        self.layout.removeWidget(self.spaceLabel3)
        self.spaceLabel3.setParent(None)
        self.layout.removeWidget(self.buttonPlay)
        self.buttonPlay.setParent(None)
        self.layout.removeWidget(self.buttonSettings)
        self.buttonSettings.setParent(None)
        self.layout.removeWidget(self.buttonQuit)
        self.buttonQuit.setParent(None)
        # add new buttons
        self.hbox1 = QtGui.QHBoxLayout()
        self.buttonBack = QtGui.QPushButton("")
        self.buttonBack.setStyleSheet("background-image: url(./back.png); background-position: top left;")
        self.buttonBack.setFlat(True)
        self.connect(self.buttonBack, QtCore.SIGNAL("clicked()"), self.back);
        self.hbox1.addWidget(self.buttonBack)
        self.hbox1.addWidget(self.spaceLabel1)
        self.layout.addLayout(self.hbox1) 
        
        self.layout.addWidget(self.spaceLabel2)
        self.spaceLabel4 = QtGui.QLabel("")
        self.layout.addWidget(self.spaceLabel4)
        
        self.hbox2 = QtGui.QHBoxLayout()
        self.buttonSingle = QtGui.QPushButton("")
        self.buttonSingle.setStyleSheet("background-image: url(./singleplayer.png);")
        self.buttonSingle.setFlat(True)
        self.connect(self.buttonSingle, QtCore.SIGNAL("clicked()"), self.singleplayer);
        self.hbox2.addWidget(self.buttonSingle)
        self.buttonMulti = QtGui.QPushButton("")
        self.buttonMulti.setStyleSheet("background-image: url(./multiplayer.png);  background-position: left;")
        self.buttonMulti.setFlat(True)
        self.connect(self.buttonMulti, QtCore.SIGNAL("clicked()"), self.multiplayer);
        self.hbox2.addWidget(self.buttonMulti)
        self.layout.addLayout(self.hbox2) 
        
        self.layout.addWidget(self.spaceLabel3)
    
    def back(self):
        print "Going back not implemented yet, quitting."
        sys.exit()

    def settings(self):
        print "Open settings window"

    def singleplayer(self):
        print "Start Singleplayer Game"
        self.setStyleSheet("QFrame {background-image: url(./PLAYMODES.jpg);} \
            QLabel {background-image: url(./transp.png);} \
            QPushButton {height: 50px; background-color: black; \
            background-repeat:no-repeat; background-position: center;}")
    # remove buttons
        self.hbox1.setParent(None)
        self.hbox2.removeWidget(self.buttonSingle)
        self.buttonSingle.setParent(None)
        self.hbox2.removeWidget(self.buttonMulti)
        self.buttonMulti.setParent(None)
        self.hbox2.setParent(None)
        self.layout.removeWidget(self.spaceLabel2)
        self.spaceLabel2.setParent(None)
        self.layout.removeWidget(self.spaceLabel3)
        self.spaceLabel3.setParent(None)
        self.layout.removeWidget(self.spaceLabel4)
        self.spaceLabel4.setParent(None)
        # add buttons
        self.layout.addLayout(self.hbox1) 
        self.layout.addWidget(self.spaceLabel2)
        self.buttonChallenge = QtGui.QPushButton("")
        self.buttonChallenge.setStyleSheet("background-image: url(./challenge.png);")
        self.buttonChallenge.setFlat(True)
        self.connect(self.buttonChallenge, QtCore.SIGNAL("clicked()"), self.challenge);
        self.layout.addWidget(self.buttonChallenge)
        self.buttonFreestyle = QtGui.QPushButton("")
        self.buttonFreestyle.setStyleSheet("background-image: url(./freestyle.png);")
        self.buttonFreestyle.setFlat(True)
        self.connect(self.buttonFreestyle, QtCore.SIGNAL("clicked()"), self.freestyle);
        self.layout.addWidget(self.buttonFreestyle)
        self.buttonHighscore = QtGui.QPushButton("")
        self.buttonHighscore.setStyleSheet("background-image: url(./highscore.png);")
        self.buttonHighscore.setFlat(True)
        self.connect(self.buttonHighscore, QtCore.SIGNAL("clicked()"), self.highscore);
        self.layout.addWidget(self.buttonHighscore)
        self.layout.addWidget(self.spaceLabel3)
        self.layout.addWidget(self.spaceLabel4)

    

    def multiplayer(self):
        print "Start Multiplayer Game"

    def challenge(self):
        print "Start Challenge"

    def freestyle(self):
        print "Start Freestyle"

    def highscore(self):
        print "View Highscore"

    def ollie(self):
        print "Fantastischer Ollie"

    def three_sixty(self):
        print "Wow, 360!"

    def shove(self):
        print "Nice, Shove-it"

    def kickflip(self):
        print "Awesome Kickflip"

    def heelflip(self):
        print "Was für ein Heelflip"
    

    def trick_commit(self, trickid):
        if trickid == "ollie":
            self.ollie()
        elif trickid == "360":
            self.three_sixty()
        elif trickid == "kickflip":
            self.kickflip()
        elif trickid == "heelflip":
            self.heelflip()
        elif trickid == "shove":
            self.shove()
        else:
            print "Unknown Trick " + trickid



if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)

    gui = MainGui()

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("net.prometoys.solderinskater.TrickService", session_bus)
    object = DbusTrickObject(session_bus, '/net/prometoys/solderinskater/TrickService/DbusTrickObject',gui)

    #mainloop = gobject.MainLoop()
    #print "Running example service."
    #mainloop.run()


    print "GUI Laden"
    
    print "sleep"
    #time.sleep(5)
    object.ShoutSignal('Shout')
    print "shout"

    gui.show()
    app.exec_()

    
    
    
