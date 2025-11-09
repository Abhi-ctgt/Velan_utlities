@echo off
setlocal enabledelayedexpansion

:: =============================================================
:: Define paths
:: =============================================================
set "ScriptDir=%~dp0"
set "TCENV=D:\Siemens\TC2506\TC_ROOT\tc_menu\TC2506_Env_001.bat"

:: =============================================================
:: Load Teamcenter Environment
:: =============================================================
if exist "%TCENV%" (
  echo Loading Teamcenter environment...
  call "%TCENV%"
  echo Environment loaded successfully.
  ) else (
  echo [ERROR] Teamcenter environment file not found: %TCENV%
  pause
  exit /b
)

set "ScriptDir=%~dp0"

:: Remove trailing backslash if present
if "%ScriptDir:~-1%"=="\" set "ScriptDir=%ScriptDir:~0,-1%"

:: Go one level up (to reach workspace or main folder)
for %%A in ("%ScriptDir%\..") do set "WorkspaceDir=%%~fA"

:: Define the preference folder path
set "PreferencesFolder=%WorkspaceDir%\preferences"

:: Verify folder exists
if not exist "%PreferencesFolder%" (
  echo [ERROR] Preference folder not found: %PreferencesFolder%
  pause
  exit /b
)

echo Preference folder found: "%PreferencesFolder%"
echo.

echo.
echo =============================================================
echo Starting Import Process
echo =============================================================

:: =============================================================
:: Run each import script (in same console)
:: =============================================================
call "%ScriptDir%import_column_config.bat"
if errorlevel 1 echo [WARNING] import_column_config.bat returned an error.

echo -------------------------------------------------------------
call "%ScriptDir%preference_utility.exe  -u=11 -p=22 -g=33 -path="%PreferencesFolder%""
if errorlevel 1 echo [WARNING] preference_utility.exe returned an error.

echo -------------------------------------------------------------
call "%ScriptDir%import_datasets_preferences.bat"
if errorlevel 1 echo [WARNING] import_datasets_preferences.bat returned an error.


echo.
echo =============================================================
echo All scripts executed
echo =============================================================
pause
endlocal