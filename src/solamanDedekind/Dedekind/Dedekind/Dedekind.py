'''
Created on Apr 1, 2015

@author: Solaman
'''
from Controller.CommandOptions import CommandOptions
from Controller import Console
from Model.DedekindLattice import getDedekindNumber, generateDotFiles

import sys
from Algorithms.analysis import runAnalysis

def runConsole():
    global standardCommands
    
    del standardCommands._commands["console"]
    Console.run(standardCommands)
    
standardCommands = CommandOptions()

standardCommands.addCommand("getNumber", "Finds Dedekind Number for a given input size."\
                            + "\n\tInput:" + " function input size", getDedekindNumber)

standardCommands.addCommand("dotFiles", "Generates dot files of all monotone boolean functions"\
                            + " for a given input size." + "\n\tInput:" + " function input size", generateDotFiles)

standardCommands.addCommand("analyze", "Runs a System-Diagnostic algorithm"\
                            + " and perform analysis on varying MBF's" +"\n\tInput: algorithm name, input size", runAnalysis )
standardCommands.addCommand("console", "Run the program as a console.", runConsole)

        
def main():
    userInput = sys.argv[1:]
    standardCommands.selectCommand(userInput)
    
if __name__ == '__main__':
    main()