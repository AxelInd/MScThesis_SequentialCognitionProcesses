# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 14:23:02 2020

@author: Axel
"""

import basicLogic
import scp


print ("=================THE WASON SELECTION TASK=========================")
#CARDS THAT CAN BE OBSERVED
card_d = basicLogic.atom('p', setValue=False)
card_k = basicLogic.operator_monotonic_negation(card_d)
card_3 = basicLogic.atom('q', setValue=False)
card_7 = basicLogic.operator_monotonic_negation(card_3)


#STARTING RULES, FACTS
knowledge_dimp3 = basicLogic.operator_bitonic_implication(card_d,card_3)
knowledge_d = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, card_d)
knowledge_3 = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, card_3)
knowledge_k = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, card_k)
knowledge_7 = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, card_7)
#INITIALISE THE SET OF COMPLEX OPERATORS M

# create the initial state of the SCP
comp_initialise = scp.complexOperation_init ()
# create the complex operation to add abnormalities
comp_addAB = scp.complexOperation_addAB ()
# create the complex operation to delete a named variable
comp_deleteo = scp.complexOperation_deleteVariable('o')
# create the complex operation to fix a named variable to a specified value
comp_fixab1 = scp.complexOperation_fixVariable('ab1', False)
# Create the complex operation to weakly complete the logic program
comp_weak = scp.complexOperation_weaklyComplete()
# create the complex operation to apply the sematic operator
comp_semantic = scp.complexOperation_semanticOperator()

 

def createwst_card (variable, knowledge, fix=False, varToFix = None, valueToFix = None):
    wst =  scp.scp()
    print ("The new SCP is made")
    print (wst)
    print ("----")

    # the d-> 3 rule
    wst.addKnowledge(knowledge_dimp3)
    # the observed card
    wst.addKnowledge(knowledge)
    
    wst.addVariable(card_d)
    wst.addVariable(card_3)

    print ("The variables are:")
    print (wst.strVariables(wst.initialV))   
    wst.addVariable(variable)
    print ("The variables are:")
    print (wst.strVariables(wst.initialV))       
    wst.setState1(comp_initialise)
    wst.addNext(comp_addAB)

    if fix:
        comp_fix = scp.complexOperation_fixVariable(varToFix, valueToFix)
        wst.addNext(comp_fix)
    
    wst.addNext(comp_weak)
    wst.addNext(comp_semantic)
    wst.addNext(comp_semantic)

    wst.addNext(comp_semantic)
    
    import copy
    #without this deepcopy, some object property causes the wst of the previous call to be overwritten by this one
    #@TODOfix
    return copy.deepcopy(wst)  

def createwst_card_d ():
    return createwst_card(card_d, knowledge_d) 
def createwst_card_k ():
    return createwst_card(card_k, knowledge_k) 
def createwst_card_3 ():
    return createwst_card(card_3, knowledge_3) 
def createwst_card_7 ():
    return createwst_card(card_7, knowledge_7)

 

    
def describeSCP (scp_toDescribe, label):
    print (">>>>>>" + label + "<<<<<<<<")
    print(scp_toDescribe.strDetailed())
    print ("The final sequence: " + str(scp_toDescribe))  

wst_d = createwst_card_d()
wst_k = createwst_card_k()
wst_3 = createwst_card_3()
wst_7 = createwst_card_7()
wst_fixab1 = createwst_card(card_7, knowledge_7, fix=True, varToFix='d', valueToFix=True)
describeSCP(wst_fixab1, "7 card observed")
