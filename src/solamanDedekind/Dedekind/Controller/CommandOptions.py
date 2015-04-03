'''
Created on Mar 31, 2015

@author: Solaman

Used to store relevant information about command options.
'''
import sys

class CommandOption(object):
    '''
    class for a particular console option
    '''


    def __init__(self, helpString, commandFunction):
        '''
        Constructor
        '''
        #Should describe what the option does
        self.helpString = helpString
        
        #Function used to execute this option
        self.commandFunction = commandFunction
        

class CommandOptions(object):
    '''
    Used to store and order console options
    '''
    
    def __init__(self):
        #If the user wants to request a command by its command string, they can do so with this
        self._commands = {}
        
        self._commands["help"] = CommandOption("displays all available commands"\
                        + " along with a description for each", self.printCommandOptions)
        
    def addCommand(self, commandString, helpString, commandFunction):
        '''
        Adds a command option. This option then can be requested by calling
        'selectOption'.
        '''
        if commandString == "help":
            exceptMessage = "attempted to overwrite \"help\" option in ConsoleOptions. Don't do that plz."
            raise Exception(exceptMessage)
        
        if not callable(commandFunction):
            exceptMessage = "Command function must be a function! (must be callable)"
            raise Exception(exceptMessage)
        
        self._commands[commandString] = CommandOption(helpString, commandFunction)
        
    def printCommandOptions(self):
        '''
        Prints all commands available along with the help string associated with each
        respective command.
        '''
        print "-----"
        print "Available Commands"
        print "-----"
        for command in self._commands.iterkeys():
            print command, ": ", self._commands[command].helpString
            print "-----"
            
    
    def selectCommand(self, userInput):
        '''
        Calls the function associated with a particular command.
        '''
        if len(userInput) == 0:
            sys.stderr.write( "Must enter a command, type \"help\" to list all commands\n" )
            return
        
        command = userInput[0]
        inputParams = userInput[1:]
        
        if command not in self._commands:
            sys.stderr.write("Command not recognized, type \"help\" to list all commands\n")
            return
        
        if len(inputParams) == 0:
            self._commands[command].commandFunction()
        else:
            self._commands[command].commandFunction(inputParams)