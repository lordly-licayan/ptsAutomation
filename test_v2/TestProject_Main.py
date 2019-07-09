import json
import time
import os
import sys
import urllib3

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from TestProject_Window_Handle import *
from TestProject_Driver_Status import driverStatus

capabilities = DesiredCapabilities.INTERNETEXPLORER.copy()
capabilities['ignoreProtectedModeSettings'] = True
capabilities['ie.ensureCleanSession'] = True
capabilities['requireWindowFocus'] = True

#to be generated from PTS
testPath = "C:/Users/rl.cruz/Documents/Selenium/ptsAutomation/TestProject/TestProject_Sample.txt"
#provided by TestProject
testCaseFolder = "C:/Users/rl.cruz/Documents/Selenium/ptsAutomation/TestProject/"
testCaseCounter = 0
windowCounter = 0

test = open(testPath,"r",encoding="UTF-8")
isSuccess = False

while(not isSuccess):
    try:
        for line in test:
            newline = line.replace('"','')
            testSplit = newline.split()

            if (not len(testSplit)) == 0:

                if("testCase" in testSplit[0]):
                    os.system('cls' if os.name == 'nt' else 'clear')
                    testCaseCounter += 1
                    screenshot_counter = 0
                    pathPerTest = testCaseFolder + "Screen_ID_" + testSplit[0] + "/"
                    if not os.path.exists(pathPerTest):
                        os.makedirs(pathPerTest)
                    sys.stdout = open(pathPerTest+'TestProject_logs.txt', 'w', encoding='UTF-8')
                    print(str(datetime.now()) + "" + cmd + " ***  Start Test Automation Powered by Selenium : " + testSplit[0])

                elif("login" in testSplit[0]):
                    driver = webdriver.Ie(capabilities=capabilities)
                    driver.get("")
                    driver.switch_to.frame(driver.find_element_by_name('top'))
                        
                    driver.find_element_by_name("btn").click()

                    windowCounter = len(driver.window_handles) - 1
                    get_next_window_handle(driver,windowCounter)

                    if(wait_element(driver,"user")):
                        driver.find_element_by_name("user").send_keys("user1")
                    else:
                        driver.quit()
                    driver.find_element_by_name("password").send_keys("1")
                    driver.find_element_by_name("btn").click()
                    driver.maximize_window()
                    time.sleep(1)
                
                elif("click" in testSplit[0]):
                    screenshot_counter += 1
                    for r in (("click ", ""), ("\"", ""), ("\n", "")):
                        line = line.replace(*r)

                    capture_element = line.replace(" ", "_")
                    driver.save_screenshot(pathPerTest+""+str(screenshot_counter)+"_"+capture_element+"_01.png")

                    print(str(datetime.now()) + "" + cmd + " ==>  Start: click "+ line)

                    if(not find_element(driver, line)):
                        if(not switch_frames(driver, line)):
                            driver.save_screenshot(pathPerTest+""+str(screenshot_counter)+"_"+capture_element+"_01.png")
                            if(not find_element(driver, line)):
                                print(str(datetime.now()) + "" + cmd + "  **  FOUND ERROR\n" + str(datetime.now()) + "" + cmd + "  **  Element:\t" + line + "\n" + str(datetime.now()) + "" + cmd + "  **  Cause:\tNoSuchElementException ")
                            
                        
                    if((windowCounter + 1) != len(driver.window_handles)):
                        windowCounter = len(driver.window_handles) - 1
                        get_next_window_handle(driver,windowCounter)

                    driver.save_screenshot(pathPerTest+""+str(screenshot_counter)+"_"+capture_element+"_02.png")
                    print(str(datetime.now()) + "" + cmd + " ==>  End: click "+ line)

            else:
                try:
                    if("Alive" == driverStatus(driver)):
                        print(str(datetime.now()) + "" + cmd + " ***  Stop Test Automation")
                except:
                    continue
                       
        isSuccess = True

    except urllib3.exceptions.MaxRetryError as err:
        print(str(datetime.now()) + "" + cmd + " ***  Error: \n" + err)
        print(str(datetime.now()) + "" + cmd + " ***  Retrying...")
        if("Alive" == driverStatus(driver)):
            print(str(datetime.now()) + "" + cmd + " ***  Stop Test Automation")

    except ConnectionRefusedError:
        print("Error")
