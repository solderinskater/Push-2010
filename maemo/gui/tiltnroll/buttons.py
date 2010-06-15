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


class SkateLabel(QtGui.QLabel):
  def __init__(self, caption, add_style="",centered=False):
    QtGui.QLabel.__init__(self, caption)
    self.setStyleSheet("background-image: url(./images/transp.png);\
      color: #86bc10; font-size:28px; font-family:Adore64; text-align:center;"+add_style)
    if centered: self.setAlignment(QtCore.Qt.AlignCenter)

class AnimatedButton(QtGui.QPushButton):
  def __init__(self, caption, image_name, time_list, add_style=""):
    QtGui.QPushButton.__init__(self, caption)
    self.setFlat(True)
    self.counter = 0
    self.max_count = len(time_list)
    self.time_list = time_list
    self.image_name = image_name
    self.setFlat(True)
    self.timer = QtCore.QBasicTimer()
    self.add_style = add_style
    self.base_style = "margin:0px; height: 74px; color: #86bc10; background-color: black; font-family:Adore64;\
        font-size:28px; background-repeat:no-repeat; background-position: center;"
    self.update_style()
    self.timer.start(self.time_list[self.counter], self)

  def timerEvent(self, event):
    if event.timerId() == self.timer.timerId():
      self.counter = (self.counter+1)%self.max_count
      self.update_style()
      self.timer.stop()
      self.timer.start(self.time_list[self.counter], self)
      
  def update_style(self):
    self.setStyleSheet(self.base_style+"background-image: url("+self.get_image_name()+");"+self.add_style);
  
  def get_image_name(self):
    name = "./images/anims/" + self.image_name
    if self.counter+1 < 10: name += "0"
    name += str(self.counter+1) + ".png"
    return name
    
  

class ShinyButton(QtGui.QPushButton):
  def __init__(self, caption, image_name="small", add_style=""):
    QtGui.QPushButton.__init__(self, caption)
    self.setFlat(True)
    self.setStyleSheet("margin:0px; height: 74px; color: #86bc10; background-color: black; font-family:Adore64;\
        font-size:28px; background-repeat:no-repeat; background-position: center;\
        background-image: url(./images/buttons/"+image_name+".png);"+add_style)

class TogglePushButton(QtGui.QPushButton):
  def __init__(self, caption, is_active=False, image_name="toggle"):
    QtGui.QPushButton.__init__(self, caption)
    self.state = is_active
    self.image_name = image_name
    self.setFlat(True)
    self.base_style = "height: 74px; background-color: black; font-size:28px;\
      font-family:Adore64; color: #86bc10; background-repeat:no-repeat; background-position: center;"
    self.update_style()
  
  def update_style(self):
    if self.state:
      self.setStyleSheet(self.base_style+"background-image: url(./images/buttons/"+self.image_name+"_on.png);color: #86bc10;")
    else:
      self.setStyleSheet(self.base_style+"background-image: url(./images/buttons/"+self.image_name+"_off.png);color: #324606;")
    
  def toggle_state(self):
    self.state = not self.state
    self.update_style()
    return self.state
    
  def is_active(self):
    return self.state

  def set_state(self, state):
    self.state = state
    self.update_style()
    
  def mousePressEvent(self,event):
    if event.button() == QtCore.Qt.LeftButton:
      self.toggle_state()
      QtGui.QPushButton.mousePressEvent(self,event)
      return
