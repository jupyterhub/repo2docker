import json
import logging
import os
import re
import tempfile
import urllib
from unittest.mock import MagicMock, mock_open, patch
from zipfile import ZipFile

import pytest

from repo2docker import __version__
from repo2docker.contentproviders.base import ContentProviderException
from repo2docker.contentproviders.doi import DoiProvider


def test_content_id():
    doi = DoiProvider()
    assert doi.content_id is None


def test_url_headers(requests_mock):
    requests_mock.get("https://mybinder.org", text="resp")
    doi = DoiProvider()

    headers = {"test1": "value1", "Test2": "value2"}
    result = doi.urlopen("https://mybinder.org", headers=headers)
    assert "test1" in result.request.headers
    assert "Test2" in result.request.headers
    assert result.request.headers["User-Agent"] == f"repo2docker {__version__}"


@pytest.mark.parametrize(
    "requested_doi, expected",
    [
        ("10.5281/zenodo.3242074", "https://zenodo.org/records/3242074"),
        # Unresolving DOI:
        ("10.1/1234", "10.1/1234"),
    ],
)
def test_doi2url(requested_doi, expected):
    doi = DoiProvider()
    assert doi.doi2url(requested_doi) == expected
