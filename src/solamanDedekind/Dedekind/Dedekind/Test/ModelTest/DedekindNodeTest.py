'''
Created on Mar 3, 2015

@author: Solaman
'''
import unittest
from Model.DedekindNode import DedekindNode
from Model.DedekindNode import getIndex

class Test(unittest.TestCase):

    
    def setUp(self):
        self.invalidConfigurations = [15, 14, 13, 4 ]
        self.unorderedConfigurations = [14, 13, 15]
        self.orderedConfigurationsByLevel = [ [15], \
                                             [14, 13] \
                                             ]
        self.orderedConfigurations = [15, 14, 13]
        self.levelOneConfigurations = [ 14, 13, 11, 7]

        self.dedekindNode = DedekindNode(4, self.orderedConfigurations)

    def tearDown(self):
        pass
    
    def testGeneratePossibleConfigurationsFullLevel(self):
        '''
        Given that we have all combinations of a level k,
        Do we get all combinations at level k+1?
        (here, input size n=4, so we have k=2 and k+1=3)
        '''
        configurationsUpToLevel3 = [15, 14, 13, 11, 7, 10, 12, 6, 5, 9, 3]
        node = DedekindNode(4, configurationsUpToLevel3)
        possibleCombinations = node._generatePossibleConfigurations()
        self.assertEquals(set(possibleCombinations), set([8, 4, 2, 1]))
        
    def testGeneratePossibleConfigurationsSatisfiedLevelNoOutput(self):
        '''
        When at level k, possible level k+1 configurations are a boolean
        "and" of k+1 of the level k configurations such that they  belong 
        at level k+1. E.G.
        11100 &
        00111 &
        01110 =
        00100
        Which is not a valid k+1 configuration, so it is not included
        '''
        configurations = [31, 30, 29, 27, 23, 15, 28, 7, 14]
        node = DedekindNode(5, configurations)
        possibleCombinations = node._generatePossibleConfigurations()
        self.assertEquals(possibleCombinations, [])
        
    def testGeneratePossibleConfigurationsSatisfiedLevelOutput(self):
        '''
        When at level k, possible level k+1 configurations are a boolean
        "and" of k+1 of the level k configurations such that they  belong 
        at level k+1. E.G.
        11100 &
        01110 &
        01101 =
        01100
        Which is a valid k+1 configuration, so it should be included
        '''
        configurations = [31, 30, 29, 27, 23, 15, 28, 14, 13]
        node = DedekindNode(5, configurations)
        possibleCombinations = node._generatePossibleConfigurations()
        self.assertEquals(possibleCombinations, [12])
        
        configurations= [31, 30, 29, 27, 23, 15, 28, 7, 14, 22, 13 ]
        node = DedekindNode(5, configurations)
        possibleCombinations = node._generatePossibleConfigurations()
        self.assertEquals( set(possibleCombinations), set([12, 6]))
        
    def testGenerateChildren(self):
        '''
        Because GenerateChildren relies on generatePossibleConfigurations,
        it is sufficient to test that, given that there are more than one child
        they are generated
        '''
        configurations = [31, 30, 29, 27, 23, 15, 28, 7, 14, 22, 13 ]
        node = DedekindNode(5, configurations)
        children = node.generateChildren()
        children = sorted(children, key = lambda child: getIndex(child))
        self.assertEquals( set(children[0].acceptedConfigurations[-1]), set([6]))
        self.assertEquals( set(children[1].acceptedConfigurations[-1]), set([12]))
        self.assertEquals( set(children[2].acceptedConfigurations[-1]), set([6, 12]))
        
        
    def testGetLevelOneConfigurations(self):
        from Model.DedekindNode import getLevelOneConfigurations
        self.assertEquals(getLevelOneConfigurations(self.dedekindNode.inputSize), self.levelOneConfigurations)

    def testGetIndex(self):
        self.assertEquals(getIndex(self.dedekindNode), 57344)
        
    def testIsConsistent(self):
        configurations = [31, 30, 29, 27, 23, 15, 28, 7, 14, 22, 13 ]
        node = DedekindNode(5, configurations)
        self.assertTrue(node.isConsistent(29))
        self.assertFalse(node.isConsistent(8))
        
        
#     def testUnorderedConfigurations(self):
#         dedekindNode = DedekindNode( 4, self.unorderedConfigurations)
#         self.assertEquals( dedekindNode.acceptedConfigurations, self.orderedConfigurationsByLevel)
        
    def testBadConfigurations(self):
        '''
        Test if the constructor will raise an error if a bad list
        of configurations is given (one configuration is two levels above all others)
        '''
        self.assertRaises( Exception, DedekindNode, (4, self.invalidConfigurations) )
        
    def testWriteToDotFile(self):
        self.dedekindNode.writeToDotFile("")
        testFile = open("writeToDotTest.dot").read()
        toTestFile = open("n_4.world_57344.dot").read()
        self.assertEquals(testFile, toTestFile)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBadConfigurations']
    unittest.main()