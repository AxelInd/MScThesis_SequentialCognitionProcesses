"""
CONVERTS A NUMBER num TO BASE base AND FORCES A LENGTH OF length
@param number: integer number
@param base: desired base (should usually be the length of the logic being used)
@return a list representing num in the desired base format with a total legth of length
"""
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
def base_n_ToValuedLogic (n, logicRep):
    
    li = [logicRep[i] for i in n]
    return li

"""
FIND EVERY POSSIBLE TRUTH ASSIGNMENT OF THE FREE VARIABLES
@param values: the variables that need assignments
@return a list of list, containing every possible logical assignment of the values
"""
def generateAllPossibleVariableAssigmentsFromV (values, logicRep=[True,False,None]):
    #the total number of possible assignments of the variables in values
    length = len(logicRep)**len(values)
    poss = []
    for i in range (0, length):
        #find the base n number that corresponds to i
        n = toBase(num=i, base=len(logicRep), length=len(values))
        #append a conversion of mapping of n to the logicRep truth table
        poss.append(base_n_ToValuedLogic(n,logicRep))
    return poss
