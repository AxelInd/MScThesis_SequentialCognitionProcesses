# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 11:28:31 2020

THE SCP CLASS

AN SCP (SEQUENTIAL COGNITION PROCESS) IS A LINKED LIST OF COMPLEX OPERATIONS. EACH SCP BEGINS WITH AN
INITIAL STATE. NO OTHER SCP EXPLICITLY STORES KNOWLEDGE ABOUT THE KNOWLEDGE BASE OR VARIABLES ON WHICH IS WORKS.

Instead, they rely on calls to their predecessors to be passed that information. The complex actions of an SCP
are only bounded by the creativity of the researcher, and the relevence of their ideas to modelling the problem at hand.
This SCP implementation focuses on the WEAK COMPLETION SEMANTICS.

@author: Axel
"""


import basicLogic

import copy
SETVAL = True
class scp (object):
    
    def __init__ (self):
        
        self.M = []
        self.initialKB = []
        self.initialV = []
        self.state1 = complexOperation_init ()
        self.state1.kb = self.initialKB
        self.state1.v = self.initialV
        self.lastState = self.getLastState


    
    #@TODO needs to be implemented
    def checkPrecondition ():
        print ("Checking precondition")


    
    def setState1 (self, state):
        """
        state = copy.deepcopy(state)
        self.state1 = state
        self.lastState = state
        """
        self.insertAtPos(state,0)
        self.state1.kb=self.initialKB
        self.state1.v=self.initialV

    def addM (self, M):
        for m in M:
            self.addComplexOperation(m)

        
    def addKnowledge (self, knowledge):
        if knowledge==None:
            return False
        
        newKnowledge = copy.copy(knowledge)
        self.initialKB.append(newKnowledge)
        return True
    def removeVariable_initial (self,varname):
        newVars = []
        for var in self.initialV:
            if var.name!= varname:
                newVars.append(var)
        return newVars
    def addVariable (self, variable, overwrite=False):
        newVariable = copy.copy(variable)
        if not overwrite:
            for v in self.initialV:
                #prevents adding duplicate variables (at the start at least)
                if v.name == newVariable.name:
                    return False
        else:
            self.initialV=self.removeVariable_initial(variable.name)
        self.initialV.append(newVariable)
        return True

    def evaluateV (self):
        if self.lastState == None:
            return []
        return self.getLastState().evaluatev()
    def evaluateKB (self):
        if self.getLastState() == None:
            return []
        return self.getLastState().evaluatekb()
    


    def getVariable (self, variableName):
        for v in self.initialV:
            if v.name==variableName:
                return v
        return None
    def existsVariable (self, variableName):
        return self.getVariable(variableName)==None
        

#==============================================================================
#=============================LINKED LIST OPERATIONS===========================
#==============================================================================
    def __len__(self):
        if self.state1==None:
            return 0
        i = 0
        node = self.state1
        while True:
            node = node.next
            i=i+1
            if (node==None):
                return i                
    def addComplexOperation (self, m):
        mcopy = copy.copy(m)
        self.M.append(mcopy)  
    def length (self):
        return self.__len__()
    def removeLast (self, lastname=None):
        if lastname==None or self.getLastState().name == lastname:
            if self.lastState!=self.state1:
                self.getLastState().prev.next=None
                return True
            return False
        return False
            
        
    def insertAtPos (self, m, pos):
        m=copy.deepcopy(m) 
        #CREATE NEW FIRST STATE
        if pos == 0:
            if self.state1!=None:
                m.next=self.state1
                if self.state1.next != None:
                    self.state1.next.prev=m
                    self.state1 = m
            else:
                self.state1=m
            return True
        #CYCLE TO THE DESIRED POSITON
        node = self.state1
        prev = None
        for i in range (0, pos):
            if node == None:
                return False
            prev=node
            node = node.next
        if node == None:
            m.prev=prev
            prev.next=m
            return True
            
        m.prev=node
        if node.next==None:
            node.next = m            
            return True
        else:
            m.next = node.next
            node.next.prev=m
            node.next=m
            return True
        return False  

    def addNext (self,nxt):
        self.insertAtPos(nxt,len(self))      
    def getLastState(self):
        node = self.state1
        if node == None:
            return None
        while node.next!=None:
            node = node.next
        return node        
#==============================================================================
#===============================OUTPUT FUNCTIONS===============================
#==============================================================================

    
    @staticmethod
    def strKnowledge(kb):
        k = u"{"
        for i in range (0, len(kb)):
            k = k + u"{}{}".format(kb[i],(", " if i<len(kb)-1 else "") )
        k=k+u"}"
        return k    
    @staticmethod    
    def strVariables(v):
        vs = "{"
        for i in range (0, len(v)):
            vs = u"{} {} : {} {}".format(vs, v[i], v[i].evaluate(), (", " if i<len(v)-1 else "") )
        vs=vs+"}"
        return vs
    def strInitialKB (self):
        return self.strKnowledge(copy.deepcopy(self.initialKB))
    def strInitialV (self):
        return self.strVariables(copy.deepcopy(self.initialV))  
    def strFinalV (self):
        return self.strVariables(self.getLastState().evaluatev())
    def strFinalKB (self):
        return self.strKnowledge(self.getLastState().evaluatekb())
    def __str__(self):
        s=""
        m = self.state1
        while m != None:
            s = s + m.name + (" >> " if m.next!= None else "")
            m = m.next
        return s
    def strDetailed (self):
        node = self.state1
        s = u''
        while node != None:
            s = s + (u'==={}===\n').format(node.name)
            s=s + u'{}\n'.format(node)
            node = node.next    
        return s
    
    

class complexOperation (object):
    def __init__(self, name=""):
        self.name = name
        self.next = None
        self.prev = None
        self.prev = None
    
    def addknowledge (self, knowledge):
        self.kb.append(knowledge)
    def addVariable (self, variable):
        self.v.append(variable)
        
    def act (self):
        print("I am acting")
    def setNext(self, nex):
        self.next=nex
        nex.prev = self
    def evaluatekb (self):
        print("I evaluate this specific KB")
    def evaluatev (self):
        print("I evaluate these specific variables")
    def setkbfromv (self, kb, v):
        for var in v:
            for rule in kb:
                rule.deepSet(var.name, var.value)
        return kb
    
    @staticmethod        
    def strKnowledge(kb):
        k = "{"
        if kb == None:
            return "{}"
        for i in range (0, len(kb)):
            k = u'{} {} {}'.format(k, kb[i], (", " if i<len(kb)-1 else "") )
        k=k+"}"
        return k
    def strKnowledge_self(self):
        return complexOperation.strKnowledge(self.evaluatekb())  
    
    @staticmethod    
    def strVariables(v):
        vs = "{"
        if v == None:
            return "{}"
        for i in range (0, len(v)):
            vs = vs + u"{} : {}{}".format(v[i],v[i].evaluate(),(", " if i<len(v)-1 else "") )
        vs=vs+"}"
        return vs
    
    def __str__(self):
        outputkb  =self.evaluatekb()
        outputv = self.evaluatev()
        
        inputkb = (self.prev.evaluatekb() if self.prev!=None else None)
        inputv = (self.prev.evaluatev() if self.prev!=None else None)
        
        s = ("-"*10) + "\n"
        s = s + ("-"*5) + "\n"
        s = s + ">>>Input" + "\n"
        s = s + self.name + "\n"
        s = s + "KB = " + complexOperation.strKnowledge(inputkb) + "\n"
        s = s + "V = " + complexOperation.strVariables(inputv) + "\n"
        
        s = s + ("-"*10) + "\n"
        s = s + ("-"*5) + "\n"
        s = s + ">>>Output" + "\n"
        s = s + self.name + "\n"
        s = s + "KB = " + complexOperation.strKnowledge(outputkb) + "\n"
        s = s + "V = " + complexOperation.strVariables(outputv) + "\n"
        s = s + ("-"*10) + "\n"
        
        return s
    
    def initKBfromPrevOperation (self):
        self.kb = self.prev.evaluatekb()
    def initVfromPrevOperation (self):
        self.v = self.prev.evaluatev()    
    
class complexOperation_init (complexOperation):
    def __init__ (self):
        complexOperation.__init__(self, "init")
    def evaluatekb (self):
        return copy.deepcopy(self.kb)
    def evaluatev (self):
        return copy.deepcopy(self.v)
    
    def initKBfromPrevOperation (self):
        print ("initKBfromPrevOperation is not definited for init")
    def initVfromPrevOperation (self):
        print ("initVfromPrevOperation is not definited for init")

class complexOperation_addAB (complexOperation):
    def __init__ (self):
        complexOperation.__init__(self, "addAB")

    def trueEvaluation (self):
        tempABs = []
        kb2 = []
        usedatoms = []
        kb = self.prev.evaluatekb()
        for i in kb:
            if isinstance(i,basicLogic.operator_bitonic_implication ):
                #atom in head
                if isinstance(i.clause2, basicLogic.atom ) and not i.immutable:
                    #check that it is not a ground truth value
                    #abnormality needs to be added
                    if not basicLogic.isGroundAtom(i.clause1):
                        if len(usedatoms)==0 or not i.clause1 in usedatoms[0]:
                            # Note that this atom/clause has an attached abnormality
                            usedatoms.append([i.clause1,i.clause2])
                            newAbnormality = basicLogic.atom("ab"+str(len(usedatoms)))
                            negativeAbnormality = basicLogic.operator_monotonic_negation(newAbnormality)
                            newclause = basicLogic.operator_bitonic_and(i.clause1, negativeAbnormality)
                            newClauseWithAbnormality = basicLogic.operator_bitonic_implication(newclause, i.clause2)
                            kb2.append(newClauseWithAbnormality)
                            #used for the evlauatev()
                            tempABs.append(newAbnormality)
                            
                        else:
                            kb2.append (i)
                    #No abnormality needs to be added
                    else:
                        kb2.append(i)
                else:
                    kb2.append(i)  
                    
        #add the rule for the abnormality
        #this adds the appropriate abnormality assignments to the kb
        #This loop handles cases where multiple non-ground clauses can affect the same head
        for pos in range (0, len(usedatoms)):
            for pos2 in range (0, len(usedatoms)):
                #they share a head
                if usedatoms[pos2][1] == usedatoms[pos][1]:
                    #the bodies are different
                    if not usedatoms[pos2][0] == usedatoms[pos][0]:
                        abnormality =  basicLogic.atom("ab"+str(pos+1))
                        negatom = basicLogic.operator_monotonic_negation(usedatoms[pos2][0])
                        newclause = basicLogic.operator_bitonic_implication(negatom, abnormality)   
                        kb2.append(newclause)
            terminate = False
            #This loop handles cases where only one non-ground clause affects a head
            for atom in usedatoms:
                for atom2 in usedatoms:
                    if atom != atom2 and atom[1]==atom2[1]:
                        terminate=True
                if not terminate:
                    abnormality =  basicLogic.atom("ab"+str(pos+1))    
                    newclause = basicLogic.operator_bitonic_implication(basicLogic.FALSE, abnormality)  
                    kb2.append(newclause)
                        
        
        return kb2, tempABs
        
    # kb is extended with abnormalities
    # add abnormality to non-ground rules
    # introduce truth value for ab to kb   
    def evaluatekb (self):
        trueEval = self.trueEvaluation()
        return trueEval[0]

    # v values are extended by this operation @TODO
    # self.tempABs requires evaluatekb to be called first (@TODO FIX THIS)
    def evaluatev (self):
        trueEval = self.trueEvaluation()
        tempABs = trueEval[1]
        v = self.prev.evaluatev()
        for i in tempABs:
            v.append(i)        
        return v   
        
        
class complexOperation_weaklyComplete (complexOperation):
    def __init__ (self):
        complexOperation.__init__(self, "weaklyComplete")
        
    def evaluatekb (self):
        
        oldkb = self.prev.evaluatekb()
        newKB = []
        
        #find duplicate heads
        #assumes kb is in terms of rules
        for pos in range (0, len(oldkb)):
            if isinstance (oldkb[0], basicLogic.operator_bitonic_implication):
                head = oldkb[pos].clause2
                bodies=[]
                for i in range (pos, len(oldkb)):
                    if (head==oldkb[i].clause2):
                        bodies.append(oldkb[i].clause1)
                body = bodies[0]
                    
                for nbody in bodies:
                    if body!=nbody and not isinstance(nbody, basicLogic.atom_truth):
                        body = basicLogic.operator_bitonic_or(clause1=body,clause2=nbody)
                newKB.append(basicLogic.operator_bitonic_bijection(body, head))
                            
                        
        return newKB
    
    def evaluatev (self):
        return self.prev.evaluatev()


class Error(Exception):
   """Base class for other exceptions"""
   pass
class NotBijectionError(Error):
   """Raised when the input value is too small"""
   pass

                
class complexOperation_semanticOperator (complexOperation):
    def __init__ (self):
        complexOperation.__init__(self, "semanticOperator")
        
    def evaluatekb (self):
        return self.prev.evaluatekb()

    
    
    

    #@TODO fix, doesn't do FOR ALL CALUSES A <- body I(body) = false
    def isBijection(self,rule):
        return isinstance (rule, basicLogic.operator_bitonic_bijection)
    def evalClause (self, clause):
        if clause.evaluate() == False or isinstance(clause, basicLogic.atom_false):
            return False
        elif clause.evaluate() == True or isinstance(clause, basicLogic.atom_truth):
            return True
        return None
    def initGroundAtoms(self, kb, v):
        #check that every rule is of a valid format
        for rule in kb:
            if not self.isBijection(rule):
                raise NotBijectionError
                
        #test false
        for rule in kb:
            head = rule.clause2
            body = rule.clause1
            if self.evalClause(body)==False:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (False)
        for rule in kb:
            head = rule.clause1
            body = rule.clause2
            if self.evalClause(body)==False:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (False)            
        #test unknown
        for rule in kb:
            head = rule.clause2
            body = rule.clause1
            if self.evalClause(body)==None:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (None)
        for rule in kb:
            head = rule.clause2
            body = rule.clause1
            if self.evalClause(body)==None:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (None)

           
        #test true
        for rule in kb:
            head = rule.clause2
            body = rule.clause1
            if self.evalClause(body)==True:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (True)
                            
        for rule in kb:
            head = rule.clause1
            body = rule.clause2
            if self.evalClause(body)==True:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (True)   
        return v
        
    def evaluatev (self):
        #@TODO THIS MUST BE FIXED
        kb = self.prev.evaluatekb()
        newV = self.prev.evaluatev()
        tempkb = self.setkbfromv(kb,newV)
        newV = self.initGroundAtoms(tempkb, newV)
        return newV



class complexOperation_deleteVariable (complexOperation):
    def __init__ (self, variableName):
        complexOperation.__init__(self, "deleteVariable" + str(variableName))
        self.toDelete = variableName
    
    def evaluatev (self):
        oldv = self.prev.evaluatev()
        newv = []
        for old in oldv:
            if not old.name == self.toDelete:
                newv.append(old)
        return newv

    def toDeleteIsHead (self, rule):
        if rule.clause2.name == self.toDelete:
            return True
        return False
    def toDeleteIsBody (self, rule):
        if rule.clause1.name == self.toDelete:
            return True
        return False
    
    #@TODO must be extended for more cases
    def evaluatekb (self):
        oldkb =  self.prev.evaluatekb()
        newkb =[]
        for old in oldkb:
            if isinstance(old, basicLogic.operator_bitonic_implication):
                if not self.toDeleteIsBody(old) and not self.toDeleteIsHead(old):
                    newkb.append(old)      
        return newkb
    
class complexOperation_fixVariable (complexOperation):
    def __init__ (self, variableName, value):
        complexOperation.__init__(self, "fixVariable" + str(variableName))
        self.toFix = variableName
        self.fixValue = value
        
    def evaluatekb (self):
        return self.prev.evaluatekb()
    def evaluatev (self):
        oldV = self.prev.evaluatev()
        for v in oldV:
            if v.name == self.toFix:
                v.setValue(self.fixValue)
                v.fixed=True
        return oldV
        
#==============================================================================

class complexOperation_modusTolens (complexOperation):
    def __init__ (self):
        complexOperation.__init__(self, "Modus Tolens")
        
    def evaluatekb (self):
        oldkb = self.prev.evaluatekb()
        newkb = copy.deepcopy(oldkb)
        for rule in oldkb:
            if isinstance(rule.clause2, basicLogic.atom) and not basicLogic.isGroundAtom(rule.clause2):
                negateClause1 = basicLogic.operator_monotonic_negation(rule.clause1)
                negateClause2 = basicLogic.operator_monotonic_negation(rule.clause2)
                contraRule = basicLogic.operator_bitonic_implication(negateClause1, negateClause2)
                newkb.append(contraRule)
            #print u"{}".format(rule.clause2)
        return newkb
    def evaluatev (self):
        return self.prev.evaluatev()
    
class scp_evaluator (object):
    @staticmethod
    def addMissingVariables (_scp, externalVariables):
        externalVariables=copy.deepcopy(externalVariables)
        scpVariables = _scp.evaluateV()
        #if we are using the _scps variable assignments to begin with, it cannot mismatch with itself
        if externalVariables==None:
            return scpVariables
        
        for v_scp in scpVariables:
            seen = False
            for v_ex in externalVariables:
                if v_scp.name == v_ex.name:
                    seen = True
            if not seen:
                varToAdd = basicLogic.atom(v_scp.name, None)
                externalVariables.append(varToAdd)
        return externalVariables
        


    @staticmethod
    def ruleMatch (_scp, externalVariables=None):
        kb = _scp.evaluateKB()
        
        kb = scp_evaluator.setkbfromv(kb,externalVariables)
        print "External Variables are {}".format(complexOperation.strVariables(externalVariables))
        for rule in kb:
            tRule = copy.deepcopy(rule)
            print u"evaluating{} to {}".format(tRule, tRule.evaluate())
            if tRule.evaluate()!=True:
                return False
        return True
            
    
    @staticmethod     
    def setkbfromv (kb, v):
        for var in v:
            for rule in kb:
                rule.deepSet(var.name, var.value)
        return kb
                

    @staticmethod  
    def incrA (a, start=0):
        poss=[]
        if start>=len(a):
            return [a]
        
        a=copy.deepcopy(a)
        a[start]=None
        poss = poss + scp_evaluator.incrA(a, start+1)
        
        a=copy.deepcopy(a)
        a[start]=True
        poss = poss + scp_evaluator.incrA(a, start+1)
        
        a=copy.deepcopy(a)
        a[start]=False
        poss = poss + scp_evaluator.incrA(a, start+1)
        return poss


    @staticmethod
    def getAbducibleNames (_scp):
        
        abducibles = []
        unabducibles = []
        variables = _scp.evaluateV()
        print "Variables are"
        for v in variables:
            if v.value==None:
                v_n = basicLogic.atom(v.name, v.value)
                abducibles.append(v_n)
            else:
                v_n = basicLogic.atom(v.name, v.value)
                unabducibles.append(v_n)                
        return abducibles, unabducibles
    
    @staticmethod    
    def getLeastModel (initialSCP):
        solutions=[]
        abducibles, unabducibles = scp_evaluator.getAbducibleNames(initialSCP)
        
        values = [None]*len(abducibles)
        possibleValues = scp_evaluator.incrA(values)
        
        for v in possibleValues:
            for v2 in v:
                print v
        for val in possibleValues:
            _scp = copy.deepcopy(initialSCP)
            newVariables = []
            for v in range (0, len(abducibles)):
                if val[v]!=None:
                    newVar = basicLogic.atom(abducibles[v].name, val[v])
                    newVariables.append(newVar)
                    
            #print u"evaluating {}".format(_scp.strFinalKB())
            
            
            for i in unabducibles:
                newVariables.append(i)
            #print u"using {}".format(_scp.strVariables(newVariables))            
            match = scp_evaluator.ruleMatch(_scp,newVariables)
            #print "Rule match : {}".format(match)
            if match:
                solutions.append(newVariables)
        return solutions
        
        # we want to find cases where lm wc P (F) = True
        
    @staticmethod
    def leastModelFormat(variables):
        _true=[]
        _false=[]
        
        for v in variables:
            if (v.value == True):
                _true.append(v)
            elif (v.value==False):
                _false.append(v)
        return (_true, _false)        
    @staticmethod
    def strLeastModel (_scp):
        least_raw = scp_evaluator.getLeastModel(_scp)

        s = u""
        for i in least_raw:
            least = scp_evaluator.leastModelFormat(i)            
            s=s+u"{"+scp_evaluator.strLeastModel_single(least)+"}\n"
        return s
            
    @staticmethod
    def strLeastModel_single (least):
        t=""
        f=""
        _true = [str(i) for i in least[0]]
        for i in range (0, len(_true)):
            t="{}{}{}".format(t,_true[i], "," if i<len(_true)-1 else "")            
        _false = [str(i) for i in least[1]]
        for i in range (0, len(_false)):
            f="{}{}{}".format(f,_false[i], "," if i<len(_false)-1 else "") 
        s = u"True=({}), False=({})".format(t,f)
        return s         



























