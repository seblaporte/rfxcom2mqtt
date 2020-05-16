#!/bin/sh
set -e
SCRIPT_DIR_RFX=$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )
VIRTUAL_ENV_RFX=$SCRIPT_DIR_RFX/.venv
if [ -d "$VIRTUAL_ENV_RFX" ]; then
    export VIRTUAL_ENV_RFX
    PATH="$VIRTUAL_ENV_RFX/bin:$PATH"
    export PATH
fi
cd "$SCRIPT_DIR_RFX"
python3 ./rfxcom_gateway.py "$@"