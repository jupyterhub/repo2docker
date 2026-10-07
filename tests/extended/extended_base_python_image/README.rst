ExtendImageBuildPack - full dependency set
-------------------------------------------

``runtime.txt`` names a public base image
(``ucbdatahub/jupyterlab-extended-base-python-image``) that already provides
a ``notebook`` conda env and the ``jovyan`` user, via the
``oci-image:`` prefix. ``environment.yaml`` (rather than
``.yml``) also exercises the buildpack's filename normalization.
``requirements.txt`` is additionally present, exercising every preassemble
step the buildpack supports (``install.R`` is covered separately by unit
tests, since it requires an R-enabled base image).
