import json
import os
import shutil
from os import makedirs, path
from urllib.error import HTTPError
from urllib.request import Request

from ..utils import copytree, deep_get
from .doi import DoiProvider


class Zenodo(DoiProvider):
    """Provide contents of a Zenodo deposit."""

    def __init__(self):
        super().__init__()
        # We need the hostname (url where records are), api url (for metadata),
        # filepath (path to files in metadata), filename (path to filename in
        # metadata), download (path to file download URL), and type (path to item type in metadata)
        self.hosts = [
            {
                "hostname": [
                    "https://sandbox.zenodo.org/record/",
                    "http://sandbox.zenodo.org/record/",
                    "http://sandbox.zenodo.org/records/",
                ],
                "api": "https://sandbox.zenodo.org/api/records/",
                "files": "links.files",
                "filepath": "entries",
                "filename": "key",
                "download": "links.content",
                "type": "metadata.upload_type",
            },
            {
                "hostname": [
                    "https://zenodo.org/record/",
                    "http://zenodo.org/record/",
                    "https://zenodo.org/records/",
                ],
                "api": "https://zenodo.org/api/records/",
                "files": "links.files",
                "filepath": "entries",
                "filename": "key",
                "download": "links.content",
                "type": "metadata.upload_type",
            },
            {
                "hostname": [
                    "https://data.caltech.edu/records/",
                    "http://data.caltech.edu/records/",
                ],
                "api": "https://data.caltech.edu/api/record/",
                "files": "",
                "filepath": "metadata.electronic_location_and_access",
                "filename": "electronic_name.0",
                "download": "uniform_resource_identifier",
                "type": "metadata.resourceType.resourceTypeGeneral",
            },
        ]

    def detect(self, doi, ref=None, extra_args=None):
        """Trigger this provider for things that resolve to a Zenodo/Invenio record"""
        url = self.doi2url(doi)

        for host in self.hosts:
            if any([url.startswith(s) for s in host["hostname"]]):
                self.record_id = url.rsplit("/", maxsplit=1)[1]
                return {"record": self.record_id, "host": host}

    def fetch(self, spec, output_dir, yield_output=False):
        """Fetch and unpack a Zenodo record"""
        record_id = spec["record"]
        host = spec["host"]

        yield f"Fetching Zenodo record {record_id}.\n"
        resp = self.urlopen(
            f'{host["api"]}{record_id}',
            headers={"accept": "application/json"},
        )
        record = resp.json()

        if host["files"]:
            yield f"Fetching Zenodo record {record_id} files.\n"
            files_url = deep_get(record, host["files"])
            resp = self.urlopen(
                files_url,
                headers={"accept": "application/json"},
            )
            record = resp.json()

        files = deep_get(record, host["filepath"])
        only_one_file = len(files) == 1
        for file_ref in files:
            yield from self.fetch_file(file_ref, host, output_dir, unzip=only_one_file)

    @property
    def content_id(self):
        """The Zenodo record ID as the content of a record is immutable"""
        return self.record_id
