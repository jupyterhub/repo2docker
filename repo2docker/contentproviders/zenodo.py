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
                "is_caltech": False
            },
            {
                "hostname": [
                    "https://zenodo.org/record/",
                    "https://zenodo.org/records/",
                    "http://zenodo.org/record/",
                ],
                "api": "https://zenodo.org/api/records/",
                "files": "links.files",
                "filepath": "entries",
                "filename": "key",
                "download": "links.content",
                "type": "metadata.upload_type",
                "is_caltech": False
            },
            {
                "hostname": [
                    "https://data.caltech.edu/records/",
                    "http://data.caltech.edu/records/",
                ],
                "api": "https://data.caltech.edu/api/records/",
                "files": "links.files",
                "filepath": "entries",
                "filename": "key",
                "download": "links.content",
                "type": "metadata.upload_type",
                "is_caltech": True
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

    def fetch_file(self, file_ref, host, output_dir, unzip=True):
        """Fetch and save a file from Zenodo."""
        filename = deep_get(file_ref, host["filename"])
        if host["is_caltech"]:
            # Construct the direct download URL for Caltech Data
            download_url = f"https://data.caltech.edu/records/{self.record_id}/files/{filename}"
        else:
            # Use the standard Zenodo download URL structure
            download_url = deep_get(file_ref, host["download"])

        # Create output directory
        makedirs(output_dir, exist_ok=True)

        output_path = path.join(output_dir, filename)
        yield f"Downloading {filename} to {output_path}\n"

        # Get file using a streaming approach
        response = self.urlopen(download_url)
        content = response.content  # Get the binary content
        
        # Write the content to file
        with open(output_path, "wb") as fp:
            fp.write(content)

        if unzip and filename.endswith(".zip"):
            yield f"Extracting {filename} to {output_dir}\n"
            shutil.unpack_archive(output_path, output_dir)
            os.remove(output_path)

    @property
    def content_id(self):
        """The Zenodo record ID as the content of a record is immutable"""
        return self.record_id
