# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 14:23:02 2020
HEREIN IS AN IMPLEMENTATION OF SCPS USING THE WASON SELECTION TASK
@author: Axel
"""

import basicLogic
import scp
import copy

#CARDS THAT CAN BE OBSERVED
card_d = basicLogic.atom("p", setValue=False)
card_k = basicLogic.atom("p'", setValue=False)
card_3 = basicLogic.atom("q", setValue=False)
card_7 = basicLogic.atom("q'", setValue=False)


#STARTING RULES, FACTS
# the rule d -> 3 which participants are asked to vericy
knowledge_dimp3 = basicLogic.operator_bitonic_implication(card_d,card_3)
# rules for if each card is seen
knowledge_d = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, card_d)
knowledge_3 = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, card_3)
knowledge_k = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, card_k)
knowledge_7 = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, card_7)
# the extra fact that 7->not(3)
pPrime = basicLogic.operator_monotonic_negation(card_3)
knowledge_primeRelationp = basicLogic.operator_bitonic_implication(card_7,pPrime, immutable=True)
# the extra fact that K->not(D)
qPrime = basicLogic.operator_monotonic_negation(card_k)
knowledge_primeRelationq = basicLogic.operator_bitonic_implication(card_d,qPrime , immutable=True)


#INITIALISE THE SET OF COMPLEX OPERATORS M
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

comp_modusTolens = scp.complexOperation_modusTolens()

"""
CREATE AN SCP CONTAING THE RULE D->3 AS WELL AS THE CARD OBSERVED
@param variable: variable to be added to the SCP (usually the card observed)
@param knowledge: information about observed card x in the form T->x
@return the SCP that results from this process
"""
def createwst_card (variable, knowledge, fix=False):
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
    

 
    wst.addVariable(variable)      
    
    print ("The variables are:")
    print (wst.strVariables(wst.initialV))  
    print ("The initial KB is ")
    print (u"{}".format(wst.strInitialKB()))
    
    wst.addNext(comp_addAB)
    
    wst.addNext(comp_weak)
    wst.addNext(comp_semantic)
    wst.addNext(comp_semantic)

    wst.addNext(comp_semantic)
    

    #without this deepcopy, some object property causes the wst of the previous call to be overwritten by this one
    #@TODOfix
    return copy.deepcopy(wst)  


"""
METHODS FOR EACH OF THE OBSERVED CARDS
"""
def createwst_card_d ():
    return createwst_card(card_d, knowledge_d) 
def createwst_card_k ():
    return createwst_card(card_k, knowledge_k) 
def createwst_card_3 ():
    return createwst_card(card_3, knowledge_3) 
def createwst_card_7 ():
    return createwst_card(card_7, knowledge_7) 

"""
METHODS FOR CASES WHERE CONTRAPOSITION TAKES PLACE
"""
def createwst_card_d_contraposition ():
    wst = createwst_card_d()
    #add p
    wst.addVariable(card_7)  
    wst.addVariable(card_k)  
    wst.addKnowledge(knowledge_primeRelationp)
    wst.addKnowledge(knowledge_primeRelationq)
    wst.insertAtPos(comp_modusTolens, 1)
    return wst
def createwst_card_k_contraposition ():
    wst = createwst_card_k()
    #add p
    wst.addVariable(card_7)  
    wst.addVariable(card_k)  
    wst.addKnowledge(knowledge_primeRelationp)
    wst.addKnowledge(knowledge_primeRelationq)
    wst.insertAtPos(comp_modusTolens, 1)
    return wst
def createwst_card_3_contraposition ():
    wst = createwst_card_3()
    #add p
    wst.addVariable(card_7)  
    wst.addVariable(card_k)  
    wst.addKnowledge(knowledge_primeRelationp)
    wst.addKnowledge(knowledge_primeRelationq)
    wst.insertAtPos(comp_modusTolens, 1)
    return wst
def createwst_card_7_contraposition ():
    wst = createwst_card_7()
    #add p
    wst.addVariable(card_7)  
    wst.addVariable(card_k)  
    wst.addKnowledge(knowledge_primeRelationp)
    wst.addKnowledge(knowledge_primeRelationq)
    wst.insertAtPos(comp_modusTolens, 1)
    return wst

"""
PRINT OUT THE SCP IN QUESTION SHOWING THEINPUT AND OUTPUTS OF EACH COMPLEX OPERATION CALL
"""
def describeSCP (scp_toDescribe, label):
    print (">>>>>>" + label + "<<<<<<<<")
    print(u'{}'.format(scp_toDescribe.strDetailed()))
    print ("The final sequence: " + str(scp_toDescribe))  

#instantiate each normal card observation
wst_d = createwst_card_d()
wst_k = createwst_card_k()
wst_3 = createwst_card_3()
wst_7 = createwst_card_7()

    
#instantiate each card observation with assumed modus tolens
wst_d_contra = createwst_card_d_contraposition()
wst_k_contra = createwst_card_k_contraposition()
wst_3_contra = createwst_card_3_contraposition()
wst_7_contra = createwst_card_7_contraposition()

# IF THE WCS MAPS A VARIABLE IN THE RULE TO TRUE, THEN WE MUST TURN THE CARD TO CHECK IT
# TODO this method still needs work
def turnFunction (_scp):
    ruleToTest = copy.deepcopy(knowledge_dimp3)
    
        
    variables = _scp.evaluateV()
    for v in variables:
        #print ("{}:{}".format(v.name, v.value))
        ruleToTest.deepSet(v.name, v.value)
    turn = ruleToTest.evaluate()
    #print(u"Testing rule: {}").format(ruleToTest)
    return turn

def strSummary (_scp, case):
    s = (u"Case: {}\n{}\n>>Turn :: {}\nLeast Model :: {}").format(case,_scp,turnFunction(_scp), _scp.strLeastModel())
    return s

print ("{}{}{}").format('-'*10, "standard Cases" ,'-'*10)
print ('='*25)
print (strSummary(wst_d, "D card seen"))
print ('='*25)
print (strSummary(wst_k, "K card seen"))
print ('='*25)
print (strSummary(wst_3, "3 card seen"))
print ('='*25)
print (strSummary(wst_7, "7 card seen"))
print ('='*25)

print ("{}{}{}").format('-'*10, "Non-standard Cases" ,'-'*10)
print (strSummary(wst_d_contra, "D card seen, with modus tolens"))
print ('='*25)
print (strSummary(wst_k_contra, "K card seen, with modus tolens"))
print ('='*25)
print (strSummary(wst_3_contra, "3 card seen, with modus tolens"))
print ('='*25)
print (strSummary(wst_7_contra, "7 card seen, with modus tolens"))
print ('='*25)

