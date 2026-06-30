$INSTALL_PATH = Split-Path -Parent $MyInvocation.MyCommand.Path

$ROVOS_CORE_ROOT = Split-Path -Parent $INSTALL_PATH

$env:ROVOS_CORE = $ROVOS_CORE_ROOT

$env:PYTHONPATH = "$ROVOS_CORE_ROOT\devel;$env:PYTHONPATH"

$env:PYTHONPYCACHEPREFIX = "$ROVOS_CORE_ROOT\build\cache"

function rovos {
    if (Test-Path "$env:ROVOS_CORE\devel\cli\rovoscli.py") {
        python "$env:ROVOS_CORE\devel\cli\rovoscli.py" $args
    } else {
        python "$env:ROVOS_CORE\devel\cli\rovoscli" $args
    }
}

function ragent {
    if (Test-Path "$env:ROVOS_CORE\devel\cli\ragentcli.py") {
        python "$env:ROVOS_CORE\devel\cli\ragentcli.py" $args
    } else {
        python "$env:ROVOS_CORE\devel\cli\ragentcli" $args
    }
}

Write-Host "[ROVOS CORE] Underlay Environment Activated!" -ForegroundColor Cyan