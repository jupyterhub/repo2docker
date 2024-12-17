import hashlib
import os
from tempfile import TemporaryDirectory

import pytest

from repo2docker.contentproviders import Dataverse

test_dv = Dataverse()
harvard_dv = next(_ for _ in test_dv.hosts if _["name"] == "Harvard Dataverse")
cimmyt_dv = next(_ for _ in test_dv.hosts if _["name"] == "CIMMYT Research Data")


@pytest.mark.parametrize(
    ("doi", "resolved"),
    [
        (
            "doi:10.7910/DVN/6ZXAGT/3YRRYJ",
            {
                "host": harvard_dv,
                "url": "https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ",
            },
        ),
        (
            "10.7910/DVN/6ZXAGT/3YRRYJ",
            {
                "host": harvard_dv,
                "url": "https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ",
            },
        ),
        (
            "10.7910/DVN/TJCLKP",
            {
                "host": harvard_dv,
                "url": "https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/TJCLKP",
            },
        ),
        (
            "https://dataverse.harvard.edu/api/access/datafile/3323458",
            {
                "host": harvard_dv,
                "url": "https://dataverse.harvard.edu/api/access/datafile/3323458",
            },
        ),
        (
            "https://data.cimmyt.org/dataset.xhtml?persistentId=hdl:11529/10016",
            {
                "host": cimmyt_dv,
                "url": "https://data.cimmyt.org/dataset.xhtml?persistentId=hdl:11529/10016",
            },
        ),
        ("/some/random/string", None),
        ("https://example.com/path/here", None),
        # Non dataverse DOIs
        ("https://doi.org/10.21105/joss.01277", None),
    ],
)
def test_detect(doi, resolved):
    assert Dataverse().detect(doi) == resolved


@pytest.mark.parametrize(
    ("url", "persistent_id"),
    [
        (
            "https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ",
            "doi:10.7910/DVN/6ZXAGT",
        ),
        (
            "https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/TJCLKP",
            "doi:10.7910/DVN/TJCLKP",
        ),
        (
            "https://dataverse.harvard.edu/api/access/datafile/3323458",
            "doi:10.7910/DVN/3MJ7IR",
        ),
        (
            "https://data.cimmyt.org/dataset.xhtml?persistentId=hdl:11529/10016",
            "hdl:11529/10016",
        ),
    ],
)
def test_get_persistent_id(url, persistent_id):
    assert Dataverse().get_persistent_id_from_url(url) == persistent_id


@pytest.mark.parametrize(
    ("spec", "md5tree"),
    [
        (
            "doi:10.7910/DVN/TJCLKP",
            {
                "data/primary/primary-data.zip": "a8f6fc3fc58f503cd48e23fa8b088694",
                "data/2023-01-03.tsv": "6fd497bf13dab9a06fe737ebc22f1917",
                "code/language.py": "9d61582bcf497c83bbd1ed0eed3c772e",
            },
        ),
        (
            # A citation targeting a single file
            "https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ",
            {
                "ARCHAEOGLOBE_CONSENSUS_ASSESSMENT.tab": "17a91888ed8e91dfb63acbbab6127ac5"
            }
        )
    ],
)
def test_fetch(spec, md5tree):
    dv = Dataverse()

    with TemporaryDirectory() as d:
        output = []
        for l in dv.fetch(dv.detect(spec), d):
            output.append(l)

        # Verify md5 sum of the files we expect to find
        # We are using md5 instead of something more secure because that is what
        # dataverse itself uses
        for subpath, expected_sha in md5tree.items():
            with open(os.path.join(d, subpath), "rb") as f:
                h = hashlib.md5()
                h.update(f.read())
                assert h.hexdigest() == expected_sha
