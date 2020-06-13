# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 09:09:55 2020

@author: Axel
"""
#an implementation of 3-valued logic
import basicLogic
#used to deepcopy complex objects
import copy
#used to create complex epistemic actions in the seuqence
import complexOperation
#used to throw exceptions for improper use
import scpError

import epistemicState


class SCP_Task (object):
    def __init__(self,si=[],M=[],f=[],gamma=[]):
        self.si=si
        self.M=M
        self.f=f
        self.gamma=gamma


    """
    ------------------------------------------------------------------------------
    --------------------------GETTERS AND SETTERS----------------------------------
    ------------------------------------------------------------------------------
    """
    def setSi(self, new_si):
        self.si=new_si
    def getSi(self):
        return self.si
    def setM(self, new_M):
        self.M=new_M
    def getM(self):
        return self.M
    def addm(self,new_m):
        self.M.append(new_m)
    def addmList(self, m_list):
        for m in m_list:
            self.addm(m)
    def setF(self, new_f):
        self.f=new_f
    def getF(self):
        return self.f
    def setGamma(self, new_gamma):
        self.gamma=new_gamma
    def getGamma(self):
        return self.gamma
    def evaluate(self):
        return self.f(self.M)
    
    
    
    
    
    
    
    
    
    
    
    
    

        