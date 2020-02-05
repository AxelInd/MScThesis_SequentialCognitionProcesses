# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 11:07:55 2020

@author: Axel
"""
# TRUTH TABLES
tbl_and = {'True' : {'True': True,'None': None,'False':False}, 
'None' : {'True': None,'None': None,'False':True},
'False' : {'True': False,'None': False,'False':False}}

tbl_or = {'True' : {'True': True,'None': True,'False':True}, 
'None' : {'True': True,'None': None,'False':None},
'False' : {'True': True,'None': None,'False':False}}

tbl_implication = {'True' : {'True': True,'None': None,'False':False}, 
'None' : {'True': True,'None': True,'False':None},
'False' : {'True': True,'None': True,'False':True}}

tbl_bijective = {'True' : {'True': True,'None': None,'False':False}, 
'None' : {'True': None,'None': True,'False':None},
'False' : {'True': False,'None': None,'False':True}}


        
class atom (object):
    def __init__(self, name, value = None, setValue = True):
        self.name = name
        self.fixed=False
        if setValue:      
            self._value = value
        else:
            self._value=None
            
        #print("I made an atom called " + self.name)
    def evaluate(self):
        return self.getValue()
    def deepSet(self, var, val):
        if (self.name == var):
            self._value = val
            return True
        return False
            #print ("Variable " + str(self.name) + " set to " + str(self.value))
    def __str__ (self):
        return u"{}".format(self.name)
    def setValue (self, val, setVal = True):
        if not self.fixed and setVal==True:
            self._value = val
    def getValue (self):
        return self._value
    def __repr__(self):
        return "({}:{})".format(self.name, self.getValue())
    
class atom_truth (atom):
    def __init__ (self, setValue=True):
        atom.__init__(self, u"\u22A4", value = True, setValue=setValue)
class atom_false (atom):
    def __init__ (self, setValue=True):
        atom.__init__(self, u"\u22A5", value = False, setValue=setValue)

class atom_unknown (atom):
    def __init__ (self, setValue=True):
        atom.__init__(self, "UNKNOWN", value = None, setValue=setValue)
        
 
        
class operator (object):
    """
    Create an instanc of the operator class
    @param immutable: This rule is assumed to be true without abnormalitites
    in practice, this means that no abnormalities will be added by the scp to this operator.
    """
    def __init__(self, immutable=False):
        self.name= ""
        self.immutable=immutable
    def app (self):
        print("applying")
    def evaluate(self):
        return "I am evaluating"
    def deepSet (self, var, val):
        print (" I am deepsetting")
    def __repr__(self):
        return self.__str__()

#ATOMS FOR BASE TRUTH VALUES      
TRUE = atom_truth (setValue=True)      
FALSE = atom_false (setValue=True)      
UNKNOWN = atom_unknown (setValue=True)
      

def getGroundAtomFor(val):
    if val==None:
        return UNKNOWN
    if val==True:
        return TRUE
    if val==False:
        return FALSE

class operator_monotonic(operator):
    def __init__(self, clause = None, immutable = False):
        operator.__init__(self,immutable = immutable)    
        self.clause=clause
        
        
    def deepSet (self, var, val):
        self.clause.deepSet(var, val)
        
    def __str__ (self): 
        return u"({} {})".format(self.name,self.clause)          
        
class operator_monotonic_negation (operator_monotonic):
    def __init__(self, clause = None, immutable = False):
        operator_monotonic.__init__(self, clause, immutable = immutable)     
        self.name = u"\u00AC"
    def getValue (self):
        return self.clause.evaluate()
        
    def evaluate(self):        
        clauseVal = self.clause.evaluate()
        if clauseVal==None:
            return None
        elif clauseVal==True:
            return False
        else:
            return True
#--------------------------------------------
class operator_bitonic (operator):
    def __init__(self, clause1=None, clause2=None, immutable = False):
        operator.__init__(self, immutable = immutable)
        self.clause1 = clause1
        self.clause2 = clause2
    def deepSet(self, var, val):
        self.clause1.deepSet(var, val)
        self.clause2.deepSet(var, val)
    def __str__(self):
        return u"({} {} {})".format(self.clause1, self.name, self.clause2)



class operator_bitonic_and (operator_bitonic):      
    def __init__(self, clause1, clause2, immutable = False):
        operator_bitonic.__init__(self,clause1,clause2, immutable = immutable)
        self.name=u"\u2227"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        
        return tbl_and[str(clauseVal1)][str(clauseVal2)]
        
class operator_bitonic_or (operator_bitonic):      
    def __init__(self, clause1, clause2, immutable = False):
        operator_bitonic.__init__(self,clause1,clause2,immutable=immutable)
        self.name=u"\u2228"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        
        return tbl_or[str(clauseVal1)][str(clauseVal2)]    

class operator_bitonic_implication (operator_bitonic):      
    def __init__(self, clause1, clause2, immutable = False):
        operator_bitonic.__init__(self,clause1,clause2, immutable = immutable)
        self.name=u"\u2192"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        
        return tbl_implication[str(clauseVal1)][str(clauseVal2)] 
    
class operator_bitonic_bijection (operator_bitonic):      
    def __init__(self, clause1, clause2,immutable=False):
        operator_bitonic.__init__(self,clause1,clause2, immutable=immutable)
        self.name=u"\u2194"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        
        return tbl_bijective[str(clauseVal1)][str(clauseVal2)]
    
    


        
        
def isGroundAtom (clause):
    if isinstance(clause, atom_truth):
        return True
    if isinstance (clause, atom_false):
        return True
    if isinstance (clause, atom_unknown):
        return True
    return False       