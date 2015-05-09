'''
Created on Apr 28, 2015

@author: Solaman

Used to perform analysis on various
algorithms for computing Minimum Inconsistent Subsets.
'''
from Algorithms.Hitting_Set_Tree import HittingSetTree
from Algorithms.Random import Random
from Algorithms.BottomUp import BottomUp
from Algorithms.TopDown import TopDown

from Model.DedekindLattice import DedekindLattice
from Model.DedekindSetMapping import getFullSet, getConfAsSet

algorithms = {}
algorithms["hitting_set_tree"] = HittingSetTree.computeAllMIS
algorithms["random"] = Random.computeAllMIS
algorithms["bottom_up"] = BottomUp.computeAllMIS
algorithms["top_down"] = TopDown.computeAllMIS
isAcceptedOriginalFunction = None 


def runAnalysis(args):
    if len(args) != 2:
        print "must provide an algorithm and input size!"
        return
    algorithmKey = args[0]
    if algorithmKey not in algorithms:
        print "sorry! That algorithm was not recognized."\
        , "\nHere are the options:"
        for _algorithmKey in algorithms.keys():
            print "\n\t", _algorithmKey
        return
    algorithm = algorithms[algorithmKey]
    
    if int(args[1]) >5:
        print "input larger than 5 is terribly slow, don't do it!"
        return
    inputSize = int(args[1])
    lattice = DedekindLattice(inputSize)
    callCounts = {}
    
    
    while True:
        currentNode = lattice.getNextNode()
        
        if currentNode == None:
            break
        
        modifyisAccepted(currentNode)
        fullConstraints = getFullSet(inputSize)
        algorithm(currentNode, fullConstraints)
        
        if currentNode.callCount not in callCounts:
            callCounts[currentNode.callCount] = 1
        else:
            callCounts[currentNode.callCount] += 1
        
    
    printStatistics(callCounts)
            
def printStatistics(callCounts):
    print "min: ", min ( callCounts.keys())
    print "max: ", max( callCounts.keys())
    
    totalAlgorithmCalls = sum( callCounts.values())
    totalIsConsistentCalls = 0
    for key in callCounts.keys():
        totalIsConsistentCalls += key * callCounts[key]
        
    print "mean: ", totalIsConsistentCalls/ totalAlgorithmCalls
    
    mean = totalIsConsistentCalls/ totalAlgorithmCalls
    variance = 0.0
    for key in callCounts:
        variance += (callCounts[key] - mean)**2
    variance = float(variance)/float(totalAlgorithmCalls)
    
    print "standard deviation: ", variance **.5
    medianCount = totalAlgorithmCalls/2
    for key in callCounts.keys():
        medianCount -= callCounts[key]
        if medianCount <= 0:
            print "median: ", key
            break
        
    print "mode: ", max( callCounts.keys(), key= lambda x: callCounts[x])
      
def modifyisAccepted(setDescription):
    '''
    In order to properly analyze an algorithm, we need to check how
    many times it has to call "isAccepted" on the given setDescription.
    We make this modification here.
    '''
    
    setDescription.callCount = 0
    setDescription.tries = []
    import types
    setDescription.isConsistent = types.MethodType(isConsistent, setDescription)
    
    

  
def isConsistent(self, configuration):
    from Model.DedekindNode import isConsistent as isConsistentOld
    self.callCount += 1
    return isConsistentOld(self, configuration)  
    
