'''
Created on Apr 2, 2015
@author: Solaman
'''
import unittest
from Model.DedekindSetMapping import DedekindSetMapping
        
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