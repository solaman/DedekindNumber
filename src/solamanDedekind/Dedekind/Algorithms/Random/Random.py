'''
Created on May 4, 2015

@author: Solaman
'''
from sets import ImmutableSet
checkedMap = {}

def computeAllMIS(setDescription, constraints):
    '''
    Finds the Minimum Inconsistent Subsets for the given constraints and set Description
    using a randomized approach. We check the powerset of constraints, and rule out possible
    MIS based on whether or not a given set is consistent.
    NOTE: There are probably far more optimal implementations of such a random algorithm. However,
    for the sake of comparison, we are only interested in the number of times
    'isConsistent' is called and so we refrain from these optimizations.
    @param setDescription- A set of rules linking several items together. 
    Think of this as boolean equation in Conjunctive Normal Form.
    @param Constraints- a set of items we would like to include.
    Think of this as a value assignment for the previous boolean equation.
    '''
    global checkedMap
    checkedMap = {}
    setsToCheck = generatePowerset(constraints)
    misSet = set()
    while len(setsToCheck) > 0:
        checkRandomSet(setsToCheck,  misSet, setDescription)
        
    return misSet
       
       
def checkRandomSet(setsToCheck, misSet, setDescription):
    '''
    Takes a random set from the possible sets available and first finds its parent and children sets.
    If it has none, then we know it is an MIS and add it to our solution.
    If it has some, then we check if it is consistent and rule out the respective sets.
    '''
    global checkedMap
    import random
    chosenSet = random.sample(setsToCheck, 1)[0]
    parentSets = set()
    childrenSets = set()
    
    for aSet in setsToCheck:
        if chosenSet == aSet:
            continue
        elif aSet.issubset(chosenSet):
            childrenSets.add(aSet)
        elif aSet.issuperset(chosenSet):
            parentSets.add(aSet)
            
    if chosenSet in checkedMap:
        if len(parentSets) + len(childrenSets) == 0:
            setsToCheck.remove(chosenSet)
            misSet.add(chosenSet)
            return
    else:
        if setDescription.isConsistent(chosenSet):
            #If consistent, then all parents are consistent and also not MIS
            for aSet in parentSets:
                setsToCheck.remove(aSet)
        else:
            #If inconsistent, then all children including this one are inconsistent and also not MIS
            for aSet in childrenSets:
                setsToCheck.remove(aSet)
            setsToCheck.remove(chosenSet)
        checkedMap[chosenSet] = 1
            
    


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