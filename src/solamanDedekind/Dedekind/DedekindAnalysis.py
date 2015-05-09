'''
Created on Mar 13, 2015

@author: Solaman
'''
import cProfile
from Model.DedekindNode import DedekindNode
from Model.DedekindLattice import DedekindLattice

node = DedekindNode(4, [15])
lattice = DedekindLattice(5, lean = True)

def analyzeDedekindNode():
    cProfile.run("node.generatePossibleConfigurations()")
    
def analyzeFindUniqueFunctions():
    cProfile.run("lattice.getDedekindNumber()")
    
if __name__ == '__main__':
    #analyzeDedekindNode()
    #analyzeDedekindLattice()
    analyzeFindUniqueFunctions()