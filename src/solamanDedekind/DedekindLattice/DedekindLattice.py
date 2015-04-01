'''
Created on Feb 26, 2015

@author: Solaman
'''
import TransitionError
from DedekindNode import DedekindNode

class DedekindLattice(object):
    '''
    We aim to generate the Dedekind Lattices using this class. Namely,
    We want to generate all monotone boolean functions given an n input size.
    Currently, we will aim to only generate the lattices in working memory.
    Future implementations will hopefully be able to dynamically
    Generate a node of a given Lattice.
    '''


    def __init__(self, inputSize):
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
        self.lattice[ self.emptyFunction.getIndex()] = self.emptyFunction
        
        self.baseFunction = DedekindNode(self.inputSize, [self.bitMask])
        self.lattice[ self.baseFunction.getIndex()] = self.baseFunction
        
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
            self.lattice[child.getIndex()] = child
        return node
        
        
    def fillLattice(self):
        self.nodeList = []
        self.nodeList.append(self.baseFunction)
        while self.getNextNode() != None:
            x = 1
        self.monotoneCount= len( self.lattice.values())
            
    def findUniqueFunctions(self):
        #We don't need to compute functions that are isomorphisms of each other.
        #We store each function by there level, and then counts by the number of possible children for the function
        #It is proven that functions by level that have the same number of possible children are isomorphisms
        #{"level" : {"isomorphismCount": count, "children" : children } }
        self.nodeList = []
        functionCount = 1
        self.childrenCounts = {}
        
        self.baseFunction.isVisited = False
        self.baseFunction.parent = None
        self.nodeList.append(self.baseFunction)
        
        while self.nodeList != []:
            node = self.nodeList.pop()
            if node.isVisited == True:
                if node.parent == None:
                    functionCount += node.childrenCount
                    print functionCount
                    continue
                else:
                    node.parent.childrenCount += node.childrenCount
                    key = self.getKey(node)
                    self.childrenCounts[ node.level][key] = node.childrenCount
                    continue
            
            node.level = len(node.acceptedConfigurations) - 1
            if node.level not in self.childrenCounts:
                self.childrenCounts [ node.level] = {}
            
            node.possibleConfigurations = node._generatePossibleConfigurations()
            node.possibleConfigurationSize = len(node.possibleConfigurations)
            key = self.getKey(node)
            if key in self.childrenCounts[node.level]:
                node.parent.childrenCount += self.childrenCounts[node.level][ key]
            else:
                children = node.generateChildren()
                node.childrenCount = 1
                node.isVisited = True
                self.nodeList.append(node)
                for child in children:
                    child.parent = node
                    child.isVisited = False
                    self.nodeList.append(child)
        
    def getKey(self, node):
        return str(len(node.acceptedConfigurations[node.level])) + "-" + str(node.possibleConfigurationSize)
                    
            
            
            
           
    def generateDotFiles(self):
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
        


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Error: must provide the input size of the Dedekind Lattice"
    inputSize = sys.argv[1]
    dedekind = DedekindLattice(int(inputSize))
    dedekind.fillLattice()
    
    if len(sys.argv) > 2:
        if sys.argv[2] == "true":
            dedekind.generateDotFiles()
    print dedekind.monotoneCount