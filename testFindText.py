import time

def findText(webdriver, fromPath, toPath, fileName, value):

    driver = webdriver.Remote(
        command_executor='http://localhost:9999',
        desired_capabilities={
            "debugConnectToRunningApp": 'false',
            "app": r""+fromPath
        })

    time.sleep(2)
    driver.find_element_by_name("Search").click()
    driver.find_element_by_name("Find...").click()
    driver.find_element_by_name("Find what :").send_keys(value)
    driver.find_element_by_name("Find Next").click()
    driver.find_element_by_name("Close").click()
    driver.save_screenshot(toPath+""+fileName+'.png')
    driver.find_element_by_name("File").click()
    driver.find_element_by_name("Close All").click()
    driver.find_element_by_name("Close").click()
    return