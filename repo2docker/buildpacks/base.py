import textwrap
import jinja2
import tarfile
import io
import os
import stat
import re
import logging
import docker

TEMPLATE = r"""
FROM buildpack-deps:artful

# Set up locales properly
RUN apt-get update && \
    apt-get install --yes --no-install-recommends locales && \
    apt-get purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Use bash as default shell, rather than sh
ENV SHELL /bin/bash

# Set up user
ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
WORKDIR ${HOME}

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
       {% for package in base_packages -%}
       {{ package }} \
       {% endfor -%}
    && apt-get purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

{% if packages -%}
RUN apt-get update && \
    apt-get install --yes \
       {% for package in packages -%}
       {{ package }} \
       {% endfor -%}
    && apt-get purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
{% endif -%}

EXPOSE 8888

{% if env -%}
# Almost all environment variables
{% for item in env -%}
ENV {{item[0]}} {{item[1]}}
{% endfor -%}
{% endif -%}

{% if path -%}
# Special case PATH
ENV PATH {{ ':'.join(path) }}:${PATH}
{% endif -%}

{% if build_script_files -%}
# If scripts required during build are present, copy them
{% for src, dst in build_script_files.items() %}
COPY {{ src }} {{ dst }}
{% endfor -%}
{% endif -%}

{% for sd in build_script_directives -%}
{{sd}}
{% endfor %}

# Copy and chown stuff. This doubles the size of the repo, because
# you can't actually copy as USER, only as root! Thanks, Docker!
USER root
COPY src/ ${HOME}
RUN chown -R ${NB_USER}:${NB_USER} ${HOME}

# Run assemble scripts! These will actually build the specification
# in the repository into the image.
{% for sd in assemble_script_directives -%}
{{ sd }}
{% endfor %}

# Container image Labels!
# Put these at the end, since we don't want to rebuild everything
# when these change! Did I mention I hate Dockerfile cache semantics?
{% for k, v in labels.items() -%}
LABEL {{k}}={{v}}
{%- endfor %}

# We always want containers to run as non-root
USER ${NB_USER}

{% if post_build_scripts -%}
{% for s in post_build_scripts -%}
RUN ./{{ s }}
{% endfor %}
{% endif -%}
"""

DOC_URL = "http://repo2docker.readthedocs.io/en/latest/samples.html"


class BuildPack:
    """
    A composable BuildPack.

    Specifically used for creating Dockerfiles for use with repo2docker only.

    Things that are kept constant:
     - base image
     - some environment variables (such as locale)
     - user creation & ownership of home directory
     - working directory

    Everything that is configurable is additive & deduplicative,
    and there are *some* general guarantees of ordering.

    """

    def __init__(self):
        self.log = logging.getLogger('repo2docker')

    def get_packages(self):
        """
        List of packages that are installed in this BuildPack.

        Versions are not specified, and ordering is not guaranteed. These
        are usually installed as apt packages.
        """
        return set()

    def get_base_packages(self):
        """
        Base set of apt packages that are installed for all images.

        These contain useful images that are commonly used by a lot of images,
        where it would be useful to share a base docker image layer that
        contains them.

        These would be installed with a --no-install-recommends option.
        """
        return {
            # Utils!
            "less",

            # FIXME: Use npm from nodesource!
            # Everything seems to depend on npm these days, unfortunately.
            "npm",
        }

    def get_env(self):
        """
        Ordered list of environment variables to be set for this image.

        Ordered so that environment variables can use other environment
        variables in their values.

        Expects tuples, with the first item being the environment variable
        name and the second item being the value.
        """
        return []

    def get_path(self):
        """
        Ordered list of file system paths to look for executables in.

        Just sets the PATH environment variable. Separated out since
        it is very commonly set by various buildpacks.
        """
        return []

    def get_labels(self):
        """
        Docker labels to set on the built image.
        """
        return {}

    def get_build_script_files(self):
        """
        Dict of files to be copied to the container image for use in building.

        This is copied before the `build_scripts` & `assemble_scripts` are
        run, so can be executed from either of them.

        It's a dictionary where the key is the source file path in the host
        system, and the value is the destination file path inside the
        container image.
        """
        return {}

    def get_build_scripts(self):
        """
        Ordered list of shell script snippets to build the base image.

        A list of tuples, where the first item is a username & the
        second is a single logical line of a bash script that should
        be RUN as that user.

        These are run before the source of the repository is copied
        into the container image, and hence can not reference stuff
        from the repository. When the build scripts are done, the
        container image should be in a state where it is generically
        re-useable for building various other repositories with
        similar environments.

        You can use environment variable substitutions in both the
        username and the execution script.
        """
        return []

    def get_assemble_scripts(self):
        """
        Ordered list of shell script snippets to build the repo into the image.

        A list of tuples, where the first item is a username & the
        second is a single logical line of a bash script that should
        be RUN as that user.

        These are run after the source of the repository is copied into
        the container image (into the current directory). These should be
        the scripts that actually build the repository into the container
        image.

        If this needs to be dynamically determined (based on the presence
        or absence of certain files, for example), you can create any
        method and decorate it with `traitlets.default('assemble_scripts)`
        and the return value of this method is used as the value of
        assemble_scripts. You can expect that the script is running in
        the current directory of the repository being built when doing
        dynamic detection.

        You can use environment variable substitutions in both the
        username and the execution script.
        """
        return []

    def get_post_build_scripts(self):
        """
        An ordered list of executable scripts to execute after build.

        Is run as a non-root user, and must be executable. Used for doing
        things that are currently not supported by other means!

        The scripts should be as deterministic as possible - running it twice
        should not produce different results!
        """
        return []

    def binder_path(self, path):
        """Locate a file"""
        if os.path.exists('binder'):
            return os.path.join('binder', path)
        else:
            return path

    def detect(self):
        return True

    def render(self):
        """
        Render BuildPack into Dockerfile
        """
        t = jinja2.Template(TEMPLATE)

        build_script_directives = []
        last_user = 'root'
        for user, script in self.get_build_scripts():
            if last_user != user:
                build_script_directives.append("USER {}".format(user))
                last_user = user
            build_script_directives.append("RUN {}".format(
                textwrap.dedent(script.strip('\n'))
            ))

        assemble_script_directives = []
        last_user = 'root'
        for user, script in self.get_assemble_scripts():
            if last_user != user:
                assemble_script_directives.append("USER {}".format(user))
                last_user = user
            assemble_script_directives.append("RUN {}".format(
                textwrap.dedent(script.strip('\n'))
            ))

        return t.render(
            packages=sorted(self.get_packages()),
            path=self.get_path(),
            env=self.get_env(),
            labels=self.get_labels(),
            build_script_directives=build_script_directives,
            assemble_script_directives=assemble_script_directives,
            build_script_files=self.get_build_script_files(),
            base_packages=sorted(self.get_base_packages()),
            post_build_scripts=self.get_post_build_scripts(),
        )

    def build(self, image_spec, memory_limit, build_args):
        tarf = io.BytesIO()
        tar = tarfile.open(fileobj=tarf, mode='w')
        dockerfile_tarinfo = tarfile.TarInfo("Dockerfile")
        dockerfile = self.render().encode('utf-8')
        dockerfile_tarinfo.size = len(dockerfile)

        tar.addfile(
            dockerfile_tarinfo,
            io.BytesIO(dockerfile)
        )

        def _filter_tar(tar):
            # We need to unset these for build_script_files we copy into tar
            # Otherwise they seem to vary each time, preventing effective use
            # of the cache!
            # https://github.com/docker/docker-py/pull/1582 is related
            tar.uname = ''
            tar.gname = ''
            tar.uid = 1000
            tar.gid = 1000
            return tar

        for src in sorted(self.get_build_script_files()):
            src_parts = src.split('/')
            src_path = os.path.join(os.path.dirname(__file__), *src_parts)
            tar.add(src_path, src, filter=_filter_tar)

        tar.add('.', 'src/', filter=_filter_tar)

        tar.close()
        tarf.seek(0)

        limits = {
            # Always disable memory swap for building, since mostly
            # nothing good can come of that.
            'memswap': -1
        }
        if memory_limit:
            limits['memory'] = memory_limit
        client = docker.APIClient(version='auto',
                                  **docker.utils.kwargs_from_env())
        for line in client.build(
                fileobj=tarf,
                tag=image_spec,
                custom_context=True,
                buildargs=build_args,
                decode=True,
                forcerm=True,
                rm=True,
                container_limits=limits
        ):
            yield line


class BaseImage(BuildPack):
    def get_env(self):
        return [
            ("APP_BASE", "/srv")
        ]

    def detect(self):
        return True

    def get_assemble_scripts(self):
        assemble_scripts = []
        try:
            with open(self.binder_path('apt.txt')) as f:
                extra_apt_packages = []
                for l in f:
                    package = l.partition('#')[0].strip()
                    if not package:
                        continue
                    # Validate that this is, indeed, just a list of packages
                    # We're doing shell injection around here, gotta be careful.
                    # FIXME: Add support for specifying version numbers
                    if not re.match(r"^[a-z0-9.+-]+", package):
                        raise ValueError("Found invalid package name {} in "
                                         "apt.txt".format(package))
                    extra_apt_packages.append(package)

            assemble_scripts.append((
                'root',
                r"""
                apt-get update && \
                apt-get install --yes --no-install-recommends {} && \
                apt-get purge && \
                apt-get clean && \
                rm -rf /var/lib/apt/lists/*
                """.format(' '.join(extra_apt_packages))
            ))
        except FileNotFoundError:
            pass
        return assemble_scripts

    def get_post_build_scripts(self):
        post_build = self.binder_path('postBuild')
        if os.path.exists(post_build):
            if not stat.S_IXUSR & os.stat(post_build).st_mode:
                raise ValueError("%s is not executable, see %s for help." % (
                                 post_build,
                                 DOC_URL+'#system-post-build-scripts'))
            return [post_build]
        return []
