import json
import os
import pytest

from contextlib import contextmanager
from io import BytesIO
from tempfile import TemporaryDirectory, NamedTemporaryFile
from unittest.mock import patch
from urllib.request import urlopen, Request
from zipfile import ZipFile

from repo2docker.contentproviders import Zenodo


def test_content_id():
    with patch.object(Zenodo, "urlopen") as fake_urlopen:
        fake_urlopen.return_value.url = "https://zenodo.org/record/3232985"
        zen = Zenodo()

        zen.detect("10.5281/zenodo.3232985")
        assert zen.content_id == "3232985"


test_zen = Zenodo()
test_hosts = [
    (
        [
            "https://zenodo.org/record/3232985",
            "10.5281/zenodo.3232985",
            "https://doi.org/10.5281/zenodo.3232985",
        ],
        {"host": test_zen.hosts[0], "record": "3232985"},
    ),
    (
        [
            "https://data.caltech.edu/records/1235",
            "10.22002/d1.1235",
            "https://doi.org/10.22002/d1.1235",
        ],
        {"host": test_zen.hosts[1], "record": "1235"},
    ),
]


@pytest.mark.parametrize("test_input,expected", test_hosts)
def test_detect_zenodo(test_input, expected):
    with patch.object(Zenodo, "urlopen") as fake_urlopen:
        fake_urlopen.return_value.url = test_input[0]
        # valid Zenodo DOIs trigger this content provider
        assert Zenodo().detect(test_input[0]) == expected
        assert Zenodo().detect(test_input[1]) == expected
        assert Zenodo().detect(test_input[2]) == expected
        # only two of the three calls above have to resolve a DOI
        assert fake_urlopen.call_count == 2

    with patch.object(Zenodo, "urlopen") as fake_urlopen:
        # Don't trigger the Zenodo content provider
        assert Zenodo().detect("/some/path/here") is None
        assert Zenodo().detect("https://example.com/path/here") is None
        # don't handle DOIs that aren't from Zenodo
        fake_urlopen.return_value.url = (
            "http://joss.theoj.org/papers/10.21105/joss.01277"
        )
        assert Zenodo().detect("https://doi.org/10.21105/joss.01277") is None


@contextmanager
def zenodo_archive(prefix="a_directory"):
    with NamedTemporaryFile(suffix=".zip") as zfile:
        with ZipFile(zfile.name, mode="w") as zip:
            zip.writestr("{}/some-file.txt".format(prefix), "some content")
            zip.writestr("{}/some-other-file.txt".format(prefix), "some more content")

        yield zfile.name


def test_fetch_software_from_github_archive():
    # we "fetch" a local ZIP file to simulate a Zenodo record created from a
    # GitHub repository via the Zenodo-GitHub integration
    with zenodo_archive() as zen_path:
        mock_response = BytesIO(
            json.dumps(
                {
                    "files": [
                        {
                            "filename": "some_dir/afake.zip",
                            "links": {"download": "file://{}".format(zen_path)},
                        }
                    ],
                    "metadata": {"upload_type": "software"},
                }
            ).encode("utf-8")
        )

        def mock_urlopen(self, req):
            if isinstance(req, Request):
                return mock_response
            else:
                return urlopen(req)

        with patch.object(Zenodo, "urlopen", new=mock_urlopen):
            zen = Zenodo()
            spec = {"host": test_zen.hosts[0], "record": "1234"}

            with TemporaryDirectory() as d:
                output = []
                for l in zen.fetch(spec, d):
                    output.append(l)

                unpacked_files = set(os.listdir(d))
                expected = set(["some-other-file.txt", "some-file.txt"])
                assert expected == unpacked_files


def test_fetch_software():
    # we "fetch" a local ZIP file to simulate a Zenodo software record with a
    # ZIP file in it
    with zenodo_archive() as zen_path:
        mock_response = BytesIO(
            json.dumps(
                {
                    "files": [
                        {
                            # this is the difference to the GitHub generated one,
                            # the ZIP file isn't in a directory
                            "filename": "afake.zip",
                            "links": {"download": "file://{}".format(zen_path)},
                        }
                    ],
                    "metadata": {"upload_type": "software"},
                }
            ).encode("utf-8")
        )

        def mock_urlopen(self, req):
            if isinstance(req, Request):
                return mock_response
            else:
                return urlopen(req)

        with patch.object(Zenodo, "urlopen", new=mock_urlopen):
            with TemporaryDirectory() as d:
                zen = Zenodo()
                spec = spec = {"host": test_zen.hosts[0], "record": "1234"}
                output = []
                for l in zen.fetch(spec, d):
                    output.append(l)

                unpacked_files = set(os.listdir(d))
                expected = set(["some-other-file.txt", "some-file.txt"])
                assert expected == unpacked_files


def test_fetch_data():
    # we "fetch" a local ZIP file to simulate a Zenodo data record
    with zenodo_archive() as a_zen_path:
        with zenodo_archive() as b_zen_path:
            mock_response = BytesIO(
                json.dumps(
                    {
                        "files": [
                            {
                                "filename": "afake.zip",
                                "links": {"download": "file://{}".format(a_zen_path)},
                            },
                            {
                                "filename": "bfake.zip",
                                "links": {"download": "file://{}".format(b_zen_path)},
                            },
                        ],
                        "metadata": {"upload_type": "data"},
                    }
                ).encode("utf-8")
            )

            def mock_urlopen(self, req):
                if isinstance(req, Request):
                    return mock_response
                else:
                    return urlopen(req)

            with patch.object(Zenodo, "urlopen", new=mock_urlopen):
                with TemporaryDirectory() as d:
                    zen = Zenodo()
                    spec = {"host": test_zen.hosts[0], "record": "1234"}
                    output = []
                    for l in zen.fetch(spec, d):
                        output.append(l)

                    unpacked_files = set(os.listdir(d))
                    # ZIP files shouldn't have been unpacked
                    expected = {"bfake.zip", "afake.zip"}
                    assert expected == unpacked_files
