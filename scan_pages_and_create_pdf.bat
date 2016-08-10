@ECHO off

SETLOCAL

REM SET LOCAL VARIABLES

SET SCRIPT_PATH=scan_pages_and_create_pdf.py
SET CONTRAST=0
SET DPI=300
SET JPGQ=50

REM READ USER INPUT

SET /P DPI=Set DPI for scanning (Default: %DPI%)?
ECHO DPI set to %DPI%
IF %DPI% lss 100 GOTO :badinputdpi
IF %DPI% gtr 1000 GOTO :badinputdpi

SET /P JPGQ=Set JPEG quality for PDF (Default: %JPGQ%)?
ECHO JPGQ set to %JPGQ%
IF %JPGQ% lss 10 GOTO :badinputjpg
IF %JPGQ% gtr 100 GOTO :badinputjpg

SET /P ANSWER=Keep temporary bitmap *.bmp files (Y/N)?
ECHO You chose: %ANSWER%
IF /i {%ANSWER%}=={y} (GOTO :yes)
IF /i {%ANSWER%}=={yes} (GOTO :yes)
GOTO :no

REM SCAN WITH KEEPING TEMPORARY DATA
:yes
%SCRIPT_PATH% -r %DPI% -c %CONTRAST% -i %JPGQ% -k
GOTO :end

REM SCAN WITHOUT KEEPING TEMPORARY DATA
:no
%SCRIPT_PATH% -r %DPI% -c %CONTRAST% -i %JPGQ%
GOTO :end

:badinputdpi
ECHO DPI must be between 100 and 1000.
GOTO :end

:badinputjpg
ECHO JPG quality must be between 10 and 100.
GOTO :end

:end
ENDLOCAL
EXIT /b 1

