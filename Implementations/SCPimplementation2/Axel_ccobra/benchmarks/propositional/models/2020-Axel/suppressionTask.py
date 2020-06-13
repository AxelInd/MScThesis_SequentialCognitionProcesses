# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 09:41:08 2020

@author: Axel
"""
import basicLogic
import scp
import complexOperation
import scpError
import epistemicState
print ("=================THE SUPPRESSION TASK=========================")





print (">>> 1) If she has an essay to write she will study late in the library (e->l).")
print (">>> 2) If the library is open she will study late in the library (o->l).")
print (">>> 3) She has an essay to write (True->e).")

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

def createAtoms (names, vals):
    li = []
    for i in range (0,len(names)):
        at = basicLogic.atom(names[i],vals[i])
        li.append(at)
    return li

def unit_compare(_scp,correctKB, correctNames, correctVals):
    epi = _scp.evaluate()
    v = epi.getV()
    kb = epi.getKB()
    
    correctV = createAtoms(correctNames,correctVals)
    if len(v)!=len(correctV):
        raise scpError.unitTestFailedError
    for i in range (0, len(correctV)):
        if v[i].name!=correctV[i].name or v[i].getValue() != correctV[i].getValue():
            raise scpError.unitTestFailedError
    
def unit_sup_standard ():
    _scp = createsuppressionTask_standard()
    correctKB = None
    print (_scp.evaluate())
    correctNames = ['e','l','o','ab1','ab2']
    correctVals = [True,None,None,None,False]
    print (_scp.strDetailed())
    unit_compare(_scp,correctKB,correctNames,correctVals)
def unit_sup_noSuppression ():
    _scp = createsuppressionTask_noSuppression()
    correctKB = None
    correctNames = ['e','l','ab1',]
    correctVals = [True, True, False]
    unit_compare(_scp,correctKB,correctNames,correctVals)    
def unit_sup_fix ():
    _scp = createsuppressionTask_fixVariableab1()
    correctKB = None
    correctNames = ['e','l','o','ab1','ab2']
    correctVals = [True,True,None,False,False]
    unit_compare(_scp,correctKB,correctNames,correctVals)      
def unit_sup_delete ():
    _scp = createsuppressionTask_deleteVariableo()
    correctKB = None
    correctNames = ['e','l','ab1',]
    correctVals = [True, True, False]
    unit_compare(_scp,correctKB,correctNames,correctVals)      
def unit_TestAll ():
    unit_sup_standard()
    unit_sup_noSuppression()
    unit_sup_fix()
    unit_sup_delete()
    print (">>**All unit tests passed**<<")

    
def describeSCP (scp_toDescribe, label):
    print (">>>>>" + label + "<<<<<<<<")
    print(scp_toDescribe.strDetailed())
    print ("The final sequence: " + str(scp_toDescribe))   
    
    
unit_TestAll()


#-----------------------------------------------------------------------------    
import SCP_Task
import StatePoint
import scpNotationParser
import CTM
import CognitiveOperation
import copy

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

  

def extractEpis(statePoint):
    if not isinstance (statePoint,list):
        return statePoint
    if len(statePoint)==1:
        return extractEpis(statePoint[0])
    li=[]
    for epi in statePoint:
        li.append(extractEpis(epi))
    return li
    
def f_studyLate(pi):
    finalStructures=pi.evaluate()
    finalStates=extractEpis(finalStructures)
    if not isinstance(finalStates,list):
        finalStates=[finalStates]
    print("Final states")
    print(finalStates)
    goal2 = [('l',True)]
    responses=[]
    for epi in finalStates:
        print ("\n")
        print (epi)
        V = epi['V']
        print(V)
        for var in V:
            for goal in goal2:
                if var.getName()==goal[0] :
                    if var.getValue()==goal[1]:
                        print ("here1")
                        responses.append("She will study late in the library")
                    if var.getValue()!=None and var.getValue()!=goal[1]:
                        print ("here2")
                        responses.append("She will not study late in the library")
                    if var.getValue()==None:
                        print ("here3")
                        responses.append("We are uncertain if she will study late in the library")
    return responses
        
        

basePoint1=epistemicState.epistemicState('el')
#The possible starting states for the SCP
delta1=["( l | e )"]
#delta1=["( l | e )", "( l | o )"]
S1 = ["( e <- T )"]

delta1AsLogic = scpNotationParser.stringListToBasicLogic(delta1)
S1AsLogic = scpNotationParser.stringListToBasicLogic(S1)
basePoint1['S']=S1AsLogic
basePoint1['Delta']=delta1AsLogic
basePoint1['V']=[e,l]


#second case, elo should show suppression
basePoint2=epistemicState.epistemicState('elo')
#The possible starting states for the SCP
delta2=["( l | e )", "( l | o )"]
S2 = ["( e <- T )"]
delta2AsLogic = scpNotationParser.stringListToBasicLogic(delta2)
S2AsLogic = scpNotationParser.stringListToBasicLogic(S2)
basePoint2['S']=S2AsLogic
basePoint2['Delta']=delta2AsLogic
basePoint2['V']=[e,l,o]



#Create the first state point
statePoints=[basePoint1,basePoint2]
s_i=StatePoint.StatePoint(childPoints=statePoints)

#The set of possible states
M=[comp_addAB,comp_deleteo,comp_fixab1,comp_weak,comp_semantic,comp_semantic_full]
#The external evaluation function
f=f_studyLate
#The desired output of the external evaluation function
Gamma="different"

#The SCP task which states what is required from a solution SCP or realised SCP
task = SCP_Task.SCP_Task(s_i,M,f,Gamma)    

ADDAB = CognitiveOperation.m_addAB()
WC = CognitiveOperation.m_wc()
SEMANTIC = CognitiveOperation.m_semantic()
#test ctm
c = CTM.CTM()
c.setSi(s_i)
c.appendm(ADDAB)
c.appendm(WC)
c.appendm(SEMANTIC)
result = f(c)
print ('result')
print (result)
"""
#CREATE AN SCP FOR EACH VARIATION OF THE TASK
suppressionTask_standard = createsuppressionTask_standard()
suppressionTask_noSuppression = createsuppressionTask_noSuppression()
suppressionTask_fix = createsuppressionTask_fixVariableab1()
suppressionTask_delete = createsuppressionTask_deleteVariableo()


#CHOOSE WHICH SCP TO SEE DETAILED HERE
describeSCP(suppressionTask_delete, "Standard Suppression Task")

#unit test to make sure the expected results are observed

"""

"""

si = epistemicState.epistemicState_weakCompletion()
si.addKnowledge(knowledge1)
si.addKnowledge(knowledge2)
#si.addKnowledge(knowledge3)

si.addVariable(e)
si.addVariable(l)
#si.addVariable(o)

suppressionTask = scp.scp(epiState1=si)

suppressionTask.addNext(comp_addAB)
suppressionTask.addNext(comp_weak)
suppressionTask.addNext(comp_semantic_full)
describeSCP(suppressionTask, "Standard Suppression Task")


#si2 = epistemicState.epistemicState_weakCompletion()
#print (si)




#suppressionTask.addNext(comp_semantic)
#suppressionTask.addNext(comp_semantic)


#print (si)
"""


def f_turn(pi,observation):
    finalStructures=pi.evaluate()
    finalStates=extractEpis(finalStructures)
    
    if not isinstance(finalStates,list):
        finalStates=[finalStates]
    #print("Final states")
    #print(finalStates)
    
    conditional = scpNotationParser.stringListToBasicLogic(['( 3 | D )'.format(observation)])
    obs = scpNotationParser.stringListToBasicLogic(['( {} <- T )'.format(observation)])
    
    responses=[]
    for epi in finalStates:
        #print ("\n")
        #print (epi)
        V = epi['V']
        #print(V)
        correct=True

        basicLogic.setkbfromv(conditional,epi['V'])
        basicLogic.setkbfromv(obs,epi['V'])
        
        #the conditional must be verified or falsified
        #the observation must be True
        allObsTrue=True
        for o in obs: 
            if o.evaluate()!=True:
                allObsTrue=False
        allCondApplicable = True
        for cond in conditional:
            if cond.evaluate()==None:
                allCondApplicable = False

        if allObsTrue and allCondApplicable:
            responses.append('Turn Card')
        else:
            responses.append('Do Not Turn Card')
            
        
        
            
    #no we need to find the minimal set of abducibles to turn the cards
    turnResponses=[]

    for i in range (0,len(responses)):
        if responses[i]=='Turn Card':
            turnResponses.append(finalStates[i])
    minimalSubset = []
    isAsubset = [False]*len(turnResponses)
    for epi in turnResponses:
        Flag=False
        #THIS SHOWS THAT WE NEED TO WRITE OUR OWN "IS SUBSET" method
        x = [properSubset(epi['R']['abducibles'],ot['R']['abducibles']) for ot in turnResponses]
        for i in range (0, len(x)):
            if x[i]==True:
                isAsubset[i]=True
    for i in range (0,len(turnResponses)):
        if isAsubset[i]==False:
            #use this if you want the epistemic states
            #minimalSubset.append(turnResponses[i])
            
            #use this if you want the chosen abducibles only
            minimalSubset.append(turnResponses[i]['R']['abducibles'])
            
    return minimalSubset

def properSubset(li1,li2):
    if li1 == li2:
        return False
    for v1 in li1:
        #if there is some v in the first list that is not in the second list, they can't be subsets
        match=False
        for v2 in li2:
            #print (v1.clause1)
            #print (v1.clause2)
            if v1.clause1 == v2.clause1:
                if v1.clause2 == v2.clause2:
                    match=True
        if not match:
            return False
    return True
    
D = basicLogic.atom('D')
K = basicLogic.atom('K')
three = basicLogic.atom('3')
seven=basicLogic.atom('7')



basePointNoAbd=epistemicState.epistemicState('')
#The possible starting states for the SCP
delta1=["( 3 | D )"]
#delta1=["( l | e )", "( l | o )"]
S1 = [""]

delta1AsLogic = scpNotationParser.stringListToBasicLogic(delta1)
S1AsLogic = scpNotationParser.stringListToBasicLogic(S1)
basePointNoAbd['S']=S1AsLogic
basePointNoAbd['Delta']=delta1AsLogic
basePointNoAbd['V']=[D, K, three, seven]


#Create the first state point
# K case
basePointD= copy.deepcopy(basePointNoAbd)
basePointD.setName('abducible:D')
basePointD['S'] = basePointD['S'] + (scpNotationParser.stringListToBasicLogic(['( D <- T )']))

basePointK= copy.deepcopy(basePointNoAbd)
basePointK.setName('abducible:K')
basePointK['S'] = basePointD['S'] + (scpNotationParser.stringListToBasicLogic(['( K <- T )']))

basePoint3= copy.deepcopy(basePointNoAbd)
basePoint3.setName('abducible:3')
basePoint3['S'] = basePointD['S'] + (scpNotationParser.stringListToBasicLogic(['( 3 <- T )']))


basePoint7= copy.deepcopy(basePointNoAbd)
basePoint7.setName('abducible:7')
basePoint7['S'] = basePointD['S'] + (scpNotationParser.stringListToBasicLogic(['( 7 <- T )']))


#statePoints=[basePointD,basePointK,basePoint3,basePoint7]
statePoints=[basePointNoAbd]
s_i=StatePoint.StatePoint(childPoints=statePoints)

#The set of possible states
M=[comp_addAB,comp_deleteo,comp_fixab1,comp_weak,comp_semantic,comp_semantic_full]
#The external evaluation function
f=f_turn
#The desired output of the external evaluation function
Gamma="different"

#The SCP task which states what is required from a solution SCP or realised SCP
task = SCP_Task.SCP_Task(s_i,M,f,Gamma)    


ADDAB = CognitiveOperation.m_addAB()
WC = CognitiveOperation.m_wc()
SEMANTIC = CognitiveOperation.m_semantic()
#abducibs = [ '( 7 <- T )', '( 7 <- F )']
abducibs = ['( D <- T )', '( D <- F )', '( K <- T )', '( K <- F )', '( 3 <- T )', '( 3 <- F )', '( 7 <- T )', '( 7 <- F )']
logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)
ABDUCIBLES=CognitiveOperation.m_addAbducibles(abducibles=logAbducibs, maxLength=4)
#test ctm
c = CTM.CTM()
c.setSi(s_i)
c.appendm(ADDAB)
c.appendm(ABDUCIBLES)
c.appendm(WC)
c.appendm(SEMANTIC)
print(c.evaluate())



observation = 'D'
result = f(c,observation)
print ("minimal subset for {} : {}".format(observation,result))

observation = 'K'
result = f(c,observation)
print ("minimal subset for {} : {}".format(observation,result))

observation = '3'
result = f(c,observation)
print ("minimal subset for {} : {}".format(observation,result))


observation = '7'
result = f(c,observation)
print ("minimal subset for {} : {}".format(observation,result))

















