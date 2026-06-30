$CURRENT_INSTALL_PATH = Split-Path -Parent $MyInvocation.MyCommand.Path

$CORE_SETUP        = Join-Path $CURRENT_INSTALL_PATH "setup_core.ps1"
$THIRDPARTY_SETUP  = Join-Path $CURRENT_INSTALL_PATH "setup_thirdparty.ps1"

if (Test-Path $CORE_SETUP) {
    . $CORE_SETUP
} else {
    Write-Error "[ROVOS] Fatal: setup_core.ps1 tidak ditemukan di $CURRENT_INSTALL_PATH"
    exit 1
}

if (Test-Path $THIRDPARTY_SETUP) {
    . $THIRDPARTY_SETUP
    Write-Host "[ROVOS CORE] Third-party Environment Loaded!" -ForegroundColor Green
}

$Host.UI.RawUI.WindowTitle = "ROVOS PowerShell Terminal"