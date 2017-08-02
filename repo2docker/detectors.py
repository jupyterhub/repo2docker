"""
Generates a variety of Dockerfiles based on an input matrix
"""
import textwrap
from traitlets.config import LoggingConfigurable
from traitlets import Unicode, Set, List, Dict, Tuple, Bool, default
from textwrap import dedent
import jinja2
import tarfile
import io
import os
import stat
import re
import json
import docker

TEMPLATE = r"""
FROM buildpack-deps:zesty

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
ENV NB_USER jovyan
ENV NB_UID 1000
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


class BuildPack(LoggingConfigurable):
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
    packages = Set(
        set(),
        help="""
        List of packages that are installed in this BuildPack by default.

        Versions are not specified, and ordering is not guaranteed. These
        are usually installed as apt packages.
        """
    )

    base_packages = Set(
        {
            # Utils!
            "less",

            # FIXME: Use npm from nodesource!
            # Everything seems to depend on npm these days, unfortunately.
            "npm",
            "nodejs-legacy"
        },
        help="""
        Base set of apt packages that are installed for all images.

        These contain useful images that are commonly used by a lot of images,
        where it would be useful to share a base docker image layer that contains
        them.

        These would be installed with a --no-install-recommends option.
        """
    )

    env = List(
        [],
        help="""
        Ordered list of environment variables to be set for this image.

        Ordered so that environment variables can use other environment
        variables in their values.

        Expects tuples, with the first item being the environment variable
        name and the second item being the value.
        """
    )

    path = List(
        [],
        help="""
        Ordered list of file system paths to look for executables in.

        Just sets the PATH environment variable. Separated out since
        it is very commonly set by various buildpacks.
        """
    )

    labels = Dict(
        {},
        help="""
        Docker labels to set on the built image.
        """
    )

    build_script_files = Dict(
        {},
        help="""
        List of files to be copied to the container image for use in building.

        This is copied before the `build_scripts` & `assemble_scripts` are
        run, so can be executed from either of them.

        It's a dictionary where the key is the source file path in the host
        system, and the value is the destination file path inside the
        container image.
        """
    )

    build_scripts = List(
        [],
        help="""
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
    )

    assemble_scripts = List(
        [],
        help="""
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
    )

    post_build_scripts = List(
        [],
        help="""
        An ordered list of executable scripts that should be executed after build.

        Is run as a non-root user, and must be executable. Used for doing things
        that are currently not supported by other means!

        The scripts should be as deterministic as possible - running it twice
        should not produce different results!
        """
    )

    name = Unicode(
        help="""
        Name of the BuildPack!
        """
    )

    components = Tuple(())

    def compose_with(self, other):
        """
        Compose this BuildPack with another, returning a new one

        Ordering does matter - the properties of the current BuildPack take
        precedence (wherever that matters) over the properties of other
        BuildPack. If there are any conflicts, this method is responsible
        for resolving them.
        """
        result = BuildPack(parent=self)
        labels = {}
        labels.update(self.labels)
        labels.update(other.labels)
        result.labels = labels
        result.packages = self.packages.union(other.packages)
        result.base_packages = self.base_packages.union(other.base_packages)
        result.path = self.path + other.path
        # FIXME: Deduplicate Env
        result.env = self.env + other.env
        result.build_scripts = self.build_scripts + other.build_scripts
        result.assemble_scripts = self.assemble_scripts + other.assemble_scripts
        result.post_build_scripts = self.post_build_scripts + other.post_build_scripts

        build_script_files = {}
        build_script_files.update(self.build_script_files)
        build_script_files.update(other.build_script_files)
        result.build_script_files = build_script_files

        result.name = "{}-{}".format(self.name, other.name)

        result.components = (self, ) + self.components + (other, ) + other.components
        return result

    def detect(self):
        return all([p.detect() for p in self.components])

    def render(self):
        """
        Render BuildPack into Dockerfile
        """
        t = jinja2.Template(TEMPLATE)

        build_script_directives = []
        last_user = 'root'
        for user, script in self.build_scripts:
            if last_user != user:
                build_script_directives.append("USER {}".format(user))
                last_user = user
            build_script_directives.append("RUN {}".format(
                textwrap.dedent(script.strip('\n'))
            ))

        assemble_script_directives = []
        last_user = 'root'
        for user, script in self.assemble_scripts:
            if last_user != user:
                assemble_script_directives.append("USER {}".format(user))
                last_user = user
            assemble_script_directives.append("RUN {}".format(
                textwrap.dedent(script.strip('\n'))
            ))

        return t.render(
            packages=sorted(self.packages),
            path=self.path,
            env=self.env,
            labels=self.labels,
            build_script_directives=build_script_directives,
            assemble_script_directives=assemble_script_directives,
            build_script_files=self.build_script_files,
            base_packages=sorted(self.base_packages),
            post_build_scripts=self.post_build_scripts,
        )

    def build(self, image_spec):
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

        for src in sorted(self.build_script_files):
            src_parts = src.split('/')
            src_path = os.path.join(os.path.dirname(__file__), 'files', *src_parts)
            tar.add(src_path, src, filter=_filter_tar)

        tar.add('.', 'src/', filter=_filter_tar)

        tar.close()
        tarf.seek(0)

        client = docker.APIClient(version='auto', **docker.utils.kwargs_from_env())
        for line in client.build(
                fileobj=tarf,
                tag=image_spec,
                custom_context=True,
                decode=True
        ):
            yield line


class BaseImage(BuildPack):
    name = "repo2docker"
    version = "0.1"

    env = [
        ("APP_BASE", "/srv")
    ]

    def detect(self):
        return True

    @default('assemble_scripts')
    def setup_assembly(self):
        assemble_scripts = []
        try:
            with open('apt.txt') as f:
                extra_apt_packages = [l.strip() for l in f]
            # Validate that this is, indeed, just a list of packages
            # We're doing shell injection around here, gotta be careful.
            # FIXME: Add support for specifying version numbers
            for p in extra_apt_packages:
                if not re.match(r"^[a-z0-9.+-]+", p):
                    raise ValueError("Found invalid package name {} in apt.txt".format(p))

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

    @default('post_build_scripts')
    def setup_post_build_scripts(self):
        if os.path.exists('postBuild'):
            if stat.S_IXUSR & os.stat('postBuild')[stat.ST_MODE]:
                return ['postBuild']
        return []

class PythonBuildPack(BuildPack):
    name = "python3.5"
    version = "0.1"

    packages = {
        'python3',
        'python3-venv',
        'python3-dev',
    }

    env = [
        ("VENV_PATH", "${APP_BASE}/venv"),
        # Prefix to use for installing kernels and finding jupyter binary
        ("NB_PYTHON_PREFIX", "${VENV_PATH}"),
    ]

    path = [
        "${VENV_PATH}/bin"
    ]

    build_scripts = [
        (
            "root",
            r"""
            mkdir -p ${VENV_PATH} && \
            chown -R ${NB_USER}:${NB_USER} ${VENV_PATH}
            """
        ),
        (
            "${NB_USER}",
            r"""
            python3 -m venv ${VENV_PATH}
            """
        ),
        (
            "${NB_USER}",
            r"""
            pip install --no-cache-dir \
                notebook==5.0.0 \
                jupyterhub==0.7.2 \
                ipywidgets==6.0.0 \
                jupyterlab==0.24.1 && \
            jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
            jupyter serverextension enable --py jupyterlab --sys-prefix
            """
        )
    ]

    @default('assemble_scripts')
    def setup_assembly(self):
        # If we have a runtime.txt & that's set to python-2.7,
        # we will *not* install requirements.txt but will find &
        # install a requirements3.txt file if it exists.
        # This way, when using python2 venv, requirements.txt will
        # be installed in the python2 venv, and requirements3.txt
        # will be installed in python3 venv. This is less of a
        # surprise than requiring python2 to be requirements2.txt tho.
        try:
            with open('runtime.txt') as f:
                runtime = f.read().strip()
        except FileNotFoundError:
            runtime = 'python-3.5'
        if runtime == 'python-2.7':
            requirements_file = 'requirements3.txt'
        else:
            requirements_file = 'requirements.txt'
        if os.path.exists(requirements_file):
            return [(
                '${NB_USER}',
                'pip3 install --no-cache-dir -r {}'.format(requirements_file)
            )]
        return []

    def detect(self):
        return os.path.exists('requirements.txt') and super().detect()

class CondaBuildPack(BuildPack):
    name = "conda"
    version = "0.1"
    env = [
        ('CONDA_DIR', '${APP_BASE}/conda'),
        ('NB_PYTHON_PREFIX', '${CONDA_DIR}')
    ]

    path = ['${CONDA_DIR}/bin']

    build_script_files = {
        'conda/install-miniconda.bash': '/tmp/install-miniconda.bash',
        'conda/environment.yml': '/tmp/environment.yml'
    }

    build_scripts = [
        (
            "root",
            r"""
            bash /tmp/install-miniconda.bash && \
            rm /tmp/install-miniconda.bash /tmp/environment.yml
            """
        )
    ]

    @default('assemble_scripts')
    def setup_assembly(self):
        assembly_scripts = []
        if os.path.exists('environment.yml'):
            assembly_scripts.append((
                '${NB_USER}',
                r"""
                conda env update -n root -f environment.yml && \
                conda clean -tipsy
                """
            ))
        if os.path.exists('requirements.txt'):
            assembly_scripts.append((
                '${NB_USER}',
                'pip install --no-cache-dir -r requirements.txt'
            ))
        return assembly_scripts

    def detect(self):
        return os.path.exists('environment.yml') and super().detect()


class Python2BuildPack(BuildPack):
    name = "python2.7"
    version = "0.1"

    packages = {
        'python',
        'python-dev',
        'virtualenv'
    }

    env = [
        ('VENV2_PATH', '${APP_BASE}/venv2')
    ]

    path = [
        "${VENV2_PATH}/bin"
    ]

    build_scripts = [
        (
            "root",
            r"""
            mkdir -p ${VENV2_PATH} && \
            chown -R ${NB_USER}:${NB_USER} ${VENV2_PATH}
            """
        ),
        (
            "${NB_USER}",
            r"""
            virtualenv -p python2 ${VENV2_PATH}
            """
        ),
        (
            "${NB_USER}",
            r"""
            pip2 install --no-cache-dir \
                 ipykernel==4.6.1 && \
            python2 -m ipykernel install --prefix=${NB_PYTHON_PREFIX}
            """
        )
    ]

    @default('assemble_scripts')
    def setup_assembly(self):
        return [
            (
                '${NB_USER}',
                'pip2 install --no-cache-dir -r requirements.txt'
            )
        ]

    def detect(self):
        if os.path.exists('requirements.txt'):
            try:
                with open('runtime.txt') as f:
                    runtime = f.read().strip()
                if runtime == 'python-2.7':
                    return True
            except FileNotFoundError:
                return False
        return False

class JuliaBuildPack(BuildPack):
    name = "julia"
    version = "0.1"
    env = [
        ('JULIA_PATH', '${APP_BASE}/julia'),
        ('JULIA_HOME', '${JULIA_PATH}/bin'),
        ('JULIA_PKGDIR', '${JULIA_PATH}/pkg'),
        ('JULIA_VERSION', '0.6.0'),
        ('JUPYTER', '${NB_PYTHON_PREFIX}/bin/jupyter')
    ]

    path = [
        '${JULIA_PATH}/bin'
    ]

    build_scripts = [
        (
            "root",
            r"""
            mkdir -p ${JULIA_PATH} && \
            curl -sSL "https://julialang-s3.julialang.org/bin/linux/x64/${JULIA_VERSION%[.-]*}/julia-${JULIA_VERSION}-linux-x86_64.tar.gz" | tar -xz -C ${JULIA_PATH} --strip-components 1
            """
        ),
        (
            "root",
            r"""
            mkdir -p ${JULIA_PKGDIR} && \
            chown ${NB_USER}:${NB_USER} ${JULIA_PKGDIR}
            """
        ),
        (
            "${NB_USER}",
            # HACK: Can't seem to tell IJulia to install in sys-prefix
            # FIXME: Find way to get it to install under /srv and not $HOME?
            r"""
            julia -e 'Pkg.init(); Pkg.add("IJulia"); using IJulia;' && \
            mv ${HOME}/.local/share/jupyter/kernels/julia-0.6  ${NB_PYTHON_PREFIX}/share/jupyter/kernels/julia-0.6
            """
        )
    ]

    @default('assemble_scripts')
    def setup_assembly(self):
        return [(
            "${NB_USER}",
            # Pre-compile all libraries if they've opted into it. `using {libraryname}` does the
            # right thing
            r"""
            cat REQUIRE >> ${JULIA_PKGDIR}/v0.6/REQUIRE && \
            julia -e ' \
               Pkg.resolve(); \
               for pkg in keys(Pkg.Reqs.parse("REQUIRE")) \
                eval(:(using $(Symbol(pkg)))) \
               end \
            '
            """
        )]

    def detect(self):
        return os.path.exists('REQUIRE') and super()


class DockerBuildPack(BuildPack):
    name = "Dockerfile"

    def detect(self):
        return os.path.exists('Dockerfile')

    def render(self):
        with open('Dockerfile') as f:
            return f.read()

    def build(self, image_spec):
        client = docker.APIClient(version='auto', **docker.utils.kwargs_from_env())
        for line in client.build(
                path=os.getcwd(),
                tag=image_spec,
                decode=True
        ):
            yield line

class LegacyBinderDockerBuildPack(DockerBuildPack):

    name = 'Legacy Binder Dockerfile'

    dockerfile_appendix = Unicode(dedent(r"""
    USER root
    COPY . /home/main/notebooks
    RUN chown -R main:main /home/main/notebooks
    USER main
    WORKDIR /home/main/notebooks
    ENV PATH /home/main/anaconda2/envs/python3/bin:$PATH
    RUN conda install -n python3 notebook==5.0.0 ipykernel==4.6.0 && \
        pip install jupyterhub==0.7.2 && \
        conda remove -n python3 nb_conda_kernels && \
        conda install -n root ipykernel==4.6.0 && \
        /home/main/anaconda2/envs/python3/bin/ipython kernel install --sys-prefix && \
        /home/main/anaconda2/bin/ipython kernel install --prefix=/home/main/anaconda2/envs/python3 && \
        /home/main/anaconda2/bin/ipython kernel install --sys-prefix
    ENV JUPYTER_PATH /home/main/anaconda2/share/jupyter:$JUPYTER_PATH
    CMD jupyter notebook --ip 0.0.0.0
    """), config=True)

    def render(self):
        with open('Dockerfile') as f:
            return f.read() + self.dockerfile_appendix

    def detect(self):
        try:
            with open('Dockerfile', 'r') as f:
                for line in f:
                    if line.startswith('FROM'):
                        if 'andrewosh/binder-base' in line.split('#')[0].lower():
                            return True
                        else:
                            return False
        except FileNotFoundError:
            pass

        return False
