import json
import os
import io
import tarfile
import shutil
import re
import urllib
import pytest
import tempfile
import logging
import requests_mock

from os import makedirs
from os.path import join
from unittest.mock import patch, MagicMock, mock_open
from zipfile import ZipFile

from repo2docker.contentproviders.swhid import Swhid, parse_swhid
from repo2docker.contentproviders.base import ContentProviderException


# this is a slightly stripped down copy of swh.model.cli.swhid_of_dir().
# We do not use this later to prevent having to depend on swh.model[cli]
def swhid_of_dir(path):
    object = Directory.from_disk(path=path).get_data()
    return swhid(DIRECTORY, object)


def test_content_id():
    swhid = Swhid()
    assert swhid.content_id is None


swhids_ok = [
    "swh:1:dir:" + "0" * 40,
    "swh:1:rev:" + "0" * 40,
]
swhids_invalid = [
    "swh:1:dir:" + "0" * 39,
    "swh:2:dir:" + "0" * 40,
    "swh:1:rev:" + "0" * 41,
    "swh:1:cnt:" + "0" * 40,
    "swh:1:ori:" + "0" * 40,
    "swh:1:rel:" + "0" * 40,
    "swh:1:snp:" + "0" * 40,
]

detect_values = [
    (swhid, {"swhid": swhid, "swhid_obj": parse_swhid(swhid)}) for swhid in swhids_ok
] + [(swhid, None) for swhid in swhids_invalid]


@pytest.mark.parametrize("swhid, expected", detect_values)
def test_detect(swhid, expected):
    provider = Swhid()
    assert provider.detect(swhid) == expected


def fake_urlopen(req):
    print(req)
    return req.headers


def test_unresolving_swhid():
    provider = Swhid()

    # swhid = "0" * 40
    # assert provider.swhid2url(swhid) is swhid


NULLID = "0" * 40


@pytest.fixture
def gen_tarfile(tmpdir):
    rootdir = join(tmpdir, "tmp")
    makedirs(rootdir)
    with open(join(rootdir, "file1.txt"), "wb") as fobj:
        fobj.write(b"Some content\n")

    # this directory hash can be computed using the swh.model package, but we do
    # nto want to depend on this later to limit dependencies and because it
    # does not support python 3.6;
    dirhash = "89a3bd29a2c5ae0b1465febbe5df09730a8576fe"
    buf = io.BytesIO()
    tarf = tarfile.open(name=dirhash, fileobj=buf, mode="w")
    tarf.add(rootdir, arcname=dirhash)
    tarf.close()
    shutil.rmtree(rootdir)
    return dirhash, buf.getvalue()


def mocked_provider(tmpdir, dirhash, tarfile_buf):
    provider = Swhid()
    adapter = requests_mock.Adapter()
    provider.base_url = "mock://api/1"
    provider.retry_delay = 0.1
    provider.session.mount("mock://", adapter)

    adapter.register_uri(
        "GET",
        "mock://api/1/revision/{}/".format(NULLID),
        json={
            "author": {"fullname": "John Doe <jdoe@example.com>"},
            "directory": dirhash,
        },
    )
    adapter.register_uri(
        "POST",
        "mock://api/1/vault/directory/{}/".format(dirhash),
        json={
            "fetch_url": "mock://api/1/vault/directory/{}/raw/".format(dirhash),
            "status": "new",
        },
    )
    adapter.register_uri(
        "GET",
        "mock://api/1/vault/directory/{}/".format(dirhash),
        [
            {
                "json": {
                    "fetch_url": "mock://api/1/vault/directory/{}/raw/".format(dirhash),
                    "status": "pending",
                }
            },
            {
                "json": {
                    "fetch_url": "mock://api/1/vault/directory/{}/raw/".format(dirhash),
                    "status": "done",
                }
            },
        ],
    )
    adapter.register_uri(
        "GET",
        "mock://api/1/vault/directory/{}/raw/".format(dirhash),
        content=tarfile_buf,
    )
    return provider


def test_fetch_revision(tmpdir, gen_tarfile):
    dir_id, tarfile_buf = gen_tarfile
    provider = mocked_provider(tmpdir, dir_id, tarfile_buf)
    swhid = "swh:1:rev:" + NULLID
    for log in provider.fetch(provider.detect(swhid), tmpdir):
        print(log)
    assert provider.content_id == "swh:1:dir:" + dir_id


def test_fetch_directory(tmpdir, gen_tarfile):
    dir_id, tarfile_buf = gen_tarfile
    provider = mocked_provider(tmpdir, dir_id, tarfile_buf)
    swhid = "swh:1:dir:" + dir_id
    for log in provider.fetch(provider.detect(swhid), tmpdir):
        print(log)
    assert provider.content_id == swhid
