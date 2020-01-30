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
card_d = basicLogic.atom("D", setValue=False)
card_k = basicLogic.atom("K", setValue=False)
card_3 = basicLogic.atom("3", setValue=False)
card_7 = basicLogic.atom("7", setValue=False)


#STARTING RULES, FACTS
# the rule d -> 3 which participants are asked to vericy
knowledge_dimp3 = basicLogic.operator_bitonic_implication(card_d,card_3)
# rules for if each card is seen
knowledge_d = basicLogic.operator_bitonic_implication(basicLogic.TRUE, card_d)
knowledge_3 = basicLogic.operator_bitonic_implication(basicLogic.TRUE, card_3)
knowledge_k = basicLogic.operator_bitonic_implication(basicLogic.TRUE, card_k)
knowledge_7 = basicLogic.operator_bitonic_implication(basicLogic.TRUE, card_7)
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
def createwst_card (variable, knowledge):
    wst =  scp.scp()

    # the d-> 3 rule
    wst.addKnowledge(knowledge_dimp3)
    # the observed card
    if knowledge !=None:
        wst.addKnowledge(knowledge)
    
    wst.addVariable(card_d)
    wst.addVariable(card_3)
    
    if variable!=None:
        wst.addVariable(variable)      

    
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
def createwst_noCard():
    return createwst_card(variable=None, knowledge=None) 
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

"""
Following @refragnietc :
O: observation
A: set of abducibles for each undefined atom
e: e subset A
P: logic program
F: formula
P:=F iff lm_wc_P(F)=T

O is eplained by e iff:
    e subset A
    P + e is satisfiable
    (p+e) := o
"""

"""
"""
def getAbducibles (_scp):
    
    abducibles = []
    variables = _scp.initialV
    for v in variables:
        if v.value==None:
            v_true = basicLogic.atom(v.name, True)
            v_false = basicLogic.atom(v.name, False)
            abducibles.append(v_true)
            abducibles.append(v_false)
    return abducibles

def getAbducibleNames (_scp):
    
    abducibles = []
    variables = _scp.initialV
    for v in variables:
        if v.value==None:
            v_n = basicLogic.atom(v.name, None)
            abducibles.append(v_n)
    return abducibles

from itertools import permutations 

def incrA (a, start=0):
    poss=[]
    if start>=len(a):
        return [a]
    
    a=copy.deepcopy(a)
    a[start]=None
    poss = poss + incrA(a, start+1)
    
    a=copy.deepcopy(a)
    a[start]=True
    poss = poss + incrA(a, start+1)
    
    a=copy.deepcopy(a)
    a[start]=False
    poss = poss + incrA(a, start+1)
    return poss
        
def turnFunction (initialSCP):
    
    #initialSCP = createwst_noCard()
    print scp.scp_evaluator.strLeastModel(initialSCP)
    """
    while isinstance(initialSCP.getLastState(), scp.complexOperation_semanticOperator):
        initialSCP.removeLast()
    """
    """
    A = getAbducibleNames(initialSCP)
    A = scp.scp_evaluator.addMissingVariables(initialSCP, A)
    
    print "{}".format(scp.complexOperation.strVariables(A))
    
    solutions=[]
    values = [None]*len(A)
    possibleValues = incrA(values)
    # we want to find cases where lm wc P (F) = True
    for val in possibleValues:
        _scp = copy.deepcopy(initialSCP)
        newVariables = []
        for v in range (0, len(A)):
            if val[v]!=None:
                body = basicLogic.getGroundAtomNoValFor(val[v])
                head = A[v]
                knowledge = basicLogic.operator_bitonic_implication(body, head)  
                #_scp.addKnowledge(knowledge)
                newVar = basicLogic.atom(A[v].name, val[v])
                newVariables.append(newVar)
                
        #print u"evaluating {}".format(_scp.strFinalKB())
        #print u"using {}".format(_scp.strVariables(newVariables))
        #print "Rule match : {}".format()
        ruleMatch = evaluator.ruleMatch(_scp,newVariables)
        
        if ruleMatch:
            solutions.append(newVariables)
    return solutions
    """

"""
def strSummary (_scp, case):
    s = (u"Case: {}\n{}\n>>Turn :: {}\nLeast Model :: {}").format(case,_scp,None, _scp.strLeastModel())
    return s
"""




"""
print (strSummary(wst_k, "K card seen"))
print ('='*25)
print (strSummary(wst_3, "3 card seen"))
print ('='*25)
print (strSummary(wst_7, "7 card seen"))
print ('='*25)
"""


#res = turnFunction(wst_7)
least = scp.scp_evaluator.strLeastModel(wst_7)
print u">>>>>>>>..Models Are<<<<<<<<<<< \n{}".format(least)
"""
print ("++LEAST MODEL++")
for r in res:
    for s in r:
        print "{}::{}".format(s.name,s.value)
    print "--"
"""
"""
"""
"""
print ("{}{}{}").format('-'*10, "Non-standard Cases" ,'-'*10)
print (strSummary(wst_d_contra, "D card seen, with modus tolens"))
print ('='*25)
print (strSummary(wst_k_contra, "K card seen, with modus tolens"))
print ('='*25)
print (strSummary(wst_3_contra, "3 card seen, with modus tolens"))
print ('='*25)
print (strSummary(wst_7_contra, "7 card seen, with modus tolens"))
print ('='*25)
"""

x = basicLogic.atom('d', None)
y = basicLogic.atom('ab1', False)
z = basicLogic.atom('3', True)

ny = basicLogic.operator_monotonic_negation(y)

pro = basicLogic.operator_bitonic_and(x,ny)
pro2 = basicLogic.operator_bitonic_bijection(pro,z)

print u"{}".format(pro2)
print pro2.evaluate()
            
"""           
a = [None,None,None]
aincr = incrA(a, start=0)
print aincr
print len(aincr)
"""




















