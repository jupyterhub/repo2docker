import json
import os


from traitlets.config import Application, LoggingConfigurable, Unicode, Dict, List
from traitlets import Type
import docker

import subprocess


from .detectors import BuildPack, PythonBuildPack

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
        [PythonBuildPack],
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

        client = docker.from_env(version='1.24')
        for line in client.images.push(self.output_image_spec, stream=True):
            progress = json.loads(line.decode('utf-8'))
            print(progress['status'])

if __name__ == '__main__':
    f = Builder()
    f.initialize()
    f.run()
