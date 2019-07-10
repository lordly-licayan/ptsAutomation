*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${efocus_url}     TO_BE_CHANGED
${browser}        ie
${_username}      GDC7
${_password}      1

*** Test Cases ***
TC1
    [Setup]    Open Main Page
    Open Login Page
    Focus Current Window
    xClick Element    [OHC]発注
    Set Exclude Window
    xClick Element    [OHC110]発注申請
    Focus Current Window
    Set Exclude Window
    xClick Element    BTNVIEW_HC1
    Focus Current Window
    xClick Element    Julian
    Close Window
    Select Previous Window
    ${expected_element}=    xGet Element    HC_CHA_CCD
    ${expected_value}=    Get Element Attribute    ${expected_element}    value
    Should Be Equal    ${expected_value}    GDCS08
    [Teardown]    Close Page

*** Keywords ***
Open Login Page
    Set Exclude Window
    xClick Element    BTNVIEW_HC1
    Focus Current Window
    Do Login    ${_username}    ${_password}

Open Main Page
    Sleep    2
    Open Browser    ${efocus_url}    ${browser}
    Page Should Contain    e-FOCUS
    Maximize Browser Window

Close Page
    Sleep    1
    Close Browser

Do Login
    [Arguments]    ${username}    ${password}
    xInput Text    EMP_CCD    ${username}
    xInput Text    PWD    ${password}
    xClick Element    BTNENTER

Find Index
    [Arguments]    ${element}    @{items}
    ${index} =    Set Variable    ${0}
    : FOR    ${item}    IN    @{items}
    \    Run Keyword If    '${item}' == '${element}'    Return From Keyword    ${index}
    \    ${index} =    Set Variable    ${index + 1}
    Return From Keyword    ${-1}    # Also [Return] would work here.

Select Previous Window
    @{windows}=    Get Window Handles
    ${win_length}=    Get Length    ${windows}
    : FOR    ${count}    IN RANGE    ${win_length}
    \    ${index} =    Set Variable    ${win_length-1-${count}}
    \    ${win_stat}=    Run Keyword and Return Status    Select Window    @{windows}[${index}]
    \    Exit For Loop If    ${win_stat}==True

Set Exclude Window
    @{excludes}=    Get Window Handles
    Set Global Variable    @{excludes}

Focus Current Window
    Log    Excluding: ${excludes}
    ${stat}=    Run Keyword And Return Status    Select Window    ${excludes}
    #${current_window}=

xInput Text
    [Arguments]    ${element}    ${value}
    ${stat}=    Run Keyword And Return Status    Input Text    ${element}    ${value}
    Return From Keyword If    ${stat}==True    ${stat}
    Input on Frame    Input Text    ${element}    ${value}

xClick Element
    [Arguments]    ${element}
    Log To Console    Clicking element ${element}
    ${stat_element}=    Run Keyword And Return Status    Click Element    ${element}
    Return From Keyword If    ${stat_element}==True    ${stat_element}
    ${stat_link}=    Run Keyword And Return Status    Click Link    ${element}
    Return From Keyword If    ${stat_link}==True    ${stat_link}
    ${stat_frame_element}=    Click on Frame    Click Element    ${element}
    Return From Keyword If    ${stat_link}==True    ${stat_link}
    ${stat_frame_link}=    Click on Frame    Click Link    ${element}

xClick Link
    [Arguments]    ${element}
    Log To Console    Clicking element ${element}
    ${stat}=    Run Keyword And Return Status    Click Link    ${element}
    Return From Keyword If    ${stat}==True    ${stat}
    Click on Frame    Click Link    ${element}

xGet Element
    [Arguments]    ${element}
    ${e}    Set Variable    ${EMPTY}
    ${elem_exist}=    Run Keyword And Return Status    Get WebElement    ${element}
    Run Keyword And Return If    ${elem_exist}==True    Get WebElement    ${element}
    ${e}=    Run Keyword If    ${elem_exist}==False    xGet Frame Element    ${element}
    [Return]    ${e}

Click on Frame
    [Arguments]    ${keyword}    ${element}
    ${frames_exist}=    Run Keyword And Return Status    Get WebElements    //frame
    Return From Keyword If    ${frames_exist}==False    ${EMPTY}
    ${frames}=    Get WebElements    //frame
    ${frames_count} =    Get Length    ${frames}
    Return From Keyword If    ${frames_count}==0    ${EMPTY}
    : FOR    ${frame}    IN    @{frames}
    \    ${frame_name}=    Get Element Attribute    ${frame}    name
    \    Select Frame    ${frame_name}
    \    ${stat}=    Run Keyword And Return Status    Run Keyword    ${keyword}    ${element}
    \    Unselect Frame
    \    Exit For Loop If    ${stat}==True
    [Return]    ${stat}

Input on Frame
    [Arguments]    ${keyword}    ${element}    ${value}
    ${frames_exist}=    Run Keyword And Return Status    Get WebElements    //frame
    Return From Keyword If    ${frames_exist}==False    ${EMPTY}
    ${frames}=    Get WebElements    //frame
    ${frames_count} =    Get Length    ${frames}
    Return From Keyword If    ${frames_count}==0    ${EMPTY}
    : FOR    ${frame}    IN    @{frames}
    \    ${frame_name}=    Get Element Attribute    ${frame}    name
    \    Select Frame    ${frame_name}
    \    ${stat}=    Run Keyword And Return Status    Run Keyword    ${keyword}    ${element}    ${value}
    \    Unselect Frame
    \    Exit For Loop If    ${stat}==True

xGet Frame Element
    [Arguments]    ${element}
    ${e}    Set Variable    ${EMPTY}
    ${frames_exist}=    Run Keyword And Return Status    Get WebElements    //frame
    Return From Keyword If    ${frames_exist}==False    ${e}
    ${frames}=    Get WebElements    //frame
    ${frames_count} =    Get Length    ${frames}
    Return From Keyword If    ${frames_count}==0    ${e}
    : FOR    ${frame}    IN    @{frames}
    \    Select Frame    ${frame}
    \    ${elem_exist}=    Run Keyword And Return Status    Get WebElement    ${element}
    \    Run Keyword If    ${element_exist}==False    Unselect Frame
    \    Continue For Loop If    ${elem_exist}==False
    \    ${e}=    Get WebElement    ${element}
    \    Unselect Frame
    \    Exit For Loop
    [Return]    ${e}
