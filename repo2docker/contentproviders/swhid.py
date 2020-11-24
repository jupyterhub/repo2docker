import io
import os
import shutil
import tarfile
import time
import re

from os import path

import requests

from .base import ContentProvider
from ..utils import copytree
from .. import __version__


def parse_swhid(swhid):
    swhid_regexp = r"^swh:(?P<version>\d+):(?P<type>ori|cnt|rev|dir|snp|rel):(?P<hash>[0-9a-f]{40})$"
    # only parse/check the <identifier_core> of the swhid
    # see https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html
    m = re.match(swhid_regexp, swhid.split(";")[0])
    if m:
        return m.groupdict()


class Swhid(ContentProvider):
    """Provide contents of a repository identified by a SWHID."""

    retry_delay = 5

    def __init__(self):
        self.swhid = None
        self.base_url = "https://archive.softwareheritage.org/api/1"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "user-agent": "repo2docker {}".format(__version__),
            }
        )

    def set_auth_token(self, token):
        header = {"Authorization": "Bearer {}".format(token)}
        self.session.headers.update(header)

    def _request(self, url, method="GET"):
        if not url.endswith("/"):
            url = url + "/"

        for retries in range(3):
            try:
                resp = self.session.request(method, url)
                if resp.ok:
                    break
            except requests.ConnectionError:
                time.sleep(self.retry_delay)

        return resp

    @property
    def content_id(self):
        """The SWHID record ID used for content retrival"""
        return self.swhid

    def detect(self, swhid, ref=None, extra_args=None):
        swhid_dict = parse_swhid(swhid)

        if (
            swhid_dict
            and swhid_dict["type"] in ("dir", "rev")
            and swhid_dict["version"] == "1"
        ):
            return {"swhid": swhid, "swhid_obj": swhid_dict}

    def fetch_directory(self, dir_hash, output_dir):
        url = "{}/vault/directory/{}/".format(self.base_url, dir_hash)
        yield "Fetching directory {} from {}\n".format(dir_hash, url)
        resp = self._request(url, "POST")
        receipt = resp.json()
        status = receipt["status"]
        assert status != "failed", receipt
        while status not in ("failed", "done"):
            time.sleep(self.retry_delay)
            resp = self._request(url)
            status = resp.json()["status"]
        if status == "failed":
            yield "Error preparing the directory for download"
            raise Exception()
        resp = self._request(resp.json()["fetch_url"])
        archive = tarfile.open(fileobj=io.BytesIO(resp.content))
        archive.extractall(path=output_dir)
        # the output_dir should have only one subdir named after the dir_hash
        # move its content one level up
        copytree(path.join(output_dir, dir_hash), output_dir)
        shutil.rmtree(path.join(output_dir, dir_hash))
        yield "Fetched files: {}\n".format(os.listdir(output_dir))

    def fetch(self, spec, output_dir, yield_output=False):
        swhid = spec["swhid"]
        swhid_obj = spec["swhid_obj"]

        if swhid_obj["type"] == "rev":
            # need to get the directory for this revision
            sha1git = swhid_obj["hash"]
            url = "{}/revision/{}/".format(self.base_url, sha1git)
            yield "Fetching revision {} from {}\n".format(sha1git, url)
            resp = self._request(url)
            assert resp.ok, (resp.content, self.session.headers)
            directory = resp.json()["directory"]
            self.swhid = "swh:1:dir:{}".format(directory)
            yield from self.fetch_directory(directory, output_dir)
        elif swhid_obj["type"] == "dir":
            self.swhid = swhid
            yield from self.fetch_directory(swhid_obj["hash"], output_dir)
