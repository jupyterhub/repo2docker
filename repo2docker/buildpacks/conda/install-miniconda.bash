#!/bin/bash
# This downloads and installs a pinned version of miniconda
set -ex

cd $(dirname $0)
MINICONDA_VERSION=4.7.12.1
CONDA_VERSION=4.7.12
# Only MD5 checksums are available for miniconda
# Can be obtained from https://repo.continuum.io/miniconda/
MD5SUM="81c773ff87af5cfac79ab862942ab6b3"

URL="https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh"
INSTALLER_PATH=/tmp/miniconda-installer.sh

# make sure we don't do anything funky with user's $HOME
# since this is run as root
unset HOME

wget --quiet $URL -O ${INSTALLER_PATH}
chmod +x ${INSTALLER_PATH}

# check md5 checksum
if ! echo "${MD5SUM}  ${INSTALLER_PATH}" | md5sum  --quiet -c -; then
    echo "md5sum mismatch for ${INSTALLER_PATH}, exiting!"
    exit 1
fi

bash ${INSTALLER_PATH} -b -p ${CONDA_DIR}
export PATH="${CONDA_DIR}/bin:$PATH"

# Allow easy direct installs from conda forge
conda config --system --add channels conda-forge

# Do not attempt to auto update conda or dependencies
conda config --system --set auto_update_conda false
conda config --system --set show_channel_urls true
# avoid future changes to default channel_priority behavior
conda config --system --set channel_priority "flexible"

# bug in conda 4.3.>15 prevents --set update_dependencies
echo 'update_dependencies: false' >> ${CONDA_DIR}/.condarc

# install conda itself
if [[ "${CONDA_VERSION}" != "${MINICONDA_VERSION}" ]]; then
    conda install -yq conda==${CONDA_VERSION}
fi

# Install mamba
# FIXME: Should this happen prior to config setting?
conda install -c conda-forge -c conda-forge/label/mamba-alpha mamba

echo "installing notebook env:"
cat /tmp/environment.yml
mamba env create -p ${NB_PYTHON_PREFIX} -f /tmp/environment.yml

# Install jupyter-offline-notebook to allow users to download notebooks
# after the server connection has been lost
# This will install and enable the extension for jupyter notebook
${NB_PYTHON_PREFIX}/bin/python -m pip install https://github.com/manics/jupyter-offlinenotebook/archive/7ba3520.zip
# and this installs it for lab. Keep going if the lab version is incompatible
# with the extension
${NB_PYTHON_PREFIX}/bin/jupyter labextension install jupyter-offlinenotebook || true

# empty conda history file,
# which seems to result in some effective pinning of packages in the initial env,
# which we don't intend.
# this file must not be *removed*, however
echo '' > ${NB_PYTHON_PREFIX}/conda-meta/history

if [[ -f /tmp/kernel-environment.yml ]]; then
    # install kernel env and register kernelspec
    echo "installing kernel env:"
    cat /tmp/kernel-environment.yml

    mamba env create -p ${KERNEL_PYTHON_PREFIX} -f /tmp/kernel-environment.yml
    ${KERNEL_PYTHON_PREFIX}/bin/ipython kernel install --prefix "${NB_PYTHON_PREFIX}"
    echo '' > ${KERNEL_PYTHON_PREFIX}/conda-meta/history
    mamba list -p ${KERNEL_PYTHON_PREFIX}
fi

# Clean things out!
mamba clean --all -f -y

# Remove the big installer so we don't increase docker image size too much
rm ${INSTALLER_PATH}

# Remove the pip cache created as part of installing miniconda
rm -rf /root/.cache

chown -R $NB_USER:$NB_USER ${CONDA_DIR}

mamba -V
mamba list -n root
mamba list -p ${NB_PYTHON_PREFIX}
