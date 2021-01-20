import json
import os
import re
import pytest

from contextlib import contextmanager
from io import BytesIO
from tempfile import TemporaryDirectory, NamedTemporaryFile
from unittest.mock import patch
from urllib.request import urlopen, Request
from zipfile import ZipFile

from repo2docker.contentproviders import Figshare
from repo2docker.__main__ import make_r2d


test_content_ids = [
    ("https://figshare.com/articles/title/9782777", "9782777.v1"),
    ("https://figshare.com/articles/title/9782777/2", "9782777.v2"),
    ("https://figshare.com/articles/title/9782777/1234", "9782777.v1234"),
]


@pytest.mark.parametrize("link,expected", test_content_ids)
def test_content_id(link, expected, requests_mock):
    def mocked_get(req, context):
        if req.url.startswith("https://doi.org"):
            context.status_code = 302
            context.headers["Location"] = link
        return link

    requests_mock.get(re.compile("https://"), text=mocked_get)
    fig = Figshare()
    fig.detect("10.6084/m9.figshare.9782777")
    assert fig.content_id == expected


test_fig = Figshare()
test_fig.article_id = "123456"
test_fig.article_version = "42"

test_dois_links = [
    (
        "10.6084/m9.figshare.9782777",
        {"host": test_fig.hosts[0], "article": "9782777", "version": "1"},
    ),
    (
        "10.6084/m9.figshare.9782777.v1",
        {"host": test_fig.hosts[0], "article": "9782777", "version": "1"},
    ),
    pytest.param(
        "10.6084/m9.figshare.9782777.v2",
        {"host": test_fig.hosts[0], "article": "9782777", "version": "2"},
        # $ curl -sIL https://dx.doi.org/10.6084/m9.figshare.9782777.v2 | grep location
        # location: https://figshare.com/articles/Binder-ready_openSenseMap_Analysis/9782777/2
        # location: https://figshare.com/articles/code/Binder-ready_openSenseMap_Analysis/9782777
        marks=pytest.mark.xfail(reason="Problem with figshare version redirects"),
    ),
    (
        "https://doi.org/10.6084/m9.figshare.9782777.v1",
        {"host": test_fig.hosts[0], "article": "9782777", "version": "1"},
        # $ curl -sIL https://doi.org/10.6084/m9.figshare.9782777.v1 | grep location
        # location: https://figshare.com/articles/Binder-ready_openSenseMap_Analysis/9782777/1
        # location: https://figshare.com/articles/code/Binder-ready_openSenseMap_Analysis/9782777
    ),
    pytest.param(
        "https://doi.org/10.6084/m9.figshare.9782777.v3",
        {"host": test_fig.hosts[0], "article": "9782777", "version": "3"},
        # $ curl -sIL https://doi.org/10.6084/m9.figshare.9782777.v3 | grep location
        # location: https://figshare.com/articles/Binder-ready_openSenseMap_Analysis/9782777/3
        # location: https://figshare.com/articles/code/Binder-ready_openSenseMap_Analysis/9782777
        marks=pytest.mark.xfail(reason="Problem with figshare version redirects"),
    ),
    (
        "https://figshare.com/articles/title/97827771234",
        {"host": test_fig.hosts[0], "article": "97827771234", "version": "1"},
    ),
    (
        "https://figshare.com/articles/title/9782777/1",
        {"host": test_fig.hosts[0], "article": "9782777", "version": "1"},
    ),
    (
        "https://figshare.com/articles/title/9782777/2",
        {"host": test_fig.hosts[0], "article": "9782777", "version": "2"},
    ),
    (
        "https://figshare.com/articles/title/9782777/",
        {"host": test_fig.hosts[0], "article": "9782777", "version": "1"},
    ),
    (
        "https://figshare.com/articles/title/9782777/1234",
        {"host": test_fig.hosts[0], "article": "9782777", "version": "1234"},
    ),
]

test_spec = {"host": test_fig.hosts[0], "article": "123456", "version": "42"}


@pytest.mark.parametrize("test_input,expected", test_dois_links)
def test_detect_figshare(test_input, expected):
    assert Figshare().detect(test_input) == expected


def test_detect_not_figshare():
    assert Figshare().detect("/some/path/here") is None
    assert Figshare().detect("https://example.com/path/here") is None
    assert Figshare().detect("10.21105/joss.01277") is None
    assert Figshare().detect("10.5281/zenodo.3232985") is None
    assert Figshare().detect("https://doi.org/10.21105/joss.01277") is None


@contextmanager
def figshare_archive(prefix="a_directory"):
    with NamedTemporaryFile(suffix=".zip") as zfile:
        with ZipFile(zfile.name, mode="w") as zip:
            zip.writestr("{}/some-file.txt".format(prefix), "some content")
            zip.writestr("{}/some-other-file.txt".format(prefix), "some more content")

        yield zfile.name


def test_fetch_zip(requests_mock):
    # see test_zenodo.py/test_fetch_software
    with figshare_archive() as fig_path:
        mock_response = {
            "files": [
                {
                    "name": "afake.zip",
                    "is_link_only": False,
                    "download_url": "file://{}".format(fig_path),
                }
            ]
        }
        requests_mock.get(
            "https://api.figshare.com/v2/articles/123456/versions/42",
            json=mock_response,
        )
        requests_mock.get(
            "file://{}".format(fig_path), content=open(fig_path, "rb").read()
        )

        # with patch.object(Figshare, "urlopen", new=mock_urlopen):
        with TemporaryDirectory() as d:
            output = []
            for l in test_fig.fetch(test_spec, d):
                output.append(l)

            unpacked_files = set(os.listdir(d))
            expected = set(["some-other-file.txt", "some-file.txt"])
            assert expected == unpacked_files


def test_fetch_data(requests_mock):
    with figshare_archive() as a_path:
        with figshare_archive() as b_path:
            mock_response = {
                "files": [
                    {
                        "name": "afake.file",
                        "download_url": "file://{}".format(a_path),
                        "is_link_only": False,
                    },
                    {
                        "name": "bfake.data",
                        "download_url": "file://{}".format(b_path),
                        "is_link_only": False,
                    },
                    {"name": "cfake.link", "is_link_only": True},
                ]
            }

            requests_mock.get(
                "https://api.figshare.com/v2/articles/123456/versions/42",
                json=mock_response,
            )
            requests_mock.get(
                "file://{}".format(a_path), content=open(a_path, "rb").read()
            )
            requests_mock.get(
                "file://{}".format(b_path), content=open(b_path, "rb").read()
            )

            with TemporaryDirectory() as d:
                output = []
                for l in test_fig.fetch(test_spec, d):
                    output.append(l)

                unpacked_files = set(os.listdir(d))
                # ZIP files shouldn't have been unpacked
                expected = {"bfake.data", "afake.file"}
                assert expected == unpacked_files
