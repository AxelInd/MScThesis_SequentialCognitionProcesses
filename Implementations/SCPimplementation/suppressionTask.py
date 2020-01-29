# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 09:41:08 2020

@author: Axel
"""
import basicLogic
import scp
import copy

print ("=================THE SUPPRESSION TASK=========================")





print (">>> 1) If she has an essay to write she will study late in the library.")
print (">>> 2) If the library is open she will study late in the library.")
print (">>> 3) She has an essay to write.")

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
knowledge2 = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, e)
# if the library is open, she will study late in the library
knowledge3 = basicLogic.operator_bitonic_implication(o, l)
# the lirary is open
knowledge4 = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, o)

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




def createsuppressionTask_standard():
    suppressionTask = scp.scp()
    #ADD THE FACTS TO THE INITIAL EPISTEMIC STATE
    suppressionTask.addKnowledge(knowledge1)
    suppressionTask.addKnowledge(knowledge2)
    suppressionTask.addKnowledge(knowledge3)
    # LEAVE UNCOMMENTED TO TEST CASES THE WHERE WE HAVE KNOWLEDGE OF THE OPENNESS OF THE LIBRARY
    #a.addKnowledge(knowledge4)
    
    #INITIAL VARIABLE ASSIGNMENTS
    # This adds variables with unknown values to the V set of the epistemic state
    suppressionTask.addVariable(e)
    suppressionTask.addVariable(l)
    suppressionTask.addVariable(o)
    
    suppressionTask.addNext(comp_addAB)
    suppressionTask.addNext(comp_weak)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    return suppressionTask

def createsuppressionTask_noSuppression():
    suppressionTask = scp.scp()
    #ADD THE FACTS TO THE INITIAL EPISTEMIC STATE
    suppressionTask.addKnowledge(knowledge1)
    suppressionTask.addKnowledge(knowledge2)
    #suppressionTask.addKnowledge(knowledge3)
    # LEAVE UNCOMMENTED TO TEST CASES THE WHERE WE HAVE KNOWLEDGE OF THE OPENNESS OF THE LIBRARY
    #a.addKnowledge(knowledge4)
    
    #INITIAL VARIABLE ASSIGNMENTS
    # This adds variables with unknown values to the V set of the epistemic state
    suppressionTask.addVariable(e)
    suppressionTask.addVariable(l)
    #suppressionTask.addVariable(o)
    
    suppressionTask.addNext(comp_addAB)
    suppressionTask.addNext(comp_weak)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    return suppressionTask

def createsuppressionTask_fixVariableab1():
    suppressionTask = scp.scp()
    #ADD THE FACTS TO THE INITIAL EPISTEMIC STATE
    suppressionTask.addKnowledge(knowledge1)
    suppressionTask.addKnowledge(knowledge2)
    suppressionTask.addKnowledge(knowledge3)
    # LEAVE UNCOMMENTED TO TEST CASES THE WHERE WE HAVE KNOWLEDGE OF THE OPENNESS OF THE LIBRARY
    #a.addKnowledge(knowledge4)
    
    #INITIAL VARIABLE ASSIGNMENTS
    # This adds variables with unknown values to the V set of the epistemic state
    suppressionTask.addVariable(e)
    suppressionTask.addVariable(l)
    suppressionTask.addVariable(o)
    
    suppressionTask.addNext(comp_addAB)
    suppressionTask.addNext(comp_fixab1)
    suppressionTask.addNext(comp_weak)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    return suppressionTask

def createsuppressionTask_deleteVariableo():
    suppressionTask = scp.scp()
    #ADD THE FACTS TO THE INITIAL EPISTEMIC STATE
    suppressionTask.addKnowledge(knowledge1)
    suppressionTask.addKnowledge(knowledge2)
    suppressionTask.addKnowledge(knowledge3)
    # LEAVE UNCOMMENTED TO TEST CASES THE WHERE WE HAVE KNOWLEDGE OF THE OPENNESS OF THE LIBRARY
    #a.addKnowledge(knowledge4)
    
    #INITIAL VARIABLE ASSIGNMENTS
    # This adds variables with unknown values to the V set of the epistemic state
    suppressionTask.addVariable(e)
    suppressionTask.addVariable(l)
    suppressionTask.addVariable(o)

    suppressionTask.addNext(comp_deleteo)
    suppressionTask.addNext(comp_addAB)
    suppressionTask.addNext(comp_weak)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)


    return suppressionTask

def describeSCP (scp_toDescribe, label):
    print (">>>>>" + label + "<<<<<<<<")
    print(scp_toDescribe.strDetailed())
    print ("The final sequence: " + str(scp_toDescribe))    
    

#CREATE AN SCP FOR EACH VARIATION OF THE TASK
suppressionTask_standard = createsuppressionTask_standard()
suppressionTask_noSuppression = createsuppressionTask_noSuppression()
suppressionTask_fix = createsuppressionTask_fixVariableab1()
suppressionTask_delete = createsuppressionTask_deleteVariableo()


#CHOOSE WHICH SCP TO SEE DETAILED HERE
describeSCP(suppressionTask_fix, "Standard Suppression Task")














