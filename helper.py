import re

TESTCASE= 'testCase'
LOGIN= 'login'
SELECT= 'select'
CLICK= 'click'
SCREENSHOT= 'screenshot'
EXPECTED_RESULT= 'expected'
NOT_EMPTY='not empty'
SPACE= ' '
EMPTY= ''
COLUMN= ':'
NEWLINE= '\n'

def assembleTestCases(pts, testCases, overallPts, testProcedure, expectedValue):
    for index, row in pts.iterrows():
        testProcedureItem = row[testProcedure].strip()
        expectedValueItem = row[expectedValue].strip()

        testCases[str(index)]= [testProcedureItem, expectedValueItem]

        overallPts.append("TestCase no.: %s" % str(index))
        overallPts.append(testProcedureItem)
        overallPts.append("Expected result:")
        overallPts.append(expectedValueItem)
        overallPts.append(NEWLINE)

def createFile(filename, items):
    try:
        f = open(filename, "w")            
        f.write(NEWLINE.join(items))
    finally:
        f.close()

def getInstructions(testCases, instructions, configMap):
    noOfTestcases= len(testCases)
    print("No. of testcases: ", noOfTestcases)
    url= configMap["url"]

    for i in range(noOfTestcases):
        #print(testCases[str(i)][0])
        stepsList= testCases[str(i)][0].split(NEWLINE)
        #print("No. of steps: ", len(stepsList))
        
        instructions.append(TESTCASE + COLUMN + str(i + 1))
        
        for item in stepsList: 
            if(item.lower().find(LOGIN) != -1):
                instructions.append(LOGIN + SPACE + url)
            elif(item.lower().find(SELECT) != -1):
                instructions.append(SELECT + SPACE + getFormattedValue(item))
            elif(item.lower().find(CLICK) != -1):
                instructions.append(SCREENSHOT)
                instructions.append(CLICK + SPACE + getFormattedValue(item))
        
        instructions.append(NEWLINE)

def getValue(str):
    result= re.findall(r'"(.*?)(?<!\\)"', str)
    if len(result) == 0:
        return ''
    else:
        return result[0].strip()

def getFormattedValue(str):
    result= getValue(str)
    if(len(result) > 0):
        return ('"%s"' %result)
    else:
        return str