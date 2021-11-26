import pytest

from repo2docker.contentproviders import IPFS

valid_cids = [
    "QmYjtig7VJQ6XsnUjqqJvj7QaMcCAwtrgNdahSiFofrE7o",
    "bafkreidon73zkcrwdb5iafqtijxildoonbwnpv7dyd6ef3qdgads2jc4su",
    "bafybeiasb5vpmaounyilfuxbd3lryvosl4yefqrfahsb2esg46q6tu6y5q",
    "zdj7WWeQ43G6JJvLWQWZpyHuAMq6uYWRjkBXFad11vE2LHhQ7",
]

not_cids = [
    "https://github.com/multiformats/cid",
    "noop",
    "https://doi.org/10.5281/zenodo.3232985",
]


@pytest.mark.parametrize("cid", valid_cids)
def test_detect_ipfs_on_valid_cid(cid):
    assert IPFS().detect(cid) == {"cid": cid}


@pytest.mark.parametrize("no_cid", not_cids)
def test_dont_detect_ipfs_on_no_cid(no_cid):
    assert IPFS().detect(no_cid) is None
