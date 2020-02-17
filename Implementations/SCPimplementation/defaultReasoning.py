# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 08:59:41 2020

@author: Axel
"""
import scp
import basicLogic
import epistemicState

a = basicLogic.atom('bird')
b = basicLogic.atom('canFly')
c = basicLogic.atom('isEmu')


aORb = basicLogic.operator_bitonic_or(a,b,logicType="P")
emuscantFly = basicLogic.operator_bitonic_implication(c,basicLogic.operator_monotonic_negation(b),logicType="P")
thisIsAnEmu = basicLogic.operator_bitonic_implication(basicLogic.TRUE,c,logicType="P")
thisIsABird = basicLogic.operator_bitonic_implication(basicLogic.TRUE,a,logicType="P")
emusAreBirds = basicLogic.operator_bitonic_implication(c, a,logicType="P")

W = [emuscantFly,thisIsAnEmu,emusAreBirds]
rule1 =  basicLogic.operator_tritonic_defaultRule(a, b, b, False)
D = [rule1]
default = scp.scp(epistemicStateType="dl")
print (default.si)

print (D)

derived = [b]

#rule1.deepSet('bird', True)
#rule1.deepSet('canFly',True)
ev = rule1.evaluate(derived=derived)

print (ev)
print (W)

print (thisIsAnEmu.evaluate())

default.addD(rule1)
for rule in W:
    default.addW(rule)

print (default.evaluate())
thW, v = epistemicState.epistemicState_defeaultReasoning.deriveFromW(W)
print ("thW:{}\nv:{}\n".format(thW,v))
thW, v = epistemicState.epistemicState_defeaultReasoning.deriveFromD(D, thW)
