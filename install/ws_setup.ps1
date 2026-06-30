if (-not $env:ROVOS_CORE) {
    Write-Host "[ERROR] Core not activated!" -ForegroundColor Red
    return
}

$ROVOS_WORKSPACE = Get-Location

$env:PYTHONPATH = "$ROVOS_WORKSPACE\devel\msgs;$env:PYTHONPATH"

$env:PYTHONPYCACHEPREFIX = "$ROVOS_WORKSPACE\build\cache"

$env:ROVOS_WS_ACTIVE = "1"

Write-Host "[ROVOS WORKSPACE] Overlay Environment Activated!" -ForegroundColor Green