'''
Created on May 4, 2015

@author: Solaman
'''
from sets import ImmutableSet

def computeAllMIS(setDescription, constraints):
    '''
    Finds the Minimum Inconsistent Subsets for the given constraints and set Description
    using a bottom up approach (where bottom is empty set). We check the powerset of constraints, and rule out possible
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
    while len(setsToCheck) > 0:
        checkNextSet(setsToCheck,  misSet, setDescription)
        
    return misSet
       
       
def checkNextSet(setsToCheck, misSet, setDescription):
    '''
    Takes the smallest set of possible MIS and finds its parents. Then checks if it is consistent.
    If it is, then it is an MIS and we should rule out all of its parents.
    If it is not, then we rule it out as a possible MIS.
    '''
    parentSets = set()
    
    chosenSet = setsToCheck.pop()
    setsToCheck.add(chosenSet)
    for aSet in setsToCheck:
        if len(chosenSet) > len(aSet):
            chosenSet = aSet
            
    for possibleParent in setsToCheck:
        if possibleParent.issuperset(chosenSet) and possibleParent != chosenSet:
            parentSets.add(possibleParent)
            
    if setDescription.isConsistent(chosenSet):
        misSet.add(chosenSet)
        for parentSet in parentSets:
            setsToCheck.remove(parentSet)
        
    setsToCheck.remove(chosenSet)      
    


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