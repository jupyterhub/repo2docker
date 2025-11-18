import os
from contextlib import contextmanager
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest.mock import patch
from zipfile import ZipFile

import pytest

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


def test_content_id():
    hydro = Hydroshare()

    hydro.detect("10.4211/hs.b8f6eae9d89241cf8b5904033460af61")
    assert hydro.content_id == "b8f6eae9d89241cf8b5904033460af61.v1585005408"


def test_detect_hydroshare():
    # valid Hydroshare DOIs trigger this content provider
    expected = {
        "host": {
            "hostname": [
                "https://www.hydroshare.org/resource/",
                "http://www.hydroshare.org/resource/",
                "https://hydroshare.org/resource/",
                "http://hydroshare.org/resource/",
            ],
            "django_s3": "https://www.hydroshare.org/django_s3/download/bags/",
            "version": "https://www.hydroshare.org/hsapi/resource/{}/scimeta/elements",
        },
        "resource": "b8f6eae9d89241cf8b5904033460af61",
        "version": "1585005408",
    }

    assert (
        Hydroshare().detect(
            "https://hydroshare.org/resource/b8f6eae9d89241cf8b5904033460af61"
        )
        == expected
    )

    assert (
        Hydroshare().detect("10.4211/hs.b8f6eae9d89241cf8b5904033460af61") == expected
    )

    assert (
        Hydroshare().detect(
            "https://doi.org/10.4211/hs.b8f6eae9d89241cf8b5904033460af61"
        )
        == expected
    )

    # Don't trigger the Hydroshare content provider
    assert Hydroshare().detect("/some/path/here") is None
    assert Hydroshare().detect("https://example.com/path/here") is None

    # don't handle DOIs that aren't from Hydroshare
    assert Hydroshare().detect("https://doi.org/10.21105/joss.01277") is None


@contextmanager
def hydroshare_archive(prefix="123456789/data/contents"):
    with NamedTemporaryFile(suffix=".zip") as zfile:
        with ZipFile(zfile.name, mode="w") as zip:
            zip.writestr(f"{prefix}/some-file.txt", "some content")
            zip.writestr(f"{prefix}/some-other-file.txt", "some more content")

        yield zfile


class MockResponse:
    def __init__(self, url, status_code):
        self.status_code = status_code
        self.url = url


def test_fetch_bag():
    # we "fetch" a local ZIP file to simulate a Hydroshare resource
    with hydroshare_archive() as hydro_path:
        with patch.object(
            Hydroshare,
            "urlopen",
            side_effect=[
                MockResponse("https://www.hydroshare.org/django_s3/download/bags/123456789.zip",
                             200),
                MockResponse("https://s3.hydroshare.org/bags/123456789.zip", 200),
            ],
        ):
            with patch.object(
                Hydroshare, "_urlretrieve", side_effect=[(hydro_path, None)]
            ):
                hydro = Hydroshare()
                hydro.resource_id = "123456789"
                spec = {
                    "host": {
                        "hostname": [
                            "https://www.hydroshare.org/resource/",
                            "http://www.hydroshare.org/resource/",
                            "https://hydroshare.org/resource/",
                            "http://hydroshare.org/resource/",
                        ],
                        "django_s3": "https://www.hydroshare.org/django_s3/download/bags/",
                    },
                    "resource": "123456789",
                }

                with TemporaryDirectory() as d:
                    output = []
                    for l in hydro.fetch(spec, d):
                        output.append(l)

                    unpacked_files = set(os.listdir(d))
                    expected = {"some-other-file.txt", "some-file.txt"}
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
                        "https://hydroshare.org/resource/",
                        "http://hydroshare.org/resource/",
                    ],
                    "django_s3": "https://www.hydroshare.org/django_s3/download/bags/",
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
                        "https://hydroshare.org/resource/",
                        "http://hydroshare.org/resource/",
                    ],
                    "django_s3": "https://www.hydroshare.org/django_s3/download/bags/",
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
