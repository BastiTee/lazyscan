@ECHO off

SETLOCAL 

REM SET LOCAL VARIABLES 

SET SCRIPT_PATH=scan_pages_and_create_pdf.py
SET CONTRAST=0
SET DPI=300

REM READ USER INPUT 

SET /P DPI=Set DPI for scanning (Default: %DPI%)? 
ECHO DPI set to %DPI%
IF %DPI% lss 100 GOTO :badinput
SET /P ANSWER=Keep temporary bitmap *.bmp files (Y/N)? 
ECHO You chose: %ANSWER% 
IF /i {%ANSWER%}=={y} (GOTO :yes) 
IF /i {%ANSWER%}=={yes} (GOTO :yes) 
GOTO :no 

REM SCAN WITH KEEPING TEMPORARY DATA
:yes 
%SCRIPT_PATH% -r %DPI% -c %CONTRAST% -keeptemp
GOTO :end

REM SCAN WITHOUT KEEPING TEMPORARY DATA
:no 
%SCRIPT_PATH% -r %DPI% -c %CONTRAST%
GOTO :end

:badinput
ECHO DPI must be greater or equal 100.
GOTO :end

:end
ENDLOCAL
EXIT /b 1

