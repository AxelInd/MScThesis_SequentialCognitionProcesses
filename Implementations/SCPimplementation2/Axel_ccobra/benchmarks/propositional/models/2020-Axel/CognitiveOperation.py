# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 11:43:35 2020

@author: Axel
"""
import basicLogic
import copy

class CognitiveOperation(object):
    def __init__(self,name):
        self.name=name
        self.inputStructuralRequirements=[]
        self.outputStructure=[]
    def evaluateEpistemicState(self, epi):
        pass
    def precondition(self, epi):
        print ("Checking preconditions")
    def __str__(self):
        return self.name
    


    @staticmethod
    def getBodiesWhichShareHead (head, S):
        bodies = []
        for rule in S:
            #for <-
            lrImplication = isinstance (rule,basicLogic.operator_bitonic_implication)
            bijection = isinstance (rule,basicLogic.operator_bitonic_bijection)
            if  (lrImplication or bijection) and rule.clause1 == head:
                bodies.append(rule.clause2)
            if  (bijection) and rule.clause2 == head:
                bodies.append(rule.clause1)
        return bodies
class m_addAB (CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="addAB")
        self.inputStructuralRequirements=['Delta']
        self.outputStructure=['S','Delta']
    @staticmethod
    def findLowestK(epi):
        #the lowest number for which ab_1 does not exist
        lowest_k = None
        
        k=1
        while lowest_k == None:
            #all atomic names that appear in these structural variables
            ats = epi.getAtomNamesInStructuralVariables(['S','Delta','V'])
            candidateAbnormality = 'ab_'+str(k)
            if candidateAbnormality not in ats:
                lowest_k = k
            k=k+1
        return lowest_k
    @staticmethod
    def findAllConditionalDependencyPreconditions(consequence, delta):
        bodies = []
        for d in delta:
            if d.clause1 == consequence:
                bodies.append(d.clause2)
        return bodies
    def evaluateEpistemicState(self,epi):
        #set of conditional rules
        delta = epi['Delta']
        S = epi['S']
        V = epi['V']
        
        resolvedDependencies=[]
        for conditional in delta:
            consequence = conditional.clause1
            precondition = conditional.clause2
            if consequence not in resolvedDependencies:
                lowestk = m_addAB.findLowestK(epi)
                allDependencies = m_addAB.findAllConditionalDependencyPreconditions(consequence,delta)
                abBody = None
                for dep in allDependencies:
                    negateDep = basicLogic.operator_monotonic_negation(dep)
                    if dep!=precondition:
                        if abBody == None:
                            abBody = negateDep
                        else:
                            abBody = basicLogic.operator_bitonic_or(abBody, negateDep)
                if abBody == None:
                    abBody = basicLogic.FALSE
                abName='ab_'+str(lowestk)
                abAtom = basicLogic.atom(abName,None)
                ab = basicLogic.operator_bitonic_implication(abAtom, abBody)
                
                negABAtom = basicLogic.operator_monotonic_negation(abAtom)
                
                newBody = basicLogic.operator_bitonic_and(precondition, negABAtom)
                newRule = basicLogic.operator_bitonic_implication(consequence, newBody)
                #add the abnormality and its assignment to the list of rules
                S.append(newRule)
                S.append(ab)
                V.append(abAtom)
            resolvedDependencies=resolvedDependencies+allDependencies
        #all conditionals have now been interpreted
        epi['Delta']=[]
        
        return epi
                
                
class m_wc (CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="wc")
        self.inputStructuralRequirements=['S']
        self.outputStructure=['S']        

    @staticmethod
    def disjunctionOfClauses(clauses):
        disjunction=[]
        
        for clause in clauses:
            if disjunction==[]:
                disjunction=clause
            else:
                disjunction = basicLogic.operator_bitonic_or(disjunction, clause)
        return disjunction
    def evaluateEpistemicState(self,epi):
        S = epi['S']
        # replace all clauses pointing to the same head with their conjunction
        # heads must be atomic so just get the list of all atoms in S
        # replace <- with <->
        # can be done in this one step
        atoms = epi.getAtomsInStructuralVariables(['S'])
        newS=[]
        handledHeads=[]
        for rule in S:
            head = rule.clause1
            if head not in handledHeads or head not in atoms:
                bodieswhichsharehead=CognitiveOperation.getBodiesWhichShareHead(head, S)
                disjunctionOfBodies=m_wc.disjunctionOfClauses(bodieswhichsharehead)
                newRule = basicLogic.operator_bitonic_bijection(head, disjunctionOfBodies)
                newS.append(newRule)
                handledHeads.append(head)
            else:
                pass
        
        epi['S']=newS
        
        #step 1, find all 
        return epi
        

class m_semantic (CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="semantic")
        self.inputStructuralRequirements=['S','V']
        self.outputStructure=['S','V']
    @staticmethod    
    def changeAssignmentInV(atomName, Value, V):
        for atom in V:
            if atom.getName()==atomName:
                atom.setValue(Value)
    @staticmethod
    def setTruth(epi):
        #I_V(S)
        S = epi['S']
        V = epi['V']
        
        
        ats = epi.getAtomNamesInStructuralVariables(['S'])
        #Assign TRUTH in possible world
        for rule in S:
            #clear the interpretation
            basicLogic.setkbfromv(epi['S'], V)
            
            left = rule.clause1
            right = rule.clause2
            if left.getName() in ats:
                evaluation = right.evaluate()
                if evaluation==True:
                    m_semantic.changeAssignmentInV(left.getName(), evaluation, V)  
            left = rule.clause2
            right = rule.clause1
            if left.getName() in ats:
                evaluation = right.evaluate()
                if evaluation==True:
                    m_semantic.changeAssignmentInV(left.getName(), evaluation, V)  
                    
        return epi
                    
    #There exists A<- body and FOR ALL clauses A <- body we find I_V(body)=False   
    # currently NOT NONMONOTONIC! @TODOfix!
    # will currently only converge to one least model!
    # possible solution, run for each possible reordering of the rules
    @staticmethod
    def setFalse(epi):
        #I_V(S)
        S = epi['S']
        V = epi['V']
        
        
        ats = epi.getAtomNamesInStructuralVariables(['S'])
        #Assign TRUTH in possible world
        for rule in S:
            #clear the interpretation
            epi['S']=basicLogic.setkbfromv(epi['S'], V)
            
            left = rule.clause1
            right = rule.clause2
            if left.getName() in ats:
                evaluation = right.evaluate()
                if evaluation==False:
                    shared = CognitiveOperation.getBodiesWhichShareHead(left, epi['S'])
                    allFalse=True
                    for body in shared:
                        if body.evaluate() != False:
                            allFalse=False
                    if allFalse:
                        m_semantic.changeAssignmentInV(left.getName(), evaluation, V) 
                     
            left = rule.clause2
            right = rule.clause1
            if left.getName() in ats:
                evaluation = right.evaluate()
                if evaluation==False:
                    shared = CognitiveOperation.getBodiesWhichShareHead(left, epi['S'])
                    allFalse=True
                    for body in shared:
                        if body.evaluate() != False:
                            allFalse=False
                    if allFalse:
                        m_semantic.changeAssignmentInV(left.getName(), evaluation, V) 
                    
        return epi
                    
                            
    def evaluateEpistemicState(self,epi):
        originalS = copy.deepcopy(epi['S'])
        originalV = copy.deepcopy(epi['V'])
        
        prevV = None
        currentV = originalV
        while currentV != prevV:
            prevV = copy.deepcopy(currentV)
            
            m_semantic.setTruth(epi)
        
            m_semantic.setFalse(epi)
            currentV=copy.deepcopy(epi['V'])
        epi['S']=originalS
        return epi
    

from itertools import combinations
class m_addAbducibles(CognitiveOperation):
    def __init__(self,abducibles, maxLength=9999):
        CognitiveOperation.__init__(self,name="addAbducibles:"+str(abducibles))
        self.abducibles=abducibles
        self.maxLength=maxLength
        self.inputStructuralRequirements=['S']
        self.outputStructure=['S']
    def evaluateEpistemicState(self,epi):
        nextEpis=[]
        #find only as many abducibles as the max length allows
        for i in range(0, min(len(self.abducibles)+1,self.maxLength)):  
            perm = combinations(self.abducibles,i)

            for j in list(perm): 
                newEpi = copy.deepcopy(epi)
                newEpi['R']={'abducibles':list(j)}
                newEpi['S']=newEpi['S']+list(j)
                        
                nextEpis.append(newEpi)
        return nextEpis        
    




       
       