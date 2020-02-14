"""Test if assemble scripts from outside of r2d repo are accepted."""
import time
from repo2docker.app import Repo2Docker
from repo2docker.buildpacks import PythonBuildPack


def test_Repo2Docker_external_build_scripts(tmpdir):
    tempfile = tmpdir.join("absolute-script")
    tempfile.write("Hello World of Absolute Paths!")

    class MockBuildPack(PythonBuildPack):
        def detect(self):
            return True

        def get_build_script_files(self):
            files = {str(tempfile): "/tmp/my_extra_script"}
            files.update(super().get_build_script_files())
            return files

    app = Repo2Docker(repo=str(tmpdir))
    app.buildpacks = [MockBuildPack]
    app.initialize()
    app.build()
    container = app.start_container()

    # give the container a chance to start
    tic = 180
    while container.status != "running" or tic < 0:
        time.sleep(1)
        tic -= 1

    assert container.status == "running"

    try:
        status, output = container._c.exec_run(["sh", "-c", "cat /tmp/my_extra_script"])
        assert status == 0
        assert output.decode("utf-8") == "Hello World of Absolute Paths!"
    finally:
        container.stop(timeout=1)
        container.reload()
        assert container.status == "exited", container.status
        container.remove()
