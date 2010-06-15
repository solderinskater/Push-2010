# Copyright 2010 Keywan Tonekaboni, Florian Fusco, Stefanie Schirmer, Alexander Lenhard, Erik Weitnauer <eweitnauer at gmail.com>
#
# This file is part of Soldering Skaters Nokia Push Project.
#
# Soldering Skaters Nokia Push Project is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Soldering Skaters Nokia Push Project is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Soldering Skaters Nokia Push Project.  If not, see <http://www.gnu.org/licenses/>.
#!/usr/bin/python4.5
# -*- coding: utf-8 -*-
import sys
import sip
from PyQt4 import QtGui
from PyQt4 import QtCore
import time
from classifier import *
from traceback import print_exc
import random
#from dbus.mainloop.glib import DBusGMainLoop
#import gobject
import dbus.mainloop.qt
from dataBridge import *

class Simulator(QtCore.QObject):

    def __init__(self, dataFile):
        QtCore.QObject.__init__(self, None)
        
#        self.dat = QtCore.QFile(dataFile)
        self.isOk = False
#        self.isStopped = True
 #       if (self.dat.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text)):
        self.isOk = True
#        self.btn = QtGui.QPushButton("Start")
#        self.btn2= QtGui.QPushButton("Stop")
#        self.connect(self.btn, QtCore.SIGNAL("clicked()"), self.replay)
#        self.connect(self.btn2, QtCore.SIGNAL("clicked()"), self.stop)
#        QtGui.QGridLayout(self)
#        self.layout().addWidget(self.btn)
#        self.layout().addWidget(self.btn2)
        self.lda = Classifier("lenny_ollie_vs_180_new.lda")
        self.lda = Classifier("ollie_vs_shoveit.lda")
        self.bridge = DataBridge()

#
        #bus = dbus.SessionBus()
        bus = dbus.bus.BusConnection('unix:path=/tmp/skater_socket')
        try:
            remote_object = bus.get_object("net.prometoys.solderinskater.TrickService",
					   "/net/prometoys/solderinskater/TrickService/DbusTrickObject")
        except dbus.DBusException:
            print_exc()
            sys.exit(1)

        self.iface = dbus.Interface(remote_object, "net.prometoys.solderinskater.TrickService")
        if self.bridge.start():
        	self.replay()

        
    def setFile(self, dataFile):
##        if self.dat.isOpen():
#            self.dat.close()
#        self.dat.setFileName(dataFile)
#        self.isOk = False
#        if (self.dat.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text)):
#            self.isOk = True
        self.k=1
    
    def trickRecognized(self, which):
        self.iface.TrickCommit(which)
        print str(which)

    
    def replay(self):
#        self.dat.reset()
        maxwin = 10
        ev=[0]*maxwin
        curSmp = 0
        smp = 0
        trickRefrac = 20
        minTrickMarks = 3
        curRefrac = 0
        self.isStopped = False
        self.stream = QtCore.QTextStream() #self.dat)
#        self.line = self.stream.readLine()
        self.line = self.bridge.readline()
        h=1
        while not (self.isStopped):
#            self.emit(QtCore.SIGNAL("newData(const QString&)"), self.line)
#            print self.line
#            if len(string.split(self.line,',')) > 0:
#                print string.split(self.line,',')
#                s = 2 #self.lda.classify(self.line)
#            else:
#                print "hhhhh "+self.line
#                s = ""
#            print self.line
            s=self.lda.classify(self.line)
            ev[smp] = 0
            if (s!=""):
                curSmp = s
                ev[smp] = 1
                if curRefrac==0:
                    if sum(ev)>=minTrickMarks:
#                        self.trickRecognized((curSmp-maxwin)/65)
                        self.trickRecognized(s)
                        curRefrac = 1
                else:
                    curRefrac = curRefrac + 1
                    if curRefrac==trickRefrac:
                        curRefrac = 0
            smp = smp+1
            if smp==maxwin:
                smp=maxwin-1
                ev[0:maxwin-1] = ev[1:]
                        
            self.line = self.bridge.readline()
#            self.line = self.stream.readLine()
#            QtGui.QApplication.processEvents()
#            time.sleep(1.0/65)
        self.isStopped = True
        
    def stop(self):
        self.isStopped = True
#       print "WHEEEEEEEEEEEEEEEEEEEEEEEEEEEE\n\n\n"
            

app = QtGui.QApplication(sys.argv)
dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
gui = Simulator("ollie.1.log")
app.exec_()
