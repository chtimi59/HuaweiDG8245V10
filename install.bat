@echo off 

if not exist "venv\" python -m venv venv
if "%~1"=="dev" goto dev
if "%~1"=="prod" goto prod

:usage
echo Usage: install.bat dev^|prod
exit /B 1

:dev
call venv\Scripts\activate.bat
pip install -U wheel pip setuptools
pip install -U -e %~p0[dev]
call venv\Scripts\deactivate.bat
exit /B 0

:prod
call venv\Scripts\activate.bat
pip install -U wheel pip setuptools
pip install -U -e %~p0
call venv\Scripts\deactivate.bat
exit /B 0
