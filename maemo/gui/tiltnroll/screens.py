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
from PyQt4 import QtCore, QtGui
from buttons import *
from highscore import *

##### Screen classes #############

class StartScreen(QtGui.QFrame):
    # variables here

  def __init__(self, parent):
    QtGui.QFrame.__init__(self, parent)
    print "Build Start Screen"
    self.setStyleSheet("QFrame {background-image: url(./images/startscreen.jpg);} \
        QLabel {background-image: url(./images/transp.png);}")
    self.layout = QtGui.QVBoxLayout()
    self.setLayout(self.layout)
  
    self.buttonPlay = ShinyButton("play","big")
    self.buttonSettings = ShinyButton("settings", "big")
    self.buttonQuit = ShinyButton("quit","big")
    self.layout.addWidget(QtGui.QLabel(""))
    self.layout.addWidget(QtGui.QLabel(""))
    self.layout.addWidget(QtGui.QLabel(""))
    self.layout.addWidget(self.buttonPlay)
    self.layout.addWidget(self.buttonSettings)
    self.layout.addWidget(self.buttonQuit)
    self.layout.addWidget(QtGui.QLabel(""))


class PlayScreen(QtGui.QFrame):
    # variables here

  def __init__(self, parent):
    QtGui.QFrame.__init__(self, parent)
    print "Build play window"
    self.setStyleSheet("QFrame {background-image: url(./images/background_playerscreen.png);} \
      QLabel {background-image: url(./images/transp.png);}")
    self.layout = QtGui.QVBoxLayout()
    self.setLayout(self.layout)
    # add new buttons
    self.buttonBack = ShinyButton("back","small","width:178;")
    self.hbox1 = QtGui.QHBoxLayout()
    self.hbox1.addWidget(self.buttonBack)
    self.spacer = QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
    self.hbox1.addItem(self.spacer)
    self.layout.addLayout(self.hbox1)

    self.layout.addWidget(QtGui.QLabel(""))
    self.layout.addWidget(QtGui.QLabel(""))
  
    self.hbox2 = QtGui.QHBoxLayout()
    self.buttonSingle = ShinyButton("singleplayer", "singleplayer", "padding-top:195px; height: 263px;")
    self.hbox2.addWidget(self.buttonSingle)
    self.buttonMulti = ShinyButton("multiplayer", "multiplayer", "padding-top:195px; height: 263px;")
    self.hbox2.addWidget(self.buttonMulti)
    self.layout.addLayout(self.hbox2) 

    self.layout.addWidget(QtGui.QLabel(""))

class SettingsScreen(QtGui.QFrame):
    # variables here

  def __init__(self, parent):
    QtGui.QFrame.__init__(self, parent)
    print "Build singleplayer window"
    self.setStyleSheet("QFrame {background-image: url(./images/background_settings.png);} \
      QLabel {background-image: url(./images/transp.png);\
      color: #86bc10; font-size:28px; font-family:Adore64; }")
    #add buttons
    self.layout = QtGui.QVBoxLayout()
    self.setLayout(self.layout)

    self.buttonBack = ShinyButton("back","small","width:178;")
    self.hbox1 = QtGui.QHBoxLayout()
    self.hbox1.addWidget(self.buttonBack)
    self.hbox1.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum))
    self.caption = QtGui.QLabel("settings")
    self.caption.setStyleSheet("font-size:40px; padding: 0px; margin: 0px 53px 21px 0px;")
    self.hbox1.addWidget(self.caption)
    self.layout.addLayout(self.hbox1)


    self.music = QtGui.QLabel("Music Style")
    self.music.setStyleSheet("font-size:30px; margin-left:40px")
    self.layout.addWidget(self.music)

    self.genres = QtGui.QHBoxLayout()
    self.buttonElectro = TogglePushButton("electro", parent.Electro)
    self.buttonGuitars = TogglePushButton("guitars", parent.Guitars)
    self.buttonHipHop = TogglePushButton("hip hop", parent.HipHop)
    self.genres.addWidget(self.buttonElectro)
    self.genres.addWidget(self.buttonGuitars)
    self.genres.addWidget(self.buttonHipHop)
    self.layout.addLayout(self.genres)

    self.stancelabel = QtGui.QLabel("Stance")
    self.stancelabel.setStyleSheet("font-size:30px; margin-left:40px")
    self.layout.addWidget(self.stancelabel)
    self.stance = QtGui.QHBoxLayout()
    self.buttonRegular  = TogglePushButton("regular", parent.Regular)
    self.buttonGoofy = TogglePushButton("goofy", parent.Goofy)
    self.stance.addWidget(self.buttonRegular)
    self.stance.addWidget(self.buttonGoofy)
    self.layout.addLayout(self.stance)
    self.connect(self.buttonRegular, QtCore.SIGNAL("clicked()"), self.buttonGoofy.toggle_state);
    self.connect(self.buttonGoofy, QtCore.SIGNAL("clicked()"), self.buttonRegular.toggle_state);

    self.networklabel = QtGui.QLabel("Social Networks")
    self.networklabel.setStyleSheet("font-size:30px; margin-left:40px")
    self.layout.addWidget(self.networklabel)
    self.networks = QtGui.QHBoxLayout()
    self.buttonTwitter  = TogglePushButton("share on twitter", parent.Twitter, "shareOnTwitter")
    
    self.networks.addWidget(self.buttonTwitter)
    self.layout.addLayout(self.networks)

    self.layout.addWidget(QtGui.QLabel(""))


class SingleplayerScreen(QtGui.QFrame):
    # variables here

  def __init__(self, parent):
    QtGui.QFrame.__init__(self, parent)
    print "Build singleplayer window"
    self.setStyleSheet("QFrame {background-image: url(./images/background_playmodes.png);} \
      QLabel {background-image: url(./images/transp.png);}")
    #add buttons
    # back button
    self.layout = QtGui.QVBoxLayout()
    self.setLayout(self.layout)
    self.buttonBack = ShinyButton("back", "small", "width:178;")
    self.hbox1 = QtGui.QHBoxLayout()
    self.hbox1.addWidget(self.buttonBack)
    self.spacer = QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
    self.hbox1.addItem(self.spacer)
    self.layout.addLayout(self.hbox1)
    # menu buttons
    self.layout.addWidget(QtGui.QLabel(""))
    self.buttonChallenge = ShinyButton("challenge","big")
    self.layout.addWidget(self.buttonChallenge)
    self.buttonFreestyle = ShinyButton("freestyle","big")
    self.layout.addWidget(self.buttonFreestyle)
    self.buttonHighscore = ShinyButton("highscore","big")
    self.layout.addWidget(self.buttonHighscore)
    self.layout.addWidget(QtGui.QLabel(""))
    self.layout.addWidget(QtGui.QLabel(""))
    self.layout.addWidget(QtGui.QLabel(""))

class MultiplayerScreen(QtGui.QFrame):
    # variables here

  def __init__(self, parent):
    QtGui.QFrame.__init__(self, parent)
    print "Build multiplayer window"


class ChallengeScreen(QtGui.QFrame):

  def __init__(self, parent):
    QtGui.QFrame.__init__(self, parent)
    self.layout = QtGui.QVBoxLayout()
    self.setLayout(self.layout)
    self.levelwidget = QtGui.QLabel("2")
    self.pointswidget = QtGui.QLabel("2342")
    self.musicwidget = QtGui.QLabel("Playing This Song")
    self.layout.addWidget(self.levelwidget)
    self.layout.addWidget(self.pointswidget)
    self.layout.addWidget(self.musicwidget)
    print "Build game screen challenge"

def time_beautify(seconds):
  secs = seconds%60
  mins = int(seconds/60)
  if secs < 10:
    return str(mins) + ":0" + str(secs)
  else:
    return str(mins) + ":" + str(secs)

class FreestyleScreen(QtGui.QFrame):
  def __init__(self, parent):
    QtGui.QFrame.__init__(self, parent)
    self.parent = parent
    self.levellist = [200,800,1000,2000,100000]
    self.tricklabels = []
    self.tricklabelcount = 4
    print "Build game screen freestyle"
    self.setStyleSheet("QFrame {background-image: url(./images/PLAYMODES.jpg);} \
      QLabel {background-image: url(./images/transp.png);\
      color: #86bc10; font-size:28px; font-family:Adore64; text-align:center; }\
      #timelabel {font-size: 40px;}\
      #levellabel {font-size: 40px;}\
      #pointslabel {font-size: 100px;}\
      #tricklabel1 {font-size: 50px;}\
      #tricklabel2 {font-size: 25px;}\
      #tricklabel3 {font-size: 15px;}\
      #tricklabel4 {font-size: 10px;}\
      #musicwidget {font-size: 24px;}")
    self.layout = QtGui.QVBoxLayout()
    self.setLayout(self.layout)

    self.upperbar = QtGui.QHBoxLayout()
    self.timewidget = QtGui.QLabel(time_beautify(parent.time))
    self.timewidget.setObjectName("timelabel")
    self.timewidget.setAlignment(QtCore.Qt.AlignLeft)
    self.levelwidget = QtGui.QLabel(" ")
    self.calculateLevel(self.parent.level, self.parent.points)
    self.levelwidget.setAlignment(QtCore.Qt.AlignRight)
    self.levelwidget.setObjectName("levellabel")
    self.upperbar.addWidget(self.timewidget)
    self.upperbar.addWidget(QtGui.QLabel(""))
    self.upperbar.addWidget(self.levelwidget)
    self.layout.addLayout(self.upperbar)

    self.layout.addWidget(QtGui.QLabel(""))
    self.pointswidget = QtGui.QLabel(str(int(parent.points)))
    self.pointswidget.setAlignment(QtCore.Qt.AlignCenter)
    self.pointswidget.setObjectName("pointslabel")
    self.layout.addWidget(self.pointswidget)
    self.layout.addWidget(QtGui.QLabel(""))
  
    self.tricklistlayout = QtGui.QVBoxLayout()
    for i in range(0,self.tricklabelcount):
      label = QtGui.QLabel(" ")
      label.setObjectName("tricklabel"+str(i+1))
      label.setAlignment(QtCore.Qt.AlignCenter)
      if len(parent.tricks_done) > i:
        label.setText(parent.tricks_done[i].name)
      self.tricklistlayout.addWidget(label)
      self.tricklabels.append(label)
    self.layout.addLayout(self.tricklistlayout)

    self.musicwidget = QtGui.QLabel("Playing This Song")
    self.musicwidget.setAlignment(QtCore.Qt.AlignCenter)
    self.musicwidget.setObjectName("musicwidget")
    #self.layout.addWidget(self.musicwidget)
  
    self.connect(parent, QtCore.SIGNAL("nextSecond(int)"), self.nextSecond)
    self.connect(parent, QtCore.SIGNAL("trickEvent(str,int)"), self.trickEvent)

  def mousePressEvent(self, event):
    self.emit(QtCore.SIGNAL("showPauseScreen()"))

  def nextSecond(self, seconds):
    self.timewidget.setText(time_beautify(seconds))
      
  def calculateLevel(self, old_level, points):
    level = 1
    for val in self.levellist:
      if points>val:
        level += 1
    if old_level != level:
      print "Trying to set level to " + str(level)
      self.emit(QtCore.SIGNAL("changeLevelTo(int)"),level)
    self.levelwidget.setText("lvl " + str(self.parent.level))
      
  def update_trick_list(self, tricks_done):
    for i in range(0,self.tricklabelcount):
      if len(tricks_done) > i:
        self.tricklabels[i].setText(tricks_done[i].name)
      else:
        self.tricklabels[i].setText(" ")
      
  def trickEvent(self, trickid, time):
    trick = self.parent.tricklist[trickid]
    self.parent.points += trick.points * 50
    self.calculateLevel(self.parent.level, self.parent.points)
    self.pointswidget.setText(str(int(self.parent.points)))
    self.update_trick_list(self.parent.tricks_done)
    

class PauseScreen(QtGui.QFrame):
  def __init__(self, parent):
    QtGui.QFrame.__init__(self, parent)
    self.setStyleSheet("QFrame {background-image: url(./images/pauseScreenBackground.png);\
      background-color: black;background-position: top left;}")
    self.layout = QtGui.QVBoxLayout()
    self.setLayout(self.layout)
    self.hbox = QtGui.QHBoxLayout()
    self.buttonResume = ShinyButton("resume","pause_resume", "width:286;")
    self.buttonMenu = ShinyButton("end game","pause_resume", "width:286;")
    self.hbox.addWidget(self.buttonResume)
    self.hbox.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum))
    self.hbox.addWidget(self.buttonMenu)
    self.layout.addLayout(self.hbox)
    self.hbox2 = QtGui.QHBoxLayout()
    self.rauchmonster = AnimatedButton("", "rauchmonster", [2000,700,200,100,100,100,100], "margin-left: 20px; width: 332px; height: 354px;")
    self.hbox2.addWidget(self.rauchmonster)
    self.hbox2.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum))
    self.vbox = QtGui.QVBoxLayout()
    self.vbox.addItem(QtGui.QSpacerItem(0,130,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum))
    self.vbox.addWidget(SkateLabel("pause","font-size: 48px;margin-right: 30px;"))
    self.vbox.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding))
    self.hbox2.addLayout(self.vbox)
    self.layout.addLayout(self.hbox2)
#    self.layout.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding))

  def mousePressEvent(self, event):
    self.emit(QtCore.SIGNAL("hidePauseScreen()"))

class EnterHeroNameScreen(QtGui.QFrame):
  def __init__(self, parent):
    QtGui.QFrame.__init__(self, parent)
    self.setStyleSheet("QFrame {background-image: url(./images/highscorescreen.png);\
      background-repeat: no-repeat; background-position: top left;\
      background-color: black;}")

    self.layout = QtGui.QHBoxLayout()
    self.setLayout(self.layout)

    self.layout.addItem(QtGui.QSpacerItem(420,0,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum))

    self.entryLayout = QtGui.QVBoxLayout()
    self.entryLayout.addWidget(SkateLabel("NEW HIGHSCORE!","margin-top:20px",True))
    self.entryLayout.addItem(QtGui.QSpacerItem(0,120,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum))
    self.entryLayout.addWidget(SkateLabel("your name:","margin-left: 30px; margin-bottom: 4px;"))
    self.edit = QtGui.QLineEdit(self)
    self.edit.setStyleSheet("color: #86bc10; font-size:40px; font-family:Adore64; background: black; border: 2px solid #49762c; border-radius: 10px;\
     padding: 6px 10px;selection-background-color: black;width:120px;margin-left:42px;")
    self.edit.setMaxLength(3)
    self.edit.grabKeyboard()
        
    hbox1 = QtGui.QHBoxLayout()
    hbox1.addWidget(self.edit)
    hbox1.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum))
    self.entryLayout.addLayout(hbox1)
    self.buttonOk = ShinyButton("ok", "small", "width:178;")
    hbox2 = QtGui.QHBoxLayout()
    hbox2.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum))
    hbox2.addWidget(self.buttonOk)
    self.entryLayout.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding))
    self.entryLayout.addLayout(hbox2)
    self.connect(self.buttonOk, QtCore.SIGNAL("clicked()"), self.commit_settings);
    self.connect(self.edit, QtCore.SIGNAL("returnPressed()"), self.commit_settings);
    self.layout.addLayout(self.entryLayout)

  def commit_settings(self):
    self.emit(QtCore.SIGNAL("commit_highscore(str)"), self.edit.text())

class HighscoreScreen(QtGui.QFrame):
  def __init__(self, parent):
    QtGui.QFrame.__init__(self, parent)
    self.setStyleSheet("QFrame {background-image: url(./images/highscorescreen.png);\
      background-repeat: no-repeat; background-position: top left;\
      background-color: black;}")

    self.layout = QtGui.QHBoxLayout()
    self.setLayout(self.layout)

    self.buttonBack = ShinyButton("back", "small", "width:178;")
    self.vbox1 = QtGui.QVBoxLayout()
    self.vbox1.addWidget(self.buttonBack)
    self.vbox1.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding))
    self.layout.addLayout(self.vbox1)

    self.heroes = []
    self.heroes = readHeroesFromFile()
    labeltext = ""
    for h in self.heroes:
      labeltext += h.to_string_pretty() + "\n"
    self.highscorelabel = SkateLabel(labeltext.rstrip(),"font-size: 35px;margin-right: 3px;")
    self.layout.addItem(QtGui.QSpacerItem(0,0,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum))
    self.layout.addWidget(self.highscorelabel)
