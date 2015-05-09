'''
Created on Apr 23, 2015

@author: Solaman
'''
from LogarithmicExtraction import computeSingleMIS
import LogarithmicExtraction
from sets import ImmutableSet

def computeAllMIS(setDescription, constraints):
    '''
    Taken from 'A Hybrid Diagnosis Approach Combining Black-Box
    and White-Box Reasoning'. This attempts to find all Minimal Subset of Constraints
    that will be inconsistent for the given Set Description.
    @param setDescription- A set of rules linking several items together. 
    Think of this as boolean equation in Conjunctive Normal Form.
    @param Constraints- a set of items we would like to include.
    Think of this as an assignment for the previous boolean equation.
    '''
    misSet= set()
    currPath = ImmutableSet() 
    paths = set()
    LogarithmicExtraction.newRun = True
    computeAllMISHelper(setDescription, constraints,
                                   misSet, currPath, paths)
    return misSet
    
def computeAllMISHelper(setDescription, constraints, misSet, currPath, paths):
    #paths holds all previously visited paths of the hitting set tree
    #currPath is the current. If any previous path is a subset of this one
    #the we have already computed all MIS that would be found in the current path's subtree.
    for path in paths:
        if path in currPath:
            return
       
    #if the current set of constraints is consistent
    #Then there cannot be anymore MIS in its subtree
    #so we add the current path to the set of paths enumerated and return. 
    if not setDescription.isConsistent(constraints):
        paths.add(currPath)
        return
    #In order to avoid redundant MIS computations
    #We check the current set of MIS misSet
    #If it is possible to find any of the already computed MIS in the current iteration
    #(it does not share an element in the currPath) then we just use that MIS
    #and continue down the tree
    currentMIS = ImmutableSet()
    for mis in misSet:
        if len(mis.intersection(currPath)) == 0:
            currentMIS = mis
            break
    #If not MIS matches the previous description, we will need to 
    #compute a new one.
    if currentMIS == ImmutableSet():
        currentMIS = computeSingleMIS(setDescription, constraints)
        misSet.add(currentMIS)
        
    #iterate through the children of the current path
    for element in currentMIS:
        childPath = currPath.union( set(element))
        computeAllMISHelper(setDescription, constraints - ImmutableSet(element), misSet, childPath, paths)
        
import sets
def computeAllJust(setDescription, artSet, justSet, curpath, allpaths):
    '''
    Implementation of Hitting Set Tree found directly from EulerX.
    A few modifications are made to ensure that it is compatible with this library's
    implementation of logarathmic Extraction, otherwise everything else is the same
    '''
    for path in allpaths:
        if path.issubset(curpath):
            return
    #must be 'not' to be consistent with this library's implementation. 
    #Without it, it does not compute the MIS properly
    #i.e. it does not pass any of the algorithm tests.
    if not setDescription.isConsistent(artSet):
        allpaths.add(curpath)
        return
    j = sets.Set()
    for s in justSet:
        if len(s.intersection(curpath)) == 0:
            j = s
    if len(j) == 0:
        j = computeSingleMIS(setDescription, artSet)
    if len(j) != 0:
        justSet.add(j)
    for a in j:
        tmpcur = curpath.union( set(a))
        tmpart = artSet - ImmutableSet(a)
        computeAllJust(setDescription, tmpart, justSet, tmpcur, allpaths) 
