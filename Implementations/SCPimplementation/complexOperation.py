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
    
    """
    USE THE PREVIOUS OPERATION'S OUTPUT RULES TO CALCULATE THE NEW OUTPUT RULES
    """
    def evaluatekb (self):
        raise scpError.notImplementedError_AbstractClass
    """
    USE THE PREVIOUS OPERATION'S OUTPUT VARIABLES TO CALCULATE THE NEW OUTPUT VARIABLES
    """        
    def evaluatev (self):
        raise scpError.notImplementedError_AbstractClass
    """
    INSTANTIATES THE VARIABLES IN kb WITH THE VALUES IN v
    @param kb: the knowledge base (list of rules)
    @param v: the variables (list of basicLogic.atom abjects)
    @return the kb with each atom in each rule set to the values in v
    """
    @staticmethod
    def setkbfromv (kb, v):
        for var in v:
            for rule in kb:
                rule.deepSet(var.name, var.value)
        return kb
    """
    REPRESENT A SET OF VARIABLES AS A UNICODE STRING
    @param v: the variables to represent
    @return the variables as a human-readable string
    """
    @staticmethod    
    def strVariables(v):
        vs = "{"
        if v == None:
            return "{}"
        for i in range (0, len(v)):
            vs = vs + u"{} : {}{}".format(v[i],v[i].evaluate(),(", " if i<len(v)-1 else "") )
        vs=vs+"}"
        return vs
    
    """
    REPRESENT A SET OF RULES AS A UNICODE STRING
    @param kb: the knowledge to represent
    @return the rules as a human-readable string
    """
    @staticmethod        
    def strKnowledge(kb):
        k = "{"
        if kb == None:
            return "{}"
        for i in range (0, len(kb)):
            k = u'{} {} {}'.format(k, kb[i], (", " if i<len(kb)-1 else "") )
        k=k+"}"
        return k
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
    """
    REPRESENT THIS COMPLEX OPERATION AS A STRING IN TERMS OF INPUT AND OUTPUT
    @return The name of operation as well as the (KB,V) values for both input and output
    """
    def __str__(self):
        inputkb = (self.prev.evaluatekb() if self.prev!=None else None)
        inputv = (self.prev.evaluatev() if self.prev!=None else None)
        
        outputkb  =self.evaluatekb()
        outputv = self.evaluatev()
        
        #input
        s = "{}\n{}\n>>>Input: {}\n".format(("-"*10),("-"*5), self.name)
        s = s + u"KB = {}\nV = {}\n".format(complexOperation.strKnowledge(inputkb),complexOperation.strVariables(inputv))
        
        #output
        s = s+"{}\n>>>Output: {}\n".format(("-"*5), self.name)
        s = s + u"KB = {}\nV = {}\n".format(complexOperation.strKnowledge(outputkb),complexOperation.strVariables(outputv))
        
        s = s + "{}\n".format("-"*10)  
        return s 
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
    """
    RETURNS A COPY OF THE INITIAL KNOWLEDGE BASE OF THE SCP THAT CONTAINS IT
    @return a copy of the initial rules of the scp
    """
    def evaluatekb (self):
        return copy.deepcopy(self.kb)
    """
    RETURNS A COPY OF THE INITIAL VARIABLES OF THE THE SCO THAT CONTAINS IT
    @return a copy of the initial variables of the scp
    """
    def evaluatev (self):
        return copy.deepcopy(self.v)

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
    """
    CREATE THE ABNORMALITIES AND APPEND THEM TO THE EPISTEMIC STATE (KB AND V)
    This method follows that in the complexOperation_addAB class description.
    This method is necessary to keep complexOperation_addAB a pipeline class, but
    still able to pass evaluate v and kb without code duplication.
    @return kb2: the new knowledge base containing the created abnormalities
    @return tempABs: a list of the added abnormalities
    """
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

    """
    DETERMINE THE OUTPUT RULES
    @return the new output rules with appropriate abnormalities
    """
    def evaluatekb (self):
        trueEval = self.trueEvaluation()
        return trueEval[0]

    """
    DETEMRINE THE OUTPUT VARIABLES
    @return the input variables with the abnormalities added (and set to unknown)
    """
    def evaluatev (self):
        trueEval = self.trueEvaluation()
        tempABs = trueEval[1]
        v = self.prev.evaluatev()
        #for each ab that was added to the rules, add that ab to the variables
        for i in tempABs:
            v.append(i)        
        return v   
        
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
        
    """
    WEAKLY COMPLETE THE PREVIOUS EPISTEMIC STATE
    This method follows that in the complexOperation_weaklyComplete class description.
    @return the weakly completed epistemic state
    """
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
    """
    WEAK COMPLETION DOES NOT CHANGE THE OUTPUT VARIABLES
    @return the output of the previous complex action
    """
    def evaluatev (self):
        return self.prev.evaluatev()

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
    """
    THE SEMANTIC OPERATOR DOES NOT CHANGE THE KNOWLEDGE BASE
    @return the output rules of the previous complex operation
    """
    def evaluatekb (self):
        return self.prev.evaluatekb()

    
    
    

    """
    DETERMINE IF THE OPERATOR IN QUESTION IS A BIJECTION
    return True if it is a bijection, False otherwise
    """
    def isBijection(self,rule):
        return isinstance (rule, basicLogic.operator_bitonic_bijection)
    """
    DETERMINE IF THE CLAUSE EVALUATES TO True/False/None.
    Note: does not use the values stored in V, only those of atoms in the rules
    which are usually unknown until set
    @param clause: the logical clause or atom to evaluate
    @return the logical evaluation of the clause
    """
    def evalClause (self, clause):
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
    def initGroundAtoms(self, kb, v):
        #check that every rule is of a valid format
        for rule in kb:
            if not self.isBijection(rule):
                raise scpError.NotBijectionError
                
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
    """
    DETERMINE THE VARIABLE VALUES OF THE OUTPUT AFTER APPLICATION OF THE SEMANTIC OPERATOR
    @return an updated variable list where new values have been assigned
    """
    def evaluatev (self):
        #get the kb of the previous complex operation
        kb = self.prev.evaluatekb()
        #get the v of the previous complex operation
        newV = self.prev.evaluatev()
        #set the values of atoms in kb to those mentioned in v
        tempkb = self.setkbfromv(kb,newV)
        #determine which heads in clauses can be set to true with the new v assignments
        newV = self.initGroundAtoms(tempkb, newV)
        return newV


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
    REMOVE THE VARIABLE FROM OUTPUT OF THIS COMPLEX ACTION
    @return v-(self.toDelete)
    """
    def evaluatev (self):
        oldv = self.prev.evaluatev()
        newv = []
        for old in oldv:
            if not old.name == self.toDelete:
                newv.append(old)
        return newv
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
    @return all rules which do no have the variable to delete as a head
    """
    def evaluatekb (self):
        #@TODO must be extended for more cases
        
        oldkb =  self.prev.evaluatekb()
        newkb =[]
        for old in oldkb:
            if isinstance(old, basicLogic.operator_bitonic_implication):
                if not self.toDeleteIsBody(old) and not self.toDeleteIsHead(old):
                    newkb.append(old)      
        return newkb
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
    """
    FIXING A VARIABLE DOES NOT CHANGE THE OUTPUT RULES
    @return the output of the previous complex operation
    """
    def evaluatekb (self):
        return self.prev.evaluatekb()
    """
    THE EXACT SAME LIST OF VARIABLES IS RETURNED, BUT WITH THE ATOM FOR THE VARIABLE
    IN QUESTION FIXED
    @return the list of variables with one variable now fixed
    """
    def evaluatev (self):
        oldV = self.prev.evaluatev()
        for v in oldV:
            if v.name == self.toFix:
                v.setValue(self.fixValue)
                v.fixed=True
        return oldV
        
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
    
    """
    FOR EVERY RULE THAT IS NOT A GROUND ATOM (a->b), CREATE A NEW RULE not(b)->not(a)
    @TODO this class needs to be extended to add temporary variables so that negative atoms don't
    appear in the heads of clauses
    @return the knowledge base with the new modus tolens rules
    """
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
    """
    MODUS TOLENS DOES NOT CHANGE VARIABLES AVAILABLE
    @TODO this class needs to be extended to add temporary variables so that negative atoms don't
    appear in the heads of clauses
    @return the output variables of the previous complex operation
    """
    def evaluatev (self):
        return self.prev.evaluatev()
 