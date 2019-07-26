*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Library           DateTime
Library           ModifyIniFile.py
Resource          WindowHandling.robot
Resource          VarDef.robot

*** Keywords ***
Open Login Page
    [Arguments]     ${username}
    Click On Element    BTNVIEW_HC1
    Opens Window
    Do Login    ${username}    1

Open Main Page
    [Arguments]    ${test_case_no}
    Sleep    2
    Create Test Case Folder     ${test_case_no}
    Open Browser    ${SERVER1}    ${BROWSER}
    Page Should Contain    e-FOCUS
    Maximize Browser Window
    Set Windows

Close Page
    Sleep    1
    Close Browser

Close Page With Ini Revert
    Revert Ini File
    Close Page

Backup Ini File
    ${stat_file}=   Run Keyword And Return Status   Get File Size   ${LOCAL_INI_PATH}\\${INI_FILENAME}
    Run Keyword If    ${stat_file}==False    Copy File   ${ORIG_INI_PATH}\\${INI_FILENAME}    ${LOCAL_INI_PATH}

Revert Ini File
    ${stat_file}=   Run Keyword And Return Status   Get File Size   ${LOCAL_INI_PATH}\\${INI_FILENAME}
    Run Keyword If    ${stat_file}==True    Copy File   ${LOCAL_INI_PATH}\\${INI_FILENAME}    ${ORIG_INI_PATH}

# Performs login
Do Login
    [Arguments]    ${username}    ${password}
    Input On Text    EMP_CCD    ${username}
    Input On Text    PWD    ${password}
    Click On Element    BTNENTER

# Performs writing of value on input text
#
# @param element the referred item
# @param value the value to write on input text
Input On Text
    [Arguments]    ${element}    ${value}
    ${stat}=    Run Keyword And Return Status    Input Text    ${element}    ${value}
    Return From Keyword If    ${stat}==True    ${stat}
    ${stat_frame}=    Perform On Frame    Input Text    ${element}    ${value}
    Element Should Exist    ${element}    ${stat}

# Performs clicking on an element
#
# @param element the referred item
Click On Element
    [Arguments]    ${element}
    ${stat_element}=    Run Keyword And Return Status    Click Element    ${element}
    Return From Keyword If    ${stat_element}==True    ${stat_element}
    ${stat_link}=    Run Keyword And Return Status    Click Link    ${element}
    Return From Keyword If    ${stat_link}==True    ${stat_link}
    ${stat_frame_element}=    Perform On Frame    Click Element    ${element}
    Return From Keyword If    ${stat_frame_element}==True    ${stat_link}
    ${stat_frame_link}=    Perform On Frame    Click Link    ${element}
    Element Should Exist    ${element}    ${stat_frame_link}

# Performs clicking of an element inside a frame
#
# @param keyword the command to invoke
# @param element the referred item
Click On Frame
    [Arguments]    ${keyword}    ${element}
    ${frames_exist}=    Run Keyword And Return Status    Get WebElements    //frame
    Return From Keyword If    ${frames_exist}==False    False
    ${frames}=    Get WebElements    //frame
    ${frames_count} =    Get Length    ${frames}
    Return From Keyword If    ${frames_count}==0    False
    : FOR    ${frame}    IN    @{frames}
    \    ${frame_name}=    Get Element Attribute    ${frame}    name
    \    Select Frame    ${frame_name}
    \    ${stat}=    Run Keyword And Return Status    Run Keyword    ${keyword}    ${element}
    \    Unselect Frame
    \    Exit For Loop If    ${stat}==True
    [Return]    ${stat}

# Writes value on input text that is inside a frame
#
# @param keyword the command to invoke
# @param element the referred item
# @param value the value to write on input text
Input On Frame
    [Arguments]    ${keyword}    ${element}    ${value}
    ${frames_exist}=    Run Keyword And Return Status    Get WebElements    //frame
    Return From Keyword If    ${frames_exist}==False    False
    ${frames}=    Get WebElements    //frame
    ${frames_count} =    Get Length    ${frames}
    Return From Keyword If    ${frames_count}==0    False
    : FOR    ${frame}    IN    @{frames}
    \    ${frame_name}=    Get Element Attribute    ${frame}    name
    \    Select Frame    ${frame_name}
    \    ${stat}=    Run Keyword And Return Status    Run Keyword    ${keyword}    ${element}    ${value}
    \    Unselect Frame
    \    Exit For Loop If    ${stat}==True
    [Return]    ${stat}

# Performs the keyword inside the frame
#
# @param keyword the command to invoke
# @param args a list of arguments
Perform On Frame
    [Arguments]    ${keyword}    @{args}
    Log     arguments: @{args}
    ${frames_exist}=    Run Keyword And Return Status    Get WebElements    //frame
    Return From Keyword If    ${frames_exist}==False    False
    ${frames}=    Get WebElements    //frame
    ${frames_count} =    Get Length    ${frames}
    Return From Keyword If    ${frames_count}==0    False
    ${args_length}=     Get Length      ${args}
    : FOR    ${frame}    IN    @{frames}
    \    ${frame_name}=    Get Element Attribute    ${frame}    name
    \    Select Frame    ${frame_name}
    \    ${stat}=   Run Keyword If      ${args_length} == 1       Run Keyword And Return Status    Run Keyword    ${keyword}    @{args}[0]
    \    Run Keyword If     ${stat}==True       Run Keywords    Unselect Frame      Exit For Loop
    \    ${stat}=   Run Keyword If      ${args_length} == 2       Run Keyword And Return Status    Run Keyword    ${keyword}    @{args}[0]    @{args}[1]
    \    Unselect Frame
    \    Exit For Loop If    ${stat}==True
    [Return]    ${stat}

# Sets the specified Radio Button as selected
#
# @param group_name the name of the radio button
# @param value the value of the radio button
Select On Radio Button
    [Arguments]    ${group_name}    ${value}
    ${stat_element}=    Run Keyword And Return Status    Select Radio Button    ${group_name}    ${value}
    Return From Keyword If    ${stat_element}==True    ${stat_element}
    ${stat_frame_element}=      Perform On Frame    Select Radio Button    ${group_name}    ${value}
    Element Should Exist    ${value}    ${e}    

############################################ TODO ############################################
# Scroll to the specified element on screen
#
# @param element the referred item
Scroll To Element
    [Arguments]    ${element}
    ${e}=    Get Element    ${element}
    Scroll Element Into View    ${e}

# Retry keyword until it succeeds based on the specified
# ${DEFAULT_RETRY} and ${DEFAULT_RETRY_INTERVAL}
#
# @param keywrord the command to invoke
# @param args a list of arguments
Wait Keyword
    [Arguments]     ${keyword}      @{args}
    ${args_length}=     Get Length      ${args}
    Run Keyword If    ${args_length} == 1     Wait Until Keyword Succeeds    ${DEFAULT_RETRY}    ${DEFAULT_RETRY_INTERVAL}    ${keyword}   @{args}[0]
    Run Keyword If    ${args_length} == 2     Wait Until Keyword Succeeds    ${DEFAULT_RETRY}    ${DEFAULT_RETRY_INTERVAL}    ${keyword}   @{args}[0]   @{args}[1]
    Run Keyword If    ${args_length} == 3     Wait Until Keyword Succeeds    ${DEFAULT_RETRY}    ${DEFAULT_RETRY_INTERVAL}    ${keyword}   @{args}[0]   @{args}[1]   @{args}[2]

# Retrieves the element on screen
#
# @param element the referred item
Get Element
    [Arguments]    ${element}
    ${e}    Set Variable    False
    ${elem_exist}=    Run Keyword And Return Status    Get WebElement    ${element}
    Run Keyword And Return If    ${elem_exist}==True    Get WebElement    ${element}
    ${e}=    Run Keyword If    ${elem_exist}==False    Get Frame Element    ${element}
    Element Should Exist    ${element}    ${e}
    [Return]    ${e}

# Retrieves the current value on input text
#
# @param element the referred item
Get Input Value
    [Arguments]    ${element}
    ${e}=    Get Element    ${element}
    ${value}=   Get Element Attribute    ${e}    value
    [Return]    ${value}

# Retrieves the element inside a frame
#
# @param element the referred item
# @return either false or the item in frame
Get Frame Element
    [Arguments]    ${element}
    ${e}    Set Variable    False
    ${frames_exist}=    Run Keyword And Return Status    Get WebElements    //frame
    Return From Keyword If    ${frames_exist}==False    ${e}
    ${frames}=    Get WebElements    //frame
    ${frames_count} =    Get Length    ${frames}
    Return From Keyword If    ${frames_count}==0    ${e}
    : FOR    ${frame}    IN    @{frames}
    \    Select Frame    ${frame}
    \    ${elem_exist}=    Run Keyword And Return Status    Get WebElement    ${element}
    \    Run Keyword If    ${elem_exist}==False    Unselect Frame
    \    Continue For Loop If    ${elem_exist}==False
    \    ${e}=    Get WebElement    ${element}
    \    Unselect Frame
    \    Exit For Loop
    [Return]    ${e}

# Asserts that the element is existing
#
# @param element the referred item
# @param flag the expected boolean value
Element Should Exist
    [Arguments]    ${element}    ${flag}
    Should Be True    ${flag}    Element '${element}' not found

# Asserts that the value of input text is exact
#
# @param element the current input text
# @param value the expected value of the input text
Expect Input Value
    [Arguments]    ${element}    ${value}
    Sleep    1
    ${expected_value}=    Get Input Value    ${element}
    Should Be Equal    ${expected_value}    ${value}

# Asserts that the checkbox is currently ticked/unticked
#
# @param element the current checkbox
# @param state signifies that the checkbox is either ${ON} or ${OFF}
Expect Checkbox State
    [Arguments]    ${element}    ${state}
    Sleep    1
    ${e}=    Get Element    ${element}
    Run Keyword If    ${state}==${ON}    Checkbox Should Be Selected    ${e}
    Run Keyword If    ${state}==${OFF}    Checkbox Should Not Be Selected    ${e}

############################################ TODO ############################################
# Ensures that the radio button is currently selected
#
# @param group_name the name of the radiobutton specified on the html
# @param value the value of the radiobutton specified on the html
Expect Radiobutton Selected
    [Arguments]    ${group_name}    ${value}
    Sleep    1
    ${stat_element}=    Run Keyword And Return Status    Select Radio Button    ${group_name}    ${value}
    Return From Keyword If    ${stat_element}==True    ${stat_element}
    ${stat_frame_element}=      Perform On Frame    Select Radio Button    ${group_name}    ${value}
    Element Should Exist    ${value}    ${e}  

# Creates a folder for the test case and 
# sets the output directory for the screenshots
#
# @param test_case_no a number that specifies the current test case
Create Test Case Folder
    [Arguments]     ${test_case_no}
    ${DIR_EVIDENCE}=      Set Variable    ${OUTPUTDIR}\\TestCase${test_case_no}
    Set Global Variable     ${DIR_EVIDENCE}
    Set Screenshot Directory    ${DIR_EVIDENCE}
    Create Directory        ${DIR_EVIDENCE}

# Performs screenshot on page
#
# @param filename the actual name of output file
Do Page Screenshot
    [Arguments]     ${filename}
    Capture Page Screenshot     ${filename}
    Sleep   1