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

:: =============================================================
:: Define Input Files
:: =============================================================
set "Org_file=%ScriptDir%Velan_Organization.txt"
set "Proj_file=%ScriptDir%Velan_Projects.txt"

:: =============================================================
:: Go to TC bin folder
:: =============================================================
pushd "%TC_ROOT%\bin"

echo.
echo =============================================================
echo Starting Importing Velan_Organization
echo =============================================================

call make_user.exe -u=infodba -p=infodba -g=dba -file="%Org_file%"

if errorlevel 1 (
    echo [WARNING] make_user.exe returned an error while importing Velan_Organization
)

echo.
echo =============================================================
echo Starting Importing Velan_Projects
echo =============================================================

call create_project.exe -u=infodba -p=infodba -g=dba -input="%Proj_file%"

if errorlevel 1 (
    echo [WARNING] create_project.exe returned an error while importing Velan_Projects
)

echo.
echo =============================================================
echo All imports executed
echo =============================================================

pause
popd
endlocal
