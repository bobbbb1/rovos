#!/bin/bash

if [ -z "$ROVOS_CORE" ]; then
    echo -e "\e[31m[ERROR] Core not activated!\e[0m"

    return 2>/dev/null || exit 1
fi

ROVOS_WORKSPACE="$(pwd)"

if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH="$ROVOS_WORKSPACE/devel/msgs"
else
    export PYTHONPATH="$ROVOS_WORKSPACE/devel/msgs:$PYTHONPATH"
fi

export PYTHONPYCACHEPREFIX="$ROVOS_WORKSPACE/build/cache"

export ROVOS_WS_ACTIVE="1"

echo -e "\e[32m[ROVOS WORKSPACE] Overlay Environment Activated!\e[0m"