'''
Created on Apr 13, 2015

@author: Solaman
'''
from collections import Iterator

class DedekindNodeIter(Iterator):
    '''
    classdocs
    '''


    def __init__(self, dedekindNode):
        '''
        Constructor
        '''
        self.dedekindNode = dedekindNode
        self.configIndex = 0
        self.levelIndex = 0
        
    def next(self):
        if self.levelIndex >= len(self.dedekindNode.acceptedConfigurations):
            raise StopIteration
        
        result = self.dedekindNode.acceptedConfigurations[self.levelIndex][self.configIndex]
        self.configIndex += 1
        
        if self.configIndex >= len(self.dedekindNode.acceptedConfigurations[self.levelIndex]):
            self.configIndex = 0
            self.levelIndex += 1
        
        return result
        