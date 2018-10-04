Docker - Edit mode
------------------

Using the --editable option with a local repository, one can modify a
file or create a new file in the container, and this change is
reflected in the respective host directory. It is essentially a
shortcut for `--mount
type=bind,source=<local-host-repository>,target=.` (where the target
resolves into the container working directory).

This is tested by running the change.sh script inside the container
(using the 'cmd' argument to the Repo2Docker app), which creates a new
file, and then verifying on the host side the new file is created with
the proper contents.

In practice, this can be used to run a notebook from inside a
container (which provides the proper environment), making changes as
necessary, which are then immediately reflected in the host
repository.
