.. _builder:

Creating a New Builder for jupyter-repo2docker
----------------------------------------------
Builders determine how to transform the contents of a git repository
into a Docker image. They know how to handle things like dependency
files that are language-specific in order to create the computational
environment that you want.

Builders will be used along with ``s2i`` in order to create the Docker image.
These steps show the basics for creating your own builder. You'll need a
little bit of information about Dockerfiles and how they're created.

The most common reason to create a builder is if one does not yet exist
for a language that you wish to use. For example, below we'll demo
how to create a s2i builder for ``npm``, which may be used to install
``javascript`` packages.

Making a new s2i builder
========================

1. Choose a name for a new builder, ``<buildername>``. Typically, the
   ``<buildername>`` will correspond to a package manager name.

   For our example, we'll use ``npm``.

2. Move into the ``s2i-builders`` directory::

      cd s2i-builders

3. Initialize a directory where our image will live. We'll do this by
   running the ``s2i create`` like so::

      s2i create jupyterhub/repo2docker-<buildername> <buildername>

   Here's how it looks for our example::

      # Example `s2i create` command where <buildername> is npm
      s2i create jupyterhub/repo2docker-npm npm

4. Move into the newly-created directory::

      cd npm

5. Build the image by running::

      make

   This step creates a ``Dockerfile`` within the folder.

This Dockerfile contains will contain all of the instructions for
how to generate an image from a repository. Next we'll cover how to
fill this Dockerfile with instructions.

Modifying the Dockerfile
========================

Next we'll modify Dockerfile to perform the actions that we care about.
You can modify your ``Dockerfile`` and fill out the ``docker build`` as you want.
There are two files that may be edited:

1. **The ``Dockerfile`` for the builder itself**. This is used to
   create the base builder image (e.g. installing the base runtime environment).

2. **The ``s2i/bin/assemble`` script**. This is run
   when creating each new image from a given repository (e.g. pulling in
   repo-specific dependencies and repo contents). This manages the logic
   for how dependencies are installed.

<<<TODO: ADD EXAMPLE FOR NPM>>>

You can view the `existing s2i-builders
<https://github.com/jupyter/repo2docker/tree/master/s2i-builders>`_ in this repo for some examples.

Now that we have the basic scripts to generate images from a git repository,
we need to create a ``BuildPack`` in Python. ``repo2docker`` will use this
to know when we should run the scripts we've just created above.

Adding the BuildPack
====================

Once you builder image is finished, you need to add a Buildpack to run your
builds and to make sure that your new builder is used on the appropriate source
repos. For some examples, see `detectors.py
<https://github.com/jupyter/repo2docker/blob/master/repo2docker/detectors.py>`_.

1. Define your BuildPack class in ``detectors.py``. In most cases, you only need
   to implement two things if you subclass ``S2IBuildPack``:

    - **The ``detect`` method**. This should return a single ``bool`` variable
      that corresponds to whether this buildpack should be used for the given
      repository. For example, the ``conda`` buildpack checks to see whether
      ``environment.yml`` exists.
    - **The ``build_image``  attribute**. This defines which base Docker image
      will be used for the build. This can be set either via config or
      within the ``.detect()`` method.

2. Finally, to get the builder application to use your BuildPack, add it to
   the ``buildpacks`` list in ``app.py``.

Building / testing your builder
===============================
Once everything above is done, you will be able to build a repo by
specifying a source repo URL with this command::

  python3 -m repo2docker <url-to-source-repo>
