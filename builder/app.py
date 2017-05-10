import json
import os


from traitlets.config import Application, LoggingConfigurable, Unicode, Dict, List
from traitlets import Type
import docker

import subprocess


from .detectors import BuildPack, PythonBuildPack, DockerBuildPack

class Builder(Application):
    config_file = Unicode(
        'builder_config.py',
        config=True
    )

    build_name = Unicode(
        None,
        allow_none=True,
        config=True
    )

    source_url = Unicode(
        None,
        allow_none=True,
        config=True
    )

    output_image_spec = Unicode(
        None,
        allow_none=True,
        config=True
    )

    git_workdir = Unicode(
        "/tmp/git",
        config=True
    )

    buildpacks = List(
        None,
        [DockerBuildPack, PythonBuildPack],
        config=True
    )

    aliases = Dict({
        'source': 'Builder.source_url',
        'output': 'Builder.output_image_spec',
        'f': 'Builder.config_file',
        'n': 'Builder.build_name'
    })


    def fetch(self, url, ref, output_path):
        subprocess.check_call([
            "git", "clone", "--depth", "1",
            url, output_path
        ])


    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)

        self.load_config_file(self.config_file)

    def run(self):
        # HACK: Try to just pull this and see if that works.
        # if it does, then just bail.
        # WHAT WE REALLY WANT IS TO NOT DO ANY WORK IF THE IMAGE EXISTS
        client = docker.APIClient(base_url='unix://var/run/docker.sock', version='auto')

        try:
            repo, tag = self.output_image_spec.split(':')
            for line in client.pull(
                    repository=repo,
                    tag=tag,
                    stream=True,
            ):
                print(json.loads(line.decode('utf-8')))
            return
        except docker.errors.ImageNotFound:
            pass

        output_path = os.path.join(self.git_workdir, self.build_name)
        self.fetch(
            self.source_url,
            'master',
            output_path
        )
        for bp_class in self.buildpacks:
            bp = bp_class()
            if bp.detect(output_path):
                bp.build(output_path, self.output_image_spec)
                break
        else:
            raise Exception("No compatible builders found")


        for line in client.push(self.output_image_spec, stream=True):
            progress = json.loads(line.decode('utf-8'))
            print(progress)

if __name__ == '__main__':
    f = Builder()
    f.initialize()
    f.run()
