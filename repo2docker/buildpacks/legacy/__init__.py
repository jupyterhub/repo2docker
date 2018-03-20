"""
Generates a variety of Dockerfiles based on an input matrix
"""
import os
import shutil
from textwrap import dedent
from ..docker import DockerBuildPack

class LegacyBinderDockerBuildPack(DockerBuildPack):

    dockerfile = '._binder.Dockerfile'

    legacy_appendix = dedent(r"""
    USER root
    COPY . /home/main/notebooks
    RUN chown -R main:main /home/main/notebooks
    USER main
    WORKDIR /home/main/notebooks
    # update conda in two steps because the base image
    # has very old conda that can't upgrade past 4.3
    RUN conda install -yq conda>=4.3 && \
        conda install -yq conda==4.4.11 && \
        conda env update -n python3 -f python3.frozen.yml && \
        conda remove -yq -n python3 nb_conda_kernels && \
        conda env update -n root -f root.frozen.yml && \
        /home/main/anaconda2/envs/python3/bin/ipython kernel install --sys-prefix && \
        /home/main/anaconda2/bin/ipython kernel install --prefix=/home/main/anaconda2/envs/python3 && \
        /home/main/anaconda2/bin/ipython kernel install --sys-prefix
    RUN rm python3.frozen.yml root.frozen.yml
    ENV PATH /home/main/anaconda2/envs/python3/bin:$PATH
    ENV JUPYTER_PATH /home/main/anaconda2/share/jupyter:$JUPYTER_PATH
    CMD jupyter notebook --ip 0.0.0.0
    """)

    def render(self):
        with open('Dockerfile') as f:
            return '\n'.join([f.read(), self.legacy_appendix, self.appendix, ''])

    def get_build_script_files(self):
       return {
            'legacy/root.frozen.yml': '/tmp/root.frozen.yml',
            'legacy/python3.frozen.yml': '/tmp/python3.frozen.yml',
        }
            
    def build(self, image_spec, memory_limit, build_args):
        with open(self.dockerfile, 'w') as f:
            f.write(self.render())
        for env in ('root', 'python3'):
            env_file = env + '.frozen.yml'
            src_path = os.path.join(
                os.path.dirname(__file__),
                env_file,
            )
            shutil.copy(src_path, env_file)
        return super().build(image_spec, memory_limit, build_args)

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
