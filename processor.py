import pandas as pd
import numpy as np
import helper
import os
import re
import json

from pathlib import Path


def processInput(inputFile, configMap):
    print("Processing file: ", inputFile)
    
    ptsFilename= Path(inputFile).resolve().stem
    ptsOutputFilename=  ptsFilename + configMap["outputFileSuffix"]
    ptsFeedFilename= ptsFilename + configMap["feedFileSuffix"]
    testProcedure= configMap["testProcedure"]
    expectedValue= configMap["expectedValue"]
    
    data = pd.read_excel (inputFile, sheet_name= configMap["sheetName"], skiprows= int(configMap["startingRow"]))
    df = pd.DataFrame(data, columns = [testProcedure, expectedValue])
    pts = df[df[testProcedure].notnull()].reset_index()

    testCases={}
    overallPts=[]
    helper.assembleTestCases(pts, testCases, overallPts, testProcedure, expectedValue)
    helper.createFile(ptsOutputFilename, overallPts)

    instructions= []
    helper.getInstructions(testCases, instructions, configMap)
    helper.createFile(ptsFeedFilename, instructions)
    
