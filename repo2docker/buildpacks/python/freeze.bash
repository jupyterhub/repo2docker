#!/bin/bash
set -euo pipefail
# Freeze requirements.txt into requirements.frozen.txt, pinning all dependent library versions to
# versions that are resolved at time of freezing.
# Does the same for requirements2.txt to requirements2.frozen.txt...

# cd to the directory where the freeze script is located
dirname "$(readlink -f "$0")"

function freeze-requirements {
    # Freeze a requirements file $2 into a frozen requirements file $3
    # Requires that a completely empty venv of appropriate version exist in $1
    VENV_PATH="$1"
    REQUIREMENTS_FILE="$2"
    FROZEN_FILE="$3"

    ./${VENV_PATH}/bin/pip install --no-cache-dir -r ${REQUIREMENTS_FILE}
    echo "# AUTO GENERATED FROM ${REQUIREMENTS_FILE}, DO NOT MANUALLY MODIFY" > ${FROZEN_FILE}
    echo "# Frozen on $(date -u)" >> ${FROZEN_FILE}
    ./${VENV_PATH}/bin/pip freeze | sort >> ${FROZEN_FILE}
}

rm -rf py3venv
python3 -m venv py3venv
freeze-requirements py3venv requirements.txt requirements.frozen.txt
rm -rf py3venv


rm -rf py2venv
virtualenv -p python2 py2venv
freeze-requirements py2venv requirements2.txt requirements2.frozen.txt
rm -rf py2venv
