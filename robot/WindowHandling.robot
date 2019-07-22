*** Settings ***
Library           Collections

*** Variables ***
@{WINDOWS}        

*** Keywords ***
Opens Window
    Set Windows
    Select Current Window

Closes Window
    Close Window
    Remove Last Window
    Select Current Window
    
Remove Last Window
    ${last_window}=     Get Last Window
    Run Keyword If    "${last_window}" != "False"   Remove Values From List     ${WINDOWS}      ${last_window}

Set Windows
    @{opened_windows}=     Get Window Handles
    : FOR     ${window}     IN      @{opened_windows}
    \    ${matches}=     Get Match Count     ${WINDOWS}     ${window}
    \    Run Keyword If     ${matches} == 0     Append To List    ${WINDOWS}   ${window}

Get Last Window
    ${windows_size}=      Get Length        ${WINDOWS}
    Return From Keyword If      ${windows_size}==0      False
    ${window}=      Set Variable     @{WINDOWS}[${windows_size-1}]
    [Return]    ${window}

Select Current Window
    ${window}=      Get Last Window
    Select Window       ${window}