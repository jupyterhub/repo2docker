import json
import os
import pytest

from contextlib import contextmanager
from io import BytesIO
from tempfile import TemporaryDirectory, NamedTemporaryFile
from unittest.mock import patch
from urllib.request import urlopen, Request, urlretrieve
from zipfile import ZipFile

from repo2docker.contentproviders import Hydroshare


def test_content_id():
    with patch.object(Hydroshare, "urlopen") as fake_urlopen:
        fake_urlopen.return_value.url = "https://www.hydroshare.org/resource/b8f6eae9d89241cf8b5904033460af61"
        hydro = Hydroshare()

        hydro.detect("10.4211/hs.b8f6eae9d89241cf8b5904033460af61")
        assert hydro.content_id == "b8f6eae9d89241cf8b5904033460af61"


test_hosts = [
    (
        [
            "https://www.hydroshare.org/resource/b8f6eae9d89241cf8b5904033460af61",
            "10.4211/hs.b8f6eae9d89241cf8b5904033460af61",
            "https://doi.org/10.4211/hs.b8f6eae9d89241cf8b5904033460af61",
        ],
        {
            "host": {
                "hostname": ["https://www.hydroshare.org/resource/", "http://www.hydroshare.org/resource/"],
                "django_irods": "https://www.hydroshare.org/django_irods/download/bags/",
            },
            "resource": "b8f6eae9d89241cf8b5904033460af61",
        },
    ),
]

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

@pytest.mark.parametrize("test_input,expected", test_hosts)
def test_detect_hydroshare(test_input, expected):
    with patch.object(Hydroshare, "urlopen") as fake_urlopen:
        fake_urlopen.return_value.url = test_input[0]
        # valid Hydroshare DOIs trigger this content provider
        assert Hydroshare().detect(test_input[0]) == expected
        assert Hydroshare().detect(test_input[1]) == expected
        assert Hydroshare().detect(test_input[2]) == expected
        # only two of the three calls above have to resolve a DOI
        assert fake_urlopen.call_count == 2

    with patch.object(Hydroshare, "urlopen") as fake_urlopen:
        # Don't trigger the Hydroshare content provider
        assert Hydroshare().detect("/some/path/here") is None
        assert Hydroshare().detect("https://example.com/path/here") is None
        # don't handle DOIs that aren't from Hydroshare
        fake_urlopen.return_value.url = (
            "http://joss.theoj.org/papers/10.21105/joss.01277"
        )
        assert Hydroshare().detect("https://doi.org/10.21105/joss.01277") is None

@contextmanager
def hydroshare_archive(prefix="b8f6eae9d89241cf8b5904033460af61/data/contents"):
    with NamedTemporaryFile(suffix=".zip") as zfile:
        with ZipFile(zfile.name, mode="w") as zip:
            zip.writestr("{}/some-file.txt".format(prefix), "some content")
            zip.writestr("{}/some-other-file.txt".format(prefix), "some more content")

        yield zfile

def test_fetch_bag():
    # we "fetch" a local ZIP file to simulate a Hydroshare resource
    with hydroshare_archive() as hydro_path:
        with patch.object(Hydroshare, "urlopen", side_effect=[MockResponse("application/html", 200), MockResponse("application/zip", 200)]):
            with patch.object(Hydroshare, "_urlretrieve", side_effect=[(hydro_path, None)]):
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
    with hydroshare_archive() as hydro_path:
        with patch.object(Hydroshare, "urlopen", side_effect=[MockResponse("application/html", 500)]):
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
                output = []
                for l in hydro.fetch(spec, d):
                    output.append(l)
                assert "Failed to download bag. status code 500.\n" == output[-1]

def test_fetch_bag_timeout():
    with hydroshare_archive() as hydro_path:
        with patch.object(Hydroshare, "urlopen", side_effect=[MockResponse("application/html", 200)]):
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
                output = []
                for l in hydro.fetch(spec, d, timeout=0):
                    output.append(l)
                assert "Bag taking too long to prepare, exiting now, try again later." == output[-1]

