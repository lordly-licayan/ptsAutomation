*** Settings ***
Resource          TestingSuiteKeywords.txt

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
	Expect Value    HC_CHA_CCD    GDCS08
    [Teardown]    Close Page


