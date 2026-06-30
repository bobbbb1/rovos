function rovjoy {
    if (Test-Path "$env:ROVOS_CORE\install\thirdparty\joy\main.py") {
        python "$env:ROVOS_CORE\install\thirdparty\joy\main.py" $args
    } else {
        python "$env:ROVOS_CORE\install\thirdparty\joy\main" $args
    }
}
