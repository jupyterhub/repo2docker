import os
import sys
import subprocess
from textwrap import dedent

import docker
from docker.utils import kwargs_from_env

from traitlets import Unicode, Dict, Bool
from traitlets.config import LoggingConfigurable

import logging
from pythonjsonlogger import jsonlogger

from .utils import execute_cmd

here = os.path.abspath(os.path.dirname(__file__))

class BuildPack(LoggingConfigurable):
    name = Unicode()
    capture = Bool(False, help="Capture output for logging")

    def detect(self, workdir):
        """
        Return True if app in workdir can be built with this buildpack
        """
        pass

    def build(self, workdir, ref, output_image_spec):
        """
        Run a command that will take workdir and produce an image ready to be pushed
        """
        pass


class DockerBuildPack(BuildPack):
    name = Unicode('Dockerfile')
    def detect(self, workdir):
        return os.path.exists(os.path.join(workdir, 'Dockerfile'))

    def build(self, workdir, ref, output_image_spec):
        client = docker.APIClient(version='auto', **kwargs_from_env())
        for progress in client.build(
                path=workdir,
                tag=output_image_spec,
                decode=True
        ):
            if 'stream' in progress:
                if self.capture:
                    self.log.info(progress['stream'], extra=dict(phase='building'))
                else:
                    sys.stdout.write(progress['stream'])


class LegacyBinderDockerBuildPack(DockerBuildPack):
    
    name = Unicode('Legacy Binder Dockerfile')
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
        /home/main/anaconda2/bin/ipython kernel install --prefix=/home/main/anaconda2/envs/python3
    ENV JUPYTER_PATH /home/main/anaconda2/share/jupyter:$JUPYTER_PATH
    CMD jupyter notebook --ip 0.0.0.0
    """), config=True)
    
    def detect(self, workdir):
        dockerfile = os.path.join(workdir, 'Dockerfile')
        if not os.path.exists(dockerfile):
            return False
        with open(dockerfile, 'r') as f:
            for line in f:
                if line.startswith('FROM'):
                    if 'andrewosh/binder-base' in line.split('#')[0].lower():
                        self.amend_dockerfile(dockerfile)
                        return True
                    else:
                        return False
        # No FROM?!
        return False

    def amend_dockerfile(self, dockerfile):
        print(self.dockerfile_appendix)
        with open(dockerfile, 'a') as f:
            f.write(self.dockerfile_appendix)


class S2IBuildPack(BuildPack):
    # Simple subclasses of S2IBuildPack must set build_image,
    # either via config or during `detect()`
    build_image = Unicode('')
    
    def s2i_build(self, workdir, ref, output_image_spec, build_image):
        # Note: Ideally we'd just copy from workdir here, rather than clone and check out again
        # However, setting just --copy and not specifying a ref seems to check out master for
        # some reason. Investigate deeper FIXME
        cmd = [
            's2i',
            'build',
            '--exclude', '""',
            '--ref', ref,
            '.',
            build_image,
            output_image_spec,
        ]
        env = os.environ.copy()
        # add bundled s2i to *end* of PATH,
        # in case user doesn't have s2i
        env['PATH'] = os.pathsep.join([env.get('PATH') or os.defpath, here])
        try:
            for line in execute_cmd(cmd, cwd=workdir, env=env, capture=self.capture):
                self.log.info(line, extra=dict(phase='building', builder=self.name))
        except subprocess.CalledProcessError:
            self.log.error('Failed to build image!', extra=dict(phase='failed'))
            sys.exit(1)
    
    def build(self, workdir, ref, output_image_spec):
        return self.s2i_build(workdir, ref, output_image_spec, self.build_image)


class CondaBuildPack(S2IBuildPack):
    """Build Pack for installing from a conda environment.yml using S2I"""

    name = Unicode('conda')
    build_image = Unicode('jupyterhub/singleuser-builder-conda:v0.1.5', config=True)

    def detect(self, workdir):
        return os.path.exists(os.path.join(workdir, 'environment.yml'))


class PythonBuildPack(S2IBuildPack):
    """Build Pack for installing from a pip requirements.txt using S2I"""
    name = Unicode('python-pip')
    runtime_builder_map = Dict({
        'python-2.7': 'jupyterhub/singleuser-builder-venv-2.7:v0.1.5',
        'python-3.5': 'jupyterhub/singleuser-builder-venv-3.5:v0.1.5',
    })

    runtime = Unicode(
        'python-3.5',
        config=True
    )

    def detect(self, workdir):
        if os.path.exists(os.path.join(workdir, 'requirements.txt')):
            try:
                with open(os.path.join(workdir, 'runtime.txt')) as f:
                    self.runtime = f.read().strip()
            except FileNotFoundError:
                pass
            self.build_image = self.runtime_builder_map[self.runtime]
            return True
