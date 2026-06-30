@echo off

if "%ROVOS_CORE%"=="" (
    echo [ERROR] Core not activated!
    exit /b 1
)

set "ROVOS_WORKSPACE=%CD%"

set "PYTHONPATH=%ROVOS_WORKSPACE%\devel\msgs;%PYTHONPATH%"

set "PYTHONPYCACHEPREFIX=%ROVOS_WORKSPACE%\build\cache"

set ROVOS_WS_ACTIVE = "1"

echo [ROVOS WORKSPACE] Overlay Environment Activated!