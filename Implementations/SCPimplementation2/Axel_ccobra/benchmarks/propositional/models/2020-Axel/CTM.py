# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 09:29:03 2020

@author: Axel
"""
import epistemicState
import StatePoint
import copy

class CTM (object):
    def __init__(self):
        print ("I am a new CTM")
        self.si=None
        self.last=[]
        #partial transition model (no intial state)
        self.pCTM=[]
    def setSi(self,si):
        self.si=si
    def insertm (self, pos, m):
        self.pCTM.insert(pos,m)
    def appendm (self, m):
        self.insertm(len(self.pCTM),m)
        
    def evaluate(self):
        currentStatePoint=self.si
        for m in self.pCTM:
            currentStatePoint=self.J(currentStatePoint,m)
        return currentStatePoint
    @staticmethod
    def J(p,m):
        #if it is a base point
        if isinstance (p,epistemicState.epistemicState):
            return [CTM.J_epi(p,m)]
        #if it is only a state point
        pPrime=[]
        for sub in p:
            pPrime.append(CTM.J(sub,m))
        return pPrime
    def __getitem__(self, pos):
        if pos==0:
            return self.si
        return self.pCTM[pos-1]
    @staticmethod
    def J_epi(epi,m):
        #copy the epi so that it won't be overwritten if accessed elsewhere
        epi=copy.deepcopy(epi)
        return m.evaluateEpistemicState(epi)
        
    def __str__(self):
        s = str(self.si)
        pCTM = ""
        for i in self.pCTM:
            pCTM = " => "+str(i)
        return s + pCTM
        