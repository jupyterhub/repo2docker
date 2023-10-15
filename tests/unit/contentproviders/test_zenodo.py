import json
import os
import re
from contextlib import contextmanager
from io import BytesIO
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest.mock import patch
from urllib.request import Request, urlopen
from zipfile import ZipFile

import pytest

from repo2docker.contentproviders import Zenodo

doi_responses = {
    "https://doi.org/10.5281/zenodo.3232985": ("https://zenodo.org/record/3232985"),
    "https://doi.org/10.22002/d1.1235": ("https://data.caltech.edu/records/1235"),
    "https://doi.org/10.21105/joss.01277": (
        "https://joss.theoj.org/papers/10.21105/joss.01277"
    ),
}


def doi_resolver(req, context):
    resp = doi_responses.get(req.url)
    # doi responses are redirects
    if resp is not None:
        context.status_code = 302
        context.headers["Location"] = resp
    return resp


def test_content_id(requests_mock):
    requests_mock.get(re.compile("https://"), json=doi_resolver)

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
        {"host": test_zen.hosts[1], "record": "3232985"},
    ),
    (
        [
            "https://data.caltech.edu/records/1235",
            "10.22002/d1.1235",
            "https://doi.org/10.22002/d1.1235",
        ],
        {"host": test_zen.hosts[2], "record": "1235"},
    ),
]


@pytest.mark.parametrize("test_input,expected", test_hosts)
def test_detect_zenodo(test_input, expected, requests_mock):
    requests_mock.get(re.compile("https://"), json=doi_resolver)
    # valid Zenodo DOIs trigger this content provider
    assert Zenodo().detect(test_input[0]) == expected
    assert Zenodo().detect(test_input[1]) == expected
    assert Zenodo().detect(test_input[2]) == expected
    # only two of the three calls above have to resolve a DOI (2 req per doi resolution)
    assert requests_mock.call_count == 4
    requests_mock.reset_mock()

    # Don't trigger the Zenodo content provider
    assert Zenodo().detect("/some/path/here") is None
    assert Zenodo().detect("https://example.com/path/here") is None

    # don't handle DOIs that aren't from Zenodo
    assert Zenodo().detect("https://doi.org/10.21105/joss.01277") is None


@contextmanager
def zenodo_archive(prefix="a_directory"):
    with NamedTemporaryFile(suffix=".zip") as zfile:
        with ZipFile(zfile.name, mode="w") as zip:
            zip.writestr(f"{prefix}/some-file.txt", "some content")
            zip.writestr(f"{prefix}/some-other-file.txt", "some more content")

        yield zfile.name


def test_fetch_software_from_github_archive(requests_mock):
    # we "fetch" a local ZIP file to simulate a Zenodo record created from a
    # GitHub repository via the Zenodo-GitHub integration
    with zenodo_archive() as zen_path:
        mock_record = {
            "files": [
                {
                    "filename": "some_dir/afake.zip",
                }
            ],
            "links": {
                "files": "https://zenodo.org/api/records/1234/files",
            },
            "metadata": {"upload_type": "other"},
        }
        requests_mock.get("https://zenodo.org/api/records/1234", json=mock_record)

        mock_record_files = {
            "entries": [
                {
                    "key": "some_dir/afake.zip",
                    "links": {"content": f"file://{zen_path}"},
                }
            ],
        }
        requests_mock.get(
            "https://zenodo.org/api/records/1234/files", json=mock_record_files
        )

        requests_mock.get(f"file://{zen_path}", content=open(zen_path, "rb").read())

        zen = Zenodo()
        spec = {"host": test_zen.hosts[1], "record": "1234"}

        with TemporaryDirectory() as d:
            output = []
            for l in zen.fetch(spec, d):
                output.append(l)

            unpacked_files = set(os.listdir(d))
            expected = {"some-other-file.txt", "some-file.txt"}
            assert expected == unpacked_files


def test_fetch_software(requests_mock):
    # we "fetch" a local ZIP file to simulate a Zenodo software record with a
    # ZIP file in it
    with zenodo_archive() as zen_path:
        mock_record = {
            "files": [
                {
                    # this is the difference to the GitHub generated one,
                    # the ZIP file isn't in a directory
                    "filename": "afake.zip",
                }
            ],
            "links": {
                "files": "https://zenodo.org/api/records/1234/files",
            },
            "metadata": {"upload_type": "software"},
        }
        requests_mock.get("https://zenodo.org/api/records/1234", json=mock_record)

        mock_record_files = {
            "entries": [
                {
                    "key": "afake.zip",
                    "links": {"content": f"file://{zen_path}"},
                }
            ],
        }
        requests_mock.get(
            "https://zenodo.org/api/records/1234/files", json=mock_record_files
        )

        requests_mock.get(f"file://{zen_path}", content=open(zen_path, "rb").read())

        with TemporaryDirectory() as d:
            zen = Zenodo()
            spec = spec = {"host": test_zen.hosts[1], "record": "1234"}
            output = []
            for l in zen.fetch(spec, d):
                output.append(l)

            unpacked_files = set(os.listdir(d))
            expected = {"some-other-file.txt", "some-file.txt"}
            assert expected == unpacked_files


def test_fetch_data(requests_mock):
    # we "fetch" a local ZIP file to simulate a Zenodo data record
    with zenodo_archive() as a_zen_path:
        with zenodo_archive() as b_zen_path:
            mock_record = {
                "files": [
                    {
                        "filename": "afake.zip",
                    },
                    {
                        "filename": "bfake.zip",
                    },
                ],
                "links": {
                    "files": "https://zenodo.org/api/records/1234/files",
                },
                "metadata": {"upload_type": "data"},
            }
            requests_mock.get("https://zenodo.org/api/records/1234", json=mock_record)

            mock_record_files = {
                "entries": [
                    {
                        "key": "afake.zip",
                        "links": {"content": f"file://{a_zen_path}"},
                    },
                    {
                        "key": "bfake.zip",
                        "links": {"content": f"file://{b_zen_path}"},
                    },
                ],
            }
            requests_mock.get(
                "https://zenodo.org/api/records/1234/files", json=mock_record_files
            )

            requests_mock.get(
                f"file://{a_zen_path}", content=open(a_zen_path, "rb").read()
            )
            requests_mock.get(
                f"file://{b_zen_path}", content=open(b_zen_path, "rb").read()
            )

            with TemporaryDirectory() as d:
                zen = Zenodo()
                spec = {"host": test_zen.hosts[1], "record": "1234"}
                output = []
                for l in zen.fetch(spec, d):
                    output.append(l)

                unpacked_files = set(os.listdir(d))
                # ZIP files shouldn't have been unpacked
                expected = {"bfake.zip", "afake.zip"}
                assert expected == unpacked_files
