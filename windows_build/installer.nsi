; Enhanced installer for Timer Assistant
; Handles all installation steps silently with minimal user interaction

!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "x64.nsh"

!define MUI_ICON "generated-icon.png"
!define APP_NAME "Timer Assistant"
!define COMP_NAME "Timer Assistant"
!define VERSION "1.0.0"
!define COPYRIGHT "Timer Assistant"
!define DESCRIPTION "Timer Management Application"
!define LICENSE_TXT "LICENSE"
!define INSTALLER_NAME "TimerAssistant-Setup.exe"
!define MAIN_APP_EXE "TimerAssistant.exe"
!define INSTALL_TYPE "SetShellVarContext current"
!define REG_ROOT "HKCU"
!define REG_APP_PATH "Software\Microsoft\Windows\CurrentVersion\App Paths\${MAIN_APP_EXE}"
!define UNINSTALL_PATH "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"

; Modern UI settings
!define MUI_ABORTWARNING
!define MUI_UNABORTWARNING
!define MUI_FINISHPAGE_RUN "$INSTDIR\${MAIN_APP_EXE}"
!define MUI_FINISHPAGE_RUN_TEXT "Launch Timer Assistant"

; Minimal UI - only show progress
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Name "${APP_NAME}"
OutFile "${INSTALLER_NAME}"
InstallDir "$PROGRAMFILES64\${APP_NAME}"
ShowInstDetails nevershow
ShowUnInstDetails nevershow

Function .onInit
    ; Prevent multiple instances
    System::Call 'kernel32::CreateMutexA(i 0, i 0, t "${APP_NAME}") i .r1 ?e'
    Pop $R0
    StrCmp $R0 0 +3
        MessageBox MB_OK|MB_ICONEXCLAMATION "The installer is already running."
        Abort

    ; Check if application is running
    FindWindow $R0 "" "${APP_NAME}"
    StrCmp $R0 0 +3
        MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION "${APP_NAME} is running. Please close it first." IDOK +2
        Abort

    ; Check Windows version
    ${If} ${AtLeastWin10}
        ; Windows 10 or later - continue
    ${Else}
        MessageBox MB_OK|MB_ICONSTOP "Windows 10 or later required!"
        Quit
    ${EndIf}

    ; Check if .NET Framework is installed (if needed)
    ReadRegDWORD $0 HKLM "SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full" "Release"
    ${If} $0 >= 528040 ; .NET Framework 4.8 or later
        ; .NET Framework is installed - continue
    ${Else}
        ; Silently download and install .NET Framework
        NSISdl::download "https://go.microsoft.com/fwlink/?LinkId=2085155" "$TEMP\netframework48.exe"
        ExecWait '"$TEMP\netframework48.exe" /q /norestart'
    ${EndIf}
FunctionEnd

Section -MainProgram
    ${INSTALL_TYPE}
    SetOverwrite on
    SetOutPath "$INSTDIR"

    ; Main executable and dependencies
    File "TimerAssistant.exe"

    ; Create application directory and set permissions
    CreateDirectory "$APPDATA\${APP_NAME}"
    AccessControl::GrantOnFile "$INSTDIR" "(S-1-5-32-545)" "FullAccess"
    AccessControl::GrantOnFile "$APPDATA\${APP_NAME}" "(S-1-5-32-545)" "FullAccess"

    ; Create shortcuts and registry entries
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${MAIN_APP_EXE}"

    ; Add to registry
    WriteRegStr ${REG_ROOT} "${REG_APP_PATH}" "" "$INSTDIR\${MAIN_APP_EXE}"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}" "DisplayName" "${APP_NAME}"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}" "DisplayIcon" "$INSTDIR\${MAIN_APP_EXE}"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}" "DisplayVersion" "${VERSION}"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}" "Publisher" "${COMP_NAME}"

    ; Create uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section Uninstall
    ${INSTALL_TYPE}

    ; Remove files and directories
    Delete "$INSTDIR\${MAIN_APP_EXE}"
    Delete "$INSTDIR\uninstall.exe"
    RMDir /r "$INSTDIR"

    ; Remove shortcuts
    Delete "$DESKTOP\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"

    ; Clean registry
    DeleteRegKey ${REG_ROOT} "${REG_APP_PATH}"
    DeleteRegKey ${REG_ROOT} "${UNINSTALL_PATH}"

    ; Remove app data
    RMDir /r "$APPDATA\${APP_NAME}"
SectionEnd