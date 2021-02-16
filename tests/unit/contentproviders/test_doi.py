import json
import os
import re
import urllib
import pytest
import tempfile
import logging

from unittest.mock import patch, MagicMock, mock_open
from zipfile import ZipFile

from repo2docker.contentproviders.doi import DoiProvider
from repo2docker.contentproviders.base import ContentProviderException
from repo2docker import __version__


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
    assert result.request.headers["User-Agent"] == "repo2docker {}".format(__version__)


def test_unresolving_doi():
    doi = DoiProvider()

    fakedoi = "10.1/1234"
    assert doi.doi2url(fakedoi) is fakedoi
