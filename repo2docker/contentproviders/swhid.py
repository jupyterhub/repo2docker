import io
import os
import re
import shutil
import sys
import tarfile
import time
from os import path

import requests

from .. import __version__
from ..utils import copytree
from .base import ContentProvider, ContentProviderException


def parse_swhid(swhid):
    swhid_regexp = r"^swh:(?P<version>\d+):(?P<type>ori|cnt|rev|dir|snp|rel):(?P<hash>[0-9a-f]{40})$"
    # only parse/check the <identifier_core> of the swhid
    # see https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html
    m = re.match(swhid_regexp, swhid.split(";")[0])
    if m:
        return m.groupdict()


def _is_within_directory(directory, target):
    """Return True if target is directory or a path inside it."""
    directory = path.realpath(directory)
    target = path.realpath(target)
    try:
        return path.commonpath([directory, target]) == directory
    except ValueError:
        return False


def _safe_extract(archive, output_dir):
    """Extract a tarball, refusing members that would write outside output_dir.

    Python 3.12+ uses tarfile's data filter. Older supported interpreters get
    equivalent path checks.
    """
    if sys.version_info >= (3, 12):
        archive.extractall(path=output_dir, filter="data")
        return

    output_dir = path.realpath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    for member in archive.getmembers():
        member_path = path.join(output_dir, member.name)
        if not _is_within_directory(output_dir, member_path):
            raise ContentProviderException(
                f"Refusing to extract {member.name!r}: path escapes the destination directory"
            )
        if member.issym() or member.islnk():
            link_target = member.linkname
            if path.isabs(link_target):
                resolved_link = link_target
            else:
                resolved_link = path.join(path.dirname(member_path), link_target)
            if not _is_within_directory(output_dir, resolved_link):
                raise ContentProviderException(
                    f"Refusing to extract {member.name!r}: link escapes the destination directory"
                )
        if not (member.isfile() or member.isdir() or member.issym() or member.islnk()):
            raise ContentProviderException(
                f"Refusing to extract {member.name!r}: unsupported archive member type"
            )
        archive.extract(member, path=output_dir)


class Swhid(ContentProvider):
    """Provide contents of a repository identified by a SWHID."""

    retry_delay = 5

    def __init__(self):
        self.swhid = None
        self.base_url = "https://archive.softwareheritage.org/api/1"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "user-agent": f"repo2docker {__version__}",
            }
        )

    def set_auth_token(self, token):
        header = {"Authorization": f"Bearer {token}"}
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
        url = f"{self.base_url}/vault/directory/{dir_hash}/"
        yield f"Fetching directory {dir_hash} from {url}\n"
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
        try:
            _safe_extract(archive, output_dir)
        finally:
            archive.close()
        copytree(path.join(output_dir, dir_hash), output_dir)
        shutil.rmtree(path.join(output_dir, dir_hash))
        yield f"Fetched files: {os.listdir(output_dir)}\n"

    def fetch(self, spec, output_dir, yield_output=False):
        swhid = spec["swhid"]
        swhid_obj = spec["swhid_obj"]

        if swhid_obj["type"] == "rev":
            sha1git = swhid_obj["hash"]
            url = f"{self.base_url}/revision/{sha1git}/"
            yield f"Fetching revision {sha1git} from {url}\n"
            resp = self._request(url)
            assert resp.ok, (resp.content, self.session.headers)
            directory = resp.json()["directory"]
            self.swhid = f"swh:1:dir:{directory}"
            yield from self.fetch_directory(directory, output_dir)
        elif swhid_obj["type"] == "dir":
            self.swhid = swhid
            yield from self.fetch_directory(swhid_obj["hash"], output_dir)
