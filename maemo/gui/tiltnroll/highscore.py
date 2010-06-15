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
from PyQt4 import QtCore
import os.path

class Hero:
  def __init__(self,name="???",points=0,level=0):
    self.name = name
    self.points = points
    self.level = level

  def to_string_pretty(self):
    return (self.name[0:3].upper()).ljust(3," ") + " " + str(self.points).rjust(6,"0")
  
  def to_heroic_string(self):
    return str(self.name).upper() + " entered the hall of fame with *incredible* " + str(int(self.points)) + " points!"

  def to_string(self):
    return self.name + "," + str(int(self.points)) + "," + str(int(self.level))
  
  def from_string(self, s):
    fields = s.split(",")
    self.name = fields[0]
    self.points = int(fields[1])
    self.level = int(fields[2])
    return self
    
  def cmp(self, other):
    return cmp(other.points, self.points)

def getHeroRank(points, heroes):
  heroes = sorted(heroes,Hero.cmp)
  rank = 0
  for h in heroes:
    if h.points > points: rank += 1
    else: break
  return rank

def readHeroesFromFile():
  heroes = []
  highscore_file = QtCore.QFile("highscore.txt")
  if not (highscore_file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text)):
    print "Error reading file 'highscore.txt'"
  highscore_file.reset()
  stream = QtCore.QTextStream(highscore_file)
  line = stream.readLine() # first line is just a comment
  while not (line.isNull()):
    line = stream.readLine()
    strline = str(line)
    if strline.find(",") != -1:
      heroes.append(Hero().from_string(strline))
  heroes = sorted(heroes, Hero.cmp)
  heroes = heroes[0:10]
  return heroes

def writeHeroesToFile(heroes):
  f = open('highscore.txt', 'w')
  f.write("# name,points,level\n")
  for h in heroes: f.write(h.to_string()+"\n")
  f.close()
  
def createHighscoreFile():
  if os.path.isfile("highscore.txt"): return
  heroes = []
  heroes.append(Hero("Keywan",9,1))
  heroes.append(Hero("Jan",8,1))
  heroes.append(Hero("ACE aka Alexander",7,1))
  heroes.append(Hero("Flo",6,1))
  heroes.append(Hero("Nick",5,1))
  heroes.append(Hero("Linse",4,1))
  heroes.append(Hero("Sebastian",3,1))
  heroes.append(Hero("Erik",2,1))
  heroes.append(Hero("Lennart",1,1))
  writeHeroesToFile(heroes)
