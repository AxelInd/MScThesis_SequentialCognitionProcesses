# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 08:59:41 2020

@author: Axel
"""
import scp
import basicLogic
import epistemicState
import complexOperation

a = basicLogic.atom('bird')
b = basicLogic.atom('canFly')
c = basicLogic.atom('isEmu')

d = basicLogic.atom('penguin', False)
e = basicLogic.atom('evil')
f = basicLogic.atom('friend')

aORb = basicLogic.operator_bitonic_or(a,b,logicType="P")
emuscantFly = basicLogic.operator_bitonic_implication(c,basicLogic.operator_monotonic_negation(b),logicType="P")
thisIsAnEmu = basicLogic.operator_bitonic_implication(basicLogic.TRUE,c,logicType="P")
thisIsABird = basicLogic.operator_bitonic_implication(basicLogic.TRUE,a,logicType="P")
emusAreBirds = basicLogic.operator_bitonic_implication(c, a,logicType="P")


rule1 =  basicLogic.operator_tritonic_defaultRule(a, b, b, False)
rule2 = basicLogic.operator_tritonic_defaultRule(d, e, f, False)
rule3 = basicLogic.operator_tritonic_defaultRule(c, basicLogic.operator_monotonic_negation(f), e, False)
V = [a,b,c, d, e, f]
W = [emuscantFly,thisIsAnEmu,emusAreBirds]
#W = [emuscantFly,thisIsABird,emusAreBirds]
D = [rule1, rule2, rule3]

comp_def_eval = complexOperation.complexOperation_default_drawConclusions()


print (D)

derived = [b]

#rule1.deepSet('bird', True)
#rule1.deepSet('canFly',True)
ev = rule1.evaluate(derived=derived)

print (ev)
print (W)

print (thisIsAnEmu.evaluate())

#thW, v = epistemicState.epistemicState_defeaultReasoning.deriveFromW(W)
#print ("thW:{}\nv:{}\n".format(thW,v))
#thW, v = epistemicState.epistemicState_defeaultReasoning.deriveFromD(D, thW)


default = scp.scp(epistemicStateType="dl")

default.addVList(V)
default.addDList(D)
default.addWList(W)

default.addNext(comp_def_eval)
print ("---------------")
#print (default.si)
print (default.evaluate())























