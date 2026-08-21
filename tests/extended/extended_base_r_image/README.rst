ExtendImageBuildPack - full dependency set (R)
-----------------------------------------------

``runtime.txt`` names a public base image
(``ucbdatahub/jupyterlab-extended-base-r-image``) that already provides
a ``notebook`` conda env, an R installation, and the ``jovyan`` user, via
the ``oci-image:`` prefix.

``apt.txt``, ``environment.yml``, and ``install.R`` are copied from a real UC Berkeley DataHub course image, so this exercises the buildpack's full preassemble pipeline (apt packages, a conda env update, and an ``Rscript install.R`` run, including Bioconductor packages installed via ``BiocManager``) against a realistically large, real-world dependency set.
