"""
Generates a variety of Dockerfiles based on an input matrix
"""
from textwrap import dedent
from .docker import DockerBuildPack

class LegacyBinderDockerBuildPack(DockerBuildPack):

    dockerfile = '._binder.Dockerfile'

    dockerfile_appendix = dedent(r"""
    USER root
    COPY . /home/main/notebooks
    RUN chown -R main:main /home/main/notebooks
    USER main
    WORKDIR /home/main/notebooks
    ENV PATH /home/main/anaconda2/envs/python3/bin:$PATH
    RUN conda install -yq -n python3 notebook==5.0.0 ipykernel==4.6.0 && \
        conda remove -yq -n python3 nb_conda_kernels && \
        conda install -yq -n root ipykernel==4.6.0 && \
        /home/main/anaconda2/envs/python3/bin/ipython kernel install --sys-prefix && \
        /home/main/anaconda2/bin/ipython kernel install --prefix=/home/main/anaconda2/envs/python3 && \
        /home/main/anaconda2/bin/ipython kernel install --sys-prefix
    ENV JUPYTER_PATH /home/main/anaconda2/share/jupyter:$JUPYTER_PATH
    CMD jupyter notebook --ip 0.0.0.0
    """)

    def render(self):
        with open('Dockerfile') as f:
            return f.read() + self.dockerfile_appendix

    def build(self, image_spec, memory_limit, build_args):
        with open(self.dockerfile, 'w') as f:
            f.write(self.render())
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
