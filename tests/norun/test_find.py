import secrets
from pathlib import Path

from repo2docker.__main__ import make_r2d

HERE = Path(__file__).parent


def test_find_image():
    image_name = f"{secrets.token_hex(8)}:latest"
    r2d = make_r2d(["--image", image_name, "--no-run", str(HERE)])

    r2d.start()

    assert r2d.find_image()


def test_dont_find_image():
    image_name = f"{secrets.token_hex(8)}:latest"
    r2d = make_r2d(["--image", image_name, "--no-run", str(HERE)])

    # Just don't actually start the build, so image won't be found
    assert not r2d.find_image()
