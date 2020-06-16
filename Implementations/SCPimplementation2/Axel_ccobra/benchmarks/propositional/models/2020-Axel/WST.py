import SCP_Task
import scpNotationParser
import CTM
import CognitiveOperation
import copy
import basicLogic
import epistemicState
import StatePointOperations

# Minimal subsets which verify/falsify the conditional and explain the observation o
# Are vallid iff and only 
def f_turnFunction(pi,observations):
    decisions={}
    for obs in observations:
        print ("observation is ", obs)
        for i in obs:
            decisions[obs]=f_turn(pi,obs)
            
            
    return decisions
        
        
        
def f_turn(pi,observation):
    finalStructures=pi.evaluate()
    finalStates=StatePointOperations.flattenStatePoint(finalStructures)
    
    if not isinstance(finalStates,list):
        finalStates=[finalStates]
    #print("Final states")
    #print(finalStates)
    
    conditional = scpNotationParser.stringListToBasicLogic(['( 3 | D )'])
    obs = scpNotationParser.stringListToBasicLogic(['( {} <- T )'.format(observation)])
    
    responses=[]
    for epi in finalStates:
        #print ("\n")
        #print (epi)
        
        basicLogic.setkbfromv(obs,epi['V'])
        
        #the conditional must be verified or falsified
        #the observation must be True
        allObsTrue=True
        for o in obs: 
            if o.evaluate()!=True:
                allObsTrue=False
        #allCondApplicable = True

        if allObsTrue:
            responses.append('observations hold')
        else:
            responses.append('observations do not')

            
        
        
            
    #now we need to find the minimal set of abducibles to turn the cards
    turnResponses=[]
    #WE PREFER MINIMAL EXPLANATIONS
    for i in range (0,len(responses)):
        if responses[i]=='observations hold':
            turnResponses.append(finalStates[i])
    minimalSubset = []
    
    for epi in turnResponses:
        x = [StatePointOperations.properSubset(ot['R']['abducibles'],epi['R']['abducibles'])  for ot in turnResponses]
        #another least model is a subset of this one
        if True in x:
            pass
        else:
            minimalSubsetAsVariables=epi['V']
            minimalSubsetAsList=StatePointOperations.VtoTupleList(minimalSubsetAsVariables,ignoreNone=True)
            if minimalSubsetAsList not in minimalSubset:
                minimalSubset.append(minimalSubsetAsVariables)

    turns=[]
    for mini in minimalSubset:
        allCondApplicable=True
        #this is done later
        basicLogic.setkbfromv(conditional,mini)
        for cond in conditional:
            if cond.evaluate()==None:
                #print ("evaluation was ", cond.evaluate())
                allCondApplicable = False   
        #print ("cond is ",cond)
                
        if allCondApplicable:
            turns.append('Turn Card')
            #print ("1")
        else:
            turns.append('Do Not Turn Card')
            #print("2")
                    
    return turns


    
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
s_i=statePoints

#The set of possible states
M=[]
#The external evaluation function
f=f_turn
#The desired output of the external evaluation function
gamma={'D':'Turn Card','K':'Do Not Turn Card','3':'Turn Card','7':'Do Not Turn Card'}

#The SCP task which states what is required from a solution SCP or realised SCP
task = SCP_Task.SCP_Task(s_i,M,f,gamma)    


ADDAB = CognitiveOperation.m_addAB()
WC = CognitiveOperation.m_wc()
SEMANTIC = CognitiveOperation.m_semantic()
#abducibs = [ '( 7 <- T )', '( 7 <- F )']
abducibs = ['( D <- T )', '( D <- F )', '( K <- T )', '( K <- F )', '( 3 <- T )', '( 3 <- F )', '( 7 <- T )', '( 7 <- F )']
logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)
#set to 8 to run all abducibles
ABDUCIBLES=CognitiveOperation.m_addAbducibles(abducibles=logAbducibs, maxLength=3)
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

"""
results = task.deNoveSearch(depth=3,searchType='satisfying')
print ("Results",results)
"""

observations = ['D','K','3','7']
predictions=f_turnFunction(c,observations)
print (predictions)




print (StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma))
print (StatePointOperations.predictionsModelsGamma_strict(predictions,gamma))










