.. _deploy:

Using ``repo2docker`` as part of your Continuous Integration
============================================================

We've created for you the `continuous-build <https://www.github.com/binder-examples/continuous-build/>`_
repository so that you can push a `Docker <https://docs.docker.com/>`_ container
to `Docker Hub <https://hub.docker.com/>`_ directly from a Github repository
that has a Jupyter notebook. Here are instructions to do this.

Getting Started
---------------
Today you will be doing the following:

 1. Fork and clone the continuous-build Github repository to obtain the hidden ``.circleci`` folder.
 2. creating an image repository on Docker Hub
 3. connecting your repository to CircleCI
 4. push, commit, or create a pull request to trigger a build.

You don't need to install any dependencies on your host to build the container, it will be done
on a continuous integration server, and the container built and available to you
to pull from Docker Hub.


Step 1. Clone the Repository
............................
First, fork the `continuous-build <https://www.github.com/binder-examples/continuous-build/>`_ Github
repository to your account, and clone the branch.

   git clone https://www.github.com/<username>/continuous-build
   # or
   git clone git@github.com:<username>/continuous-build.git


Step 2. Choose your Configuration
.................................

The hidden folder `.circleci/config.yml` has instructions for `CircleCI <https://circleci.com/dashboard/>`_
to automatically discover and build your repo2docker jupyter notebook container.
The default template provided in the repository in this folder will do the most basic steps,
including:

1. clone of the repository with the notebook that you specify
2. build
3. push to Docker Hub

This repository aims to provide templates for your use.
If you have a request for a new template, please
`let us know <https://www.github.com/binder-examples/continuous-build/issues/>`_.
We will add templates as they are requested to do additional tasks like test containers, run
nbconvert, etc.

Thus, if I have a repository named ``myrepo`` and I want to use the default configuration on circleCI,
I would copy it there from the ``continuous-build`` folder. In the example below, I'm
creating a new folder called "myrepo" and then copying the entire folder there.

    mkdir -p myrepo
    cp -R continuous-build/.circleci myrepo/

You would then logically create a Github repository in the "myrepo" folder,
add the circleci configuration folder, and continue on to the next steps.

    cd myrepo
    git init
    git add .circleci


Step 3. Docker Hub
..................
Go to `Docker Hub <https://hub.docker.com/>`_, log in, and click the big blue
button that says "create repository" (not an automated build). Choose an organization
and name that you like (in the traditional format ``<ORG>/<NAME>``), and
remember it! We will be adding it, along with your
Docker credentials, to be encrypted CircleCI environment variables.


Step 4. Connect to CircleCI
...........................
If you navigate to the main `app page <https://circleci.com/dashboard/>`_ you
should be able to click "Add Projects" and then select your repository. If you don't
see it on the list, then select a different organization in the top left. Once
you find the repository, you can click the button to "Start Building" adn accept
the defaults.

Before you push or trigger a build, let's set up the following environment variables.
Also in the project interface on CirleCi, click the gears icon next to the project
name to get to your project settings. Under settings, click on the "Environment
Variables" tab. In this section, you want to define the following:

1. ``CONTAINER_NAME`` should be the name of the Docker Hub repository you just created.
2. ``DOCKER_TAG`` is the tag you want to use. If not defined, will use first 10 characters of commit.
3. ``DOCKER_USER`` and ``DOCKER_PASS`` should be your credentials (to allowing pushing)
4. ``REPO_NAME`` should be the full Github url (or other) of the repository with the notebook. This doesn't have to coincide with the repository you are using to do the build (e.g., "myrepo" in our example).

If you don't define the ``CONTAINER_NAME`` it will default to be the repository where it is
building from, which you should only do if the Docker Hub repository is named equivalently.
If you don't define either of the variables from step 3. for the Docker credentials, your
image will build but not be pushed to Docker Hub. Finally, if you don't define the ``REPO_NAME``
it will again use the name of the repository defined for the ``CONTAINER_NAME``.

Step 5. Push Away, Merrill!
...........................

Once the environment variables are set up, you can push or issue a pull request
to see circle build the workflow. Remember that you only need the ``.circleci/config.yml``
and not any other files in the repository. If your notebook is hosted in the same repo,
you might want to add these, along with your requirements.txt, etc.

.. tip::
    By default, new builds on CircleCI will not build for
    pull requests and you can change this default in the settings. You can easily add
    filters (or other criteria and actions) to be performed during or after the build
    by editing the ``.circleci/config.yml`` file in your repository.


Step 5. Use Your Container!
...........................

You should then be able to pull your new container, and run it! Here is an example:

  docker pull <ORG>/<NAME>
  docker run -it --name repo2docker -p 8888:8888 <ORG>/<NAME> jupyter notebook --ip 0.0.0.0


For a pre-built working example, try the following:

  docker pull vanessa/repo2docker
  docker run -it --name repo2docker -p 8888:8888 vanessa/repo2docker jupyter notebook --ip 0.0.0.0

You can then enter the url and token provided in the browser to access your notebook. When you are done and need to stop and remove the container:

  docker stop repo2docker
  docker rm repo2docker
