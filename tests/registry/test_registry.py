from pathlib import Path
import subprocess
import pytest
from repo2docker.__main__ import make_r2d
from repo2docker.utils import get_free_port
import time
import requests
import secrets

HERE = Path(__file__).parent

@pytest.fixture
def registry():
    port = get_free_port()
    # Explicitly pull the image first so it runs on time
    registry_image =  "registry:3.0.0-rc.3"
    subprocess.check_call(["docker", "pull", registry_image])
    cmd = [
        "docker", "run", "-p", f"{port}:5000", registry_image
    ]
    proc = subprocess.Popen(cmd)
    health_url = f'http://localhost:{port}/v2'
    # Wait for the registry to actually come up
    for i in range(10):
        try:
            resp = requests.get(health_url)
            if resp.status_code in (401, 200):
                break
        except requests.ConnectionError:
            # The service is not up yet
            pass
        time.sleep(i)
    else:
        raise TimeoutError("Test registry did not come up in time")

    try:
        yield f"localhost:{port}"
    finally:
        proc.terminate()
        proc.wait()


def test_registry(registry):
    image_name = f"{registry}/{secrets.token_hex(8)}:latest"
    r2d = make_r2d([
        "--image", image_name,
        "--push", "--no-run", str(HERE)
    ])

    r2d.start()

    proc = subprocess.run(["docker", "manifest", "inspect", "--insecure", image_name])
    assert proc.returncode == 0
