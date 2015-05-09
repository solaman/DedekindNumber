'''
Created on Apr 2, 2015
@author: Solaman
'''
import resources

mappings = {}

def getConfAsInt(inputConf, inputSize):
    if inputSize not in mappings:
        mappings[inputSize] = DedekindSetMapping(inputSize)
    return mappings[inputSize].getConfAsInt(inputConf)

def getConfAsSet(inputConf, inputSize):
    if inputSize not in mappings:
        mappings[inputSize] = DedekindSetMapping(inputSize)
    return mappings[inputSize].getConfAsSet(inputConf)

def getFullSet(inputSize):
    return getConfAsSet((1<<inputSize) - 1, inputSize)

class DedekindSetMapping(object):
    '''
    Since the DedekindLattice stores accepted configurations as integers, users of the library
    might find it difficult to interact with as opposed to Python Sets. This class encapsulates
    the mapping from those integer values to Elements in a set for easier use.
    '''


    def __init__(self, inputSize, inputSet = None):
        '''
        Constructor
        @inputSet - input set for monotone boolean functions. If none is provided, a set is
        constructed from "resources/setValues.csv"
        '''
        self.inputSize = inputSize
        self.bitToElement = {}
        self.elementToBit = {}
        
        if inputSet == None:
            import os
            inputSetFileName = os.path.join(os.path.dirname(resources.__file__), "setValues.csv")
            inputSet = open(inputSetFileName).read().split(",")
            
        elif isinstance(inputSet, set):
            inputSet = list(inputSet)
        
        for bitShift in range(0, self.inputSize):
            self.bitToElement[1<<bitShift] = inputSet[bitShift]
            self.elementToBit[ inputSet[bitShift]] = 1<<bitShift
            
            
            
        
    def getConfAsSet(self, inputConf):
        from sets import ImmutableSet
        confSet = set()
        bitShift = 0
        while bitShift <= self.inputSize:
            if 1<<bitShift in self.bitToElement and (1<<bitShift & inputConf):
                confSet.add( self.bitToElement[1<<bitShift])
            bitShift += 1
        return ImmutableSet(confSet)
    
    def getConfAsInt(self, inputConf):
        confInt = 0
        for element in list( inputConf):
            confInt |= self.elementToBit[element]
            
        return confInt
            
        
 