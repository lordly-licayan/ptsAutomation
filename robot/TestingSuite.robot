*** Settings ***
Resource          KeywordsDef.robot

*** Test Cases ***
TC1
    [Setup]    Open Main Page    ${1}
    Open Login Page
    Wait Keyword    Click On Element    [OHC]発注
    Wait Keyword    Click On Element    [OHC110]発注申請
    Wait Keyword    Click On Element    BTNVIEW_HC1
    Opens Window
    Wait Keyword    Click On Element    Julian
    Closes Window
    ${expect1}=    Get Input Value    HC_CHA_CCD
    Do Page Screenshot    before-expect1-{index}.png
    Wait Keyword    Click On Element    WF_HC_KBN_SY_ALL
    Wait Keyword    Click On Element    BTNENTER
    Wait Keyword    Click On Element    BTNBACK
    Wait Keyword    Expect Input Value    HC_CHA_CCD    ${expect1}
    Do Page Screenshot    after-expect1-{index}.png
    [Teardown]    Close Page
