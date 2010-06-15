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
_all_=['Classifier']

import sys
import sip
from PyQt4 import QtGui
from PyQt4 import QtCore
import time
from numpy import *
import string
import re

tricks = ['ollie','360','kickflip','heelflip','shove']

class Classifier(QtCore.QObject):

    def __init__(self, dataFile):
        QtCore.QObject.__init__(self)
        self.w = zeros((248,1))
        self.buffer = zeros((61,8))
        self.numSmp = 0
        self.loadClassifier(dataFile)
        
    def loadClassifier(self, fileName):
        self.w = loadtxt(fileName, unpack=True)
        self.w = transpose(self.w)


    def classify(self, sample):
        sample = str(sample)
#        s=re.sub('[xyzXYZ]',',',sample)
#        s=re.sub('^.','',s)
#        print s
        s = string.split(sample,',')
        s = s[0:-1] # remove last element - \r\n
        if len(s) < 11:
            return ""
        
        del s[3]
        del s[3]
        del s[3]
        # cycle ring-buffer
        if self.numSmp>=60:
            self.buffer[0:60,:] = self.buffer[1:61,:]

            for i in range(0,7):
                self.buffer[-1,i] = float(s[i])
#            print "SMP: "+str(self.numSmp)
#            print self.buffer.reshape(1,671,order='F').copy()
        else:   
            for i in range(0,8):
                self.buffer[self.numSmp+1,i] = float(s[i])
      
        self.numSmp = self.numSmp + 1
        d = self.buffer.reshape(61*8,1,order='F').copy()
        
 
        val = float(dot(self.w, d))
        print str(self.numSmp/65) + '  -  '+str(val)
#       print str(self.numSmp/65)
        if (val>50.0):
            return  tricks[0]
	elif (val<-30.0):
	    return "180"
        else:
            return ""
        
