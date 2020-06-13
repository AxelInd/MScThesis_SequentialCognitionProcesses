#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:14:20 2020

@author: axel
"""
import basicLogic
import scp
import epistemicState

def kbEvaluator(kb):
    for i in kb:
        print (i, ":::", i.evaluate())
        
def remAll(L, item):
    answer = []
    for i in L:
        if i!=item:
            answer.append(i)
    return answer
def ignoreWords(task, ignoredWords):
    for word in ignoredWords:
        task = remAll(task, word)
    return task
#task must be reversed before hand. This is because pop() is const time, but dequeue is O(n)
#@TODO I am not working!
def polishNotationParser (task, logicType="P"):
    monotonicOps = {'Not':basicLogic.operator_monotonic_negation,
                    'not':basicLogic.operator_monotonic_negation,
                    'Holds':basicLogic.operator_monotonic_holds,
                    'Mostly':basicLogic.operator_monotonic_mostly,
                    'Rarely':basicLogic.operator_monotonic_rarely}
    bitonicOps = {'and':basicLogic.operator_bitonic_and,
                  'or':basicLogic.operator_bitonic_or,
                  'if':basicLogic.operator_bitonic_implication, 
                  'iff':basicLogic.operator_bitonic_bijection,
                  'Implies':basicLogic.operator_bitonic_implication
                  }
    specialMappings = {}
    ignoredWords = []
    #This removes all words in ignoredWords from the list completely
    #Holds is in this list because its functionality is trivialized by my implementation
    task = ignoreWords(task, ignoredWords)
    
      
    if len(task)==1 and not isinstance(task[0], basicLogic.operator):
        #set true if epistemic state only has kb and no v
        return [basicLogic.atom(task[0], False)]
    #@TODO still needs to handle negative initialisations
    #PROCEDURE
    # find any case with monotonic operator, base/node
    # find any case with bitonic operator, base/node, number
    # find any case with bitonic operator, number, base/node
    # replace these cases with small node
    # repeat
    changeMade=False
    for i in range (0, len(task)):
        #Currently empty
        if task[i] in specialMappings:
            specialName = task[i]
            task[i]=specialMappings[specialName]()
            break
        #Monotonic Operations
        elif task[i] in monotonicOps  and i<len(task)-1:
            if task[i+1] not in bitonicOps and task[i+1] not in monotonicOps:
                clause = task[i+1]
                if not isinstance (clause,basicLogic.operator):
                    clause = basicLogic.atom(clause, None)
                monOp = monotonicOps[task[i]](clause, logicType=logicType)
                del task[i:i+2]
                task.insert(i,monOp)
                changeMade=True
                break
        #Bitonic Operations        
        elif task[i] in bitonicOps and i<len(task)-2:
            if task[i+1] not in bitonicOps and task[i+2] not in bitonicOps:
                if task[i+1] not in monotonicOps and task[i+2] not in monotonicOps:
                    left = task[i+1]
                    right = task[i+2]
                    if not isinstance (left, basicLogic.operator):
                        left = basicLogic.atom(left, None)
                        #x changeMade=True
                    if not isinstance (right, basicLogic.operator): 
                        right = basicLogic.atom(right, None)
                        #x changeMade=True
                    bitOp = bitonicOps[task[i]](left,right, logicType=logicType)
                    #does +3 because delete is up to but not including
                    del task[i:i+3]
                    task.insert(i,bitOp)
                    #x I changed
                    changeMade=True
                    break
    if changeMade:
        return polishNotationParser(task)
    return task

def rulesListToEpistemicState(rules, epistemicStateType='dl'):
    switch = {"wcs": epistemicState.epistemicState_weakCompletion, "dl": epistemicState.epistemicState_defeaultReasoning}
    state = switch[epistemicStateType]()
    if epistemicStateType == 'dl':
        nRules, dRules = basicRulesToDefaultLogic(rules)
        state.addD(dRules)
        state.addW(nRules)
        #@TODOneedtoaddv
        V = getVFromEpi(state)
        state.addV(V)
    if epistemicStateType == 'wcs':
        #@TODO not yet implemented
        basicRulesToWeakCompletionLogic(rules)
    return state

def basicLogicToEpistemicState(rules,  epistemicStateType='dl'):
    for rule in rules:
        print("processing", rule)
def basicRulesToWeakCompletionLogic(rules):
    print("Not implemented yet")
    raise Exception()

def createMostlyRule(rule):
    mostlyIsRule = False
    mostlyIsHead = False
    isImplication = isinstance(rule,basicLogic.operator_bitonic_implication)
    mostlyIsRule = isinstance(rule, basicLogic.operator_monotonic_mostly)
    
    if isImplication:
        mostlyIsHead = isinstance(rule.clause2, basicLogic.operator_monotonic_mostly)
    
    mostlyInRightPlace =  mostlyIsRule or mostlyIsHead
    if  mostlyIsHead:
        c1 = rule.clause1
        c2 = basicLogic.operator_monotonic_negation(rule.clause2.clause)
        #known to be mostly
        c3 = rule.clause2.clause
        r = basicLogic.operator_tritonic_defaultRule(c1,c2,c3)

        return r
    elif mostlyIsRule:
        c1=basicLogic.TRUE
        c2 = basicLogic.operator_monotonic_negation(rule.clause)
        c3 = rule.clause
        r = basicLogic.operator_tritonic_defaultRule(c1,c2,c3)
        return r
    else:
        print ("Requirement that 'mostly' is the second clause in a->m(b)")
        raise Exception()
        
def createRarelyRule(rule):
    rarelyIsRule = False
    rarelyIsHead = False
    isImplication = isinstance(rule,basicLogic.operator_bitonic_implication)
    rarelyIsRule = isinstance(rule, basicLogic.operator_monotonic_rarely)
    
    if isImplication:
        rarelyIsHead = isinstance(rule.clause2, basicLogic.operator_monotonic_rarely)
    
    rarelyInRightPlace =  rarelyIsRule or rarelyIsHead
    if  rarelyIsHead:
        c1 = rule.clause1
        c2 = basicLogic.operator_monotonic_negation(rule.clause1)
        #known to be mostly
        c3 = basicLogic.operator_monotonic_negation(rule.clause2.clause)
        r = basicLogic.operator_tritonic_defaultRule(c1,c2,c3)

        return r
    elif rarelyIsRule:
        c1 = basicLogic.TRUE
        c2=rule.clause
        c3 = basicLogic.operator_monotonic_negation(rule.clause)
        r = basicLogic.operator_tritonic_defaultRule(c1,c2,c3)
        return r
    else:
        print ("Requirement that 'mostly' is the second clause in a->m(b)")
        raise Exception()
    
def basicRulesToDefaultLogic (rules):
    nRules = []
    dRules = []
    for i in range(0,len(rules)):
        rule = rules[i]
        rule.monotonicDelete(basicLogic.operator_monotonic_holds)
        #is a default rule
        if rule.contains_operator(basicLogic.operator_monotonic_mostly):
            r = createMostlyRule(rule)
            dRules.append(r)  
        elif rule.contains_operator(basicLogic.operator_monotonic_rarely):
            r = createRarelyRule(rule)
            dRules.append(r)  
        #not a default rule
                
        #@TODO now handle rarely
        
        else:
            nRules.append(rule)
    return nRules, dRules

def getVFromEpi(epi):
    v =[]
    if isinstance(epi, epistemicState.epistemicState_weakCompletion):
        kb =epi.getKB()
        for rule in kb:
            v= v+rule[0].getAtoms()
    if isinstance(epi, epistemicState.epistemicState_defeaultReasoning):
        d = epi.getD()
        if d != [[]]:  
            for rule in d:
                v= v+rule[0].getAtoms()         
    return removeDuplicateAtomsFromList(v)
def removeDuplicateAtomsFromList (li):
    li2=[]
    for x in li:
        if not  x in li2:
            li2.append(x)
    return li2
        
        
            



























                    
                
