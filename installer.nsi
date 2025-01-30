; Timer Assistant Installer Script
!include "MUI2.nsh"

; Installer basic information
Name "Timer Assistant"
OutFile "dist\TimerAssistant-Setup.exe"
InstallDir "$PROGRAMFILES64\Timer Assistant"
RequestExecutionLevel admin

; Modern UI Settings
!define MUI_ABORTWARNING

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Languages
!insertmacro MUI_LANGUAGE "English"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"

    ; Create LICENSE.txt if it doesn't exist
    FileOpen $0 "$INSTDIR\LICENSE.txt" w
    FileWrite $0 "Timer Assistant License$\r$\n"
    FileWrite $0 "Copyright (c) 2025$\r$\n"
    FileWrite $0 "All rights reserved.$\r$\n"
    FileClose $0

    ; Add files
    File /oname=timer_app.exe "dist\timer_app.exe"

    ; Create start menu shortcut
    CreateDirectory "$SMPROGRAMS\Timer Assistant"
    CreateShortcut "$SMPROGRAMS\Timer Assistant\Timer Assistant.lnk" "$INSTDIR\timer_app.exe"
    CreateShortcut "$DESKTOP\Timer Assistant.lnk" "$INSTDIR\timer_app.exe"

    ; Write uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; Add uninstall information to Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TimerAssistant" \
                     "DisplayName" "Timer Assistant"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TimerAssistant" \
                     "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TimerAssistant" \
                     "Publisher" "Timer Assistant"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TimerAssistant" \
                     "DisplayVersion" "1.0.0"
SectionEnd

Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\timer_app.exe"
    Delete "$INSTDIR\LICENSE.txt"
    Delete "$INSTDIR\Uninstall.exe"

    ; Remove shortcuts
    Delete "$SMPROGRAMS\Timer Assistant\Timer Assistant.lnk"
    Delete "$DESKTOP\Timer Assistant.lnk"
    RMDir "$SMPROGRAMS\Timer Assistant"

    ; Remove installation directory
    RMDir "$INSTDIR"

    ; Remove registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TimerAssistant"
SectionEnd