# enable conda and activate the notebook environment
CONDA_PROFILE="${CONDA_DIR}/etc/profile.d/conda.sh"
test -f $CONDA_PROFILE && . $CONDA_PROFILE
if [[ "${KERNEL_PYTHON_PREFIX}" != "${NB_PYTHON_PREFIX}" ]]; then
    # if the kernel is a separate env, stack them
    # so both are on PATH
    mamba activate ${KERNEL_PYTHON_PREFIX}
    mamba activate --stack ${NB_PYTHON_PREFIX}
else
    mamba activate ${NB_PYTHON_PREFIX}
fi
