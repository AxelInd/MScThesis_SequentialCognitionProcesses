# -*- coding: utf-8 -*-
"""
Created on Mon Feb 03 11:58:07 2020

THE INDIVIDUAL COMPONENTS OF THE SCP

Each complex operation is pipeline of information. They all take information about
an epistemic state (rules, and actual variable assignments) and transform it according
to the purpose of the operation. However, the output of a complexOperation is ALWAYS
readable by another complex operation which uses it as input.

Together complex operations are a linear linked pipeline of transformations on
the initial epistemic state.
@author: Axel
"""

import copy
#used to create atoms and rules
import basicLogic
#used to throw exceptions for improper use
import scpError

import epistemicState

import helperFunctions

class complexOperation (object):
    """
    CREATE A COMPLEX OPERATION
    @param name: the new name for the complex operation (does not need to be unique)
    """
    def __init__(self, name=""):
        self.name = name
        #the complex operation that uses the output of this one as its input
        self.next = None
        #the complex operation whose output is the input to this complex operation
        self.prev = None
    def evaluate(self):
        raise scpError.notImplementedError_AbstractClass

    """
    REPRESENT THIS COMPLEX OPERATION'S OUTPUT RULES AS A STRING
    @return the rules as a human-readable string
    """
    def strKnowledge_self(self):
        return complexOperation.strKnowledge(self.evaluatekb())  

    """
    REPRESENT THIS COMPLEX OPERATION'S OUTPUT VARIABLES AS A STRING
    @return the variables as a human-readable string
    """
    def strVariables_self(self):
        return complexOperation.strKnowledge(self.evaluatev())
    #this method requires that the truth value of all variables with name x be identical
    @staticmethod
    def getHeads (kb):
        heads=[]
        for rule in kb:
            if isinstance (rule, basicLogic.operator_bitonic_implication):
                heads.append(rule.clause2)
            elif isinstance (rule, basicLogic.operator_bitonic_bijection):
                heads.append(rule.clause2)
                heads.append(rule.clause1)
        return list(dict.fromkeys(heads)) 
    
    """
    REPRESENT THIS COMPLEX OPERATION AS A STRING IN TERMS OF INPUT AND OUTPUT
    @return The name of operation as well as the (KB,V) values for both input and output
    """
    def __str__(self):
        
        epi_input = (self.prev.evaluate() if self.prev!=None else None)
        epi_output = self.evaluate()
        
        #input
        s = "{}\n{}\n>>>Input: {}\n".format(("-"*10),("-"*5), self.name)
        s = s + u"{}\n".format(epi_input)
        
        #output
        s = s+"{}\n>>>Output: {}\n".format(("-"*5), self.name)
        s = s + u"{}\n".format(epi_output)
        
        s = s + "{}\n".format("-"*10)  
        return s 
    
    @staticmethod
    def createEmptyNextEpi(prevEpi):
        if isinstance (prevEpi, epistemicState.epistemicState_weakCompletion):
            return epistemicState.epistemicState_weakCompletion()
        elif isinstance (prevEpi, epistemicState.epistemicState_defeaultReasoning):
            return epistemicState.epistemicState_defeaultReasoning()
        raise scpError.invalidEpistemicStateError
            
"""
THE INIT COMPLEX OPERATIONS IS ASSUMED TO BE THE FIRST STEP OF EVERY SCP
The complexOperation_init holds pointers to epistemic information from the initial state of the scp.
There should be only one init operation per scp
The init operation is the only complex operation with no prev node
"""
class complexOperation_init (complexOperation):
    """
    CREATE AN INSTANCE OF complexOperation_init
    """
    def __init__ (self):
        complexOperation.__init__(self, "init")
        self.epi_state=[]
    def evaluate(self):
        return self.getEpistemicState()
    def setEpistemicState (self, epi):
        self.epi_state=epi
    def getEpistemicState (self):
        return self.epi_state
    
class complexOperation_default (complexOperation):
    def __init__(self, name="defaultOp"):
        complexOperation.__init__(self,name)
class complexOperation_default_drawConclusions (complexOperation_default):
    def __init__(self):
        complexOperation_default.__init__(self,name="drawConcDefault")
    #@TODO should return a list of epistemic states corresponding to each possible world
    #@TODO this should run until convergence (in this case only variable assignments change)
    def evaluate(self, hastyDerive=False):
        epi_prev = self.prev.evaluate()
        epi_next = copy.deepcopy(epi_prev)
        
        prevV = epi_prev.getV()
        complexOperation_default_drawConclusions.evaluateW(epi_next)
        #@TODO we are still not doing anything with this list of epis
        possibleEpis = complexOperation_default_drawConclusions.evaluateD(epi_next,hastyDerive)
        currentV = epi_next.getV()
        
        while not basicLogic.compareVariableLists(prevV,currentV):
            prevV = epi_next.getV()
            complexOperation_default_drawConclusions.evaluateW(epi_next)
            #@TODO
            possibleEpis = complexOperation_default_drawConclusions.evaluateD(epi_next,hastyDerive) 
            currentV = epi_next.getV()
        print ("POSSIBLE EPIS ARE\n",possibleEpis)
        print ("--------------------------------ttt------------")
        return epi_next
    # W introducing no branching factor and so only returns one epistemic state
    @staticmethod
    def evaluateW(epi_next):
        prev  = []
        epi_w = epi_next.getW()
        current = complexOperation_default_drawConclusions.oneStepDeriveFromW(epi_w)
        #all variables with derivable values
        newVariables = complexOperation_default_drawConclusions.getVariablesFromThW(current)
        
        while not complexOperation_default_drawConclusions.compareCurrentToPrev(current,prev):
            prev = copy.deepcopy(current)
            current=complexOperation_default_drawConclusions.oneStepDeriveFromW(epi_w)
            newVariables = complexOperation_default_drawConclusions.getVariablesFromThW(current)

            for c in current:
                print ("---{}".format(c))
            for v in newVariables:
                for c in current:
                    c[0].deepSet(v.getName(), v.getValue())
        print (newVariables)
        derivedRules = [i[0] for i in current]
        print ("derived rules are",derivedRules)
        epi_next.addVList(newVariables)
        return epi_next
    @staticmethod
    def evaluateD(epi_next, hastyDerive=True):
        if hastyDerive:
            return [complexOperation_default_drawConclusions.evaluateD_hasty(epi_next)]
        else:
            return complexOperation_default_drawConclusions.evaluateD_full(epi_next)
    @staticmethod
    def checkEpiInList_checkV (epi,li):
        for e in li:
            if basicLogic.compareVariableLists(epi.getV(),e.getV()):
                return True
        return False
    @staticmethod
    def evaluateD_full(epi_next):        
        #generate every possible sequence of default rules
        values = epi_next.getD()
        allAss = helperFunctions.generateAllPossibleVariableAssigmentsFromV(values, logicRep=[True,False])
        uniqueEpis=[]
        for D in allAss:
            epi = copy.deepcopy(epi_next)
            epi.emptyD()
            for pos in range (0, len(D)):

                if D[pos]==True:
                    epi.addD(values[pos])
            #evaluate the epi in terms of the now limitted rules
            complexOperation_default_drawConclusions.evaluateD_hasty(epi)
            print ("=============================")
            print (epi)
            if not complexOperation_default_drawConclusions.checkEpiInList_checkV(epi, uniqueEpis):
                uniqueEpis.append(epi)
                print ("appended")
        return uniqueEpis

    @staticmethod
    def evaluateD_hasty(epi_next):
        d=epi_next.getD()
        v=epi_next.getV()
        derivs = []
        for defaultRule in d:
            #print ("Default rule is",defaultRule)
            #print ("This default rule evlauates to", defaultRule.evaluate(v))
            ruleEval = defaultRule.evaluate(v)
            if ruleEval==False:
                #nothing happens as this rule has been falsified
                #maybe it should be rmoved from the list of defeault rules?
                pass
            else:
                derivs.append((defaultRule.clause3,True))
        #print ("The following things have been derived:",derivs)
        newVariables = complexOperation_default_drawConclusions.getVariablesFromThW(derivs)
        epi_next.addVList(newVariables, overwrite=True)
        return epi_next  
    
    
    #@TODO this method is really simple and must be expanded for non-monotonic conclusions
    # that is, for cases where there are multiple possible resulting variable assignments
    @staticmethod
    def oneStepDeriveFromW(w):
        v=[]
        for rule in w:
            if isinstance(rule, basicLogic.operator_bitonic_implication):
                ce1 = rule.clause1.evaluate()
                ce2 = rule.clause2.evaluate()
                #print ("Clause 1 :{} = {}  --- Clause 2 :{} = {}".format(rule.clause1,ce1,rule.clause2,ce2))
                if ce1!=None:
                    v.append((rule.clause2,ce1))
            if isinstance(rule, basicLogic.operator_bitonic_bijection):
                ce1 = rule.clause1.evaluate()
                ce2 = rule.clause2.evaluate()
                if ce1!=None:
                    v.append((rule.clause2, ce1))
                if ce2!=None:
                    v.append((rule.clause1, ce2))
        return v

    @staticmethod
    def getVariablesFromThW(thW):
        v=[]
        for x in thW:
            if isinstance(x[0],basicLogic.atom):
                v.append(copy.deepcopy(x[0]))
                v[-1].setValue(x[1])
            elif isinstance(x[0],basicLogic.operator_monotonic_negation):
                v.append(copy.deepcopy(x[0].clause))
                doubleNeg = basicLogic.operator_monotonic_negation(basicLogic.atom('',x[1]))
                v[-1].setValue(doubleNeg.evaluate())
        return v
    @staticmethod
    def deepSetVInRules (v, rules):
        basicLogic.setkbfromv(rules,v)
    #@TODO does not compare rules, only atoms
    @staticmethod
    def compareCurrentToPrev (cur, prev):
        for c in cur:
            cFound=False
            if isinstance (c[0], basicLogic.atom):
                for p in prev:
                    if isinstance(p[0],basicLogic.atom):
                        if c[0]==p[0]:
                            cFound=True
            else:
                cFound = True
            if not cFound:
                return False
        return True

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
"""
A COMPLEX OPERATION WHICH ADDS ABNORMALITY VARIABLES TO THE EPISTEMIC STATE
The process her may differ according to the indiivdual needs of the researcher.
In this case, a simple rule is followed:
    "for every a -> b, if there exists no c -> b where c = (True, False, Unknown)
    then create a new abnormality ab_i and replace a -> b with a + ab_i -> b.
    Next, for every other rule a' with a' -> b, introduce not(a') -> ab_i
"""
class complexOperation_addAB (complexOperation):
    """
    CREATE AN INSTANCE OF A complexOperation_addAB OBJECT
    """
    def __init__ (self):
        complexOperation.__init__(self, "addAB")
    def getRulesThatAffectHead (self, head, kb):
        rulesThatAffectHead=[]
        for rule in kb:
            if isinstance (rule, basicLogic.operator_bitonic_implication):
                if rule.clause2.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause1)
            elif isinstance (rule, basicLogic.operator_bitonic_bijection):
                if rule.clause2.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause1)
                if rule.clause1.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause2)
        return rulesThatAffectHead
    
    def createBodyFromRulesThatAffectHead (self, head, body, li_abs):
        #if basicLogic.isGroundAtom(body):
        if basicLogic.isGroundAtom(body) or basicLogic.isGroundAtom(head):
            return basicLogic.operator_bitonic_implication(body, head), None, li_abs
        newAbnormality = basicLogic.atom('ab{}'.format(len(li_abs)+1))
        negAbnormality = basicLogic.operator_monotonic_negation(newAbnormality)
        li_abs.append(newAbnormality)    
        newBody = basicLogic.operator_bitonic_and(body, negAbnormality)
        newRule = basicLogic.operator_bitonic_implication(newBody, head)
        return newRule, newAbnormality, li_abs
    def removeRuleFromList (self, rule, li_rule):
        otherRules = []
        for r in li_rule:
            if r!=rule:
                otherRules.append(r)
        return otherRules
    def removeGroundFromRules (self,rules):
        newRules = []
        for rule in rules:
            if not basicLogic.isGroundAtom(rule):
                newRules.append(rule)
        return newRules
    def createNewAbnormalityInstant (self, ab, otherRulesThatAffectHead):
        # case: KB={D->3, T->3} without this (T -> ab) is created
        otherRulesThatAffectHead=self.removeGroundFromRules(otherRulesThatAffectHead)
        if otherRulesThatAffectHead==[]:
            rule = basicLogic.FALSE
            return rule    
        rule = otherRulesThatAffectHead[0] 
        for other in range (1,len(otherRulesThatAffectHead)):
            neg = basicLogic.operator_monotonic_negation(rule)
            rule = basicLogic.operator_bitonic_or(rule, neg)
        return rule
    def getHeads (self, rule):
        if isinstance(rule, basicLogic.operator_bitonic_bijection):
            return [rule.clause1, rule.clause2]
        if isinstance (rule, basicLogic.operator_bitonic_implication):
            return [rule.clause2]
        return []
    def getBodies (self, rule):
        if isinstance(rule, basicLogic.operator_bitonic_bijection):
            return [rule.clause1, rule.clause2]
        if isinstance (rule, basicLogic.operator_bitonic_implication):
            return [rule.clause1]
        return []        
    def evaluate(self):
        #get the previous epistemic state
        epi_prev = self.prev.evaluate()
        #generate an empy epistemic state of the same type as the previous one
        epi_next = complexOperation.createEmptyNextEpi(epi_prev)
        
        #all variables in prevkb will be present in the next one (plus abnormalities)
        prev_v = epi_prev.getV()
        epi_next.addVariableList(prev_v)
        
        #the list of created abnormalities
        ABs = []
        prev_kb = epi_prev.getKB()

        for rule in prev_kb:
            #we do this because there can be 1 or 2 heads/bodies depending on -> or <->
            body = self.getBodies(rule)
            head = self.getHeads(rule)
            if rule.immutable:
                epi_next.addKnowledge(rule)
            else:
                for h in head:
                    for b in body:
                        #truth values don't need abnormalities
                        if basicLogic.isGroundAtom(b):
                            newRule = basicLogic.operator_bitonic_implication(b,h)
                            epi_next.addKnowledge(newRule)
                        else:       
                            rulesThatAffectHead = self.getRulesThatAffectHead(h, prev_kb)
                            otherRulesThatAffectHead = self.removeRuleFromList(b, rulesThatAffectHead)
                            #create the new abnormality
                            newAb = basicLogic.atom("ab{}".format(len(ABs)+1))
                            ABs.append(newAb)
                            negAb = basicLogic.operator_monotonic_negation(newAb)
                            newBody = basicLogic.operator_bitonic_and(b,negAb)
                            newRule = basicLogic.operator_bitonic_implication(newBody,h)
                            epi_next.addKnowledge(newRule)
                            
                            #create a valuation for the new abnormality
                            abInstHead = newAb
                            abInstBody = self.createNewAbnormalityInstant(newAb, otherRulesThatAffectHead)
                            abInstBodyIsGroundValue = basicLogic.isGroundAtom(abInstBody)
                            newAbInstBody =  abInstBody if abInstBodyIsGroundValue else basicLogic.operator_monotonic_negation(abInstBody)
                            abInstRule = basicLogic.operator_bitonic_implication(newAbInstBody, abInstHead)
                            epi_next.addKnowledge(abInstRule)
                            
                            #add the new abnormality to the variable list
                            epi_next.addVariable(newAb) 
        return epi_next
        
        """
        
        epi_prev = self.prev.evaluate()
        epi_next=None
        if isinstance(epi_prev,epistemicState.epistemicState_weakCompletion):
            epi_next = epistemicState.epistemicState_weakCompletion()
        
        kb = epi_prev.getKB()
        li_abs = []

        for v in epi_prev.getV():
            epi_next.addVariable(v)
            
        for rule in kb:
            if isinstance(rule, basicLogic.operator_bitonic_implication):
                body = rule.clause1
                head = rule.clause2
                #includes body
                rulesThatAffectHead = self.getRulesThatAffectHead(head, kb)
                otherRulesThatAffectHead = self.getOtherRulesThatAffectHead(body, rulesThatAffectHead)
                if rule.immutable:
                    epi_next.addKnowledge(rule)
                else:
                    newRule, newAb, li_abs = self.createBodyFromRulesThatAffectHead(head, body, li_abs)
                    epi_next.addKnowledge(newRule)
                    newBody = self.createNewAbnormalityInstant(newAb, otherRulesThatAffectHead)
                    if newAb != None:             
                        abInst = basicLogic.operator_bitonic_implication(newBody, newAb)
                        epi_next.addKnowledge(abInst)
                        epi_next.addVariable(newAb)
        return epi_next
        """
        
"""
A COMPLEX OPERATION WHICH PERFORMS WEAK COMPLETION AS DEFINED BY @TODOref
1) replace a_1->x, ..., a_n->x with a_1 + ... + a_n ->x
2) replace all -> with <->
"""        
class complexOperation_weaklyComplete (complexOperation):
    """
    CREATE AN INSTANCE OF THE complexOperation_weaklyComplete CLASS
    """
    def __init__ (self):
        complexOperation.__init__(self, "weaklyComplete")

    def evaluate(self):
        prev_epi = self.prev.evaluate()
        epi_next=complexOperation.createEmptyNextEpi(prev_epi)
        tempKB = []
        
        old_v = prev_epi.getV()
        old_kb = prev_epi.getKB()


        
        uniqueHeads = complexOperation.getHeads(old_kb)
        for head in uniqueHeads:
            other = self.getRulesThatAffectHead(head, old_kb)
            disjunction = basicLogic.createOrFromAtomList(other)
            newRule = basicLogic.operator_bitonic_implication(disjunction,head)
            tempKB.append(newRule)
        #turn implications to bijections, slightly slower but much more reasable
        #than combining them in the same loop
        
        for rule in tempKB:
            if isinstance (rule, basicLogic.operator_bitonic_bijection):
                epi_next.addKnowledge(rule)
            if isinstance (rule, basicLogic.operator_bitonic_implication):
                body = rule.clause1
                head = rule.clause2
                newRule = basicLogic.operator_bitonic_bijection(body,head)
                epi_next.addKnowledge(newRule)
        """
        #ground rules remiain unchanged except that they become bijections
        groundRules = self.getGroundRules(old_kb)
        for rule in groundRules:
                body = rule.clause1
                head = rule.clause2
                newRule = basicLogic.operator_bitonic_bijection(body,head)  
                epi_next.addKnowledge(newRule)   
        """
        
        epi_next.addVariableList(old_v)
        return epi_next
        
    def getGroundRules (self, kb):
        ground = []
        for rule in kb:
            if isinstance(rule,basicLogic.operator_bitonic_implication):
                if basicLogic.isGroundAtom(rule.clause1):
                    ground.append(rule)
            if isinstance(rule, basicLogic.operator_bitonic_bijection):
                if basicLogic.isGroundAtom(rule.clause1):
                    ground.append(rule)
                if basicLogic.isGroundAtom(rule.clause2):
                    ground.append(rule)
        return ground
    
    def getRulesThatAffectHead (self, head, kb):
        rulesThatAffectHead=[]
        for rule in kb:
            if isinstance (rule, basicLogic.operator_bitonic_implication):
                if rule.clause2.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause1)
            elif isinstance (rule, basicLogic.operator_bitonic_bijection):
                if rule.clause2.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause1)
                if rule.clause1.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause2)
        return rulesThatAffectHead

"""
A COMPLEX OPERATION WHICH APPLIES THE SEMANTIC OPERATOR AS DESCRIBED IN @TODOref
T = {A|body->A exists with Interp(Body)=True}
F = {A|body->A exists and Interp(Body) is false in EVERY case}
"""
class complexOperation_semanticOperator (complexOperation):
    def __init__ (self):
        """
        CREATE AN INSTANCE OF THE complexOperation_semanticOperator CLASS
        """
        complexOperation.__init__(self, "semanticOperator")
        
    def evaluate(self):
        prev_epi = self.prev.evaluate()
        return self.semanticOperatorEpi(prev_epi)

    def semanticOperatorEpi (self, prev_epi):
        epi_next=complexOperation.createEmptyNextEpi(prev_epi)
        
        old_kb = prev_epi.getKB()
        old_v = prev_epi.getV()
        tempkb = basicLogic.setkbfromv(old_kb,old_v)
        newV = self.initGroundAtoms(tempkb, old_v)
        
        epi_next.addKnowledgeList(old_kb)
        epi_next.addVariableList(newV)
        return epi_next
        

    """
    DETERMINE IF THE OPERATOR IN QUESTION IS A BIJECTION
    return True if it is a bijection, False otherwise
    """
    @staticmethod
    def isBijection(rule):
        return isinstance (rule, basicLogic.operator_bitonic_bijection)
    """
    DETERMINE IF THE CLAUSE EVALUATES TO True/False/None.
    Note: does not use the values stored in V, only those of atoms in the rules
    which are usually unknown until set
    @param clause: the logical clause or atom to evaluate
    @return the logical evaluation of the clause
    """
    @staticmethod
    def evalClause (clause):
        if clause.evaluate() == False or isinstance(clause, basicLogic.atom_false):
            return False
        elif clause.evaluate() == True or isinstance(clause, basicLogic.atom_truth):
            return True
        return None
    """
    DETERMINE THE VALUE OF ATOMS BY FOLLOWING THE PROCEDURE OUTLINE IN THE DESCRIPTION
    OF complexOperation_semanticOperator
    The basic logic followed here is:
        1) set every atom that can be set to false first
        2) then set every atom that can be set to none
        3) then set every atom that can be set to true
    Doing this essentially masks the incorrect assignments from 1) using 2)
    @param kb: the knowledge base under consideration
    @param v: the set of variables being used
    @return the updated set of variables
    """
    @staticmethod
    def initGroundAtoms(kb, v):
        #check that every rule is of a valid format
        for rule in kb:
            if not complexOperation_semanticOperator.isBijection(rule):
                raise scpError.NotBijectionError
                
        #test false
        for rule in kb:
            head = rule.clause2
            body = rule.clause1
            if complexOperation_semanticOperator.evalClause(body)==False:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (False)
        for rule in kb:
            head = rule.clause1
            body = rule.clause2
            if complexOperation_semanticOperator.evalClause(body)==False:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (False)            
        #test unknown
        for rule in kb:
            head = rule.clause2
            body = rule.clause1
            if complexOperation_semanticOperator.evalClause(body)==None:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (None)
        for rule in kb:
            head = rule.clause2
            body = rule.clause1
            if complexOperation_semanticOperator.evalClause(body)==None:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (None)

           
        #test true
        for rule in kb:
            head = rule.clause2
            body = rule.clause1
            if complexOperation_semanticOperator.evalClause(body)==True:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (True)
                            
        for rule in kb:
            head = rule.clause1
            body = rule.clause2
            if complexOperation_semanticOperator.evalClause(body)==True:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (True)   
        return v

class complexOperation_semanticOperator_full (complexOperation_semanticOperator):
    """
    CREATE AN INSTANCE OF THE COMPLEX OPERATION VARIABLE
    """
    def __init__ (self):
        complexOperation.__init__(self, "semanticOperatorFull")
    def compareLists (self,li1, li2):
        if len(li1)!=len(li2):
            return False
        for i in li1:
            found = False
            for j in li2:
                
                if i.getName()==j.getName():
                    if i.getValue()==j.getValue():
                        found = True
            if not found:
                return False
        return True
    
    def evaluate (self):
        prev_epi=None
        current_epi=self.prev.evaluate()
        while prev_epi==None or not self.compareLists(prev_epi.getV(),current_epi.getV()):
            prev_epi=copy.deepcopy(current_epi)
            current_epi=self.semanticOperatorEpi(current_epi)
        return current_epi
        
        

"""
A COMPLEX OPERATION WHICH DELETES A NAMED VARIABLE FROM ALL SUBSEQUENT COMPLEX OPERATIONS
IN THE SCP
"""
class complexOperation_deleteVariable (complexOperation):
    """
    CREATE AN INSTANCE OF THE COMPLEX OPERATION VARIABLE
    @param variableName: the name of the variable to delete
    """
    def __init__ (self, variableName):
        complexOperation.__init__(self, "deleteVariable" + str(variableName))
        self.toDelete = variableName
    
    """
    IS THE VARIABLE TO DELETE THE HEAD OF THE RULE GIVEN?
    @param rule: implication or bijection rule x >> y
    @return y if y is the atom to delete
    """
    def toDeleteIsHead (self, rule):
        if not isinstance(rule, basicLogic.operator_bitonic):
            raise scpError.notBitonicOperatorError
        
        if rule.clause2.name == self.toDelete:
            return True
        return False
    """
    IS THE VARIABLE TO DELETE THE BODY OF THE GIVEN RULE?
    @param rule: implication or bijection rule x >> y  
    @return x if x is the atom to delete
    """
    def toDeleteIsBody (self, rule):
        if not isinstance(rule, basicLogic.operator_bitonic):
            raise scpError.notBitonicOperatorError
            
        if rule.clause1.name == self.toDelete:
            return True
        return False
    
    """
    IF NEITHER THE HEAD NOR THE BODY OF THE BOJECTION IS THE OPERATOR TO DELETE
    ADD THAT RULE TO THIS LIST OF RULES TO RETURN
    REMOVE THE VARIABLE FROM OUTPUT OF THIS COMPLEX ACTION
    @return v-(self.toDelete)
    @return all rules which do no have the variable to delete as a head
    """
    def evaluate(self):
        prev_epi = self.prev.evaluate()
        current_epi = complexOperation.createEmptyNextEpi(prev_epi)
        oldkb =  prev_epi.getKB()
        for old in oldkb:
            if isinstance(old, basicLogic.operator_bitonic_implication):
                if not self.toDeleteIsBody(old) and not self.toDeleteIsHead(old):
                    current_epi.addKnowledge(old)
            elif isinstance(old, basicLogic.operator_bitonic_bijection):
                if not self.toDeleteIsBody(old) and not self.toDeleteIsHead(old):
                    current_epi.addKnowledge(old)
                    
        oldv = prev_epi.getV()
        newv = []
        for old in oldv:
            if not old.name == self.toDelete:
                current_epi.addVariable(old)
        return current_epi        
"""
COMPLEX OPERATION THAT PREVENTS THE VALUE OF A VARIABLE FROM CHANGING IN SBUSEQUENT
COMPLEX OPERATIONS
"""
class complexOperation_fixVariable (complexOperation):
    """
    CREATE AN INSTANCE OF THE complexOperation_fixVariable CLASS
    @param variableName: the name of the variable to fix
    @param value: the value to which variableName must be fixed
    """
    def __init__ (self, variableName, value):

        complexOperation.__init__(self, "fixVariable" + str(variableName))
        self.toFix = variableName
        self.fixValue = value
    def evaluate(self):
        new_epi = copy.deepcopy(self.prev.evaluate())
        new_epi.setVariable(self.toFix, self.fixValue)
        new_epi.fixVariable(self.toFix, fixed=True)
        return new_epi
#==============================================================================
"""
COMPLEX OPERATION THAT ADDS MODUS TOLENS RULES TO THE KNOWLEDGE BASE
Modus Tolens: if a->b then not(b)->not(a)
"""
class complexOperation_modusTolens (complexOperation):
    """
    CREATE AN INSTANCE OF THE complexOperation_modusTolens CLASS
    """
    def __init__ (self):
        complexOperation.__init__(self, "Modus Tolens")
    
    def isAtom(self, rule):
        return isinstance (rule, basicLogic.atom)
    def isGroundAtom (self, rule):
        return basicLogic.isGroundAtom(rule)
    def evaluate(self):
        prev_epi = self.prev.evaluate()
        current_epi = complexOperation.createEmptyNextEpi(prev_epi)
        oldkb = prev_epi.getKB()
        oldV = prev_epi.getV()
        
        current_epi.addVariableList(oldV)
        current_epi.addKnowledgeList(oldkb)
        
        for rule in oldkb:
            if not rule.immutable:     
                if self.isAtom(rule.clause2) and not self.isGroundAtom(rule.clause2):
                        negateClause1 = basicLogic.operator_monotonic_negation(rule.clause1)
                        negateClause2 = basicLogic.operator_monotonic_negation(rule.clause2)
                        contraRule = basicLogic.operator_bitonic_implication(negateClause1, negateClause2)
                        current_epi.addKnowledge(contraRule)
                                        
        
        """
        newkb = current_epi.getKB()
        for rule in oldkb:
            if isinstance(rule.clause2, basicLogic.atom) and not basicLogic.isGroundAtom(rule.clause2):
                if not basicLogic.isGroundAtom(rule.clause1):
                    negateClause1 = basicLogic.operator_monotonic_negation(rule.clause1)
                    negateClause2 = basicLogic.operator_monotonic_negation(rule.clause2)
                    contraRule = basicLogic.operator_bitonic_implication(negateClause1, negateClause2)
                    newkb.append(contraRule)
            #print u"{}".format(rule.clause2)
        """
        return current_epi
    
    
    
    
    
    
    
 