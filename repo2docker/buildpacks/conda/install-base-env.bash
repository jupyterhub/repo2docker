#!/bin/bash
# This downloads and installs a pinned version of micromamba
# and sets up the base environment
set -ex

cd $(dirname $0)

export MAMBA_VERSION=1.5.7
export CONDA_VERSION=24.3.0

URL="https://anaconda.org/conda-forge/micromamba/${MAMBA_VERSION}/download/${CONDA_PLATFORM}/micromamba-${MAMBA_VERSION}-0.tar.bz2"

# make sure we don't do anything funky with user's $HOME
# since this is run as root
unset HOME
mkdir -p ${CONDA_DIR}

export MICROMAMBA_EXE="/usr/local/bin/micromamba"

time wget -qO- ${URL} | tar -xvj bin/micromamba
mv bin/micromamba "$MICROMAMBA_EXE"
chmod 0755 "$MICROMAMBA_EXE"

eval "$(${MICROMAMBA_EXE} shell hook -p ${CONDA_DIR} -s posix)"

micromamba activate

export PATH="${PWD}/bin:$PATH"

cat <<EOT >> ${CONDA_DIR}/.condarc
channels:
  - conda-forge
  - defaults
auto_update_conda: false
show_channel_urls: true
update_dependencies: false
# channel_priority: flexible
EOT

micromamba install conda=${CONDA_VERSION} mamba=${MAMBA_VERSION} -y

echo "installing notebook env:"
cat "${NB_ENVIRONMENT_FILE}"


time ${MAMBA_EXE} create -p ${NB_PYTHON_PREFIX} --file "${NB_ENVIRONMENT_FILE}"

if [[ ! -z "${NB_REQUIREMENTS_FILE:-}" ]]; then
    echo "installing pip requirements"
    cat "${NB_REQUIREMENTS_FILE}"
    ${NB_PYTHON_PREFIX}/bin/python -mpip install --no-cache --no-deps -r "${NB_REQUIREMENTS_FILE}"
fi
# empty conda history file,
# which seems to result in some effective pinning of packages in the initial env,
# which we don't intend.
# this file must not be *removed*, however
echo '' > ${NB_PYTHON_PREFIX}/conda-meta/history

if [[ ! -z "${KERNEL_ENVIRONMENT_FILE:-}" ]]; then
    # install kernel env and register kernelspec
    echo "installing kernel env:"
    cat "${KERNEL_ENVIRONMENT_FILE}"
    time ${MAMBA_EXE} create -p ${KERNEL_PYTHON_PREFIX} --file "${KERNEL_ENVIRONMENT_FILE}"

    if [[ ! -z "${KERNEL_REQUIREMENTS_FILE:-}" ]]; then
        echo "installing pip requirements for kernel"
        cat "${KERNEL_REQUIREMENTS_FILE}"
        ${KERNEL_PYTHON_PREFIX}/bin/python -mpip install --no-cache --no-deps -r "${KERNEL_REQUIREMENTS_FILE}"
    fi

    ${KERNEL_PYTHON_PREFIX}/bin/ipython kernel install --prefix "${NB_PYTHON_PREFIX}"
    echo '' > ${KERNEL_PYTHON_PREFIX}/conda-meta/history
    ${MAMBA_EXE} list -p ${KERNEL_PYTHON_PREFIX}
fi

# Clean things out!
time ${MAMBA_EXE} clean --all -f -y

# Remove the pip cache created as part of installing micromamba
rm -rf /root/.cache

chown -R $NB_USER:$NB_USER ${CONDA_DIR}

${MAMBA_EXE} list -p ${NB_PYTHON_PREFIX}

# Set NPM config
${NB_PYTHON_PREFIX}/bin/npm config --global set prefix ${NPM_DIR}
