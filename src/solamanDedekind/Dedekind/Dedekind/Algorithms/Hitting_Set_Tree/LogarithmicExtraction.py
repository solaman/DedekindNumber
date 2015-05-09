'''
Created on Apr 23, 2015

@author: Solaman
'''
import random
from sets import ImmutableSet

#to avoid checking the empty set as an MIS more than once for
#a given set description, an algorithm can set this to "True" before calling.
#This way the Logarithmic Extraction will know that the check is not excessive
newRun = False

def computeSingleMIS(setDescription, constraints):
    '''
    Taken from 'A Hybrid Diagnosis Approach Combining Black-Box
    and White-Box Reasoning'. This attempts to find the Minimal Subset of Constraints
    that will be inconsistent for the given Set Description.
    @param setDescription- A set of rules linking several items together. 
    Think of this as boolean equation in Conjunctive Normal Form.
    @param Constraints- a set of items we would like to include.
    Think of this as a value assignment for the previous boolean equation.
    '''
    potentialMIS = computeSingleMISHelper(setDescription, ImmutableSet(), constraints)
    
    #The Euler Implentation does not correctly compute the MIS for a set description
    #where everything is always inconsistent (an empty set is inconsistent)
    #This makes sense, but this library also considers this set description,
    #so we must check the empty configuration here.
    global newRun
    if newRun == True and len(potentialMIS) == 1 \
        and setDescription.isConsistent(ImmutableSet()):
        newRun = False
        return ImmutableSet()
    else:
        newRun = False
        return potentialMIS

def computeSingleMISHelper(setDescription, currentConstraints, constraintsToAdd):
    if len(constraintsToAdd) <= 1:
        return constraintsToAdd
    
    constraintsToAddLeft = ImmutableSet(random.sample(constraintsToAdd, len(constraintsToAdd)/2))
    constraintsToAddRight = constraintsToAdd - constraintsToAddLeft
    
    #If either subset unioned with the current constraints is inconsistent
    #then an MIS exists in the subset of them
    if setDescription.isConsistent( currentConstraints.union(constraintsToAddLeft) ):
        return computeSingleMISHelper(setDescription, currentConstraints, constraintsToAddLeft)
    if setDescription.isConsistent( currentConstraints.union(constraintsToAddRight)):
        return computeSingleMISHelper(setDescription, currentConstraints, constraintsToAddRight)
    
    #If both subsets unioned with the current constraints is consistent
    #Then an MIS of the current constraints must use elements from both subsets. 
    #This will find such an MIS
    potentialSolutionLeft = computeSingleMISHelper(setDescription, 
                                                   currentConstraints.union(constraintsToAddRight), constraintsToAddLeft)
    potentialSolutionRight = computeSingleMISHelper(setDescription,
                                                    currentConstraints.union(potentialSolutionLeft), constraintsToAddRight)
    return potentialSolutionLeft.union(potentialSolutionRight)    