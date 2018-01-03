#!/bin/bash
# This downloads and installs a pinned version of miniconda
set -ex

cd $(dirname $0)
CONDA_VERSION=4.3.30
URL="https://repo.continuum.io/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh"
INSTALLER_PATH=/tmp/miniconda-installer.sh

wget --quiet $URL -O ${INSTALLER_PATH}
chmod +x ${INSTALLER_PATH}

# Only MD5 checksums are available for miniconda
# Can be obtained from https://repo.continuum.io/miniconda/
MD5SUM="0b80a152332a4ce5250f3c09589c7a81"

if ! echo "${MD5SUM}  ${INSTALLER_PATH}" | md5sum  --quiet -c -; then
    echo "md5sum mismatch for ${INSTALLER_PATH}, exiting!"
    exit 1
fi

bash ${INSTALLER_PATH} -b -p ${CONDA_DIR}

# Allow easy direct installs from conda forge
${CONDA_DIR}/bin/conda config --system --add channels conda-forge

# Do not attempt to auto update conda or dependencies
${CONDA_DIR}/bin/conda config --system --set auto_update_conda false
# bug in conda 4.3.>15 prevents --set update_dependencies
echo 'update_dependencies: false' >> ${CONDA_DIR}/.condarc
${CONDA_DIR}/bin/conda config --system --set show_channel_urls true

${CONDA_DIR}/bin/conda env update -n root -f /tmp/environment.yml

if [[ -f /tmp/kernel-environment.yml ]]; then
    # install kernel env and register kernelspec
    ${CONDA_DIR}/bin/conda env create -n kernel -f /tmp/kernel-environment.yml
    ${CONDA_DIR}/envs/kernel/bin/ipython kernel install --prefix "${CONDA_DIR}"
fi

# Clean things out!
${CONDA_DIR}/bin/conda clean -tipsy

# Remove the big installer so we don't increase docker image size too much
rm ${INSTALLER_PATH}

chown -R $NB_USER:$NB_USER ${CONDA_DIR}
