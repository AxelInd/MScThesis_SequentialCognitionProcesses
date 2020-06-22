#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:01:15 2020

@author: axel
"""


import scp
import basicLogic
import complexOperation
import epistemicState
import copy

def trivialF (epi):
    targets = {'l':None, 'ab1':None, 'e':True}
    for v in targets:
        var = epi.getVByName(v)
        try:
            if var.getValue() != targets[v]:
                return False
        except:
            return False
    return True

class scpTask (object):
    def __init__(self, si=None, M=None, gamma=None, f=None):
        print ("Task created")
        self.si=si
        self.M=M
        self.gamma=gamma
        self.f=f
    """
    def t (self):
        s = scp.scp(self.si)
        s.addM(M)
        s.addNext(comp_addAB)
        s.addNext(comp_weak)
        s.addNext(comp_semantic)
        s.addNext(comp_semantic)
        s.addNext(comp_semantic)
        print (s)
        print (s.evaluate())
        print (self.f(s.evaluate()))
    """

    def __str__(self):
        s = ""
        s = str(self.si) + "\n"
        s = s + "Gamma: "+ str(self.gamma) + "\n"
        s = s + "Evaluation Function: " + str(self.f)+"\n"
        return s
    #@TODOcange validity type to ones described
    def deNovoSearch(self, s=None,depth=2, validityType="correct"):
        if s == None:
            s = scp.scp(self.si)
        solutions = self.ds(s=s, depth=depth, validityType=validityType)
        
        return solutions
                     
    def ds(self, s=None,depth=2, validityType="correct"):
        """
        print ("s is: ", s)
        print (s.si)
        print (s.evaluate())
        
        print ("---")
        """
        try:
            if self.f(s.evaluate())==self.gamma:
                return s
        except:
            #if it fails to evaluate, return because it is not a valid SCP and extending
            #it won't make it one
            #print ("Failed to RUN, this is okay")
            return None
        if depth == 0:
            if validityType == "All":
                return s
            else:
                return None
        li = []
        for m in range (0, len(self.M)):
            #print("Testing function: ", self.M[m].name)
            sExtend= copy.deepcopy(s)
            sExtend.addNext(self.M[m])
            li.append(self.ds(s=sExtend,depth=depth-1,validityType=validityType))
        return li
    @staticmethod
    def scoreSCP(_scp, constraints=None):
        if _scp==None:
            return 9999
        complexOperationCosts={ "<class 'complexOperation.complexOperation_init'>":0,
                               "<class 'complexOperation.complexOperation_addAB'>":1, 
                               "<class 'complexOperation.complexOperation_deleteVariable'>":2,
                               "<class 'complexOperation.complexOperation_fixVariable'>":1,
                               "<class 'complexOperation.complexOperation_weaklyComplete'>":1,
                               "<class 'complexOperation.complexOperation_semanticOperator_full'>":2,
                               "<class 'NoneType'>":999
                               }
        
                                       
        score = _scp.score(complexOperationCosts,constraints=None)
        return score
    @staticmethod
    def getBestSCP(scpList, constraints=None):
        best = None
        bestScore = 9999
        extractedList = scpTask.flattenScpList(scpList)
        for s in extractedList:
            score = scpTask.scoreSCP(s)
            print ("score is ")
            print(score)
            if score < bestScore:
                best = s
                bestScore = score
        return best, bestScore
    @staticmethod
    def flattenScpList(scp_list):
        f = []
        for item in scp_list:
            if isinstance(item, list):
                fprime = scpTask.flattenScpList(item)
                f = f + fprime
            elif item != None:
                f.append(item)
        return f
            
                
def getM_WST ():
    # create the complex operation to add abnormalities
    comp_addAB = complexOperation.complexOperation_addAB ()
    # create the complex operation to delete a named variable
    comp_deleteo = complexOperation.complexOperation_deleteVariable('o')
    # create the complex operation to fix a named variable to a specified value
    comp_fixab1 = complexOperation.complexOperation_fixVariable('ab1', False)
    # Create the complex operation to weakly complete the logic program
    comp_weak = complexOperation.complexOperation_weaklyComplete()
    # create the complex operation to apply the sematic operator
    comp_semantic = complexOperation.complexOperation_semanticOperator()
    
    comp_semantic_full = complexOperation.complexOperation_semanticOperator_full()
    return [comp_addAB,comp_deleteo,comp_fixab1,comp_weak,comp_semantic_full]

def f_trivialTrue(epi):
    return True
def f_trivialFalse(epi):
    return False

"""

#STARTING VARIABLES
# e: she has an essay to write
e = basicLogic.atom('e', setValue=False)
# l: she will study late in the library
l = basicLogic.atom('l', setValue=False)
# o: the library is open
o = basicLogic.atom('o', setValue=False)

#STARTING RULES, FACTS
# if she has an essay to write, she will study late in the library
knowledge1 = basicLogic.operator_bitonic_implication(e,l)
# she has an essay to write
knowledge2 = basicLogic.operator_bitonic_implication(basicLogic.TRUE, e)
# if the library is open, she will study late in the library
knowledge3 = basicLogic.operator_bitonic_implication(o, l)
# the lirary is open
knowledge4 = basicLogic.operator_bitonic_implication(basicLogic.TRUE, o)

#INITIALISE THE SET OF COMPLEX OPERATORS M

# create the complex operation to add abnormalities
comp_addAB = complexOperation.complexOperation_addAB ()
# create the complex operation to delete a named variable
comp_deleteo = complexOperation.complexOperation_deleteVariable('o')
# create the complex operation to fix a named variable to a specified value
comp_fixab1 = complexOperation.complexOperation_fixVariable('ab1', False)
# Create the complex operation to weakly complete the logic program
comp_weak = complexOperation.complexOperation_weaklyComplete()
# create the complex operation to apply the sematic operator
comp_semantic = complexOperation.complexOperation_semanticOperator()

comp_semantic_full = complexOperation.complexOperation_semanticOperator_full()

si = epistemicState.epistemicState_weakCompletion()
kb = [knowledge1, knowledge2, knowledge3]
v = [e,l,o]
si.addKnowledgeList(kb)
si.addVList(v)

M = [comp_addAB,comp_deleteo,comp_fixab1,comp_weak,comp_semantic_full]
gamma = True
f = trivialF

task = scpTask(si=si,M=M,gamma=gamma,f=f)
task.t()
search = task.deNovoSearch(s=None,depth=4, validityType="correct")
print (search)
print (scpTask.getBestSCP(search))
"""
 


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    