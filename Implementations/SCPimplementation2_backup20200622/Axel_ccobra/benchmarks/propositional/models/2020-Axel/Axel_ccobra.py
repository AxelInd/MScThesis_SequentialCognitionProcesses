import numpy as np

import ccobra

import basicLogic
import scp
import scpNotationParser
import scpSearch
import complexOperation

class SCP_model(ccobra.CCobraModel):
    def getM_purposeBiltToolbox (self):
        return scpSearch.getM_WST()
    def __init__(self, name='SCP_model'):
        super(SCP_model, self).__init__(
            name, ['nonmonotonic'], ['single-choice'])

    def predict(self, item, **kwargs):
        enc_string = item.task
        print (enc_string)
        epi = taskToBasicLogic(enc_string)
        #@TODOswitch
        s = scp.scp(epiState1=epi)
        #kbEvaluator(kb)
        print (s)
        
        #TODOsetupSoThatTaskWillWork
        M=self.getM_purposeBiltToolbox  ()
        #@TODO f() should be exact variable answer pattern  match
        task = scpSearch.scpTask(si=epi, M=M, gamma=True, f=scpSearch.f_trivialFalse)
        """
        print ("THE TASK IS")
        print (task)
        """
        #@TODO there is a problem here!!!
        """
        search = task.deNovoSearch(s=None,depth=2,validityType="All")
        print ("++++++++++++++++++++")
        #print(search)
        print ("++++++++++++++++++++")
        
        
        
        #once the scp has been evaluated, a choice from [choices] must be used to make a prediction
        #options for this: random, most-probable, highest scoring
        bestScp, bestScore = scpSearch.scpTask.getBestSCP(scpList=search, constraints=None)
        print ("Best SCP is ", bestScp)
        """
        choices = item.choices
        print ("<<--<<--<<--")
        print (choices)
        print (">>-->>-->>-->>-->>")  
        #@TODO turning the results into basic logic is currently filing for some reason.
        choicesAsBasicLogic = taskToBasicLogic((choices))
        print ("<<--<<--<<--")
        print (choicesAsBasicLogic)
        print (">>-->>-->>-->>-->>") 
        
        return item.choices[np.random.randint(0, len(item.choices))]
        


def taskToBasicLogic (task):
    kb = []
    for i in task:
        iAsBasicLogic = scpNotationParser.polishNotationParser(i)
        #@TODO this was changed to reflected unparsable rules
        for r in iAsBasicLogic:
            kb.append(r)
        #kb.append(iAsBasicLogic[0])    
    state = scpNotationParser.rulesListToEpistemicState(kb,epistemicStateType='dl')
    return state
    

            
    


runTest=True
if runTest: 
    prob = [['Implies', 'Holds', 'There is excess of food for her species', 
             'Holds', 'Kira will mate', 'Implies', 'Holds', 'It is the 7th month of the solar year', 
             'Holds', 'Kira will mate', 'Implies', 'Holds', 'The temperature falls below 10 Celsius', 
             'Not', 'Holds', 'Kira will mate'], ['Not', 'Holds', 'Kira mated']]

    proc_prob = taskToBasicLogic((prob))
    
    print (proc_prob)
    """
    print (x)
    for i in x:
        i.monotonicDelete(basicLogic.operator_monotonic_negation)
    print (x)
    """
    
























            