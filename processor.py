import pandas as pd
import numpy as np
import helper
import os

from pathlib import Path


def processInput(inputFile, configMap):
    print("Processing file: ", inputFile)
    
    outputPath= helper.getPath(configMap["outputFolder"])
    ptsFilename= Path(os.path.basename(inputFile)).resolve().stem
    ptsOutputFilename=  helper.getPath( outputPath, ptsFilename + configMap["outputFileSuffix"] + configMap["fileType"])
    ptsFeedFilename= helper.getPath( outputPath, ptsFilename + configMap["feedFileSuffix"] + configMap["fileType"])
    testProcedure= configMap["testProcedure"]
    expectedValue= configMap["expectedValue"]
    
    helper.makePath(outputPath)
    
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
    
