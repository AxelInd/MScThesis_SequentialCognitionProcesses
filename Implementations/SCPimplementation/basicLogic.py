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
            self.value = value
        else:
            self.value=None
            
        #print("I made an atom called " + self.name)
    def evaluate(self):
        return self.value
    def deepSet(self, var, val):
        if (self.name == var):
            self.value = val
            #print ("Variable " + str(self.name) + " set to " + str(self.value))
    def __str__ (self):
        return str(self.name)
    def setValue (self, val, setVal = True):
        if not self.fixed and setVal==True:
            self.value = val
    
class atom_truth (atom):
    def __init__ (self, setValue=True):
        atom.__init__(self, "TRUTH", value = True, setValue=setValue)
class atom_false (atom):
    def __init__ (self, setValue=True):
        atom.__init__(self, "FALSE", value = False, setValue=setValue)

class atom_unknown (atom):
    def __init__ (self, setValue=True):
        atom.__init__(self, "UNKNOWN", value = None, setValue=setValue)
        
 
        
class operator (object):
    def __init__(self):
        self.name= ""
    def app (self):
        print("applying")
    def evaluate(self):
        return "I am evaluating"
    def deepSet (self, var, val):
        print (" I am deepsetting")

#ATOMS FOR BASE TRUTH VALUES      
TRUE = atom_truth (setValue=False)      
FALSE = atom_false (setValue=False)      
UNKNOWN = atom_unknown (setValue=False)

TRUE_noValue = atom_truth (setValue=False)      
FALSE_noValue = atom_false (setValue=False)      
UNKNOWN_noValue = atom_unknown (setValue=False)        
        
class operator_monotonic(operator):
    def __init__(self, clause = None):
        operator.__init__(self)    
        self.clause=clause
        
    def deepSet (self, var, val):
        self.clause.deepSet(var, val)
        
    def __str__ (self):
        return "("+self.name + str(self.clause)+")"
        
class operator_monotonic_negation (operator_monotonic):
    def __init__(self, clause = None):
        operator_monotonic.__init__(self, clause)     
        self.name = "NOT"
        self.value=self.evaluate
    def setValue(self, value, setVal):
        if setVal:    
            if value == True:
                self.value = TRUE
            elif value == False:
                self.value = FALSE
            elif value == None:
                self.value==UNKNOWN
        else:
            if value == True:
                self.value = TRUE_noValue
            elif value == False:
                self.value = FALSE_noValue
            elif value == None:
                self.value==UNKNOWN_noValue
        
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
    def __init__(self, clause1=None, clause2=None):
        operator.__init__(self)
        self.clause1 = clause1
        self.clause2 = clause2
    def deepSet(self, var, val):
        self.clause1.deepSet(var, val)
        self.clause2.deepSet(var, val)
    def __str__(self):
        return "("+str(self.clause1)  + self.name + str(self.clause2)+")"



class operator_bitonic_and (operator_bitonic):      
    def __init__(self, clause1, clause2):
        operator_bitonic.__init__(self,clause1,clause2)
        self.name="AND"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        
        return tbl_and[str(clauseVal1)][str(clauseVal2)]
        
class operator_bitonic_or (operator_bitonic):      
    def __init__(self, clause1, clause2):
        operator_bitonic.__init__(self,clause1,clause2)
        self.name="OR"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        
        return tbl_or[str(clauseVal1)][str(clauseVal2)]    

class operator_bitonic_implication (operator_bitonic):      
    def __init__(self, clause1, clause2):
        operator_bitonic.__init__(self,clause1,clause2)
        self.name="IMPLICATION"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        
        return tbl_implication[str(clauseVal1)][str(clauseVal2)] 
    
class operator_bitonic_bijection (operator_bitonic):      
    def __init__(self, clause1, clause2):
        operator_bitonic.__init__(self,clause1,clause2)
        self.name="BIJECTION"
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