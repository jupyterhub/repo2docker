import os
from contextlib import contextmanager
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from repo2docker.contentproviders import CKAN

test_ckan = CKAN()
test_hosts = [
    (
        [
            "http://demo.ckan.org/dataset/sample-dataset-1",
        ],
        {
            "dataset_id": "sample-dataset-1",
            "api_url": "http://demo.ckan.org/api/3/action/",
            "version": "1707387710",
        },
    )
]


@pytest.mark.parametrize("test_input, expected", test_hosts)
def test_detect_ckan(test_input, expected):
    assert CKAN().detect(test_input[0]) == expected

    # Don't trigger the CKAN content provider
    assert CKAN().detect("/some/path/here") is None
    assert CKAN().detect("https://example.com/path/here") is None
    assert CKAN().detect("https://data.gov.tw/dataset/6564") is None


@contextmanager
def ckan_file():
    with NamedTemporaryFile() as file:
        file.write(b"some content")
        yield file.name


def test_ckan_fetch(requests_mock):
    with ckan_file() as ckan_path:
        mock_response = {"result": {"resources": [{"url": f"file://{ckan_path}"}]}}
        requests_mock.get(
            "http://demo.ckan.org/api/3/action/package_show?id=1234", json=mock_response
        )
        requests_mock.get(f"file://{ckan_path}", content=open(ckan_path, "rb").read())
        with TemporaryDirectory() as d:
            ckan = CKAN()
            spec = {
                "dataset_id": "1234",
                "api_url": "http://demo.ckan.org/api/3/action/",
            }
            output = []
            for l in ckan.fetch(spec, d):
                output.append(l)
            expected = {ckan_path.rsplit("/", maxsplit=1)[1]}
            assert expected == set(os.listdir(d))
