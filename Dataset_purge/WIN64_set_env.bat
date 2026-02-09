set CUR_DIR=%~dps0 
echo "Please set up your enviroment variables!"

set TC_ROOT=D:\Siemens\TC2506\TC_ROOT
set TC_DATA=D:\Siemens\TC2506\TC_DATA
set TC_BIN=%TC_ROOT%\bin
set TC_INCLUDE=%TC_ROOT%\include
set DEV_TOOL=D:\Visual_Studio\Microsoft Visual Studio\2022\Professional\Common7\IDE\devenv.exe
call %TC_DATA%\tc_profilevars.bat

GOTO CONTINUE

:CONTINUE
cd %CUR_DIR%
"%DEV_TOOL%" dataset_purge.sln
goto END

:END