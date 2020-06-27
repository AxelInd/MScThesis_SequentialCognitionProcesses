import sys
sys.path.append("/SCPFramework") 
import copy


from SCPFramework import SCP_Task
from SCPFramework import scpNotationParser
from SCPFramework import CTM
from SCPFramework import CognitiveOperation
from SCPFramework import basicLogic
from SCPFramework import epistemicState
from SCPFramework import StatePointOperations



#INSTANTIATE EACH <cognitiveOperation> object which might be used later
ADDAB = CognitiveOperation.m_addAB()
WC = CognitiveOperation.m_wc()
SEMANTIC = CognitiveOperation.m_semantic()
ABDUCIBLES=CognitiveOperation.m_addAbducibles(maxLength=2)


# Minimal subsets which verify/falsify the conditional and explain the observation o
# Are vallid iff and only 

def f_turnFunction(pi,observations= ['D','K','3','7']):
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
    
    #severe problem using interpetation of conditionals with de-finnetti truth table
    # @TODO how do we resolve????
    # maybe determine if the conditional CAN be falsified?
    #@TODO parser struggles with ( ( a | b) or ( c | d ) )
    conditional = scpNotationParser.stringListToBasicLogic(["( ( 3 | D ) or ( D' | 7 ) )"])
    # we are willing to turn the card if either the (3 | D) or the contrapositive case ( D' | 7 ) holds
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
        print ("epi is ", epi)
        #print ("we made it here")
        #print (epi['R']['abducibles'])
        #print ("and then here")
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
        #print ("mini is : ", mini)
        for cond in conditional:
            #print (cond, "Evaluates to ", cond.evaluate())
            if cond.evaluate()==None:
                
                #print ("evaluation was ", cond.evaluate())
                allCondApplicable = False   
        #print ("cond is ",cond)
                
        if allCondApplicable:
            turns.append('Turn Card')
            #print ("1")
        else:
            turns.append('Do Not Turn')
            #print("2")
                    
    return turns
#a preference function which will returned the prefered response if it is one of the response
#and all the other responses otherwise
def pref_f(responses,pref):
    preferedResonses={}
    for card in pref:
        if pref[card] in responses[card]:
            preferedResonses[card]=pref[card]
        else:
            preferedResonses[card]=responses[card]
    return preferedResonses
#creates the initial state point with only the conditional (3|D)
def create_si_noContra():
    #define the initial atomic name in the WCS: one for each observed card
    #these atoms have value None
    D    = basicLogic.atom('D')
    K     = basicLogic.atom('K')
    three = basicLogic.atom('3')
    seven = basicLogic.atom('7')
    #this is the atom which means NOT (D)
    Dprime = basicLogic.atom("D'")    

    #create an epistemic state containing the known facts and conditionals
    basePointNoContra=epistemicState.epistemicState('WST')
    #the set of conditionals without the contraposition rule
    delta_nocontra=["( 3 | D )"]
    #the set of conditionals as a set of <basicLogic> clauses
    deltaAsLogic = scpNotationParser.stringListToBasicLogic(delta_nocontra)
    #the set of facts known
    S_nocontra = [""]
    #the set of known facts as <basicLogic>
    SAsLogic = scpNotationParser.stringListToBasicLogic(S_nocontra)
    #the set of abducibles, any subset of which might be an explanation
    abducibs = ['( D <- T )', '( D <- F )', '( K <- T )', '( K <- F )', 
                '( 3 <- T )', '( 3 <- F )', '( 7 <- T )', '( 7 <- F )']
    #transform the set of abducibles to a set of <basicLogic> clauses
    logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)

    #set the structural variables of the only epistemic state in the intial state point
    basePointNoContra['S']=SAsLogic
    basePointNoContra['Delta']=deltaAsLogic
    basePointNoContra['V']=[D, K, three, seven, Dprime]
    basePointNoContra['R']={'abducibles':logAbducibs}   
    return [basePointNoContra]

#creates the initial state point wit the conditional (3|D) AND (D'|7)
def create_si_contra():
    #define the initial atomic name in the WCS: one for each observed card
    #these atoms have value None
    D    = basicLogic.atom('D')
    K     = basicLogic.atom('K')
    three = basicLogic.atom('3')
    seven = basicLogic.atom('7')
    #this is the atom which means NOT (D)
    Dprime = basicLogic.atom("D'")    

    #create an epistemic state containing the known facts and conditionals
    basePointContra=epistemicState.epistemicState('WST')
    #the set of conditionals with the contraposition rule
    delta_contra=["( 3 | D )"," ( D' | 7 ) "]
    #the set of conditionals as a set of <basicLogic> clauses
    deltaAsLogic = scpNotationParser.stringListToBasicLogic(delta_contra)
    #the set of facts known, this prevents negative heads in rules
    S_contra = ["( ( D ) <- ( !  D'  ) )"]
    #the set of known facts as <basicLogic>
    SAsLogic = scpNotationParser.stringListToBasicLogic(S_contra)
    #the set of abducibles, any subset of which might be an explanation
    abducibs = ['( D <- T )', '( D <- F )', '( K <- T )', '( K <- F )', 
                '( 3 <- T )', '( 3 <- F )', '( 7 <- T )', '( 7 <- F )']
    #transform the set of abducibles to a set of <basicLogic> clauses
    logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)

    #set the structural variables of the only epistemic state in the intial state point
    basePointContra['S']=SAsLogic
    basePointContra['Delta']=deltaAsLogic
    basePointContra['V']=[D, K, three, seven, Dprime]
    basePointContra['R']={'abducibles':logAbducibs}   
    return [basePointContra]
    
#The most common case of the WST, where the cards D and 3 are turned
def mu_D3 ():
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_noContra()
    
    #the set of cognitive operations which we believe might model this case of the WST
    M=[ABDUCIBLES, ADDAB, SEMANTIC, WC]
    #The final state dependent external evaluation function
    f=f_turnFunction
    #the turn responses which would we would like to achieve
    gamma_D3={'D':'Turn Card','K':'Do Not Turn','3':'Turn Card','7':'Do Not Turn'}    
    
    #The SCP task which states what is required from a solution SCP or realised SCP
    task_D3 = SCP_Task.SCP_Task(s_i,M,f,gamma_D3)   
    
    searchRes = task_D3.deNoveSearch(depth = 3, searchType="satisfying")
    
    print ("search results are ", searchRes)
    #This is a test SCP mu=(c,f()) which is known to work
    
    """
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    c.appendm(ABDUCIBLES)
    c.appendm(WC)
    c.appendm(SEMANTIC)

    #the set of possible observations which might need to be explained to see if we should 
    # turn a card
    observations = ['D','K','3','7']
    
    #use the turn function to evaluate the ctm and see if the card should be turned
    predictions=f_turnFunction(c,observations)    
    
    #print True if mu|=gamma_D3
    print ("Responses: ",predictions)
    print ("Lenient: mu|=gamma_D3 :", StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma_D3))
    print ("Strict:  mu|=gamma_D3 :", StatePointOperations.predictionsModelsGamma_strict(predictions,gamma_D3))
    """
    
#The most common case of the WST, where the cards D and 3 are turned
def mu_D ():
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_noContra()
    
    #the set of cognitive operations which we believe might model this case of the WST
    M=[ABDUCIBLES, ADDAB, SEMANTIC, WC]
    #The final state dependent external evaluation function
    f=f_turn
    #prefer to turn the card if any realised SCP would cause the card to be turned
    prefDontTurn = {'D':'Do Not Turn','K':'Do Not Turn','3':'Do Not Turn','7':'Do Not Turn'}  
    #the turn responses which would we would like to achieve
    gamma_D={'D':'Turn Card','K':'Do Not Turn','3':'Do Not Turn','7':'Do Not Turn'}  

    #The SCP task which states what is required from a solution SCP or realised SCP
    task_D = SCP_Task.SCP_Task(s_i,M,f,gamma_D)   
    
    #This is a test SCP mu=(c,f()) which is known to work
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    c.appendm(ABDUCIBLES)
    c.appendm(WC)
    c.appendm(SEMANTIC)

    #the set of possible observations which might need to be explained to see if we should 
    # turn a card
    observations = ['D','K','3','7']
    
    #use the turn function to evaluate the ctm and see if the card should be turned
    # we prefer the 'Do Not Turn' response in this case
    predictions=pref_f(f_turnFunction(c,observations), prefDontTurn)   
    
    #print True if mu|=gamma_D3
    print ("Responses: ",predictions)
    print ("Lenient: mu|=gamma_D :", StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma_D))
    print ("Strict:  mu|=gamma_D :", StatePointOperations.predictionsModelsGamma_strict(predictions,gamma_D))

#The classical logic response to the WST, turning the cards D and 7
def mu_D7 ():
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_contra()
    
    #the set of cognitive operations which we believe might model this case of the WST
    M=[ABDUCIBLES, ADDAB, SEMANTIC, WC]
    #The final state dependent external evaluation function
    f=f_turn
    #prefer to turn the card if any realised SCP would cause the card to be turned
    prefDontTurn = {'D':'Do Not Turn','K':'Do Not Turn','3':'Do Not Turn','7':'Do Not Turn'}  
    #the turn responses which would we would like to achieve
    gamma_D7={'D':'Turn Card','K':'Do Not Turn','3':'Do Not Turn','7':'Turn Card'}  

    #The SCP task which states what is required from a solution SCP or realised SCP
    task_D7 = SCP_Task.SCP_Task(s_i,M,f,gamma_D7)   
    
    #This is a test SCP mu=(c,f()) which is known to work
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    c.appendm(ABDUCIBLES)
    c.appendm(WC)
    c.appendm(SEMANTIC)

    #the set of possible observations which might need to be explained to see if we should 
    # turn a card
    observations = ['D','K','3','7']
    
    #use the turn function to evaluate the ctm and see if the card should be turned
    # we prefer the 'Do Not Turn' response in this case
    predictions=pref_f(f_turnFunction(c,observations), prefDontTurn)   
    
    #print True if mu|=gamma_D3
    print ("Responses: ",predictions)
    print ("Lenient: mu|=gamma_D7 :", StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma_D7))
    print ("Strict:  mu|=gamma_D7 :", StatePointOperations.predictionsModelsGamma_strict(predictions,gamma_D7))


#The individual case of the WST, where the cards D, 3, and 7 are turned
def mu_D37 ():
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_contra()
    
    #the set of cognitive operations which we believe might model this case of the WST
    M=[ABDUCIBLES, ADDAB, SEMANTIC, WC]
    #The final state dependent external evaluation function
    f=f_turn
    #the turn responses which would we would like to achieve
    gamma_D37={'D':'Turn Card','K':'Do Not Turn','3':'Turn Card','7':'Turn Card'}    
    
    #The SCP task which states what is required from a solution SCP or realised SCP
    task_D37 = SCP_Task.SCP_Task(s_i,M,f,gamma_D37)   
    
    #This is a test SCP mu=(c,f()) which is known to work
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    c.appendm(ABDUCIBLES)
    c.appendm(WC)
    c.appendm(SEMANTIC)

    #the set of possible observations which might need to be explained to see if we should 
    # turn a card
    observations = ['D','K','3','7']
    
    #use the turn function to evaluate the ctm and see if the card should be turned
    predictions=f_turnFunction(c,observations)    
    
    #print True if mu|=gamma_D37
    print ("Responses: ",predictions)
    print ("Lenient: mu|=gamma_D37 :", StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma_D37))
    print ("Strict:  mu|=gamma_D37 :", StatePointOperations.predictionsModelsGamma_strict(predictions,gamma_D37))

mu_D3()
#mu_D37()

#mu_D()
#mu_D7()






































