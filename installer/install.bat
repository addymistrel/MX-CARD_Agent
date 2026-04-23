@echo off
setlocal EnableDelayedExpansion

:: ============================================================
::  MX-CARD Agent - Installer
::  Installs mxcardagent.exe to system and adds to PATH.
::
::  Usage:  Run install.bat after build.bat
:: ============================================================

echo.
echo ============================================================
echo   MX-CARD Agent - Installer
echo ============================================================
echo.

:: ── Determine paths ──────────────────────────────────────────

set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "EXE_SRC=%SCRIPT_DIR%\dist\mxcardagent.exe"
set "INSTALL_DIR=%LOCALAPPDATA%\MXCardAgent"

:: ── Check exe exists ─────────────────────────────────────────

echo [1/4] Checking for mxcardagent.exe...
if not exist "%EXE_SRC%" (
    echo.
    echo [ERROR] mxcardagent.exe not found at:
    echo         %EXE_SRC%
    echo.
    echo         Please run build.bat first.
    goto :error
)
echo        Found mxcardagent.exe
echo.

:: ── Create install directory ─────────────────────────────────

echo [2/4] Installing to %INSTALL_DIR%...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy the exe
copy /y "%EXE_SRC%" "%INSTALL_DIR%\mxcagent.exe" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to copy exe. Is it running?
    goto :error
)
echo        Copied mxcagent.exe
echo.

:: ── Create uninstaller ───────────────────────────────────────

echo [3/4] Creating uninstaller...

(
echo @echo off
echo setlocal EnableDelayedExpansion
echo.
echo echo.
echo echo ============================================================
echo echo   MX-CARD Agent - Uninstaller
echo echo ============================================================
echo echo.
echo echo This will completely remove MX-CARD Agent from your system.
echo echo.
echo set /p "CONFIRM=Are you sure? [Y/N]: "
echo if /i "%%CONFIRM%%" NEQ "Y" ^(
echo     echo Uninstall cancelled.
echo     pause
echo     exit /b 0
echo ^)
echo echo.
echo echo [1/3] Removing from PATH...
echo :: Read current user PATH
echo for /f "tokens=2,*" %%%%A in ^('reg query "HKCU\Environment" /v Path 2^^^>nul'^) do set "CURRENT_PATH=%%%%B"
echo :: Remove our install dir from PATH
echo set "NEW_PATH=%%CURRENT_PATH%%"
echo set "NEW_PATH=!NEW_PATH:%%LOCALAPPDATA%%\MXCardAgent;=!"
echo set "NEW_PATH=!NEW_PATH:;%%LOCALAPPDATA%%\MXCardAgent=!"
echo set "NEW_PATH=!NEW_PATH:%%LOCALAPPDATA%%\MXCardAgent=!"
echo if "!NEW_PATH!" NEQ "%%CURRENT_PATH%%" ^(
echo     reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "!NEW_PATH!" /f ^>nul 2^>^&1
echo     echo        Removed from PATH.
echo ^) else ^(
echo     echo        Was not in PATH.
echo ^)
echo echo.
echo echo [2/3] Removing files...
echo del /f /q "%%LOCALAPPDATA%%\MXCardAgent\mxcagent.exe" 2^>nul
echo echo        Removed mxcagent.exe
echo echo.
echo echo [3/3] Broadcasting PATH change...
echo powershell -NoProfile -Command "[System.Environment]::SetEnvironmentVariable('_dummy_','1','User'); [System.Environment]::SetEnvironmentVariable('_dummy_',$null,'User')" 2^>nul
echo echo.
echo echo ============================================================
echo echo   MX-CARD Agent has been completely uninstalled.
echo echo ============================================================
echo echo.
echo echo Note: The uninstaller folder will remain. You can delete it:
echo echo   %%LOCALAPPDATA%%\MXCardAgent
echo echo.
echo pause
echo :: Self-delete: start a background cmd to delete us after exit
echo start /b "" cmd /c "timeout /t 2 /nobreak >nul & rmdir /s /q "%%LOCALAPPDATA%%\MXCardAgent""
) > "%INSTALL_DIR%\uninstall.bat"

echo        Created uninstall.bat at %INSTALL_DIR%
echo.

:: ── Add to user PATH ─────────────────────────────────────────

echo [4/4] Adding to PATH...

:: Check if already in PATH
echo %PATH% | findstr /i /c:"%INSTALL_DIR%" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo        Already in PATH.
) else (
    :: Read current user PATH from registry
    for /f "tokens=2,*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%B"
    
    if "!USER_PATH!"=="" (
        :: No user PATH exists, create one
        reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "%INSTALL_DIR%" /f >nul 2>&1
    ) else (
        :: Append to existing user PATH
        reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "!USER_PATH!;%INSTALL_DIR%" /f >nul 2>&1
    )
    
    :: Broadcast WM_SETTINGCHANGE so open terminals pick it up
    powershell -NoProfile -Command "[System.Environment]::SetEnvironmentVariable('_dummy_','1','User'); [System.Environment]::SetEnvironmentVariable('_dummy_',$null,'User')" 2>nul
    
    echo        Added %INSTALL_DIR% to user PATH.
)
echo.

:: ── Done ─────────────────────────────────────────────────────

echo ============================================================
echo.
echo   mxcagent has been successfully installed!
echo.
echo   You can now run it from anywhere using:
echo.
echo       mxcagent
echo.
echo   Install location:
echo       %INSTALL_DIR%\mxcagent.exe
echo.
echo   To uninstall, run:
echo       %INSTALL_DIR%\uninstall.bat
echo.
echo   NOTE: Open a NEW terminal for PATH changes to take effect.
echo.
echo ============================================================
echo.

goto :done

:error
echo.
echo ============================================================
echo   INSTALLATION FAILED
echo ============================================================
echo.
pause
exit /b 1

:done
pause
exit /b 0
