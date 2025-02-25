set -ex

# Setup conda
CONDA_PROFILE="${CONDA_DIR}/etc/profile.d/conda.sh"
echo "Activating profile: ${CONDA_PROFILE}"
test -f $CONDA_PROFILE && . $CONDA_PROFILE

# Setup micromamba
eval $(micromamba shell hook -s posix -r ${CONDA_DIR})

# Setup mamba
export MAMBA_ROOT_PREFIX="${CONDA_DIR}"
__mamba_setup="$("${CONDA_DIR}/bin/mamba" shell hook --shell posix 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__mamba_setup"
else
    alias mamba="${CONDA_DIR}/bin/mamba"  # Fallback on help from mamba activate
fi
unset __mamba_setup

# Activate the environment
if [[ "${KERNEL_PYTHON_PREFIX}" != "${NB_PYTHON_PREFIX}" ]]; then
    # if the kernel is a separate env, stack them
    # so both are on PATH, notebook first
    mamba activate ${KERNEL_PYTHON_PREFIX}
    mamba activate --stack ${NB_PYTHON_PREFIX}

    # even though it's second on $PATH
    # make sure CONDA_DEFAULT_ENV is the *kernel* env
    # so that `!conda install PKG` installs in the kernel env
    # where user packages are installed, not the notebook env
    # which only contains UI when the two are different
    export CONDA_DEFAULT_ENV="${KERNEL_PYTHON_PREFIX}"
else
    mamba activate ${NB_PYTHON_PREFIX}
fi

set +ex
