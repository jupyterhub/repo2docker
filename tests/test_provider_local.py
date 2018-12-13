import os
from tempfile import TemporaryDirectory, NamedTemporaryFile

from repo2docker.contentproviders import Local


def test_detect_local_dir():
    with TemporaryDirectory() as d:
        local = Local()
        spec = local.detect(d)

        # should accept a local directory
        assert spec is not None, spec
        assert 'path' in spec, spec
        assert spec['path'] == d


def test_not_detect_local_file():
    with NamedTemporaryFile() as f:
        local = Local()
        spec = local.detect(f.name)

        # should NOT accept a local file
        assert spec is None, spec


def test_content_available():
    # create a directory with files, check they are available in the output
    # directory
    with TemporaryDirectory() as d:
        with open(os.path.join(d, 'test'), 'w') as f:
            f.write("Hello")

        spec = {'path': d}
        for _ in Local().fetch(spec, d):
            pass
        assert os.path.exists(os.path.join(d, 'test'))
