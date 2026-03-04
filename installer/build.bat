@echo off
setlocal EnableDelayedExpansion

:: ============================================================
::  MX-CARD Agent — Build Script
::  Builds a single mxcardagent.exe with everything baked in.
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

echo [1/4] Checking for .env file...
if not exist "%PROJECT_ROOT%\.env" (
    echo [ERROR] .env file not found at %PROJECT_ROOT%\.env
    echo         The exe needs .env with your API key baked in.
    goto :error
)
echo        .env found.
echo.

:: ── Check for PyInstaller ────────────────────────────────────

echo [2/4] Checking for PyInstaller...
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

echo [3/4] Cleaning previous builds...
if exist "%SCRIPT_DIR%\dist" rmdir /s /q "%SCRIPT_DIR%\dist"
if exist "%SCRIPT_DIR%\build" rmdir /s /q "%SCRIPT_DIR%\build"
mkdir "%SCRIPT_DIR%\dist"
echo        Clean.
echo.

:: ── Build the exe ────────────────────────────────────────────

echo [4/4] Building mxcardagent.exe...
echo        This may take a few minutes...
echo.
pyinstaller "%SCRIPT_DIR%\mxcardagent.spec" --distpath "%SCRIPT_DIR%\dist" --workpath "%SCRIPT_DIR%\build" --noconfirm
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Build failed.
    goto :error
)
echo.

:: Verify
if not exist "%SCRIPT_DIR%\dist\mxcardagent.exe" (
    echo [ERROR] mxcardagent.exe not found after build.
    goto :error
)

:: ── Done ─────────────────────────────────────────────────────

echo ============================================================
echo   BUILD SUCCESSFUL
echo ============================================================
echo.
echo   Output:
echo     %SCRIPT_DIR%\dist\mxcardagent.exe
echo.
for %%A in ("%SCRIPT_DIR%\dist\mxcardagent.exe") do echo   Size: %%~zA bytes
echo.
echo   This single exe has everything baked in:
echo     - Python runtime
echo     - All dependencies
echo     - Agent source code
echo     - API key from .env
echo.
echo   Just copy it anywhere and run it. No install needed.
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
