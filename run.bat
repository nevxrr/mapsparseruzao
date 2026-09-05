@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if %ERRORLEVEL%==0 (
  py -3 run.py %*
  exit /b %ERRORLEVEL%
)

where python >nul 2>&1
if %ERRORLEVEL%==0 (
  python run.py %*
  exit /b %ERRORLEVEL%
)

echo Не найден Python.
echo Сначала установите Python и запустите install.bat
exit /b 1
