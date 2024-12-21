import os
import hashlib
from tempfile import TemporaryDirectory

import pytest

from repo2docker.contentproviders import Hydroshare


@pytest.mark.parametrize(
    ("spec", "url"),
    [
        # Test a hydroshare DOI
        ("10.4211/hs.b8f6eae9d89241cf8b5904033460af61", "http://www.hydroshare.org/resource/b8f6eae9d89241cf8b5904033460af61"),
        # Hydroshare DOI in a different form
        ("https://doi.org/10.4211/hs.b8f6eae9d89241cf8b5904033460af61", "http://www.hydroshare.org/resource/b8f6eae9d89241cf8b5904033460af61"),
        # Test a non-hydroshare DOI
        ("doi:10.7910/DVN/TJCLKP", None),
        # Test a hydroshare URL
        ("http://www.hydroshare.org/resource/b8f6eae9d89241cf8b5904033460af61", "http://www.hydroshare.org/resource/b8f6eae9d89241cf8b5904033460af61"),
        # Test a random URL
        ("https://www.eff.org/cyberspace-independence", None)
    ]
)
def test_detect(spec, url):
    assert Hydroshare().detect(spec) == url


@pytest.mark.parametrize(
    ("specs", "md5tree"),
    [
        (
            ("https://www.hydroshare.org/resource/8f7c2f0341ef4180b0dbe97f59130756/", ),
            {
                "binder/Dockerfile": "872ab0ef22645a42a5560eae640cdc77",
                "README.md": "88ac547c3a5f616f6d26e0689d63a113",
                "notebooks/sanity-check.ipynb": "7fc4c455bc8cd244479f4d2282051ee6"
            },
        ),
    ],
)
def test_fetch(specs: list[str], md5tree):
    dv = Hydroshare()

    for spec in specs:
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

