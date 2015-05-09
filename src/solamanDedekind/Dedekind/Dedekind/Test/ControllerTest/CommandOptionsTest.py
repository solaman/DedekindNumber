'''
Created on Apr 1, 2015

@author: Solaman
'''
import unittest
from Controller.CommandOptions import CommandOptions
from StringIO import StringIO
import sys
class Test(unittest.TestCase):


    def setUp(self):
        self.testOutput = StringIO()
        self.oldSTDError = sys.stderr
        sys.stderr = self.testOutput
        
        self.commandOptions = CommandOptions()


    def tearDown(self):
        sys.stderr = self.oldSTDError


    def testaddCommandOverwriteHelp(self):
        '''
        Asserts that an exception is thrown when the "-help" option is being overwritten
        '''
        self.assertRaises(Exception, self.commandOptions.addCommand, ("-help", "test", self.setUp))
        
    def testaddCommandNoFunction(self):
        '''
        Asserts that an exception is thrown when the optionFunction is not a function
        '''
        self.assertRaises(Exception, self.commandOptions.addCommand, ("-test", "help string", 5))
        
    def testselectCommandValidCommand(self):
        '''
        Asserts that an option can be selected after added.
        Mocking for this seems overly complex, we'll just create something small
        '''
        self.wasCalled = False
        def dummyFunction():
            self.wasCalled = True
            
        self.commandOptions.addCommand("-test", "help string", dummyFunction)
        self.commandOptions.selectCommand(["-test"])
        self.assertTrue(self.wasCalled)
        
    def testselectCommandInValidCommand(self):
        '''
        Asserts that we notify the user if an invalid command was passed.
        '''
        self.commandOptions.selectCommand(["-test"])
        self.assertEquals(self.testOutput.getvalue(), "Command not recognized, type \"-help\" to list all commands")
        
    def testselectCommandNoCommand(self):
        '''
        Asserts that we notify the user if no command was passed
        '''
        self.commandOptions.selectCommand([])
        self.assertEquals(self.testOutput.getvalue(), "Must enter a command, type \"-help\" to list all commands" )
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()