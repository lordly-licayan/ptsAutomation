'''
Please insert new functions WITH DESCRIPTIVE COMMENT below.
'''

#sample imports
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

#set capabilities to enhance IE response
capabilities = DesiredCapabilities.INTERNETEXPLORER.copy()
capabilities['ignoreProtectedModeSettings'] = True
capabilities['ie.ensureCleanSession'] = True
capabilities['requireWindowFocus'] = True

#creating connection and opening IE browser
driver = webdriver.Ie(capabilities=capabilities)
driver.get("http://localhost/testSelenium/login")
assert "Test Login" in driver.title

#creating list
loginElements = [['username','testUser'],['password', 'testPassword'],['userDetails','testUserDetails'],['businessDate','testBusinessDate']]

#iterate list of details and set values to respective elements
for elements in loginElements:
	#get, clear and set values to the specified element
    element = driver.find_element_by_id(elements[0])
    element.clear()
    element.send_keys(elements[1])

#click button element
driver.find_element_by_name("login").click()

#taking screenshot
fileName = 'screen_init'
driver.save_screenshot('C:/desired_path/'+fileName+'.png')

#creating and writing a file
pageSource = open('C:/desired_path/pageSource.html','w+',1,'UTF-8')
pageSource.write(driver.page_source)

#closing the webdriver
driver.close()
driver.quit()

#controlling notepad
myDriver = webdriver.Remote(
	#winium desktop driver is used to create a connection below
    command_executor='http://localhost:9999',
    desired_capabilities={
        "debugConnectToRunningApp": 'false',
        "app": r"C:/desired_path/pageSource.html"
    })
	
def searchNotepad(myDriver, searchValue, fileName):
    myDriver.find_element_by_name("Search").click()
    myDriver.find_element_by_name("Find...").click()
    myDriver.find_element_by_name("Find what :").send_keys(searchValue)
    myDriver.find_element_by_name("Find Next").click()
    myDriver.find_element_by_name("Close").click()
    myDriver.save_screenshot('C:/desired_path/'+fileName+'.png')
    myDriver.find_element_by_name("File").click()
    myDriver.find_element_by_name("Close All").click()
    return
	
searchNotepad(myDriver,'sampleValue','sampleFileName')
myDriver.close()
myDriver.quit()
