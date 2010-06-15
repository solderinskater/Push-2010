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
        self.w = zeros((671,1))
        self.buffer = zeros((61,11))
        self.numSmp = 0
        self.loadClassifier(dataFile)
        
    def loadClassifier(self, fileName):
        self.w = loadtxt(fileName, unpack=True)
        self.w = transpose(self.w)
    def classify(self, sample):
        sample = str(sample)
        s=re.sub('[xyzXYZ]',',',sample)
    #    s=re.sub('^.','',s)
#        print s
        s = string.split(s,',')
        s = s[0:-1] # remove last element - \r\n
        if len(s) < 11:
            return ""
        # cycle ring-buffer
        if self.numSmp>=60:
            self.buffer[0:60,:] = self.buffer[1:61,:]
  #          print s
            for i in range(0,4):
                self.buffer[-1,i] = float(s[i])
        else:   
            for i in range(0,5):
                self.buffer[self.numSmp+1,i] = float(s[i])
        
        self.numSmp = self.numSmp + 1
        
        d = self.buffer.reshape(671,1)
        
        
        val = float(dot(self.w, d))
 #       print val
#       print str(self.numSmp/65)
        if (val>-150.0):
            return tricks[0]
        else:
            return ""
        
