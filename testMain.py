import os
import sys
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from testFindText import findText
from testDriverStatus import driverStatus

capabilities = DesiredCapabilities.INTERNETEXPLORER.copy()
capabilities['ignoreProtectedModeSettings'] = True
capabilities['ie.ensureCleanSession'] = True
capabilities['requireWindowFocus'] = True

#supposed to be generated
testPath = "C:/Users/rl.cruz/Documents/Selenium/ptsAutomation/template/sample.txt"
#provided by e-Focus
testCaseFolder = "C:/Users/rl.cruz/Documents/Selenium/ptsAutomation/template/"
testCaseCounter = 0

def jsonConvert(str, word):
    return str[:1] + word + str[1:]

test = open(testPath,"r",encoding="UTF-8")
for line in test:
    newline = line.replace('"','')
    newline = newline.replace(':', ' ')
    testSplit = newline.split()

    if not len(testSplit) == 0:
        
        if("testCase" in testSplit[0]):
            testCaseCounter += 1
            screenShotCounter = 0
            pathPerTest = testCaseFolder + "" + testSplit[0] + "/"
            configPerTest = Path(testCaseFolder + "testcaseConfig"+str(testCaseCounter)+".json")
            if not os.path.exists(pathPerTest):
                os.makedirs(pathPerTest)
            if configPerTest.is_file():
                configFile = json.loads(open(configPerTest, encoding="UTF-8").read())
            else:
                configFile = json.loads(open(testCaseFolder + "testcaseConfig.json", encoding="UTF-8").read())
        
        elif("login" in testSplit[0]):
            driver = webdriver.Ie(capabilities=capabilities)
            driver.get(configFile.get(testSplit[1]))
            assert "Test Login" in driver.title

        elif("select" in testSplit[0]):
            line = line.replace("select ", "")
            converted = jsonConvert("{}",line)
            newJson = json.loads(converted)

            if("input" == testSplit[1]):
                element = driver.find_element_by_tag_name(testSplit[1])
            else:
                element = driver.find_element_by_id(testSplit[1])
            element.clear()
            if(len(configFile.get(testSplit[1])) == 0):
                element.send_keys(newJson.get(testSplit[1]))
            else:
                element.send_keys(configFile.get(testSplit[1]))

        elif("screenshot" in testSplit[0]):
            screenShotCounter += 1
            driver.save_screenshot(pathPerTest+"evidence"+str(screenShotCounter)+".png")

        elif("click" in testSplit[0]):
            if("button" == testSplit[1]):
                driver.find_element_by_tag_name(testSplit[1]).click()
            else:    
                driver.find_element_by_name(testSplit[1]).click()

        elif("save" in testSplit[0]):
            pageSourcePath = pathPerTest+"pageSource.html"
            pageSource = open(pageSourcePath,"w+",1,"UTF-8")
            pageSource.write(driver.page_source)

        elif("find" in testSplit[0]):
            findText(webdriver,pageSourcePath,pathPerTest,testSplit[1],testSplit[1])

        elif("logout" in testSplit[0]):
            if("Alive" == driverStatus(driver)):
                driver.quit()

test.close()