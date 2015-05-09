'''
Created on Apr 30, 2015

@author: Solaman
'''
from itertools import combinations as genCombinations
from DedekindSetMapping import getConfAsInt

#To avoid cost of calculating configuration levels continuously,
#We will calculate the levels from the very beginning.
configurationLevelss = {}

class DedekindNodeLean(object):
    '''
    Attempt to speed up generation of nodes. For computing the Dedekind number,
    we only need the "highest" level of configurations, so we attempt
    to reduce overhead by keeping only this level.
    '''   
    
    def __init__(self, inputSize, acceptedConfigurations):
        '''
        Each function has a set of accepted configurations. To aid in the book keeping of this algorithm,
        each accepted configuration is stored by "level", namely, how many of the given inputs must be "off"
        in the configuration. so if the configuration 0b0001 is accepted and the bitmask is 0b1111, 
        then the configuration would be stored at the 3rd level.
        For rudimentary checking, the accepted configurations are added by descending level.
        '''
        self.childrenSize = 0
        self.inputSize = inputSize
        self.bitMask = self.bitMask = 2**(inputSize) - 1
        self.acceptedConfigurations = acceptedConfigurations
        self.level = -1
        if acceptedConfigurations != []:
            self.level = getConfigurationLevel(inputSize, acceptedConfigurations[0])
        
        self.index = -1
    
    def _generatePossibleConfigurations(self):
        '''
        Generates possible configurations to add to the function such that the new functions would be monotone
        (given that this function is monotone). We observe that this can be done by level combinations.
        E.G. if the input size is 4, and the last level of the function is 1->[0b1011, 0b0111], then the children
        of the node in the lattice can have the level 2 configuration [0b0011]. 
        (if any other, then it would not be monotone).
        ''' 
        possibleConfigurations = []
        
        #current max configuration level is [self.bitMask]
        if self.level == 0:
            possibleConfigurations = getLevelOneConfigurations(self.inputSize)
            
        #Entire Dedekind Node Lattice is filled, can add [0] as an accepted configuration
        elif self.level == self.inputSize - 1 \
        and len(self.acceptedConfigurations) == self.inputSize:
            possibleConfigurations = [0]
        #current max configuration level is [] (none are accepted)     
        elif self.level == -1:
            return []
        elif self.level< self.inputSize - 1:
            combinations = genCombinations(self.acceptedConfigurations, self.level + 1)
            possibleConfigurations = []
            for combination in combinations:
                possibleConfiguration = self.bitMask
                for configuration in combination:
                    possibleConfiguration &= configuration
                if getConfigurationLevel(self.inputSize, possibleConfiguration) == self.level + 1:
                    possibleConfigurations.append(possibleConfiguration)
            return possibleConfigurations
        
        return possibleConfigurations
        
    
    def generateChildren(self):
        '''
        Generates all Dedekind Nodes that would be considered the children of this
        DedekindNode
        '''
        children = []
        possibleConfigurations = self._generatePossibleConfigurations()

        for numberOfConfigurations in range(1, len(possibleConfigurations) + 1):
            combinations = genCombinations(possibleConfigurations, numberOfConfigurations)
            for combination in combinations:
                children.append( DedekindNodeLean(self.inputSize, combination))
                
        return children
        
    def getLastLevel(self):
        return self.acceptedConfigurations
    
    def getAcceptedConfigurationsAsList(self):
        return self.acceptedConfigurations

def getConfigurationLevel(inputSize, configuration):
    global configurationLevelss
    if inputSize not in configurationLevelss:
        bitMask = (1<<inputSize) - 1
        configurationLevels = [0] *(bitMask + 1)
        for index in range (0, bitMask + 1):
            configurationLevels[index] = hamming_distance(bitMask, index)
            
        configurationLevelss[inputSize] = configurationLevels
    return configurationLevelss[inputSize][configuration]         

def getLevelOneConfigurations(inputSize):
    '''
    Possible level One configurations are generated uniquely from all others. Given that the current
    function only accepts the state where all inputs are "on", possible level one configurations are any
    input such that one input is "off".
    E.G. if input size is 4, the children of {0b1111} can potentially have any of {0b0111, 0b1011, 0b1101, 0b1110}
    '''
    levelOneConfigurations = []
    bitMask = (1<< inputSize) -1
    for inputIndex in range(0, inputSize):
        levelOneConfigurations.append( (1 << inputIndex) ^ bitMask ) 
        
    return levelOneConfigurations     
                
        

def hamming_distance( x, y):
    '''
    Calculates hamming distance between two unsigned int values.
    Code was copied from http://en.wikipedia.org/wiki/Hamming_distance
    '''
    dist = 0
    val = x ^ y
    while( val != 0):
        dist += 1
        val &= val -1
        
    return dist 
        