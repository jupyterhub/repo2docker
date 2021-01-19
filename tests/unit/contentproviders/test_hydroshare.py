import os
import pytest

from contextlib import contextmanager
from tempfile import TemporaryDirectory, NamedTemporaryFile
from unittest.mock import patch
from zipfile import ZipFile
import re

from repo2docker.contentproviders import Hydroshare
from repo2docker.contentproviders.base import ContentProviderException


doi_responses = {
    "https://doi.org/10.4211/hs.b8f6eae9d89241cf8b5904033460af61": (
        "https://www.hydroshare.org/resource/b8f6eae9d89241cf8b5904033460af61"
    ),
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


hydroshare_data = {
    "dates": [{"type": "modified", "start_date": "2019-09-25T16:09:17.006152Z"}]
}


def test_content_id(requests_mock):

    requests_mock.get(re.compile("https://"), json=hydroshare_data)
    requests_mock.get(re.compile("https://doi.org"), json=doi_resolver)

    hydro = Hydroshare()

    hydro.detect("10.4211/hs.b8f6eae9d89241cf8b5904033460af61")
    assert hydro.content_id == "b8f6eae9d89241cf8b5904033460af61.v1569427757"


def test_detect_hydroshare(requests_mock):
    requests_mock.get(re.compile("https://"), json=hydroshare_data)
    requests_mock.get(re.compile("https://doi.org"), json=doi_resolver)

    # valid Hydroshare DOIs trigger this content provider
    expected = {
        "host": {
            "hostname": [
                "https://www.hydroshare.org/resource/",
                "http://www.hydroshare.org/resource/",
            ],
            "django_irods": "https://www.hydroshare.org/django_irods/download/bags/",
            "version": "https://www.hydroshare.org/hsapi/resource/{}/scimeta/elements",
        },
        "resource": "b8f6eae9d89241cf8b5904033460af61",
        "version": "1569427757",
    }

    assert (
        Hydroshare().detect(
            "https://www.hydroshare.org/resource/b8f6eae9d89241cf8b5904033460af61"
        )
        == expected
    )
    # assert a call to urlopen was called to fetch version
    assert requests_mock.call_count == 1
    requests_mock.reset_mock()

    assert (
        Hydroshare().detect("10.4211/hs.b8f6eae9d89241cf8b5904033460af61") == expected
    )
    # assert 3 calls were made, 2 to resolve the DOI (302 + 200) and another to fetch the version
    assert requests_mock.call_count == 3
    requests_mock.reset_mock()

    assert (
        Hydroshare().detect(
            "https://doi.org/10.4211/hs.b8f6eae9d89241cf8b5904033460af61"
        )
        == expected
    )
    # assert 3 more calls were made, 2 to resolve the DOI and another to fetch the version
    assert requests_mock.call_count == 3
    requests_mock.reset_mock()

    # Don't trigger the Hydroshare content provider
    assert Hydroshare().detect("/some/path/here") is None
    assert Hydroshare().detect("https://example.com/path/here") is None

    # don't handle DOIs that aren't from Hydroshare
    assert Hydroshare().detect("https://doi.org/10.21105/joss.01277") is None


@contextmanager
def hydroshare_archive(prefix="b8f6eae9d89241cf8b5904033460af61/data/contents"):
    with NamedTemporaryFile(suffix=".zip") as zfile:
        with ZipFile(zfile.name, mode="w") as zip:
            zip.writestr("{}/some-file.txt".format(prefix), "some content")
            zip.writestr("{}/some-other-file.txt".format(prefix), "some more content")

        yield zfile


class MockInfo:
    def __init__(self, content_type):
        self.content_type = content_type

    def get_content_type(self):
        return self.content_type


class MockResponse:
    def __init__(self, content_type, status_code):
        self.content_type = content_type
        self.status_code = status_code
        self.mock_info = MockInfo(self.content_type)

    def getcode(self):
        return self.status_code

    def info(self):
        return self.mock_info


def test_fetch_bag():
    # we "fetch" a local ZIP file to simulate a Hydroshare resource
    with hydroshare_archive() as hydro_path:
        with patch.object(
            Hydroshare,
            "urlopen",
            side_effect=[
                MockResponse("application/html", 200),
                MockResponse("application/zip", 200),
            ],
        ):
            with patch.object(
                Hydroshare, "_urlretrieve", side_effect=[(hydro_path, None)]
            ):
                hydro = Hydroshare()
                hydro.resource_id = "b8f6eae9d89241cf8b5904033460af61"
                spec = {
                    "host": {
                        "hostname": [
                            "https://www.hydroshare.org/resource/",
                            "http://www.hydroshare.org/resource/",
                        ],
                        "django_irods": "https://www.hydroshare.org/django_irods/download/bags/",
                    },
                    "resource": "123456789",
                }

                with TemporaryDirectory() as d:
                    output = []
                    for l in hydro.fetch(spec, d):
                        output.append(l)

                    unpacked_files = set(os.listdir(d))
                    expected = set(["some-other-file.txt", "some-file.txt"])
                    assert expected == unpacked_files


def test_fetch_bag_failure():
    with hydroshare_archive():
        with patch.object(
            Hydroshare, "urlopen", side_effect=[MockResponse("application/html", 500)]
        ):
            hydro = Hydroshare()
            spec = {
                "host": {
                    "hostname": [
                        "https://www.hydroshare.org/resource/",
                        "http://www.hydroshare.org/resource/",
                    ],
                    "django_irods": "https://www.hydroshare.org/django_irods/download/bags/",
                },
                "resource": "123456789",
            }
            with TemporaryDirectory() as d:
                with pytest.raises(
                    ContentProviderException,
                    match=r"Failed to download bag\. status code 500\.",
                ):
                    # loop for yield statements
                    for l in hydro.fetch(spec, d):
                        pass


def test_fetch_bag_timeout():
    with hydroshare_archive():
        with patch.object(
            Hydroshare, "urlopen", side_effect=[MockResponse("application/html", 200)]
        ):
            hydro = Hydroshare()
            spec = {
                "host": {
                    "hostname": [
                        "https://www.hydroshare.org/resource/",
                        "http://www.hydroshare.org/resource/",
                    ],
                    "django_irods": "https://www.hydroshare.org/django_irods/download/bags/",
                },
                "resource": "123456789",
            }
            with TemporaryDirectory() as d:
                with pytest.raises(
                    ContentProviderException,
                    match=r"Bag taking too long to prepare, exiting now, try again later\.",
                ):
                    # loop for yield statements
                    for l in hydro.fetch(spec, d, timeout=0):
                        pass
