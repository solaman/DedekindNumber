'''
Created on May 4, 2015

@author: Solaman

We note that each test is essentially the same; can it find the correct MIS?
Being that this is the case, we just run the same test for all algorithms.
'''
import unittest
from Model.DedekindNode import DedekindNode, getFullNode
from Algorithms.Hitting_Set_Tree import HittingSetTree
from Algorithms.Random import Random
from Algorithms.BottomUp import BottomUp
from Algorithms.TopDown import TopDown

from Model.DedekindSetMapping import getFullSet
from Model.DedekindSetMapping import getConfAsSet
from sets import ImmutableSet


class Test(unittest.TestCase):


    def setUp(self):
        self.dedekindNode = DedekindNode(6, [63, 62,47, 31, 55, 46, 30, 15,23, 14 ])
        self.answerSet = set()
        self.answerSet.add( ImmutableSet( getConfAsSet(14, 6) ) )
        self.answerSet.add( ImmutableSet( getConfAsSet(23, 6)))
        
        self.fullNode = getFullNode(6)
        self.fullAnswerSet = set()
        self.fullAnswerSet.add(ImmutableSet())
        
        self.emptyNode = DedekindNode(6, [])
        self.emptyAnswerSet = set()


    def tearDown(self):
        pass


    def testHittingSetTree(self):
        answer = HittingSetTree.computeAllMIS(self.dedekindNode, getFullSet(6))
        self.assertEquals( answer, self.answerSet)
        
    def testRandom(self):
        answer = Random.computeAllMIS(self.dedekindNode, getFullSet(6))
        self.assertEquals( answer, self.answerSet)
        
    def testTopDown(self):
        answer = TopDown.computeAllMIS(self.dedekindNode, getFullSet(6))
        self.assertEquals( answer, self.answerSet)
    
        
    def testBottomUp(self):
        answer = BottomUp.computeAllMIS(self.dedekindNode, getFullSet(6))
        self.assertEquals( answer, self.answerSet)
        
    def testHittingSetTreeFullNode(self):
        answer = HittingSetTree.computeAllMIS(self.fullNode, getFullSet(6))
        self.assertEquals( answer, self.fullAnswerSet)
        
    def testRandomFullNode(self):
        answer = Random.computeAllMIS(self.fullNode, getFullSet(6))
        self.assertEquals( answer, self.fullAnswerSet)
        
    def testTopDownFullNode(self):
        answer = TopDown.computeAllMIS(self.fullNode, getFullSet(6))
        self.assertEquals( answer, self.fullAnswerSet)
        
    def testBottomUpFullNode(self):
        answer = BottomUp.computeAllMIS(self.fullNode, getFullSet(6))
        self.assertEquals( answer, self.fullAnswerSet)
        
    def testHittingSetTreeEmptyNode(self):
        answer = HittingSetTree.computeAllMIS(self.emptyNode, getFullSet(6))
        self.assertEquals( answer, self.emptyAnswerSet)
        
    def testRandomEmptyNode(self):
        answer = Random.computeAllMIS(self.emptyNode, getFullSet(6))
        self.assertEquals( answer, self.emptyAnswerSet)
        
    def testTopDownemptyNode(self):
        answer = TopDown.computeAllMIS(self.emptyNode, getFullSet(6))
        self.assertEquals( answer, self.emptyAnswerSet)
        
    def testBottomUpemptyNode(self):
        answer = BottomUp.computeAllMIS(self.emptyNode, getFullSet(6))
        self.assertEquals( answer, self.emptyAnswerSet)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()