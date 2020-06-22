"""
This is my first test with CCOBRA
"""

import ccobra

print ("Running ccobra")

class NVCModel(ccobra.CCobraModel):
    def __init__(self, name='NVCModel'):
        super(NVCModel, self).__init__(name, ['syllogistic'], ['single-choice'])

    def predict(self, item, **kwargs):
        enc_task = ccobra.syllogistic.encode_task(item.task)
        print ("Task Encoded")
        print (enc_task)
        enc_string = item.task
        print (enc_string)
        
        return [['NVC']]
    
