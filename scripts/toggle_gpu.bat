@echo off
setlocal enabledelayedexpansion

echo =============================================
echo   NVIDIA GPU Toggler (Interactive Script)
echo =============================================
echo.

echo Listing NVIDIA GPUs...
echo ---------------------------------------------
set count=0
rem List only lines that start with "PCI\VEN_10DE" (ignoring audio and extra messages)
for /f "delims=" %%A in ('devcon find "PCI\VEN_10DE*" ^| findstr /R "^PCI\\VEN_10DE"') do (
    set /a count+=1
    set "gpu[!count!]=%%A"
    echo [!count!] %%A
)
echo ---------------------------------------------
echo.
echo %count% matching device(s) found.
echo.

if "%count%"=="0" (
    echo No NVIDIA GPUs found.
    pause
    goto :end
)

:choose
set /p choice="Enter the number of the GPU you want to toggle: "
if not defined gpu[%choice%] (
    echo Invalid choice. Please try again.
    goto :choose
)

rem Extract the hardware ID (text before the first colon) from the selected line
for /f "tokens=1 delims=:" %%I in ("!gpu[%choice%]!") do (
    set "selectedID=%%I"
)

echo.
echo You selected: !gpu[%choice%]!
echo.
echo Current status for !selectedID!:
devcon status "!selectedID!"
echo.

:actionPrompt
set /p action="Do you want to ENABLE or DISABLE this GPU? (type enable/disable or exit to quit): "
if /I "%action%"=="enable" (
    echo Enabling GPU: !selectedID!...
    devcon enable "!selectedID!"
    echo GPU enabled.
) else if /I "%action%"=="disable" (
    echo Disabling GPU: !selectedID!...
    devcon disable "!selectedID!"
    echo GPU disabled.
) else if /I "%action%"=="exit" (
    goto :end
) else (
    echo Invalid action. Please type "enable", "disable", or "exit".
    goto :actionPrompt
)

echo.
echo Updated status for !selectedID!:
devcon status "!selectedID!"
echo.
pause

:end
endlocal
