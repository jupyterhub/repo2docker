import json
import os
import pytest
import re

from io import BytesIO
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.request import urlopen, Request

from repo2docker.contentproviders import Dataverse


test_dv = Dataverse()
harvard_dv = next((_ for _ in test_dv.hosts if _["name"] == "Harvard Dataverse"))
cimmyt_dv = next((_ for _ in test_dv.hosts if _["name"] == "CIMMYT Research Data"))
test_hosts = [
    (
        [
            "doi:10.7910/DVN/6ZXAGT/3YRRYJ",
            "10.7910/DVN/6ZXAGT",
            "https://dataverse.harvard.edu/api/access/datafile/3323458",
            "https://data.cimmyt.org/dataset.xhtml?persistentId=hdl:11529/10016",
        ],
        [
            {"host": harvard_dv, "record": "doi:10.7910/DVN/6ZXAGT"},
            {"host": cimmyt_dv, "record": "hdl:11529/10016"},
        ],
    )
]
doi_responses = {
    "https://doi.org/10.7910/DVN/6ZXAGT/3YRRYJ": (
        "https://dataverse.harvard.edu/file.xhtml"
        "?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ"
    ),
    "https://doi.org/10.7910/DVN/6ZXAGT": (
        "https://dataverse.harvard.edu/dataset.xhtml"
        "?persistentId=doi:10.7910/DVN/6ZXAGT"
    ),
    "https://dataverse.harvard.edu/api/access/datafile/3323458": (
        "https://dataverse.harvard.edu/api/access/datafile/3323458"
    ),
    "https://doi.org/10.21105/joss.01277": (
        "https://joss.theoj.org/papers/10.21105/joss.01277"
    ),
}


@pytest.mark.parametrize("test_input, expected", test_hosts)
def test_detect_dataverse(test_input, expected, requests_mock):
    def doi_resolver(req, context):
        resp = doi_responses.get(req.url)
        # doi responses are redirects
        if resp is not None:
            context.status_code = 302
            context.headers["Location"] = resp
        return resp

    requests_mock.get(re.compile("https://"), json=doi_resolver)
    requests_mock.get(
        "https://dataverse.harvard.edu/api/search?q=entityId:3323458&type=file",
        json={
            "data": {
                "count_in_response": 1,
                "items": [{"dataset_persistent_id": "doi:10.7910/DVN/6ZXAGT"}],
            }
        },
    )

    assert requests_mock.call_count == 0
    # valid Dataverse DOIs trigger this content provider
    assert Dataverse().detect(test_input[0]) == expected[0]
    # 4: doi resolution (302), File, doi resolution (302), then dataset
    assert requests_mock.call_count == 4
    requests_mock.reset_mock()

    assert Dataverse().detect(test_input[1]) == expected[0]
    # 2: doi (302), dataset
    assert requests_mock.call_count == 2
    requests_mock.reset_mock()

    assert Dataverse().detect(test_input[2]) == expected[0]
    # 1: datafile (search dataverse for the file id)
    assert requests_mock.call_count == 1
    requests_mock.reset_mock()

    assert Dataverse().detect(test_input[3]) == expected[1]
    requests_mock.reset_mock()

    # Don't trigger the Dataverse content provider
    assert Dataverse().detect("/some/path/here") is None
    assert Dataverse().detect("https://example.com/path/here") is None
    # don't handle DOIs that aren't from Dataverse
    assert Dataverse().detect("https://doi.org/10.21105/joss.01277") is None


@pytest.fixture
def dv_files(tmpdir):

    f1 = tmpdir.join("some-file.txt")
    f1.write("some content")

    f2 = tmpdir.mkdir("directory").join("some-other-file.txt")
    f2.write("some other content")

    f3 = tmpdir.join("directory").mkdir("subdirectory").join("the-other-file.txt")
    f3.write("yet another content")

    return [f1, f2, f3]


def test_dataverse_fetch(dv_files, requests_mock):
    mock_response = {
        "data": {
            "latestVersion": {
                "files": [
                    {"dataFile": {"id": 1}, "label": "some-file.txt"},
                    {
                        "dataFile": {"id": 2},
                        "label": "some-other-file.txt",
                        "directoryLabel": "directory",
                    },
                    {
                        "dataFile": {"id": 3},
                        "label": "the-other-file.txt",
                        "directoryLabel": "directory/subdirectory",
                    },
                ]
            }
        }
    }

    spec = {"host": harvard_dv, "record": "doi:10.7910/DVN/6ZXAGT"}

    def mock_filecontent(req, context):
        file_no = int(req.url.split("/")[-1]) - 1
        return open(dv_files[file_no], "rb").read()

    requests_mock.get(
        "https://dataverse.harvard.edu/api/datasets/"
        ":persistentId?persistentId=doi:10.7910/DVN/6ZXAGT",
        json=mock_response,
    )
    requests_mock.get(
        re.compile("https://dataverse.harvard.edu/api/access/datafile"),
        content=mock_filecontent,
    )

    dv = Dataverse()

    with TemporaryDirectory() as d:
        output = []
        for l in dv.fetch(spec, d):
            output.append(l)
        unpacked_files = set(os.listdir(d))
        expected = set(["directory", "some-file.txt"])
        assert expected == unpacked_files
        assert os.path.isfile(
            os.path.join(d, "directory", "subdirectory", "the-other-file.txt")
        )
