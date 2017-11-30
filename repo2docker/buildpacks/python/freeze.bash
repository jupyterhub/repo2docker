#!/bin/bash
set -euo pipefail
# Freeze requirements.txt into requirements.frozen.txt, pinning all dependent library versions to
# versions that are resolved at time of freezing.
# Does the same for requirements2.txt to requirements2.frozen.txt...

# cd to the directory where the freeze script is located
if [[ ! -z "$(which realpath 2>/dev/null)" ]]; then
    realpath=realpath
else
    realpath="readlink -f"
fi

cd $(dirname "$($realpath "$0")")


function freeze-requirements {
    # Freeze a requirements file $2 into a frozen requirements file $3
    # Requires that a completely empty venv of appropriate version exist in $1
    PYTHON_VERSION="$1"
    REQUIREMENTS_FILE="$2"
    FROZEN_FILE="$3"
    if [[ $(echo ${PYTHON_VERSION} | cut -d. -f 1) == "2" ]]; then
        VENV=virtualenv
    else
        VENV=venv
    fi

    echo "# AUTO GENERATED FROM ${REQUIREMENTS_FILE}, DO NOT MANUALLY MODIFY" > ${FROZEN_FILE}
    echo "# Frozen on $(date -u)" >> ${FROZEN_FILE}
    docker run --rm -v $PWD:/python -it python:${PYTHON_VERSION} \
        sh -c "
            python -m $VENV /venv
            /venv/bin/pip install -r /python/${REQUIREMENTS_FILE} &&
            /venv/bin/pip freeze | sort --ignore-case >> /python/${FROZEN_FILE}"
}

freeze-requirements 3.5 requirements.txt requirements.frozen.txt
freeze-requirements 2.7 requirements2.txt requirements2.frozen.txt
