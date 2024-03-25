import os
from contextlib import contextmanager
from tempfile import NamedTemporaryFile, TemporaryDirectory

from repo2docker.contentproviders import CKAN


def test_detect_ckan(requests_mock):
    mock_response = {"result": {"metadata_modified": "2024-02-27T14:15:54.573058"}}
    requests_mock.get("http://demo.ckan.org/api/3/action/status_show", status_code=200)
    requests_mock.get(
        "http://demo.ckan.org/api/3/action/package_show?id=1234", json=mock_response
    )

    expected = {
        "dataset_id": "1234",
        "api_url": "http://demo.ckan.org/api/3/action/",
        "version": "1709043354",
    }

    assert CKAN().detect("http://demo.ckan.org/dataset/1234") == expected


def test_detect_not_ckan():
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
