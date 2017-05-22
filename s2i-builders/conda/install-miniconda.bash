#!/bin/bash
# This downloads and installs a pinned version of miniconda
set -ex

cd $(dirname $0)
CONDA_VERSION=4.3.14
URL="https://repo.continuum.io/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh"
INSTALLER_PATH=/tmp/miniconda-installer.sh

wget --quiet $URL -O ${INSTALLER_PATH}
chmod +x ${INSTALLER_PATH}

# Only MD5 checksums are available for miniconda
# Can be obtained from https://repo.continuum.io/miniconda/
MD5SUM="fc6fc37479e3e3fcf3f9ba52cae98991"

if ! echo "${MD5SUM}  ${INSTALLER_PATH}" | md5sum  --quiet -c -; then
    echo "md5sum mismatch for ${INSTALLER_PATH}, exiting!"
    exit 1
fi

bash ${INSTALLER_PATH} -b -p ${CONDA_DIR}

# Allow easy direct installs from conda forge
${CONDA_DIR}/bin/conda config --system --add channels conda-forge

# Do not attempt to auto update conda or dependencies
${CONDA_DIR}/bin/conda config --system --set auto_update_conda false
${CONDA_DIR}/bin/conda config --system --set update_dependencies false
${CONDA_DIR}/bin/conda config --system --set show_channel_urls true

${CONDA_DIR}/bin/conda env update -n root -f /tmp/environment.yml
# Clean things out!
${CONDA_DIR}/bin/conda clean -tipsy

# Remove the big installer so we don't increase docker image size too much
rm ${INSTALLER_PATH}

chown -R $NB_USER:$NB_USER ${CONDA_DIR}
