# -*- coding: utf-8 -*-
"""
Created on Mon Feb 03 08:26:26 2020

@author: Axel
"""

import copy
import basicLogic
import scp

"""
THE SCP EVALUATOR IS A STATIC CLASS THAT HANDLES CARIOUS FUNCITON ASSOCIATED WITH
WITH ABDUCTION AND GENERATING LEAST MODELS (as seen in @TODOref).
"""
class scp_evaluator (object):
    #a mapping of every possible truth value to an integer
    logicRep = {0:None, 1:True, 2:False}
  
    """
    DETERMINE IF EVERY RULE IN THE KB OF THE SCP EVALUATES TO TRUE
    @param _scp: The SCP under consideration
    @param externalVariables: The variables that should be used to evaluate the SCP
    when None, uses the SCP's own instance variable list
    @return True if every rule in the KB evaluates to True, False otherwise
    """
    @staticmethod
    def ruleMatch (_scp, externalVariables=None):
        kb = _scp.evaluateKB()
        
        # If returns a copy of the KB with each atom's value set from those in externalVariables
        # or _scp.V by default
        kb = scp_evaluator.setkbfromv(kb,externalVariables)
        # check that every rule in the kb evaluates to true
        for rule in kb:
            tRule = copy.deepcopy(rule)
            if tRule.evaluate()!=True:
                return False
        return True
            
    """
    INSTANTIATES THE VARIABLES IN kb WITH THE VALUES IN v
    @param kb: the knowledge base (list of rules)
    @param v: the variables (list of basicLogic.atom abjects)
    @return the kb with each atom in each rule set to the values in v
    """
    @staticmethod     
    def setkbfromv (kb, v):
        kb=copy.deepcopy(kb)
        for var in v:
            for rule in kb:
                rule.deepSet(var.name, var.getValue())
        return kb
                
    """
    CONVERTS A NUMBER num TO BASE base AND FORCES A LENGTH OF length
    @param number: integer number
    @param base: desired base (should usually be the length of the logic being used)
    @return a list representing num in the desired base format with a total legth of length
    """
    @staticmethod 
    def toBase (num, base, length=-1):
        n = []
        tn = num
        
        while tn >= base:
            n.append(tn%base)
            tn = tn // base
        n.append(tn%base)
        
        if length > 0 and len(n) < length: 
            padding=[0]*(length-len(n))
            n = n + padding
        n.reverse()
        return n
    """
    CONVERTS A BASE n NUMBER IN A LIST INTO A LIST OF GROUND TRUTH VALUES FOR THE LOGIC
    @param n: the list representing the base n number
    @return a list with each number replaced by its logical equivalent in logicRep
    """
    @staticmethod
    def base_n_ToValuedLogic (n):
        
        li = [scp_evaluator.logicRep[i] for i in n]
        return li
    
    """
    FIND EVERY POSSIBLE TRUTH ASSIGNMENT OF THE FREE VARIABLES
    @param values: the variables that need assignments
    @return a list of list, containing every possible logical assignment of the values
    """
    @staticmethod  
    def generateAllPossibleVariableAssigmentsFromV (values):
        #the total number of possible assignments of the variables in values
        length = len(scp_evaluator.logicRep)**len(values)
        poss = []
        for i in range (0, length):
            #find the base n number that corresponds to i
            n = scp_evaluator.toBase(num=i, base=len(scp_evaluator.logicRep), length=len(values))
            #append a conversion of mapping of n to the logicRep truth table
            poss.append(scp_evaluator.base_n_ToValuedLogic(n))
        return poss

    """
    FIND THE NAME OF EVERY ATOM MENTIONED IN THE VARIABLES OF THE SCP THAT DOES NOT
    HAVE A BOUND VALUE
    @param _scp: the SCP which describes the task
    @return: all abducible variables, and all unabducible variables
    """
    @staticmethod
    def getAbducibleNames (_scp):
        #free variables
        abducibles = []
        #variables with set truth values
        unabducibles = []
        #all variables in the final epistemic state of the scp
        variables = _scp.evaluateV()
        #assign every variable in the scp to abducibles or unabducibles
        for v in variables:
            if v._value==None:
                v_n = basicLogic.atom(v.name, v.getValue())
                abducibles.append(v_n)
            else:
                v_n = basicLogic.atom(v.name, v.getValue())
                unabducibles.append(v_n)                
        return abducibles, unabducibles
    
 
    """
    GIVEN AN INITIAL SCP, FIND THE SHORTES ARRANGEMENT OF THE FREE VARIABLES THAT
    SATISFIES EVERY RULE IN THE EPISTEMIC STATE USING ABDUCTION
    @param initialSCP: the SCP which describes the task
    @return the least model of the final epistemic state
    """
    @staticmethod   
    def getLeastModel (initialSCP):
        solutions=[]
        abducibles, unabducibles = scp_evaluator.getAbducibleNames(initialSCP)
        
        #every possible assigment of the variables in V
        possibleValues = scp_evaluator.generateAllPossibleVariableAssigmentsFromV(abducibles)
        
        #test every possible assignment of the free variables in the epistemic state
        #those which satisfy the entire knowledge base are solutions
        for val in possibleValues:
            _scp = copy.deepcopy(initialSCP)
            newVariables = []
            #create atoms of the abducibles corresponding the truth list in possibleValues
            for v in range (0, len(abducibles)):
                if val[v]!=None:
                    newVar = basicLogic.atom(abducibles[v].name, val[v])
                    newVariables.append(newVar)
            #add the unabducibles to the variables too
            for i in unabducibles:
                newVariables.append(i)   
            #test if the new assignments satisfy the knowledge base
            match = scp_evaluator.ruleMatch(_scp,newVariables)
            if match:
                solutions.append(newVariables)
        return solutions
    
    """
    TAKE A LIST OF ATOMS AND TURN INTO A TWO LIST OF TRUE AND FALSE ATOMS
    @param variables: the variables with corresponding assignments in the least model
    @return the least model as a tuple (_true, _false) of the true and false variable lists respectively
    """
    @staticmethod
    def leastModelFormat(variables):
        _true=[]
        _false=[]
        for v in variables:
            if (v.getValue() == True):
                _true.append(v)
            elif (v.getValue()==False):
                _false.append(v)
        return (_true, _false)     
    
    """
    TURN A LEAST MODEL IN SET FORMAT INTO A STRING FOR PRINTING
    @param _leastModelAsSets: a tuple (_true, _false) generated by the leastModelFormat() function
    @return each least model as a string on a new line
    """
    @staticmethod
    def strLeastModelFromSets (_leastModelAsSets):
        least_raw = _leastModelAsSets
        s = u""
        for i in least_raw:        
            s=s+u"{"+scp_evaluator.strLeastModel_single(i)+"}\n"
        return s
    """
    TURN A LEAST MODEL IN VARIABLE FORMAT INTO A STRING FOR PRINTING
    @param leastModelAsSets: a list of atoms generated by the getLeastModel() function
    @return each least model as a string on a new line
    """
    @staticmethod
    def strLeastModelFromVariables (leastModelAsVariables):
        least_raw = scp_evaluator.leastModelAsSets(leastModelAsVariables)
        s = u""
        for i in least_raw:        
            s=s+u"{"+scp_evaluator.strLeastModel_single(i)+"}\n"
        return s    
    """
    TURN EACH LEAST MODEL INTO A SET OF VARIABLES
    @param least_raw: the set of least models, each of which is a set of variables
    @return the true, false sets of each least model as a list
    """
    @staticmethod
    def leastModelAsSets (least_raw):
        li = []
        for i in least_raw:
            least = scp_evaluator.leastModelFormat(i)    
            li.append(least)
        return li
    
    """
    TURN A SINGLE LEAST MODEL IN SET FORMAT INTO A STRING
    @param least: a single least model in set format
    @return the least model as a string
    """
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
