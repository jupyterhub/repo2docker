"""Generates Dockerfiles from the legacy Binder Dockerfiles
based on `andrewosh/binder-base`.

The Dockerfile is amended to add the contents of the repository
to the image and install a supported version of the notebook
and IPython kernel.

"""
import os
import shutil
from textwrap import dedent
from ..docker import DockerBuildPack

class LegacyBinderDockerBuildPack(DockerBuildPack):
    """Legacy build pack for compatibility to first version of Binder."""
    dockerfile = '._binder.Dockerfile'

    legacy_prependix = dedent(r"""
    COPY python3.frozen.yml /tmp/python3.frozen.yml
    COPY root.frozen.yml /tmp/root.frozen.yml
    # update conda in two steps because the base image
    # has very old conda that can't upgrade past 4.3
    RUN conda install -yq conda>=4.3 && \
        conda install -yq conda==4.4.11 && \
        conda env update -n python3 -f /tmp/python3.frozen.yml && \
        conda remove -yq -n python3 nb_conda_kernels _nb_ext_conf && \
        conda env update -n root -f /tmp/root.frozen.yml && \
        /home/main/anaconda2/envs/python3/bin/ipython kernel install --sys-prefix && \
        /home/main/anaconda2/bin/ipython kernel install --prefix=/home/main/anaconda2/envs/python3 && \
        /home/main/anaconda2/bin/ipython kernel install --sys-prefix
    """)

    legacy_appendix = dedent(r"""
    USER root
    COPY . /home/main/notebooks
    RUN chown -R main:main /home/main/notebooks && \
        rm /home/main/notebooks/root.frozen.yml && \
        rm /home/main/notebooks/python3.frozen.yml
    USER main
    WORKDIR /home/main/notebooks
    ENV PATH /home/main/anaconda2/envs/python3/bin:$PATH
    ENV JUPYTER_PATH /home/main/anaconda2/share/jupyter:$JUPYTER_PATH
    CMD jupyter notebook --ip 0.0.0.0
    """)

    def render(self):
        """Render buildpack into a Dockerfile.

        Render legacy image source (andrewosh/binder-base at a specific commit)
        and then prependix. Render appendix (post-build commands) at the end of
        the Dockerfile.

        """
        segments = [
            'FROM andrewosh/binder-base@sha256:eabde24f4c55174832ed8795faa40cea62fc9e2a4a9f1ee1444f8a2e4f9710ee',
            self.legacy_prependix,
        ]
        with open('Dockerfile') as f:
            for line in f:
                if line.strip().startswith('FROM'):
                    break
            segments.append(f.read())
        segments.append(self.legacy_appendix)
        return '\n'.join(segments)

    def get_build_script_files(self):
        """
        Dict of files to be copied to the container image for use in building.

        This is copied before the `build_scripts` & `assemble_scripts` are
        run, so can be executed from either of them.

        It's a dictionary where the key is the source file path in the host
        system, and the value is the destination file path inside the
        container image.

        This currently adds a frozen set of Python requirements to the dict
        of files.

        """
        return {
            'legacy/root.frozen.yml': '/tmp/root.frozen.yml',
            'legacy/python3.frozen.yml': '/tmp/python3.frozen.yml',
        }

    def build(self, client, image_spec, memory_limit, build_args, cache_from, extra_build_kwargs):
        """Build a legacy Docker image."""
        with open(self.dockerfile, 'w') as f:
            f.write(self.render())
        for env in ('root', 'python3'):
            env_file = env + '.frozen.yml'
            src_path = os.path.join(
                os.path.dirname(__file__),
                env_file,
            )
            shutil.copy(src_path, env_file)
        return super().build(client, image_spec, memory_limit, build_args, cache_from, extra_build_kwargs)

    def detect(self):
        """Check if current repo should be built with the Legacy BuildPack.
        """
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
