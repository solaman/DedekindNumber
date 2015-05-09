'''
Created on May 4, 2015

@author: Solaman
'''
from sets import ImmutableSet

def computeAllMIS(setDescription, constraints):
    '''
    Finds the Minimum Inconsistent Subsets for the given constraints and set Description
    using a top down approach (where top is full set). We check the powerset of constraints, and rule out possible
    MIS based on whether or not a given set is consistent.
    NOTE: There are probably far more optimal implementations of such an algorithm. However,
    for the sake of comparison, we are only interested in the number of times
    'isConsistent' is called and so we refrain from these optimizations.
    @param setDescription- A set of rules linking several items together. 
    Think of this as boolean equation in Conjunctive Normal Form.
    @param Constraints- a set of items we would like to include.
    Think of this as a value assignment for the previous boolean equation.
    '''
    
    setsToCheck = generatePowerset(constraints)
    misSet = set()
    findMISSets(setsToCheck,  misSet, setDescription)
        
    return misSet
       
       
def findMISSets(setsToCheck, misSet, setDescription):
    '''
    Takes the largest set from potential MIS and find its children. Check if it is consistent
    If it is, and it has children, then rule it out as an MIS, else add it to the MIS
    If it is not, then rule it and its children out as MIS.
    '''
    setsToCheckList = list(setsToCheck)
    setsToCheckList.sort(key = lambda self: len(self), reverse = True)
    
    for currentSet in setsToCheckList:
        if currentSet not in setsToCheck:
            continue
        childrenSets = set()
        parentSets = set()
        for aSet in setsToCheck:
            if aSet.issubset(currentSet) and aSet != currentSet:
                childrenSets.add(aSet)
            
            if aSet.issuperset(currentSet) and aSet != currentSet:
                parentSets.add(aSet)
        
        if not setDescription.isConsistent(currentSet):
            for child in childrenSets:
                setsToCheck.remove(child)
            setsToCheck.remove(currentSet)
        else:
            for parent in parentSets:
                setsToCheck.remove(parent)
            
    for currentSet in setsToCheckList:
        if currentSet in setsToCheck:
            misSet.add(currentSet)    
    
def generatePowerset(theSet): 
    '''
    Generates powerset of a given set.
    Original code found at http://stackoverflow.com/questions/18826571/python-powerset-of-a-given-set-with-generators
    '''
    powerSet = set()
    from itertools import chain, combinations
    for subset in chain.from_iterable(combinations(theSet, r) for r in range(len(theSet)+1)):
        powerSet.add( ImmutableSet(subset))
    return powerSet