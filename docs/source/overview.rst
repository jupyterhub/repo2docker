Overview
--------

Repo2Docker uses 
`source-to-image <https://github.com/openshift/source-to-image>`_ (s2i)
to turn a git repository into a Docker image. This image:

- may be used with Jupyter notebooks, including via JupyterHub
- includes the contents of the source git repo

This process is handled via an `s2i builder
<https://github.com/openshift/source-to-image/blob/master/docs/builder_image.md>`_.
A builder contains two components:

1. the **s2i builder image**, which turns GitHub repos into docker images
2. the **BuildPack object** in `repo2docker/detectors.py`, which detects
   which builder to use based on the source repo contents, and then invokes
   the appropriate, matching builder image

For instructions on customizing your own builder, see
:ref:`builder`.