'''
Created on Mar 2, 2015

@author: Solaman
'''
class TransitionError(Exception):
    '''
    Raised when an operation attempts a state transition that is 
    not allowed.
    '''
    
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr(self.value)