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


def test_content_id():
    doi = DoiProvider()
    assert doi.content_id is None


def fake_urlopen(req):
    print(req)
    return req.headers


@patch("urllib.request.urlopen", fake_urlopen)
def test_url_headers():
    doi = DoiProvider()

    headers = {"test1": "value1", "Test2": "value2"}
    result = doi.urlopen("https://mybinder.org", headers=headers)
    assert "Test1" in result
    assert "Test2" in result
    assert len(result) is 3  # User-agent is also set


def test_unresolving_doi():
    doi = DoiProvider()

    fakedoi = "10.1/1234"
    assert doi.doi2url(fakedoi) is fakedoi
