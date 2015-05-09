'''
Created on Mar 3, 2015

@author: Solaman
'''
from itertools import combinations as genCombinations
import os
from collections import Iterable
from DedekindNodeIter import DedekindNodeIter
from DedekindSetMapping import getConfAsInt

#Used for Dot file generation
#Once a node is written to a dot file
#A full Node is created to help
fullNodes = {}
    
#Used for Dot file generation
#Once a node is written to a dot file
#labels for each configuration are made
configurationLabelss = {}
    
#Used for Dot file Generation
#Once a node is written to a dot file
#edges between configurations are written as dot edges.
dotEdgess = {}

#To avoid cost of calculating configuration levels continuously,
#We will calculate the levels from the very beginning.
configurationLevelss = {}

class DedekindNode(Iterable):
    '''
    A boolean function. It is up to the user to ensure that it is monotone.
    '''
    
    
    def __init__(self, inputSize, acceptedConfigurations, nodeToCopy = None):
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
        
        
        if nodeToCopy != None:
            temp = nodeToCopy.getAcceptedConfigurationsAsList()
            temp.extend(acceptedConfigurations)
            acceptedConfigurations = temp
        self.acceptedConfigurations = []
        
        for acceptedConfiguration in acceptedConfigurations:
            level = getConfigurationLevel(self.inputSize, acceptedConfiguration)
            if level > len( self.acceptedConfigurations):
                exceptionMessage = "Cannot add configurations beyond the highest level + 1" \
                + "\n attempted level: " + str(level) \
                +"\n level limit: " + str(len(self.acceptedConfigurations))
                raise Exception( exceptionMessage)
            
            if level == len(self.acceptedConfigurations):
                self.acceptedConfigurations.append( [acceptedConfiguration])
            else:
                self.acceptedConfigurations[level].append( acceptedConfiguration)
        
        self.index = -1
            
        
    def getAcceptedConfigurationsAsList(self):
        acceptedConfigurations = []
        for level in self.acceptedConfigurations:
            acceptedConfigurations.extend(level)
            
        return acceptedConfigurations
    
    def isConsistent(self, configuration):
        '''
        Checks if a configuration would be accepted or not.
        '''
        return isConsistent(self, configuration)
    
    def _generatePossibleConfigurations(self):
        '''
        Generates possible configurations to add to the function such that the new functions would be monotone
        (given that this function is monotone). We observe that this can be done by level combinations.
        E.G. if the input size is 4, and the last level of the function is 1->[0b1011, 0b0111], then the children
        of the node in the lattice can have the level 2 configuration [0b0011]. 
        (if any other, then it would not be monotone).
        ''' 
        possibleConfigurations = []
        newMaxLevel = len(self.acceptedConfigurations)
        
        #current max configuration level is [self.bitMask]
        if newMaxLevel == 1:
            possibleConfigurations = getLevelOneConfigurations(self.inputSize)
            
        #Entire Dedekind Node Lattice is filled, can add [0] as an accepted configuration
        elif newMaxLevel == self.inputSize \
        and len(self.acceptedConfigurations[-1]) == self.inputSize:
            possibleConfigurations = [0]
        #current max configuration level is [] (none are accepted)     
        elif newMaxLevel == 0:
            return []
        elif newMaxLevel< self.inputSize:
            combinations = genCombinations(self.acceptedConfigurations[-1], newMaxLevel)
            possibleConfigurations = []
            for combination in combinations:
                possibleConfiguration = self.bitMask
                for configuration in combination:
                    possibleConfiguration &= configuration
                if getConfigurationLevel(self.inputSize, possibleConfiguration) == newMaxLevel:
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
                children.append( DedekindNode(self.inputSize, combination, self))
                
        return children
    
    def __iter__(self):
        '''
        Implemented this with good design in mind, however
        If you want something fast, it is better to use
        getAcceptedConfigurationsAsList
        '''
        return DedekindNodeIter(self)
    
    def getLastLevel(self):
        if len(self.acceptedConfigurations) > 0:
            return self.acceptedConfigurations[-1]
        else:
            return []
    
    def writeToDotFile(self, writeLocation):
        global fullNodes, configurationLabelss, dotEdgess
        
        dotFileName = os.path.join(writeLocation, "n_" + str(self.inputSize)\
                                   + "." + "world_" + str(getIndex(self.getAcceptedConfigurationsAsList()))\
                                   + ".dot")
        dotFile = open( dotFileName, "w")
        dotFile.write("""digraph{
        rankdir=BT
        node[shape=circle, style=filled, label=""]
        edge[dir=none]\n""")
        
        initDotVariables(self.inputSize)
        fullNode = fullNodes[self.inputSize]
        configurationLabels = configurationLabelss[self.inputSize]
        dotEdges = dotEdgess[self.inputSize]
        
        #configurationList = self.getAcceptedConfigurationsAsList()
        for configuration in fullNode:
            if configuration in self:
                dotFile.write( configurationLabels[configuration] +" [ color = green, "\
                               + "label = \""+ configurationLabels[configuration] + "\"]\n")
            else:
                dotFile.write( configurationLabels[configuration] +" [ color = red, "\
                               + "label = \""+ configurationLabels[configuration] + "\"]\n")
                    
        dotFile.write(dotEdges)
        dotFile.write("}")
        
        dotFile.close()
                 
def isConsistent(node, configuration):
    '''
    Checks if a configuration would be deemed "inconsistent".
    This is confusing! The DedekindNode represents a faulty system, and the
    "accepted configurations" represent sets such that, if you deemed the given
    components (represented by bits) as "faulty" and all others as safe, you would explain 
    erroneous output.
    '''
    from sets import ImmutableSet
    if isinstance(configuration, ImmutableSet):
        configuration = getConfAsInt(configuration, node.inputSize)
    if (getIndex(node.getAcceptedConfigurationsAsList()) & 1 << configuration ) == 0:
        return False
    else:
        return True
    
def getFullNode(inputSize):
    global fullNodes
    if inputSize not in fullNodes:
        bitMask = (1<<inputSize) - 1
        configurations = range(0, bitMask + 1)
        configurations = sorted(configurations, key = lambda configuration: getConfigurationLevel(inputSize, configuration))  
        fullNodes[inputSize] = DedekindNode(inputSize, configurations)
        
    return fullNodes[inputSize]

def initDotVariables(inputSize):
    global fullNodes, configurationLabelss, dotEdgess
    '''
    Helper function used to set up variables used for writing
    a Dedekind Node to a dot file.
    '''
    bitMask = (1<<inputSize) - 1
    if inputSize in fullNodes:
        return
    configurationLabels = {}
    dotEdges = ""
    
    #Take accepted configurations as integers and convert them to binary strings for labeling
    configurations = range(0, bitMask + 1)
    configurations = sorted(configurations, key = lambda configuration: getConfigurationLevel(inputSize, configuration))
    fullNode = DedekindNode(inputSize, configurations)
    for configurationLevel in fullNode.acceptedConfigurations:
        for configuration in configurationLevel:
            configurationLabels[configuration] = bin(configuration + bitMask+1)[3:]
           
    for levelIndex in range(1, len(fullNode.acceptedConfigurations) ):
        for configuration in fullNode.acceptedConfigurations[levelIndex]:
            for parentConfiguration in fullNode.acceptedConfigurations[levelIndex - 1]:
                if hamming_distance(configuration, parentConfiguration) == 1:
                    edgeString = configurationLabels[parentConfiguration] + " -> " \
                        + configurationLabels[configuration] + "\n"
                    dotEdges += edgeString
                    
    fullNodes[inputSize] = fullNode
    configurationLabelss[inputSize] = configurationLabels
    dotEdgess[inputSize] = dotEdges
    
def getIndex(configurationList):
    '''
    If we treat each configuration as its own integer value, we can combine each value into an integer
    of size 2**inputSize bits. E.G. if the input size is 4, then each configuration has a value between 0-15.
    So an integer of 16 bits, where each bit is for each configuration, will represent the function
    and its accepted configurations. Since this value is unique, we can also use it as an index for the function
    '''
    index = 0
    for configuration in configurationList:
        index |= (1 << configuration) 
            
    return index

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