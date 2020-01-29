# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:14:20 2020

@author: Axel

This file provides two different search mechanisms for SCPs in the context of the suppression task
1) de novo search from the initially provided rules to meet a specified variable assignment goal
2) modifying (without removing): inserting complex operations into an existing SCP to go from modelling a general to an individual reasoner
"""
import scp
import copy
import basicLogic
#STARTING VARIABLES
# e: she has an essay to write
e = basicLogic.atom('e', setValue=False)
# l: she will study late in the library
l = basicLogic.atom('l', setValue=False)
# o: the library is open
o = basicLogic.atom('o', setValue=False)

#STARTING RULES, FACTS
# if she has an essay to write, she will study late in the library
knowledge1 = basicLogic.operator_bitonic_implication(e,l)
# she has an essay to write
knowledge2 = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, e)
# if the library is open, she will study late in the library
knowledge3 = basicLogic.operator_bitonic_implication(o, l)
# the lirary is open
knowledge4 = basicLogic.operator_bitonic_implication(basicLogic.TRUE_noValue, o)

#INITIALISE THE SET OF COMPLEX OPERATORS M
# create the complex operation to add abnormalities
comp_addAB = scp.complexOperation_addAB ()
# create the complex operation to delete a named variable
comp_deleteo = scp.complexOperation_deleteVariable('o')
# create the complex operation to fix a named variable to a specified value
comp_fixab1 = scp.complexOperation_fixVariable('ab1', False)
# Create the complex operation to weakly complete the logic program
comp_weak = scp.complexOperation_weaklyComplete()
# create the complex operation to apply the sematic operator
comp_semantic = scp.complexOperation_semanticOperator()

# =============================== SEARCH ===========================================
M = []
# create the list containing all comple operations which should be considered during search.
# the paper @TODO describes the procedure and best practices for choosing these.
# note that comp_initialise is exluded from this list, as the de-facto start variable, it is only used once in an SCP.
#M.append(comp_addAB)
M.append(comp_deleteo) 
M.append(comp_fixab1)
M.append(comp_semantic)
M.append(comp_weak)
# The maximum search depth of the algorithm for either search type
LIMIT = 5
#==============================================================================
#================================DE NOVO SEARCH================================
#==============================================================================
"""
THIS IS A BASIC BREADTH-FIRST SEARCH IMPLEMNTATION FOR A VARIABLE ASSIGNMENT
@param p: the empty scp, containing the variables and rules of the problem (as present in state s_0)
@param iteration: the depth to which the bfs has already searched
@param solutions: a list of the scps which, when evaluated to the final state, satisfy the goal conditions
@param goalV: the set of variable assignments which constitute a success, in the form (string:variableName,bool:truthValue=True/False/None)
@param limit: the maximum search depth for the bfs
@param goalKB: the rules which should be present in the final epistemic state (@TODO not yet implemented)
"""
def scpDeNovoSearch (p, iteration, solutions = [], goalV = None, limit = LIMIT, goalKB = None):
    # the final epistemic state of the agent after the SCP is run
    kb = p.evaluateKB()
    # the final epistemic variable assignments of the agent after the SCP is run
    v=[]
    try:
        v = p.evaluateV()
    except scp.NotBijectionError:
        return []
    # check goal condition
    # at present goals are limitted to variable assignments @TODO extend
    # duplicate solutions are removed
    for var in v:
        if var.name == goalV[0] and var.value==goalV[1]:
            solutions = solutions + [p]
            return list(dict.fromkeys(solutions))
    # check that maximum search depth has not yet been reached
    # returns an empty list if it has
    if iteration + 1 >= limit:
        return []
    # create an scp that is the current scp + m, where m is complex operation in M
    # deepcopy ensures that the scp pointers to objects are not shared
    # repeats the search using the newscps
    for m in p.M:
        scpTemp = copy.deepcopy(p)
        scpTemp.addNext(m)
        result  = scpDeNovoSearch(scpTemp, iteration+1, solutions, goalV, limit, goalKB)
        solutions = solutions  + result
    # returns the list of all solutions found thus far
    # duplicate solutions are removed
    return list(dict.fromkeys(solutions))

"""
GET A PRINTABLE STRING DESCRIBING EACH SOLUTION ON A NEW LINE
@param li: The list of solutions generated by either scpDeNovoSearch(...) or @TODO
@return a string detailing each scp in li on a new line
"""    
def strSCPList (li):
    s = (">" * 15) + "SOLUTIONS"+("<"*15) +"\n"
    for sc in li:
        s = s + str(sc) + "\n"
    s=s+"-------------------------"
    return s
        
#==============================================================================
#=============================MODIFICATION SEARCH==============================
#==============================================================================
"""
INSERT A COMPLEX OPERATION INTO AN SCP AT A SPECIFIED POSITION
@param m: a complex operation
@param _scp: the SCP into which m must be insterted
@param pos: the position in the scp into which m must be insterted
"""
def insert(m,_scp, pos):
    newscp=copy.deepcopy(_scp)
    newscp.insertAtPos(m,pos)
    return newscp
"""
REMOVE A SINGLE COMPLEX OPERATION FROM A LIST OF COMPLEX OPERATIONS
@param m: the complex operation to be removed (passed by reference)
@param M: the list of complex operations from which m should be removed
@return the set of complex operations M without the complex operation m ([] if all m in M are deleted)
"""
def remove (m,M):
    alreadyRemoved=False
    # the empty list that will contain all m' in M except for m
    newM = []
    # append an operation i in M to newM iff m isn't the complex operation that must be deleted
    for i in M:
        if i != m:
            newM.append(i)
        elif alreadyRemoved == False:
            alreadyRemoved=True
    return newM

#==============================================================================
#==================================TESTING=====================================
#==============================================================================
"""
USE THE DE NOVO SEARCH TO FIND ALL SOLUTIONS WHICH SATISFY THE GOAL VARIABLES
@param goalV: the set of variable assignments which constitute a success, in the form (string:variableName,bool:truthValue=True/False/None)
@param limit: the maximum search depth for the bfs
"""
def testDeNovoSearch (goalV, limit=LIMIT ):
    # the empty scp which will be used to find the solutions
    p = scp.scp()   
    # add the list of allowable complex operations to the SCP
    p.addM(M)
    # add the known rules
    p.addKnowledge(knowledge1)
    p.addKnowledge(knowledge2)
    p.addKnowledge(knowledge3)
    # add the known variables
    p.addVariable(e)
    p.addVariable(l)
    p.addVariable(o)
    # add the initialise complex operation
    # add any other complex operations guaranteed to be performed next by p
    #p.addNext(comp_addAB)
    #p.addNext(comp_weak)
    
    # get a list of all possible successive SCPs which meet the given goal conditions
    solutions = scpDeNovoSearch(p, iteration=0, goalV=goalV, limit=limit)   
    # print all the solutions found
    print(strSCPList(solutions))    
    print ("Number of solutions found: " + str(len(solutions)))
    
"""
USE THE MODIFIED BFS SEARCH TO INSERT limit NUMBER OF NEW OPERATION INTO AND EXISTING SCP IN ORDER TO
FIND ALL EXTENSIONS WHICH SATISFY SOME GOAL CONDITION
@param goalV: the set of variable assignments which constitute a success, in the form (string:variableName,bool:truthValue=True/False/None)
@param limit: the number of complex operations to be added to the SCP
"""
def testModificationSearch(goalV, limit=LIMIT):
    q = scp.scp()   
    
    q.addM(M)
    
    q.addKnowledge(knowledge1)
    q.addKnowledge(knowledge2)
    q.addKnowledge(knowledge3)
    
    q.addVariable(e)
    q.addVariable(l)
    q.addVariable(o)
    #p.addNext(comp_addAB)
    q.addNext(comp_addAB)
    q.addNext(comp_weak)
    q.addNext(comp_semantic)
    q.addNext(comp_semantic)
    #q.addNext(comp_semantic)
    solutions = modificationSearch(q, goalV, limit)
    return solutions
    
    """"
    solutions = scpCombinationSearch(Mprime=[], depth=limit, _scp=q, goalV=goalV)
    print (strSCPList(solutions))
    print ("Number of solutions found: " + str(len(solutions)))
    print ("The initial SCP was:")
    """
    print(q)
from itertools import permutations 

def randomisedInsert2 (Mprime,_scp, goalV, solutions):
    # if M' is the empty set, check if the current scp, when evluated, leads to variable assignments that satisfy the goal
    # if the final epistemic state satisfies the goal, return the scp, else return the empty set
    
    if len(Mprime)==0:
        v=[]
        try:
            v = _scp.evaluateV()
            for var in v:
                #print "var is :: {} :: {}".format(var.name,var.value)
                if var.name == goalV[0] and var.value == goalV[1]:
                    #print ("FOUND")
                    return [_scp]
            return []
        except scp.NotBijectionError:
            return v
    # combination(...) already generates every possible combination, so we are only concerned with inserting them
    # we insert the first m in every position in the scp, then we remove that m from Mprime and repreat the process with the shortened list
    # we ignore position 0 as this is the init operation in the SCP
    for pos in range (1, len(_scp)):      
        # insert the first m in M' into the position pos
        newscp = insert(Mprime[0],_scp, pos)
        # remove the first complex operation in M' from the list
        newMprime = remove(Mprime[0],Mprime)
        # repeat this operation using the extended SCP and the shortened M'
        insertAndEvaluate = randomisedInsert2(Mprime=newMprime,_scp=newscp, goalV=goalV, solutions=solutions)
        # add any solutions that can use this scp as a base and then add some m in newM' to it to satisfy the goal
        solutions = solutions + insertAndEvaluate
    #return the solutions without any duplicates
    return list(dict.fromkeys(solutions))


def modificationSearch (_scp, goalV, depth):
    M = _scp.M
    solutions=[]
    for i in range (0, depth+1):
        li = permutations(M,i)
        for l in list(li):
            solutions = solutions+randomisedInsert2(l, _scp, goalV, [])
    print "{} solutions found".format(len(solutions))
    return solutions
            
            
        
    
# use this method to test a general BFS search algorithm that finds a set of SCPs that model the suppression task
denSearch = testDeNovoSearch(goalV=('l',True), limit=5)
# Use this method to test a modified BFS algorithm that finds possible extensions of an existing SCP that satisfy a goal
#modSearch = testModificationSearch(goalV=('l',True), limit=2)

#for i in modSearch:
#    print i

































