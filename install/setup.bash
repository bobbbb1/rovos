#!/bin/bash

INSTALL_PATH="/opt/rovos/install"
ROVOS_CORE_ROOT="/opt/rovos"

export ROVOS_CORE="$ROVOS_CORE_ROOT"

if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH="$ROVOS_CORE_ROOT/devel"
else
    export PYTHONPATH="$ROVOS_CORE_ROOT/devel:$PYTHONPATH"
fi

export PYTHONPYCACHEPREFIX="$ROVOS_CORE_ROOT/build/cache"

rovos() {
    if [ -f "$ROVOS_CORE/devel/cli/rovoscli.py" ]; then
        python3 "$ROVOS_CORE/devel/cli/rovoscli.py" "$@"
    else
        python3 "$ROVOS_CORE/devel/cli/rovoscli" "$@"
    fi
}

ragent() {
    if [ -f "$ROVOS_CORE/devel/cli/ragentcli.py" ]; then
        python3 "$ROVOS_CORE/devel/cli/ragentcli.py" "$@"
    else
        python3 "$ROVOS_CORE/devel/cli/ragentcli" "$@"
    fi
}

echo -e "\e[36m[ROVOS CORE] Underlay Environment Activated!\e[0m"