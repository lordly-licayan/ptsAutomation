*** Settings ***
Resource          KeywordsDef.robot

*** Test Cases ***
TC1
    [Setup]    Open Main Page       ${1}
    Open Login Page
    Focus Current Window
    Click On Element    [OHC]発注
    Set Exclude Window
    Click On Element    [OHC110]発注申請
    Set Exclude Window
    Click On Element    BTNVIEW_GAI1
    Focus Current Window
    Select On Radio Button      Sel     1
    [Teardown]    Close Page