'''
Created on Feb 26, 2015

@author: Solaman
'''
from DedekindNode import DedekindNode
from Model.LevelPermutor import LevelPermutor
from DedekindNode import getIndex

class LatticeFiller(object):
    '''
    Constructed when the Lattice is constructed if the user wants to fill in the 
    lattice with each Monotone Boolean Function individually.  
    This class provides a level of abstraction from the inner workings of the module.
    '''
    def __init__(self, lattice):
        self.lattice = lattice
        self.nodeList = []
        self.nodeList.append(lattice.emptyFunction)
        self.nodeList.append(lattice.baseFunction)
        self.wasFilled = False
        
    def getNextNode(self):
        '''
        Returns the most recently added node to the queue 
        if it is not empty.
        '''
        if self.nodeList == []:
            return None
        node = self.nodeList.pop()
        children = node.generateChildren()
        for child in children:
            self.nodeList.append(child)
            self.lattice.lattice[getIndex(child)] = child
        return node
    
    def fillLattice(self):
        while self.getNextNode() != None:
            continue
        
    def getDedekindNumber(self):
        if self.wasFilled == False:
            self.fillLattice()
        self.wasFilled = True
        return len(self.lattice.lattice.values())
        
class LatticeFillerUnique(object):
    '''
    Constructed when the Lattice is constructed if the user would like to fill in
    the lattice with Monotone Boolean Functions that are equivalent by level.
    This class provides a level of abstraction from the inner workings of the module.
    '''
    def __init__(self, lattice, lean= False):
        from Model.DedekindNodeLean import DedekindNodeLean
        if lean == True:
            lattice.baseFunction = DedekindNodeLean(lattice.baseFunction.inputSize,\
                                                    lattice.baseFunction.acceptedConfigurations[-1])
            
        self.lattice = lattice
        self.nodeList = []
        lattice.emptyFunction.isVisited = False
        lattice.emptyFunction.parent = None
        self.nodeList.append(lattice.emptyFunction)
        lattice.baseFunction.isVisited = False
        lattice.baseFunction.parent = None
        self.nodeList.append(lattice.baseFunction)
        self.levelPermutor = LevelPermutor(lattice.inputSize)
        self.mileMarker = 10000
        
        self.wasFilled = False
        
    def getNextNode(self):
        #We don't need to compute functions that are isomorphisms of each other.
        #We store each function by there level, and then counts by the number of possible children for the function
        #It is proven that functions by level that have the same number of possible children are isomorphisms
        #{"level" : {"isomorphismCount": count, "children" : children } }
        if self.nodeList == []:
            return None
        node = self.nodeList.pop()
        if node.isVisited == True:
            if node.parent == None:
                return node
            else:
                node.parent.childrenCount += node.childrenCount
                if node.parent.childrenCount >= self.mileMarker:
                    print "marker: ", self.mileMarker
                    self.mileMarker = node.parent.childrenCount * 2
                return self.getNextNode()
        
        if self.getKey(node) in self.levelPermutor:
            node.parent.childrenCount += self.levelPermutor[self.getKey(node)].childrenCount
            return self.getNextNode()
        else:
            self.lattice.lattice[ getIndex(node.getAcceptedConfigurationsAsList()) ] = node
            node.childrenCount = 1
            self.levelPermutor[node.getLastLevel()] = node
            children = node.generateChildren()
            node.isVisited = True
            self.nodeList.append(node)
            for child in children:
                child.parent = node
                child.isVisited = False
                self.nodeList.append(child)
            return node
        
    def getKey(self, node):
        if hasattr(node, "key"):
            return node.key
        else:
            node.key = getIndex(node.getLastLevel())
        return node.key
        
    def fillLattice(self):
        while self.getNextNode() != None:
            continue
        
    def getDedekindNumber(self):
        if self.wasFilled == False:
            self.fillLattice()
        self.wasFilled = True
        return self.lattice.baseFunction.childrenCount + 1
        
class DedekindLattice(object):
    '''
    We aim to generate the Dedekind Lattices using this class. Namely,
    We want to generate all monotone boolean functions given an n input size.
    Currently, we will aim to only generate the lattices in working memory.
    Future implementations will hopefully be able to dynamically
    Generate a node of a given Lattice.
    '''

    def __init__(self, inputSize, generateUnique = True, lean = False):
        '''
        Constructor. For now, we will store each monotone boolean function
        as an object. Future implementations will store them as a single bit
        for lean memory usage
        '''
        if inputSize < 0:
            raise Exception("Input size must be greater than or equal to 0")
        self.lattice = {}
        
        #bit mask refers to the possible bit values
        #of a given configuration. E.G. boolean functions with 4 inputs
        #Will have a bit mask of 0xF
        self.bitMask = 2**(inputSize) - 1
        self.inputSize = inputSize
        
        self.emptyFunction = DedekindNode(self.inputSize, [])
        self.lattice[ getIndex(self.emptyFunction)] = self.emptyFunction
        
        self.baseFunction = DedekindNode(self.inputSize, [self.bitMask])
        self.lattice[ getIndex(self.baseFunction)] = self.baseFunction
        
        if generateUnique:
            self.latticeFiller = LatticeFillerUnique(self, lean)
            
        else:
            self.latticeFiller = LatticeFiller(self)
            
    def getDedekindNumber(self):
        return self.latticeFiller.getDedekindNumber()
    
    def getNextNode(self):
        return self.latticeFiller.getNextNode()
                    
                  
    def generateDotFiles(self):
        '''
        
        '''
        import os
        directoryName = os.path.join("GeneratedDedekindLattices", str(self.inputSize) + "_DedekindLattice")
        if not os.path.exists(directoryName):
            os.mkdir(directoryName)
        updateTime = self.monotoneCount/10
        generatedFiles = 0
        for function in self.lattice.itervalues():
            function.writeToDotFile(directoryName)
            generatedFiles += 1
            if generatedFiles % updateTime == 0:
                print generatedFiles, " written so far"
        print "Done"
        

def getDedekindNumber(userInput):
    '''
    Constructs the Dedekind Lattice for the given input size and 
    returns the dedekind number associated with that input.
    Values that return within a minute are currently n <= 5.
    '''
    inputSize = int(userInput[0])
    dedekindLattice = DedekindLattice(inputSize, lean =True)
    print dedekindLattice.getDedekindNumber()
    
def generateDotFiles(userInput):
    '''
    Constructs the Dedekind Lattice for the given input size and
    generates the dot files for each monotone boolean function with the given input size.
    '''
    inputSize = int(userInput[0])
    dedekindLattice = DedekindLattice(inputSize)
    dedekindLattice.fillLattice()
    dedekindLattice.generateDotFiles()