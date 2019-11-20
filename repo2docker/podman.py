# Use Podman instead of Docker
import json
import re
from subprocess import CalledProcessError
from tempfile import TemporaryDirectory
import tarfile
from .utils import execute_cmd

# https://docker-py.readthedocs.io/en/stable/containers.html


def exec_podman(args, capture=False, **kwargs):
    cmd = ["podman"] + args
    print("Executing: {} {}".format(" ".join(cmd), kwargs))
    try:
        p = execute_cmd(cmd, capture=capture, **kwargs)
    except CalledProcessError:
        print(kwargs["stdout"])
        print(kwargs["stderr"])
        raise
    if capture:
        yield from p
    for line in p:
        print(line)
        # pass


class Container:
    def __init__(self, cid):
        self.id = cid
        self.reload()

    def reload(self):
        lines = list(
            exec_podman(
                ["inspect", "--type", "container", "--format", "json", self.id],
                capture=True,
            )
        )
        d = json.loads("".join(lines))
        assert len(d) == 1
        self.attrs = d[0]
        assert self.attrs["Id"] == self.id

    def logs(self, stream=False):
        if stream:

            def iter_logs(cid):
                exited = False
                try:
                    for line in exec_podman(
                        ["attach", "--no-stdin", cid], capture=True
                    ):
                        if exited or line.startswith(
                            "Error: you can only attach to running containers"
                        ):
                            # Swallow all output to ensure process exited
                            print(line)
                            exited = True
                            continue
                        else:
                            yield line.encode("utf-8")
                except CalledProcessError as e:
                    print(e, line.encode("utf-8"))
                    if e.returncode == 125 and exited:
                        for line in exec_podman(["logs", self.id], capture=True):
                            yield line.encode("utf-8")
                    else:
                        raise

            return iter_logs(self.id)
        return "".join(exec_podman(["logs", self.id], capture=True))

    def kill(self, signal="KILL"):
        for line in exec_podman(["kill", "--signal", signal, self.id]):
            print(line)

    def remove(self, **kwargs):
        print("podman remove kwargs: {}".format(kwargs))
        cmdargs = ["rm"]
        if kwargs.pop("v", False):
            cmdargs.append("--volumes")
        if kwargs.pop("link", False):
            cmdargs.append("--link")
        if kwargs.pop("force", False):
            cmdargs.append("--force")
        for line in exec_podman(cmdargs + [self.id]):
            print(line)

    @staticmethod
    def run(image_spec, **kwargs):
        print("podman run kwargs: {} {}".format(image_spec, kwargs))
        cmdargs = ["run"]

        try:
            if kwargs.pop("publish_all_ports"):
                cmdargs.append("--publish-all")
        except KeyError:
            pass

        ports = kwargs.pop("ports", {})
        for k, v in ports.items():
            if k.endswith("/tcp"):
                k = k[:-4]
            cmdargs.extend(["--publish", "{}:{}".format(k, v)])

        detach = kwargs.pop("detach", False)
        if detach:
            cmdargs.append("--detach")

        volumes = kwargs.pop("volumes", {})
        for k, v in volumes.items():
            raise NotImplementedError("podman run volumes not implemented")

        env = kwargs.pop("env", [])
        for e in env:
            cmdargs.extend(["--env", e])

        if kwargs.pop("remove", False):
            cmdargs.append("--rm")

        command = kwargs.pop("command", [])

        cmdline = cmdargs + [image_spec] + command
        lines = list(exec_podman(cmdline, capture=True))
        if detach:
            # If image was pulled the progress logs will also be present
            # assert len(lines) == 1, lines
            return Container(lines[-1].strip())
        else:
            return lines

    def stop(self, timeout=10):
        for line in exec_podman(["stop", "--timeout", str(timeout), self.id]):
            print(line)

    @property
    def status(self):
        return self.attrs["State"]["Status"]


class PodmanClient:

    containers = Container

    def __init__(self):
        exec_podman(["info"])
        self.default_transport = "docker://docker.io/"

    def build(self, **kwargs):
        """
        Implement docker.Client.build in podman
        https://docker-py.readthedocs.io/en/stable/api.html
        """
        print("podman build kwargs: %s", kwargs)
        cmdargs = ["build"]

        bargs = kwargs.pop("buildargs", {})
        for k, v in bargs.items():
            cmdargs.extend(["--build-arg", "{}={}".format(k, v)])

        # podman --cache-from is a NOOP
        cachef = kwargs.pop("cache_from", [])
        if cachef:
            cmdargs.extend(["--cache-from", ",".join(cachef)])

        try:
            climits = kwargs.pop("container_limits")
            try:
                cmdargs.extend(["--cpuset-cpus", climits.pop("cpusetcpus")])
            except KeyError:
                pass
            try:
                cmdargs.extend(["--cpu-shares", climits.pop("cpushares")])
            except KeyError:
                pass
            try:
                cmdargs.extend(["--memory", climits.pop("memory")])
            except KeyError:
                pass
            try:
                cmdargs.extend(["--memory-swap", climits.pop("memswap")])
            except KeyError:
                pass
        except KeyError:
            pass

        try:
            if kwargs.pop("forcerm"):
                cmdargs.append("--force-rm")
        except KeyError:
            pass

        try:
            if kwargs.pop("rm"):
                cmdargs.append("--rm")
        except KeyError:
            pass

        try:
            cmdargs.extend(["--tag", kwargs.pop("tag")])
        except KeyError:
            pass

        try:
            cmdargs.extend(["--file", kwargs.pop("dockerfile")])
        except KeyError:
            pass

        for ignore in ("custom_context", "decode"):
            try:
                kwargs.pop(ignore)
            except KeyError:
                pass

        # Avoid try-except so that if build errors occur they don't result in a
        # confusing message about an exception whilst handling an exception
        if "fileobj" in kwargs:
            fileobj = kwargs.pop("fileobj")

            with TemporaryDirectory() as builddir:
                tarf = tarfile.open(fileobj=fileobj)
                tarf.extractall(builddir)
                print(builddir)
                for line in execute_cmd(["ls", "-lRa", builddir]):
                    print(line)
                for line in exec_podman(cmdargs + [builddir], capture=True):
                    yield {"stream": line}
        else:
            builddir = kwargs.pop("path")
            for line in exec_podman(cmdargs + [builddir], capture=True):
                yield {"stream": line}

    def images(self):
        lines = "".join(
            exec_podman(["image", "list", "--format", "json"], capture=True)
        )
        if lines.strip():
            return json.loads(lines)
        return []

    def push(self, output_image_spec, stream=True):
        if re.match("\w+://", output_image_spec):
            destination = output_image_spec
        else:
            destination = self.default_transport + output_image_spec
        args = ["push", output_image_spec, destination]

        def parse(line):
            # Copying blob sha256:c3251e9470f15a56da9566af818bb8a573620416da2e8d5eb22d6cb253b4851f
            # line = line.encode("utf-8")
            m = re.match("(?P<error>Error.+)", line, re.IGNORECASE)
            if m:
                m = m.groupdict()
            else:
                m = re.match("(?P<before>.+) (?P<id>sha256:\w+)( (?P<after>.+))?", line)
                if m:
                    m = m.groupdict()
                    m["status"] = m["before"]
                    if m["after"]:
                        m["status"] += ", " + m["after"]
            if m:
                return json.dumps(m).encode("utf-8")
            print("No logmatch:", line)
            return line.encode("utf-8")

        if stream:

            def iter_out():
                for line in exec_podman(args, capture=True):
                    # yield {"stream": line}
                    yield parse(line)

            return iter_out()
        return "".join(exec_podman(args, capture=True))
