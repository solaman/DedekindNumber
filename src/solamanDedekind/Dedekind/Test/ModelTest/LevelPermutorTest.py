'''
Created on Apr 13, 2015

@author: Solaman
'''
import unittest
from Model.LevelPermutor import LevelPermutor
from astropy.io.ascii.core import IntType


class Test(unittest.TestCase):

    def setUp(self):
        self.levelPermutor = LevelPermutor(4)

    def testPut(self):
        intObject = IntType()
        self.levelPermutor[ [3, 6]] = intObject
        self.assertTrue( self.levelPermutor[[3, 6]] is intObject)
        self.assertTrue( self.levelPermutor[[5, 6]] is intObject)
        self.assertTrue( self.levelPermutor[[3, 5]] is intObject)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()