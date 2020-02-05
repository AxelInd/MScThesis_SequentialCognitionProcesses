# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 08:33:01 2020

@author: Axel
"""





from itertools import permutations 
import copy
  
# Get all permutations of [1, 2, 3] 



def removeFromList (val, li):
    tempLi = []
    for v in li:
        if val!=v:
            tempLi.append(v)
    return tempLi
def reduceStringByOneSize (s):
    poss=[]  
    for i in range (0,len(s)):
        temps = copy.deepcopy(s)
        temps=removeFromList(temps[i],temps)
        poss.append(temps)
    return poss

def order (a,b):
    return (a,b)
def createOrdersFromList (li):
    orders=[]
    for i in range (0, len(li)):
        for j in range (i, len(li)):
            pair = li[i],li[j]
            orders.append(pair)
    return orders
def testOrders (s, orders):
    if len(orders)==0:
        return True
    for o in orders:
        try:
            if s.index(o[0])> s.index(o[1]):
                return False
        #if the order isn't maintained in the final string then we have deleted part of the SCP
        except ValueError:
            return False
    return True

def countTotalPermutations (s):
    if len(s)==0:
        return 1
    perm = permutations(s)
    counter = 0
    for i in list(perm):
        counter = counter +1
    return counter

def countValidPermutations (s, orders,withPrintout=False):
    perm = permutations(s)
    counter = 0
    for i in list(perm):
        if (testOrders(i,orders)):
            if withPrintout:
                print(i)
            counter = counter +1
    return counter    

def countAllValidPermutations (s, orders, withPrintout=False, first = True):
    if len(s)==0 and testOrders(s,orders):
        return 1
    total=0
    for i in range (0, len(s)+1):
        x = permutations(s,i)
        for j in list(x):
            if testOrders(j, orders):
                total = total+1
                if withPrintout:
                    print j
    return total

    
def sequenceMaker (startChar, length):
    liKeepOrder=[]
    symbol = startChar
    for i in range (0, length):
        liKeepOrder.append(symbol)
        symbol = chr(ord(symbol)+1)
    return liKeepOrder



def factorial (n):
    if n==0:
        return 1
    return n * factorial(n-1)
def permutation (n,r):
    return factorial(n)/(factorial(n-r))


def nk (l,k):
    return permutation(l+k, k)
def total_nk(l,k):
    if k==0:
        return 1
    return nk(l,k)+total_nk(l,k-1) * permutation(k,k-1)

#==============================================================================
#=================================UNIT TESTING=================================
#==============================================================================
def unit_nkXcountValidPermutations(printout=False):
    for i in range (0, 5):
        liKeepOrder = sequenceMaker('A',i)
        orders = createOrdersFromList(liKeepOrder)
        for j in range (0, 5):
            liToInsert = sequenceMaker('p',j)
            s = liKeepOrder+liToInsert
            if printout:
                print ("EQUATION: The number of valid permutations with l={}, k={} is: {}".format(i,j,nk(l=i,k=j)))
                print ("TEST: The number of valid permutations with l={}, k={} is: {}".format(i,j,countValidPermutations(s,orders,withPrintout=False)))
            _nk = nk(l=i,k=j)
            _count = countValidPermutations(s,orders,withPrintout=False)
            if _nk!=_count:
                return False
    return True

def unit_total_nkXcountAllValidPermutations(printout=False):
    for i in range (0, 5):
        liKeepOrder = sequenceMaker('A',i)
        orders = createOrdersFromList(liKeepOrder)
        for j in range (0, 5):
            liToInsert = sequenceMaker('p',j)
            s = liKeepOrder+liToInsert
            _nk = total_nk(l=i,k=j)
            _count = countAllValidPermutations(s,orders,withPrintout=False)
            if printout:
                print ("EQUATION: The number of valid permutations with l={}, k={} is: {}").format(i,j,_nk)
                print ("TEST: The number of valid permutations with l={}, k={} is: {}").format(i,j,_count)
                print ("String is {}").format(s)

            #if _nk!=_count:
            #    return False
    return True

#print (">>Unit Testing unit_nk() and countValidPermutations() : {}").format(unit_nkXcountValidPermutations(printout=True))
#print (">>Unit Testing unit_total_nk() and countAllValidPermutations() : {}").format(unit_total_nkXcountAllValidPermutations(printout=True))

"""
liKeepOrder = sequenceMaker('A',2)
liToInsert = sequenceMaker('p',2)
l=len(liKeepOrder)
k=len(liToInsert)
s=liToInsert+liKeepOrder

print ("Total Permutation : " + str(countTotalPermutations(s)))
orders = createOrdersFromList(liKeepOrder)
print ("Order restrictions: " + str(orders))

print ("Total Valid Permutation of any length: " + str(countAllValidPermutations(s,orders, withPrintout=False)))
"""


#x = nk(l=4,k=4)

#print ("GUESS TOTOAL IS : {}").format(x)

def definitelyNot (l,k):
    if k==0:
        return 1
    return (l * k)*(definitelyNot(l+1,k-1))
    
    
    
    
def countNonEmptySubstr(s): 
    n = len(s); 
    print ("s is {}".format(len(s)))
    return int(n * (n + 1) / 2)

def totalNumberOfPermutationsWithSubstrings (s):
    total = 0
    for i in range (0, len(s)+1):
        x = permutations(s,i)
        for j in list(x):
            total=total+1
    return total
    
# driver code 
    """
s = "abcd"; 
n=len(s)
print (countNonEmptySubstr(s)*permutation(n,n-1)+countNonEmptySubstr(s[1:])*permutation(n-1,n-2)+countNonEmptySubstr(s[2:])*permutation(n-2,n-3))    
    
total=totalNumberOfPermutationsWithSubstrings(s)
print ("TOTAL IS: {}".format(total)) 

    
"""

import numpy as np

def calculateR (matrices,n):
    print "---"
#n : number of matrices

m1 = np.matrix([[1, 2], [3, 4]])
m2 = np.matrix([[5, 6, 13], [7, 14]])
m3 = np.matrix([[9, 10], [11, 12]])
    
matrices = [m1,m2,m3]

    
    
# n matrices each has r cols and var num rows
# make an Iterator that yields m r * r matrices without loading them into memory

n = len(matrices)
    
    
    
    
    
    
    
    
    
    
#print (definitelyNot(1,4))