# enable conda and activate the notebook environment
eval $(micromamba shell hook -s posix -p ${CONDA_DIR})
for name in conda mamba; do
    CONDA_PROFILE="${CONDA_DIR}/etc/profile.d/${name}.sh"
    test -f $CONDA_PROFILE && . $CONDA_PROFILE
done
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
