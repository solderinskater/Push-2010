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
#!/usr/bin/python
# -*- coding: utf-8-*-
# tiltnroll.py

import sys
import random
from PyQt4 import QtCore, QtGui
import dbus
import dbus.service
import dbus.mainloop.qt
from screens import *
import os
import twitter.twitter as twitter


class TrickObject():
  def __init__(self, trickID, points, name): # TODO soundfiles hinzu
    self.trickID = trickID
    self.points = points
    self.name = name

class TiltnRoll(QtGui.QMainWindow):
  # variables here

  is_ingame = False
  CHALLENGE_MODE = 1
  FREESTYLE_MODE = 2
  MENU_MODE = 0
  state = MENU_MODE
  tricklist = {'ollie':TrickObject('ollie', 1., 'Ollie'),
      '180':TrickObject('180', 1.5,'180'),
      'nollie360':TrickObject('nollie360', 3.,'Nollie 360'),
      'nollie180':TrickObject('nollie180', 2.,'Nollie 180'),
      '360':TrickObject('360', 5.,'360'),
      'kickflip':TrickObject('kickflip', 5.,'Kickflip'),
      'heelflip':TrickObject('heelflip', 2.,'Heelflip'),
      'shove':TrickObject('shove', 3.,'Shove'),
      'frontsideflip':TrickObject('frontsideflip', 3.,'Frontsideflip'),
      'caballerial':TrickObject('caballerial',8.,'Caballerial'),
      'unknown':TrickObject('unknown',0.,'some trick')}

  tricks_done = list()
  dbusCommunicator = 0
  
  level = 1
  points = 0
  lastChallenge = 0
  currentChallenge = 0
  nextChallenge = 0
  time = 0
  
  # settings 
  Electro=True
  Guitars=True
  HipHop=True
  Regular=True
  Goofy=False
  Twitter=False
  twitterName='skater_test'
  twitterPass='sk4ter!'

  def __init__(self):
    QtGui.QMainWindow.__init__(self)

    self.setGeometry(0, 0, 800, 480)
    self.setWindowTitle("Tilt'n'Roll")
    self.showFullScreen()
    self.timer = QtCore.QBasicTimer()
    self.start()
    createHighscoreFile()

    # menu functions

  def start(self):
    state = self.MENU_MODE
    print "Start game"
    self.startscreen = StartScreen(self)
    self.connect(self.startscreen.buttonPlay, QtCore.SIGNAL("clicked()"), self.play);
    self.connect(self.startscreen.buttonSettings, QtCore.SIGNAL("clicked()"), self.settings);
    self.connect(self.startscreen.buttonQuit, QtCore.SIGNAL("clicked()"), sys.exit);
    self.setCentralWidget(self.startscreen)


  def play(self):
    state = self.MENU_MODE
    print "Open play window"
    self.playscreen = PlayScreen(self)
    self.connect(self.playscreen.buttonBack, QtCore.SIGNAL("clicked()"), self.start);
    self.connect(self.playscreen.buttonSingle, QtCore.SIGNAL("clicked()"), self.singleplayer);
    self.connect(self.playscreen.buttonMulti, QtCore.SIGNAL("clicked()"), self.multiplayer);
    self.setCentralWidget(self.playscreen)


  def settings(self):
    state = self.MENU_MODE
    print "Open settings window"
    self.settingsscreen = SettingsScreen(self) # TODO build like the current settings are
    self.connect(self.settingsscreen.buttonBack, QtCore.SIGNAL("clicked()"), self.commit_settings);
    self.setCentralWidget(self.settingsscreen) 

  def commit_settings(self):
    self.Electro = self.settingsscreen.buttonElectro.is_active()
    self.Guitars = self.settingsscreen.buttonGuitars.is_active()
    self.HipHop = self.settingsscreen.buttonHipHop.is_active()
    self.Regular = self.settingsscreen.buttonRegular.is_active()
    self.Goofy = self.settingsscreen.buttonGoofy.is_active()
    self.Twitter = self.settingsscreen.buttonTwitter.is_active()
    music_styles = []
    if self.HipHop: music_styles.append("hip hop")
    if self.Guitars: music_styles.append("guitars")
    if self.Electro: music_styles.append("electro")
    #keywan: send music settings to music player (benutz die music_styles variable)
    dbusCommunicator.MusicSignal(music_styles)
    self.start()

  def singleplayer(self):
    state = self.MENU_MODE
    print "Singleplayer"
    self.singleplayerscreen = SingleplayerScreen(self)
    self.connect(self.singleplayerscreen.buttonBack, QtCore.SIGNAL("clicked()"), self.play);
    self.connect(self.singleplayerscreen.buttonChallenge, QtCore.SIGNAL("clicked()"), self.freestyle); #TODO: change to challenge
    self.connect(self.singleplayerscreen.buttonFreestyle, QtCore.SIGNAL("clicked()"), self.freestyle);
    self.connect(self.singleplayerscreen.buttonHighscore, QtCore.SIGNAL("clicked()"), self.highscore);
    self.setCentralWidget(self.singleplayerscreen)


  def multiplayer(self):
    state = self.MENU_MODE
    print "Multiplayer"
    self.setCentralWidget(self.playscreen) # TODO


  def challenge(self):
    self.state = self.CHALLENGE_MODE
    print "Challenge"
    self.challengescreen = ChallengeScreen(self)
    self.setCentralWidget(self.challengescreen) # TODO
    self.is_ingame = True

  def freestyle(self, reset_values=True):
    freestylescreen = FreestyleScreen(self)
    self.connect(freestylescreen, QtCore.SIGNAL("showPauseScreen()"), self.showPauseScreen)
    self.connect(freestylescreen, QtCore.SIGNAL("changeLevelTo(int)"), self.changeLevelTo)
    self.state = self.FREESTYLE_MODE
    self.setCentralWidget(freestylescreen) # TODO
    if (reset_values):
      self.time = 0
      self.points = 0
      self.level = 1
      self.tricks_done = list()
    self.is_ingame = True
    self.timer.start(1000, self)
    dbusCommunicator.MusicCommandSignal("play")
    #keywan: send play to music player


  def timerEvent(self, event):
    if event.timerId() == self.timer.timerId():
      self.time += 1
      self.emit(QtCore.SIGNAL("nextSecond(int)"),self.time)
    else:
      QtGui.QFrame.timerEvent(self, event)

  def check_highscore(self):
    self.heroes = readHeroesFromFile()
    rank = getHeroRank(self.points, self.heroes)
    print rank
    if rank < 10:
      self.showEnterHeroName()
    else:
      self.highscore()

  def twitterHighscore(self, hero):
    if self.Twitter:
      print "twittering highscore: " + hero.to_heroic_string()
      api = twitter.Api(self.twitterName, self.twitterPass)
      status = api.PostUpdate(hero.to_heroic_string())

  def commit_highscore(self,name):
    our_hero = Hero(name, self.points, self.level)
    self.heroes.append(our_hero)
    self.heroes = sorted(self.heroes, Hero.cmp)
    writeHeroesToFile(self.heroes)
    self.twitterHighscore(our_hero)
    self.highscore()
  
  def showEnterHeroName(self):
    self.enter_name_screen = EnterHeroNameScreen(self)
    self.setCentralWidget(self.enter_name_screen)
    self.connect(self.enter_name_screen, QtCore.SIGNAL("commit_highscore(str)"), self.commit_highscore)

  def showPauseScreen(self):
    self.is_ingame = False
    self.timer.stop()
    self.pausescreen = PauseScreen(self)
    self.setCentralWidget(self.pausescreen)
    self.connect(self.pausescreen, QtCore.SIGNAL("hidePauseScreen()"), self.hidePauseScreen)
    self.connect(self.pausescreen.buttonResume, QtCore.SIGNAL("clicked()"), self.hidePauseScreen)
    self.connect(self.pausescreen.buttonMenu, QtCore.SIGNAL("clicked()"), self.check_highscore)
    #keywan: send pause to music player
    dbusCommunicator.MusicCommandSignal("pause")

  def hidePauseScreen(self):
    if (self.state == self.FREESTYLE_MODE):
      self.freestyle(False)
    elif (self.state == self.CHALLENGE_MODE):
      self.challenge()
    else:
      #keywan: send stop to music player
      dbusCommunicator.MusicCommandSignal("stop")
      self.play()

  def highscore(self):
    state = self.MENU_MODE
    print "Highscore"  
    self.highscorescreen = HighscoreScreen(self)
    self.connect(self.highscorescreen.buttonBack, QtCore.SIGNAL("clicked()"), self.singleplayer);
    self.setCentralWidget(self.highscorescreen)
    
  # level functions
  def changeLevelTo(self, new_level):
    self.level = new_level
    dbusCommunicator.LevelSignal(new_level)


  def points_up(self, points):# auslagern?
    print "Points Up"


  def newChallenge(self):
    print "Please perform an Ollie now"

  def trick_commit(self, trickid):
    if not self.is_ingame:
      return
    if not self.tricklist.has_key(trickid):
      trickid = 'unknown'
    else:
      self.tricks_done.insert(0,self.tricklist[trickid])
      self.emit(QtCore.SIGNAL("trickEvent(str, int)"), trickid, self.time)
      points =  str(self.tricklist[trickid].points * 50)
      dbusCommunicator.ShoutSignal([trickid,"good"])

####### Dbus stuff #####

class DemoException(dbus.DBusException):
  _dbus_error_name = 'net.prometoys.solderinskater.DemoException'


class DbusTrickObject(dbus.service.Object):
  def __init__(self, bus_name,method,gui):
    # Here the object path
    dbus.service.Object.__init__(self, bus_name, method)
    self.gui = gui
    print "dbus init ready"

  @dbus.service.method("net.prometoys.solderinskater.TrickService", in_signature='s', out_signature='')
  def TrickCommit(self, trick):
    self.gui.trick_commit(str(trick))

  @dbus.service.method("net.prometoys.solderinskater.TrickService", in_signature='', out_signature='')
  def RaiseException(self):
    raise DemoException('The RaiseException method does what you might '
                            'expect')

    # Signal senden
  @dbus.service.signal('net.prometoys.solderinskater.TrickService', signature='as')
  def ShoutSignal(self, shout_array):
    print "Shout " + str(shout_array)
    # The signal is emitted when this method exits
    # You can have code here if you wish
    pass

  # Musik senden
  @dbus.service.signal('net.prometoys.solderinskater.TrickService', signature='as')
  def MusicSignal(self, music_array):
    print "Music " + str(music_array)
    # The signal is emitted when this method exits
    # You can have code here if you wish
    pass

  @dbus.service.signal('net.prometoys.solderinskater.TrickService', signature='i')
  def LevelSignal(self, level):
    print "Level " + str(level)
    # The signal is emitted when this method exits
    # You can have code here if you wish
    pass
    
  @dbus.service.signal('net.prometoys.solderinskater.TrickService', signature='s')
  def MusicCommandSignal(self, command):
    print "MusicCommand " + str(command)
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

######### Main script schnick schnack ###############

app = QtGui.QApplication(sys.argv)

tiltnroll = TiltnRoll()
tiltnroll.show()

#os.system('./start_dbus_session.sh &')

dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
#session_bus = dbus.SessionBus()
#bus = dbus.bus.BusConnection('tcp:host=localhost,port=1337')
bus = dbus.bus.BusConnection('unix:path=/tmp/skater_socket')
print "leet"
name = dbus.service.BusName("net.prometoys.solderinskater.TrickService", bus)
dbusCommunicator = DbusTrickObject(bus, '/net/prometoys/solderinskater/TrickService/DbusTrickObject', tiltnroll)
tiltnroll.dbusCommunicator = dbusCommunicator

#os.system('run-standalone.sh python2.5 tricksimulator.py &')
#os.system('run-standalone.sh python2.5 classifier/simul.py &')

sys.exit(app.exec_())

