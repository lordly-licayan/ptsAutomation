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

TC2
    [Setup]    Open Main Page    ${2}
    Backup Ini File
    &{OHC_VALUES}=    Create Dictionary    MitsumoriShokaiShinsaFlg=1
    &{efocus_ini_values}    Create Dictionary    [OHC]    ${OHC_VALUES}
    ${stat}=    modify ini file    ${ORIG_INI_PATH}\\${INI_FILENAME}    ${efocus_ini_values}    Shift-JIS
    Open Login Page     GDCP08
    Wait Keyword    Click On Element    [OHC]発注
    Wait Keyword    Click On Element    [OHC110]発注申請
    Wait Keyword    Click On Element    WF_TETSU_MISHO
    Wait Keyword    Input On Text       HC_PLN_NNO      0000383873-00
    Wait Keyword    Click On Element    BTNENTER
    Wait Keyword    Click On Element    BTNBACK
    Expect Checkbox State    WF_TETSU_MISHO    ${ON}
    Copy File       ${ORIG_INI_PATH}\\${INI_FILENAME}       ${DIR_EVIDENCE}
    [Teardown]    Close Page With Ini Revert
