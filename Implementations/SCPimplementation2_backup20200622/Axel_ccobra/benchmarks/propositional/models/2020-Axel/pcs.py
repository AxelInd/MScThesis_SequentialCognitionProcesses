# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 09:09:55 2020

@author: Axel
"""
#an implementation of 3-valued logic
import basicLogic
#used to deepcopy complex objects
import copy
#used to create complex epistemic actions in the seuqence
import complexOperation
#used to throw exceptions for improper use
import scpError

import epistemicState


class pcs (object):
    def __init__(self):
        self.M=[]
        