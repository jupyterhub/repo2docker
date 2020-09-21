#!/bin/bash
# This downloads and installs a pinned version of miniforge
# and sets up the base environment
set -ex


cd $(dirname $0)
MINIFORGE_VERSION=4.8.2-1
MAMBA_VERSION=0.5.1
# SHA256 for installers can be obtained from https://github.com/conda-forge/miniforge/releases
SHA256SUM="4f897e503bd0edfb277524ca5b6a5b14ad818b3198c2f07a36858b7d88c928db"

URL="https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-x86_64.sh"
INSTALLER_PATH=/tmp/miniforge-installer.sh

# make sure we don't do anything funky with user's $HOME
# since this is run as root
unset HOME

time wget --quiet $URL -O ${INSTALLER_PATH}
chmod +x ${INSTALLER_PATH}

# check sha256 checksum
if ! echo "${SHA256SUM}  ${INSTALLER_PATH}" | sha256sum  --quiet -c -; then
    echo "sha256 mismatch for ${INSTALLER_PATH}, exiting!"
    exit 1
fi

time bash ${INSTALLER_PATH} -b -p ${CONDA_DIR}
export PATH="${CONDA_DIR}/bin:$PATH"

# Preserve behavior of miniconda - packages come from conda-forge + defaults
conda config --system --append channels defaults

# Do not attempt to auto update conda or dependencies
conda config --system --set auto_update_conda false
conda config --system --set show_channel_urls true

# bug in conda 4.3.>15 prevents --set update_dependencies
echo 'update_dependencies: false' >> ${CONDA_DIR}/.condarc

# avoid future changes to default channel_priority behavior
conda config --system --set channel_priority "flexible"

# do all installation with mamba
time conda install -y mamba==${MAMBA_VERSION}
# switch back to conda
# ln -s $CONDA_DIR/bin/conda $CONDA_DIR/bin/mamba

echo "installing notebook env:"
cat /tmp/environment.yml
time mamba env create -p ${NB_PYTHON_PREFIX} -f /tmp/environment.yml

# Install jupyter-offline-notebook to allow users to download notebooks
# after the server connection has been lost
# This will install and enable the extension for jupyter notebook
time ${NB_PYTHON_PREFIX}/bin/python -m pip install jupyter-offlinenotebook==0.1.0
# and this installs it for lab. Keep going if the lab version is incompatible
# with the extension.
# Don't minimize build as it may fail, possibly due to excessive resource usage
# https://discourse.jupyter.org/t/tip-binder-jupyterlab-extension/6022
# https://discourse.jupyter.org/t/jupyter-lab-build-hangs-and-then-fails-at-webpack-config-webpack-prod-minimize-config-js/6017/3
time ${NB_PYTHON_PREFIX}/bin/jupyter labextension install --no-build jupyter-offlinenotebook && \
time $NB_PYTHON_PREFIX/bin/jupyter lab build --minimize=False || \
true

# empty conda history file,
# which seems to result in some effective pinning of packages in the initial env,
# which we don't intend.
# this file must not be *removed*, however
echo '' > ${NB_PYTHON_PREFIX}/conda-meta/history

if [[ -f /tmp/kernel-environment.yml ]]; then
    # install kernel env and register kernelspec
    echo "installing kernel env:"
    cat /tmp/kernel-environment.yml

    time mamba env create -p ${KERNEL_PYTHON_PREFIX} -f /tmp/kernel-environment.yml
    ${KERNEL_PYTHON_PREFIX}/bin/ipython kernel install --prefix "${NB_PYTHON_PREFIX}"
    echo '' > ${KERNEL_PYTHON_PREFIX}/conda-meta/history
    mamba list -p ${KERNEL_PYTHON_PREFIX}
fi

# Clean things out!
time mamba clean --all -f -y

# Remove the big installer so we don't increase docker image size too much
rm ${INSTALLER_PATH}

# Remove the pip cache created as part of installing miniforge
rm -rf /root/.cache

chown -R $NB_USER:$NB_USER ${CONDA_DIR}

mamba list -n root
mamba list -p ${NB_PYTHON_PREFIX}
