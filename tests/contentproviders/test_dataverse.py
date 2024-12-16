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
        ("doi:10.7910/DVN/6ZXAGT/3YRRYJ", {"host": harvard_dv, "record": "doi:10.7910/DVN/6ZXAGT"}),
        ("10.7910/DVN/6ZXAGT/3YRRYJ", {"host": harvard_dv, "record": "doi:10.7910/DVN/6ZXAGT"}),
        ("https://dataverse.harvard.edu/api/access/datafile/3323458", {"host": harvard_dv, "record": "doi:10.7910/DVN/6ZXAGT"}),
        ("https://data.cimmyt.org/dataset.xhtml?persistentId=hdl:11529/10016", {"host": cimmyt_dv, "record": "doi:10.7910/DVN/6ZXAGT"}),
        ("/some/random/string", None),
        ("https://example.com/path/here", None),
        # Non dataverse DOIs
        ("https://doi.org/10.21105/joss.01277", None)
    ]
)
def test_detect(doi, resolved):
    assert Dataverse().detect(doi) == resolved


def test_dataverse_fetch():
    spec = {"host": harvard_dv, "record": "doi:10.7910/DVN/TJCLKP"}

    dv = Dataverse()

    with TemporaryDirectory() as d:
        output = []
        for l in dv.fetch(spec, d):
            output.append(l)

        # Verify two directories
        assert set(os.listdir(d)) == {"data", "code"}

        # Verify sha256sum of three files
        expected_sha = {
            'data/primary/primary-data.zip': '880f99a1e1d54a2553be61301f92e06b29236785b8d4d1b7ad0b4595d9d7512b',
            'data/2023-01-03.tsv': 'cc9759e8e6bc076dd7c1a8eb53a7ea3d38e8697fa9f544d15768db308516cc5f',
            'code/language.py': '1ffb3b3cdc9de01279779f3fc88824672c8ec3ab1c41ecdd5c1b59a9b0202215'
        }

        for subpath, expected_sha in expected_sha.items():
            with open(os.path.join(d, subpath), 'rb') as f:
                h = hashlib.sha256()
                h.update(f.read())
                assert h.hexdigest() == expected_sha