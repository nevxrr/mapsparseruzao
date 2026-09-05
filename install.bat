@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if %ERRORLEVEL%==0 (
  py -3 -m pip install -r requirements.txt
  goto :done
)

where python >nul 2>&1
if %ERRORLEVEL%==0 (
  python -m pip install -r requirements.txt
  goto :done
)

echo Не найден Python.
echo Скачайте https://www.python.org/downloads/
echo При установке включите галочку "Add python.exe to PATH".
exit /b 1

:done
if %ERRORLEVEL% NEQ 0 (
  echo Установка библиотек не удалась.
  exit /b 1
)
echo.
echo Готово. Дальше запустите run.bat
exit /b 0
