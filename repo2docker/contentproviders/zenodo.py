import os
import json
import shutil

from os import makedirs
from os import path
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from zipfile import ZipFile, is_zipfile

from .base import ContentProvider
from ..utils import copytree, deep_get
from ..utils import normalize_doi, is_doi
from .. import __version__


class Zenodo(ContentProvider):
    """Provide contents of a Zenodo deposit."""

    def _urlopen(self, req, headers=None):
        """A urlopen() helper"""
        # someone passed a string, not a request
        if not isinstance(req, Request):
            req = Request(req)

        req.add_header("User-Agent", "repo2docker {}".format(__version__))
        if headers is not None:
            for key, value in headers.items():
                req.add_header(key, value)

        return urlopen(req)

    def _doi2url(self, doi):
        # Transform a DOI to a URL
        # If not a doi, assume we have a URL and return
        if is_doi(doi):
            doi = normalize_doi(doi)

            try:
                resp = self._urlopen("https://doi.org/{}".format(doi))
            # If the DOI doesn't resolve, just return URL
            except HTTPError:
                return doi
            return resp.url
        else:
            # Just return what is actulally just a URL
            return doi

    def detect(self, doi, ref=None, extra_args=None):
        """Trigger this provider for things that resolve to a Zenodo/Invenio record"""
        # We need the hostname (url where records are), api url (for metadata),
        # filepath (path to files in metadata), filename (path to filename in
        # metadata), download (path to file download URL), and type (path to item type in metadata)
        hosts = [
            {
                "hostname": ["https://zenodo.org/record/", "http://zenodo.org/record/"],
                "api": "https://zenodo.org/api/records/",
                "filepath": "files",
                "filename": "filename",
                "download": "links.download",
                "type": "metadata.upload_type",
            },
            {
                "hostname": [
                    "https://data.caltech.edu/records/",
                    "http://data.caltech.edu/records/",
                ],
                "api": "https://data.caltech.edu/api/record/",
                "filepath": "metadata.electronic_location_and_access",
                "filename": "electronic_name.0",
                "download": "uniform_resource_identifier",
                "type": "metadata.resourceType.resourceTypeGeneral",
            },
        ]

        url = self._doi2url(doi)

        for host in hosts:
            if any([url.startswith(s) for s in host["hostname"]]):
                self.record_id = url.rsplit("/", maxsplit=1)[1]
                return {"record": self.record_id, "host": host}

    def fetch(self, spec, output_dir, yield_output=False):
        """Fetch and unpack a Zenodo record"""
        record_id = spec["record"]
        host = spec["host"]

        yield "Fetching Zenodo record {}.\n".format(record_id)
        req = Request(
            "{}{}".format(host["api"], record_id),
            headers={"accept": "application/json"},
        )
        resp = self._urlopen(req)

        record = json.loads(resp.read().decode("utf-8"))

        def _fetch(file_ref, unzip=False):
            # the assumption is that `unzip=True` means that this is the only
            # file related to the zenodo record
            with self._urlopen(deep_get(file_ref, host["download"])) as src:
                fname = deep_get(file_ref, host["filename"])
                if path.dirname(fname):
                    sub_dir = path.join(output_dir, path.dirname(fname))
                    if not path.exists(sub_dir):
                        yield "Creating {}\n".format(sub_dir)
                        makedirs(sub_dir, exist_ok=True)

                dst_fname = path.join(output_dir, fname)
                with open(dst_fname, "wb") as dst:
                    yield "Fetching {}\n".format(fname)
                    shutil.copyfileobj(src, dst)
                # first close the newly written file, then continue
                # processing it
                if unzip and is_zipfile(dst_fname):
                    yield "Extracting {}\n".format(fname)
                    zfile = ZipFile(dst_fname)
                    zfile.extractall(path=output_dir)
                    zfile.close()

                    # delete downloaded file ...
                    os.remove(dst_fname)
                    # ... and any directories we might have created,
                    # in which case sub_dir will be defined
                    if path.dirname(fname):
                        shutil.rmtree(sub_dir)

                    new_subdirs = os.listdir(output_dir)
                    # if there is only one new subdirectory move its contents
                    # to the top level directory
                    if len(new_subdirs) == 1:
                        d = new_subdirs[0]
                        copytree(path.join(output_dir, d), output_dir)
                        shutil.rmtree(path.join(output_dir, d))

        is_software = deep_get(record, host["type"]).lower() == "software"
        files = deep_get(record, host["filepath"])
        only_one_file = len(files) == 1
        for file_ref in files:
            for line in _fetch(file_ref, unzip=is_software and only_one_file):
                yield line

    @property
    def content_id(self):
        """The Zenodo record ID as the content of a record is immutable"""
        return self.record_id
