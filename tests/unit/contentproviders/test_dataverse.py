import json
import os
import pytest

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
            "hdl:11529/10016",
        ],
        [
            {"host": harvard_dv, "record": "doi:10.7910/DVN/6ZXAGT"},
            {"host": cimmyt_dv, "record": "hdl:11529/10016"},
        ],
    )
]
test_responses = {
    "doi:10.7910/DVN/6ZXAGT/3YRRYJ": (
        "https://dataverse.harvard.edu/file.xhtml"
        "?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ"
    ),
    "doi:10.7910/DVN/6ZXAGT": (
        "https://dataverse.harvard.edu/dataset.xhtml"
        "?persistentId=doi:10.7910/DVN/6ZXAGT"
    ),
    "10.7910/DVN/6ZXAGT": (
        "https://dataverse.harvard.edu/dataset.xhtml"
        "?persistentId=doi:10.7910/DVN/6ZXAGT"
    ),
    "https://dataverse.harvard.edu/api/access/datafile/3323458": "https://dataverse.harvard.edu/api/access/datafile/3323458",
    "hdl:11529/10016": "https://data.cimmyt.org/dataset.xhtml?persistentId=hdl:11529/10016",
}
test_search = {
    "data": {
        "count_in_response": 1,
        "items": [{"dataset_persistent_id": "doi:10.7910/DVN/6ZXAGT"}],
    }
}


@pytest.mark.parametrize("test_input, expected", test_hosts)
def test_detect_dataverse(test_input, expected):
    def doi_resolver(url):
        return test_responses.get(url)

    with patch.object(Dataverse, "urlopen") as fake_urlopen, patch.object(
        Dataverse, "doi2url", side_effect=doi_resolver
    ) as fake_doi2url:
        fake_urlopen.return_value.read.return_value = json.dumps(test_search).encode()
        # valid Dataverse DOIs trigger this content provider
        assert Dataverse().detect(test_input[0]) == expected[0]
        assert fake_doi2url.call_count == 2  # File, then dataset
        assert Dataverse().detect(test_input[1]) == expected[0]
        assert Dataverse().detect(test_input[2]) == expected[0]
        # only two of the three calls above have to resolve a DOI
        assert fake_urlopen.call_count == 1
        assert Dataverse().detect(test_input[3]) == expected[1]

    with patch.object(Dataverse, "urlopen") as fake_urlopen:
        # Don't trigger the Dataverse content provider
        assert Dataverse().detect("/some/path/here") is None
        assert Dataverse().detect("https://example.com/path/here") is None
        # don't handle DOIs that aren't from Dataverse
        fake_urlopen.return_value.url = (
            "http://joss.theoj.org/papers/10.21105/joss.01277"
        )
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


def test_dataverse_fetch(dv_files):
    mock_response_ds_query = BytesIO(
        json.dumps(
            {
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
        ).encode("utf-8")
    )
    spec = {"host": harvard_dv, "record": "doi:10.7910/DVN/6ZXAGT"}

    dv = Dataverse()

    def mock_urlopen(self, req):
        if isinstance(req, Request):
            return mock_response_ds_query
        else:
            file_no = int(req.split("/")[-1]) - 1
            return urlopen("file://{}".format(dv_files[file_no]))

    with patch.object(Dataverse, "urlopen", new=mock_urlopen):
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
