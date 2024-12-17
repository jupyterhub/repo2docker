import hashlib
import os
from tempfile import TemporaryDirectory

import pytest

from repo2docker.contentproviders import Dataverse


@pytest.mark.parametrize(
    ("doi", "resolved"),
    [
        (
            "doi:10.7910/DVN/6ZXAGT/3YRRYJ",
            "https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ",
        ),
        (
            "10.7910/DVN/6ZXAGT/3YRRYJ",
            "https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ",
        ),
        (
            "10.7910/DVN/TJCLKP",
            "https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/TJCLKP",
        ),
        (
            "https://dataverse.harvard.edu/api/access/datafile/3323458",
            "https://dataverse.harvard.edu/api/access/datafile/3323458",
        ),
        (
            "https://data.cimmyt.org/dataset.xhtml?persistentId=hdl:11529/10016",
            "https://data.cimmyt.org/dataset.xhtml?persistentId=hdl:11529/10016",
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
    ("url", "persistent_id", "is_ambiguous"),
    [
        (
            "https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ",
            "doi:10.7910/DVN/6ZXAGT",
            False,
        ),
        (
            "https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/TJCLKP",
            "doi:10.7910/DVN/TJCLKP",
            True,
        ),
        (
            "https://dataverse.harvard.edu/api/access/datafile/3323458",
            "doi:10.7910/DVN/3MJ7IR",
            False,
        ),
        (
            "https://data.cimmyt.org/dataset.xhtml?persistentId=hdl:11529/10016",
            "hdl:11529/10016",
            False,
        ),
    ],
)
def test_get_persistent_id(url, persistent_id, is_ambiguous):
    assert Dataverse().parse_dataverse_url(url) == (persistent_id, is_ambiguous)


@pytest.mark.parametrize(
    ("specs", "md5tree"),
    [
        (
            (
                "doi:10.7910/DVN/TJCLKP",
                "https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/TJCLKP",
            ),
            {
                "data/primary/primary-data.zip": "a8f6fc3fc58f503cd48e23fa8b088694",
                "data/2023-01-03.tsv": "6fd497bf13dab9a06fe737ebc22f1917",
                "code/language.py": "9d61582bcf497c83bbd1ed0eed3c772e",
            },
        ),
        (
            (
                "https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ",
                "https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ",
                "doi:10.7910/DVN/6ZXAGT/3YRRYJ",
            ),
            {
                "ArchaeoGLOBE-master/analysis/figures/1_response_distribution.png": "243c6a3dd66bc3c84102829b277ef333",
                "ArchaeoGLOBE-master/analysis/figures/2_trends_map_knowledge.png": "2ace6ae9d470dda6cf2f9f9a6588171a",
                "ArchaeoGLOBE-master/analysis/figures/3_trends_global.png": "63ccd0a7b2d20440cd8f418d4ee88c4d",
                "ArchaeoGLOBE-master/analysis/figures/4_consensus_transitions.png": "facfaedabeac77c4496d4b9e962a917f",
                "ArchaeoGLOBE-master/analysis/figures/5_ArchaeoGLOBE_HYDE_comparison.png": "8e002e4d50f179fc1808f562b1353588",
                "ArchaeoGLOBE-master/apt.txt": "b4224032da6c71d48f46c9b78fc6ed77",
                "ArchaeoGLOBE-master/analysis/archaeoglobe.pdf": "f575be4790efc963ef1bd40d097cc06d",
                "ArchaeoGLOBE-master/analysis/archaeoglobe.Rmd": "f37d5f7993fde9ebd64d16b20fc22905",
                "ArchaeoGLOBE-master/ArchaeoGLOBE.Rproj": "d0250e7918993bab1e707358fe5633e0",
                "ArchaeoGLOBE-master/CONDUCT.md": "f87ef290340322089c32b4e573d8f1e8",
                "ArchaeoGLOBE-master/.circleci/config.yml": "6eaa54073a682b3195d8fab3a9dd8344",
                "ArchaeoGLOBE-master/CONTRIBUTING.md": "b3a6abfc749dd155a3049f94a855bf9f",
                "ArchaeoGLOBE-master/DESCRIPTION": "745ef979494999e483987de72c0adfbd",
                "ArchaeoGLOBE-master/dockerfile": "aedce68e5a7d6e79cbb24c9cffeae593",
                "ArchaeoGLOBE-master/.binder/Dockerfile": "7564a41246ba99b60144afb1d3b6d7de",
                "ArchaeoGLOBE-master/.gitignore": "62c1482e4febbd35dc02fb7e2a31246b",
                "ArchaeoGLOBE-master/analysis/data/derived-data/hyde_crop_prop.RDS": "2aea7748b5586923b0de9d13af58e59d",
                "ArchaeoGLOBE-master/analysis/data/derived-data/kk_anthro_prop.RDS": "145a9e5dd2c95625626a720b52178b70",
                "ArchaeoGLOBE-master/LICENSE.md": "3aa9d41a92a57944bd4590e004898445",
                "ArchaeoGLOBE-master/analysis/data/derived-data/placeholder": "d41d8cd98f00b204e9800998ecf8427e",
                "ArchaeoGLOBE-master/.Rbuildignore": "df15e4fed49abd685b536fef4472b01f",
                "ArchaeoGLOBE-master/README.md": "0b0faabe580c4d76a0e0d64a4f54bca4",
                "ArchaeoGLOBE-master/analysis/data/derived-data/README.md": "547fd1a6e874f6178b1cf525b5b9ae72",
                "ArchaeoGLOBE-master/analysis/figures/S1_FHG_consensus.png": "d2584352e5442b33e4b23e361ca70fe1",
                "ArchaeoGLOBE-master/analysis/figures/S2_EXAG_consensus.png": "513eddfdad01fd01a20263a55ca6dbe3",
                "ArchaeoGLOBE-master/analysis/figures/S3_INAG_consensus.png": "b16ba0ecd21b326f873209a7e55a8deb",
                "ArchaeoGLOBE-master/analysis/figures/S4_PAS_consensus.png": "05695f9412337a00c1cb6d1757d0ec5c",
                "ArchaeoGLOBE-master/analysis/figures/S5_URBAN_consensus.png": "10119f7495d3b8e7ad7f8a0770574f15",
                "ArchaeoGLOBE-master/analysis/figures/S6_trends_map_landuse.png": "b1db7c97f39ccfc3a9e094c3e6307af0",
                "ArchaeoGLOBE-master/analysis/figures/S7_ArchaeoGLOBE_KK10_comparison.png": "30341748324f5f66acadb34c114c3e9d",
            },
        ),
    ],
)
def test_fetch(specs: list[str], md5tree):
    dv = Dataverse()

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
