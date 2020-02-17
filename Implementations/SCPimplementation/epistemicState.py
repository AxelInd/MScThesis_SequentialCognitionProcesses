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
        #V: set of evaluated Variables
        self.v=[]
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
    def oneStepDeriveFromW(w):
        v=[]
        for rule in w:
            if isinstance(rule, basicLogic.operator_bitonic_implication):
                ce1 = rule.clause1.evaluate()
                ce2 = rule.clause2.evaluate()
                print ("Clause 1 :{} = {}  --- Clause 2 :{} = {}".format(rule.clause1,ce1,rule.clause2,ce2))
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
    @staticmethod
    def getVariablesFromThW(thW):
        v=[]
        for x in thW:
            if isinstance(x[0],basicLogic.atom):
                v.append(copy.deepcopy(x[0]))
                v[-1].setValue(x[1])
        return v
    @staticmethod
    def deepSetVInRules (v, rules):
        basicLogic.setkbfromv(rules,v)
    #@TODO does not compare rules, only atoms
    @staticmethod
    def compareCurrentToPrev (cur, prev):
        for c in cur:
            cFound=False
            if isinstance (c[0], basicLogic.atom):
                for p in prev:
                    if isinstance(p[0],basicLogic.atom):
                        if c[0]==p[0]:
                            cFound=True
            else:
                cFound = True
            if not cFound:
                print("{} did not exist in the prev".format(c))
                return False
        return True
                        
        return True
    @staticmethod
    def deriveFromW(w):
        prev  = []
        current = epistemicState_defeaultReasoning.oneStepDeriveFromW(w)
        #all variables with derivable values
        variables = epistemicState_defeaultReasoning.getVariablesFromThW(current)
        while not epistemicState_defeaultReasoning.compareCurrentToPrev(current,prev):
            prev = copy.deepcopy(current)
            current=epistemicState_defeaultReasoning.oneStepDeriveFromW(w)
            variables = epistemicState_defeaultReasoning.getVariablesFromThW(current)
            
            print ("Ich bin hier")
            for c in current:
                print ("---{}".format(c))
            for v in variables:
                for c in current:
                    c[0].deepSet(v.getName(), v.getValue())
        print (variables)
        derivedRules = [i[0] for i in current]
        return derivedRules, variables
    @staticmethod
    def deriveFromD(d,v):
        d = copy.deepcopy(d)
        print ("v is ", v)
        for defaultRule in d:
            print ("Default rule is",defaultRule)
            print ("This default rule evlauates to", defaultRule.evaluate(v))
        return d, v

    @staticmethod
    def oneStepDeriveFromD(d, v):
        for defaultRule in d:
            pass
                
        
        




















