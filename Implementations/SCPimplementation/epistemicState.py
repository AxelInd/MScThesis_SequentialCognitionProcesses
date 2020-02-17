# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 09:47:35 2020

@author: Axel
"""
import basicLogic
import copy
class epistemicState (object):
    def __init__(self):
        print ("epistemic State Created")
    def __str__(self):
        return "ABSTRACT"
    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, other):
        if isinstance(other, epistemicState):
            return self.__str__() == other.__str__()
        else:
            return False
        
class epistemicState_weakCompletion (epistemicState):
    def __init__(self):
        self.v=[]
        self.kb=[]
        
    def addKnowledge (self, knowledge):
        #still needs checks for duplicate knowledge
        newKnowledge=copy.deepcopy(knowledge)
        self.kb.append(newKnowledge)
        
        #remove duplicates
        self.kb=list(dict.fromkeys(self.kb))
    def addVariable (self, variable, overwrite=False):
        newVariable = copy.copy(variable)
        if not overwrite:
            for v in self.v:
                #prevents adding duplicate variables (at the start at least)
                if v.name == newVariable.name:
                    return False
        else:
            self.removeVariable(variable.name)
        self.v.append(newVariable)
        return True
    def addKnowledgeList (self, li):
        for rule in li:
            self.addKnowledge(rule)
    def addVariableList (self, li):
        for v in li:
            self.addVariable(v)
    def getKB (self):
        return self.kb
    def getV (self):
        return self.v
    
    def removeVariable(self,varName):
        self.v = [var for var in self.v if var.getName()!=varName]
        return True
    def setVariable (self, varName, varVal):
        for var in self.v:
            if var.getName()==varName and not var.fixed:
                var.setValue(varVal)
    def fixVariable (self, varName, fixed=True):
        for var in self.v:
            if var.getName()==varName:
                var.fixed=fixed 
    def __str__(self):
        sv = basicLogic.strVariables(self.v)
        skb = basicLogic.strKnowledge(self.kb)
        return "KB = {}\nV = {}".format(skb, sv)
    
class epistemicState_defeaultReasoning (epistemicState):
    def __init__(self):
        print ("Default Rule Created")
        #D: set of default rules
        self.d=[]
        #W: set of rules
        self.w=[]
    def deriveRules (self):
        return True
        
        
    def getD (self):
        return self.d
    def getW (self):
        return self.w
    def addD(self, d):
        self.d.append(d)
    def addW(self,w):
        self.w.append(w)
    def __str__(self):
        sw = self.w
        sd = self.d
        return "W = {}  D = {}".format(sw, sd)
    #@TODO this method is really simple and must be expanded for non-monotonic conclusions
    # that is, for cases where there are multiple possible resulting variable assignments
    @staticmethod
    def deriveFromW(w):
        v=[]
        for rule in w:
            if isinstance(rule, basicLogic.operator_bitonic_implication):
                ce1 = rule.clause1.evaluate()
                ce2 = rule.clause2.evaluate()
                if ce1!=None:
                    v.append((rule.clause2,ce1))
            if isinstance(rule, basicLogic.operator_bitonic_bijection):
                ce1 = rule.clause1.evaluate()
                ce2 = rule.clause2.evaluate()
                if ce1!=None:
                    v.append((rule.clause2, ce1))
                if ce2!=None:
                    v.append((rule.clause1, ce2))
        return v
                
        
        




















