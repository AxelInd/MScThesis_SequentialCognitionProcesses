# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 09:33:36 2020

@author: Axel
"""

import epistemicState
class StatePoint(object):
    def __init__(self,childPoints=None):
        #child points are either a set of state points, or an epistemic state
        self.childPoints=childPoints
    def setChildPoints(self,childPoints):
        self.childPoints=childPoints
    def getChildPoints(self):
        return self.childPoints
    def __str__(self):
        return "<"+str(self.childPoints)+">"
    def __getitem__(self, pos):
        return self.childPoints[pos]  
    