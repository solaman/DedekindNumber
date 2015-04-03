'''
Created on Mar 31, 2015

@author: Solaman
This is the main interface with the application if the user chooses to use
it as a console application.
'''
import os

class Console(object):

    def __init__(self, commandOptions):
        self.commandOptions = commandOptions

        self.commandOptions.addCommand("exit", "exits the console.", self.endConsole)
        
        self.shouldContinue = True
        
        
    def selectCommand(self, userInput):
        self.commandOptions.selectCommand(userInput)
        
    def endConsole(self):
        print "Bye!"
        self.shouldContinue = False

def run(commandOptions):
    console = Console(commandOptions)
    print "hello! To list commands, type \"help\""
    while console.shouldContinue:
        userInput = raw_input("enter command: ")
        userInput = userInput.split(" ")
        console.selectCommand(userInput)