# Use Podman isntead of Docker
from tempfile import TemporaryDirectory
import tarfile
from .utils import execute_cmd

class PodmanClient:

    def __init__(self):
        list(execute_cmd(['podman', 'info']))

    def build(self, **kwargs):
        """
        Implement docker.Client.build in podman
        https://docker-py.readthedocs.io/en/stable/api.html
        """
        print('podman build kwargs: %s', kwargs)
        cmdargs = []

        bargs = kwargs.pop('buildargs', {})
        for k, v in bargs.items():
            cmdargs.extend(['--build-arg', '{}={}'.format(k, v)])

        # podman --cache-from is a NOOP
        cachef = kwargs.pop('cache_from', [])
        if cachef:
            cmdargs.extend(['--cache-from', ','.join(cachef)])

        try:
            climits = kwargs.pop('container_limits')
            try:
                cmdargs.extend(['--cpuset-cpus', climits.pop('cpusetcpus')])
            except KeyError:
                pass
            try:
                cmdargs.extend(['--cpu-shares', climits.pop('cpushares')])
            except KeyError:
                pass
            try:
                cmdargs.extend(['--memory', climits.pop('memory')])
            except KeyError:
                pass
            try:
                cmdargs.extend(['--memory-swap', climits.pop('memswap')])
            except KeyError:
                pass
        except KeyError:
            pass

        try:
            if kwargs.pop('forcerm'):
                cmdargs.append('--force-rm')
        except KeyError:
            pass

        try:
            if kwargs.pop('rm'):
                cmdargs.append('--rm')
        except KeyError:
            pass

        try:
            cmdargs.extend(['--tag', kwargs.pop('tag')])
        except KeyError:
            pass

        for ignore in (
            'custom_context',
            'decode',
        ):
            try:
                kwargs.pop(ignore)
            except KeyError:
                pass

        fileobj = kwargs.pop('fileobj')

        with TemporaryDirectory() as builddir:
            tarf = tarfile.open(fileobj=fileobj)
            tarf.extractall(builddir)
            print(builddir)
            for line in execute_cmd(['ls', '-lRa', builddir]):
                print(line)

            cmdline = ['podman', 'build'] + cmdargs + [builddir]
            print(cmdline)
            for line in execute_cmd(cmdline):
                yield line
