@echo off
setlocal EnableDelayedExpansion

:: ============================================================
::  MX-CARD Agent — Build Script
::  Step 1: Builds mxcardagent.exe (the agent)
::  Step 2: Builds mxcagent-installer.exe (installer + uninstaller)
::
::  Usage:
::    cd installer
::    build.bat
:: ============================================================

echo.
echo ============================================================
echo   MX-CARD Agent — Build Script
echo ============================================================
echo.

:: ── Determine paths ──────────────────────────────────────────

set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
for %%I in ("%SCRIPT_DIR%\..") do set "PROJECT_ROOT=%%~fI"

echo   Project root : %PROJECT_ROOT%
echo.

:: ── Check for .env ───────────────────────────────────────────

echo [1/5] Checking for .env file...
if not exist "%PROJECT_ROOT%\.env" (
    echo [ERROR] .env file not found at %PROJECT_ROOT%\.env
    echo         The exe needs .env with your API key baked in.
    goto :error
)
echo        .env found.
echo.

:: ── Check for PyInstaller ────────────────────────────────────

echo [2/5] Checking for PyInstaller...
pip show pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo        PyInstaller not found. Installing...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install PyInstaller.
        goto :error
    )
)
echo        PyInstaller OK.
echo.

:: ── Clean previous builds ────────────────────────────────────

echo [3/5] Cleaning previous builds...
if exist "%SCRIPT_DIR%\dist" rmdir /s /q "%SCRIPT_DIR%\dist"
if exist "%SCRIPT_DIR%\build" rmdir /s /q "%SCRIPT_DIR%\build"
mkdir "%SCRIPT_DIR%\dist"
echo        Clean.
echo.

:: ── Build the agent exe ──────────────────────────────────────

echo [4/5] Building mxcardagent.exe (agent)...
echo        This may take a few minutes...
echo.
pyinstaller "%SCRIPT_DIR%\mxcardagent.spec" --distpath "%SCRIPT_DIR%\dist" --workpath "%SCRIPT_DIR%\build" --noconfirm
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Agent build failed.
    goto :error
)

if not exist "%SCRIPT_DIR%\dist\mxcardagent.exe" (
    echo [ERROR] mxcardagent.exe not found after build.
    goto :error
)
echo.
for %%A in ("%SCRIPT_DIR%\dist\mxcardagent.exe") do echo        mxcardagent.exe — %%~zA bytes
echo.

:: ── Build the installer exe ─────────────────────────────────

echo [5/5] Building mxcagent-installer.exe (installer)...
echo        Bundling agent exe inside installer...
echo.
pyinstaller "%SCRIPT_DIR%\installer.spec" --distpath "%SCRIPT_DIR%\dist" --workpath "%SCRIPT_DIR%\build\installer" --noconfirm
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Installer build failed.
    goto :error
)

if not exist "%SCRIPT_DIR%\dist\mxcagent-installer.exe" (
    echo [ERROR] mxcagent-installer.exe not found after build.
    goto :error
)
echo.
for %%A in ("%SCRIPT_DIR%\dist\mxcagent-installer.exe") do echo        mxcagent-installer.exe — %%~zA bytes
echo.

:: ── Done ─────────────────────────────────────────────────────

echo ============================================================
echo   BUILD SUCCESSFUL
echo ============================================================
echo.
echo   Output:
echo     %SCRIPT_DIR%\dist\mxcagent-installer.exe
echo.
echo   This single .exe:
echo     - Installs mxcagent to your system
echo     - Adds it to PATH
echo     - Registers in Apps ^& Features
echo     - Embeds a full uninstaller
echo.
echo   Just run mxcagent-installer.exe to install!
echo.
echo ============================================================
echo.

goto :done

:error
echo.
echo ============================================================
echo   BUILD FAILED
echo ============================================================
echo.
pause
exit /b 1

:done
pause
exit /b 0
