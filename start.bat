@echo off
setlocal ENABLEEXTENSIONS
title Jinja2 Real-time Renderer Tool
echo Starting Jinja2 Tool...

set "MODE=%~1"
set "PIP_DISABLE_PIP_VERSION_CHECK=1"

:: Check Python
where python >nul 2>&1 || ( echo Error: Python is not installed or not in PATH. & exit /b 1 )

:: Param branches
if /I "%MODE%"=="install" goto INSTALL
if /I "%MODE%"=="noinstall" goto RUN

:: Auto install only when dependencies missing
python -m pip show Flask >nul 2>&1 && python -m pip show Jinja2 >nul 2>&1 && goto RUN

:INSTALL
echo Installing/Updating dependencies...
python -m pip install -r requirements.txt -q --no-input -i https://pypi.tuna.tsinghua.edu.cn/simple || goto RUN

:RUN
echo Starting Flask Server...
python app.py

endlocal
