from datetime import datetime

now = datetime.now()
cmd = " [TestProject] Test Automation Activity Logs: "

def name_method(driver,element_name):
    print(str(datetime.now()) + "" + cmd + " ==>  Start: name_method")
    try:
        driver.find_element_by_name(element_name).click()
        isFound = True
        print(str(datetime.now()) + "" + cmd + "      Result: " + element_name + " Found by Name Method")
    except Exception:
        print(str(datetime.now()) + "" + cmd + "      Result: " + element_name + " Not found by Name Method")
        isFound = False
    print(str(datetime.now()) + "" + cmd + " <==  End: name_method")
    return isFound

def link_text_method(driver,element_name):
    print(str(datetime.now()) + "" + cmd + " ==>  Start: link_text_method")
    try:
        driver.find_element_by_link_text(element_name).click()
        isFound = True
        print(str(datetime.now()) + "" + cmd + "      Result: " + element_name + " Found by Link Text Method")
    except Exception:
        print(str(datetime.now()) + "" + cmd + "      Result: " + element_name + " Not found by Link Text Method")
        isFound = False
    print(str(datetime.now()) + "" + cmd + " <==  End: link_text_method")
    return isFound
