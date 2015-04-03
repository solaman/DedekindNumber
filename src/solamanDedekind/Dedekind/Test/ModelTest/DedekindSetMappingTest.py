'''
Created on Apr 2, 2015

@author: Solaman
'''
import unittest
import mock
from Model.DedekindSetMapping import DedekindSetMapping
from mock import mock_open, patch
from pandas.util.testing import assertRaises

class FakeFile(object):
        def __init__(self):
            pass
        def readAll(self):
            return "A,B,C,D,E,F,G"
        
class Test(unittest.TestCase):
        
    def setUp(self):
        self.setMapping = DedekindSetMapping(4)


    def tearDown(self):
        pass


    def testGetConfAsSet(self):
        getSetResult = self.setMapping.getConfAsSet(9)
        self.assertEquals(set({'A', 'D'}), getSetResult)
        
    def testGetConfAsInt(self):
        getSetResult = self.setMapping.getConfAsInt( set({'A', 'D'}))
        self.assertEquals(9, getSetResult)
        
    def testGetConfAsSetBadConf(self):
        self.assertRaises(Exception, self.setMapping.getConfAsSet(2<<9))
        
    def testGetConfAsIntBadConf(self):
        self.assertRaises(Exception, self.setMapping.getConfAsInt( set('BAD')))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()