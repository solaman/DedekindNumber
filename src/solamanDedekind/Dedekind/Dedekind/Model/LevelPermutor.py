'''
Created on Apr 10, 2015

@author: Solaman
'''
from itertools import permutations
from DedekindNode import getIndex

class LevelPermutor(object):
    '''
    This ungodly monstrosity will be used to store equivalence classes
    of configurations by level. Instead of going through the monumental pain of
    calculating all equivalence classes, we do equivalence classes by level in hopes
    that we can save on running time a bit. I doubt it. I highly doubt it. But we 
    will see.
    '''


    def __init__(self, inputSize):
        '''
        Constructor
        '''
        self.permutations = list(permutations( range(0, inputSize)) )
        self.permutations = self.permutations[:len(self.permutations)]
        self.inputSize = inputSize
        self.classes = {}
        
    def __contains__(self, value):
        if isinstance(value, int):
            if value in self.classes:
                return True
        elif isinstance(value, list):
            if getIndex(value) in self.classes:
                return True
        return False
    
    def __getitem__(self, key):
        if key not in self:
            return None
        else:
            if isinstance(key, int):
                return self.classes[key]
            elif isinstance(key, list):
                return self.classes[ getIndex(key)]
    
    def __setitem__(self, configurations, value):
        if configurations in self:
            return
        self.__putPermutations(configurations, value)
        
        
    def __putPermutations(self, configurations, value):
        '''
        This upsetting function will place all of the permutations
        of the configuration into the mapping. We are guaranteed
        that each of these permutations will be visited by the current function,
        so the running time isn't slowed down all too much. But the memory usage,
        it makes me sad.
        '''
        for permutation in self.permutations:
            permutedConfigurations = []
            for configuration in configurations:
                permutedConfiguration = 0
                for index in range(0, self.inputSize):
                    if configuration & (1 << index):
                        permutedConfiguration |= (1 << permutation[index])
                        
                permutedConfigurations.append(permutedConfiguration)
            index = getIndex(permutedConfigurations)
            self.classes[index] = value
            
        