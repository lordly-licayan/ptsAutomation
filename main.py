import sys, getopt
import os
import processor

from config import configSetup as config
from helper import getPath
from distutils.util import strtobool


def main(argv):
    inputFile = ''
    configFile= ''
    verbose= False
   
    try:
        opts, args = getopt.getopt(argv,"i:c:v:h",["ifile=","config=","verbose="])
        
        for opt, arg in opts:
            if opt == '-h':
                print ("main.py --i <PTS input file.xlsx> --c <configuration file.xml> --v <boolean>")
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputFile= arg
            elif opt in ("-c", "--config"):
                configFile = arg
            elif opt in("-v","--verbose"):
                verbose= strtobool(arg)

    except (getopt.GetoptError, ValueError):
        print ("Syntax:")
        print ('main.py --i <input file> --c <configuration file> --v <boolean>')
        sys.exit(2)

    
    if not inputFile:
        print("No input file!")
        sys.exit()
    
    if not configFile:
        configFile= getPath("config", "config.xml")

    if verbose:
        print("Configuration file: " + configFile)
        
    #get the configuration map.
    configMap= config.parseXML(configFile)
    
    #time to process the file.
    processor.processInput(inputFile, configMap)

if __name__ == "__main__":
   main(sys.argv[1:])