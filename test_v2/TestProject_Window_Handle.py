import time
import re
from TestProject_Element_Finder import *
from bs4 import BeautifulSoup
from datetime import datetime

cmd = " [TestProject] Test Automation Activity Logs: "
switch_window_seconds = 2

def get_next_window_handle(driver, pointer):
    print(str(datetime.now()) + "" + cmd + " ==>  Start: get_next_window_handle")
    next_window_handle = None

    while (not next_window_handle):
        try:
            next_window_handle = driver.window_handles[pointer]
            driver.switch_to.window(next_window_handle)
            time.sleep(switch_window_seconds)
            print(str(datetime.now()) + "" + cmd + "      Window handle: " + next_window_handle)
        except Exception:
            next_window_handle = None
        break
    print(str(datetime.now()) + "" + cmd + " <==  End: get_next_window_handle")

def get_previous_window_handle(driver, pointer):
    print(str(datetime.now()) + "" + cmd + " ==>  Start: get_previous_window_handle")
    previous_window_handle = None

    while (not previous_window_handle):
        try:
            previous_window_handle = driver.window_handles[pointer]
            driver.switch_to.window(previous_window_handle)
            time.sleep(switch_window_seconds)
            print(str(datetime.now()) + "" + cmd + "      Window handle: " + previous_window_handle)
        except Exception:
            previous_window_handle = None
        break
    print(str(datetime.now()) + "" + cmd + " <==  End: get_previous_window_handle")

def find_element(driver, element_name):
    print(str(datetime.now()) + "" + cmd + " ==>  Start: find_element")
    found_element = False
    
    if(name_method(driver, element_name)):
        found_element = True  
    elif(link_text_method(driver, element_name)):
        found_element = True
    print(str(datetime.now()) + "" + cmd + " <==  End: find_element")
    return found_element

def wait_element(driver, element_name):
    print(str(datetime.now()) + "" + cmd + " ==>  Start: wait_element")
    wait_time = time.time() + 10
    wait_element = False

    while (not wait_element):
        driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
        wait_element = find_element(driver, element_name)
        if(wait_element):
            print(str(datetime.now()) + "" + cmd + "      Result: Waited")
            continue
        elif time.time() > wait_time:
            print(str(datetime.now()) + "" + cmd + "      Result: Not found after 10 seconds of searching")
            break
        
    print(str(datetime.now()) + "" + cmd + " <==  End: wait_element")       
    return wait_element

def switch_frames(driver,element_name):
    found_element = False
    try:
        driver.page_source
    except:
        windowCounter = len(driver.window_handles) - 1
        get_previous_window_handle(driver,windowCounter)
        return found_element
    
    print(str(datetime.now()) + "" + cmd + " ==>  Start: switch_frames")
    web_source = BeautifulSoup(driver.page_source, "html.parser")
    frames = web_source.find_all("frame")
    for frame_name in frames:
        driver.switch_to.window(driver.current_window_handle)
        frame = str(frame_name.get("name"))
        if(wait_element(driver,frame)):
            time.sleep(2)
            driver.switch_to.frame(driver.find_element_by_name(frame))
            time.sleep(2)
            print(str(datetime.now()) + "" + cmd + "      Switched to: " + frame)
            if(find_element(driver,element_name)):
                found_element = True
    print(str(datetime.now()) + "" + cmd + " ==>  End: switch_frames")
    return found_element
