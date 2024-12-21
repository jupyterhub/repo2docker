import json
import logging
import os
import shutil
from os import makedirs, path
from zipfile import ZipFile, is_zipfile

from requests import HTTPError, Session

from .. import __version__
from ..utils import copytree, deep_get, is_doi, normalize_doi
from .base import ContentProvider


class DoiProvider(ContentProvider):
    """Provide contents of a repository identified by a DOI and some helper functions."""

    def __init__(self):
        super().__init__()
        self.session = Session()
        self.session.headers.update(
            {
                "user-agent": f"repo2docker {__version__}",
            }
        )

    def _request(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def doi2url(self, doi):
        # Transform a DOI to a URL
        # If not a doi, assume we have a URL and return
        if is_doi(doi):
            normalized_doi = normalize_doi(doi)

            # Use the doi.org resolver API
            # documented at https://www.doi.org/the-identifier/resources/factsheets/doi-resolution-documentation#5-proxy-server-rest-api
            req_url = f"https://doi.org/api/handles/{normalized_doi}"
            resp = self._request(req_url)
            if resp.status_code == 404:
                # Not a doi, return what we were passed in
                return doi
            elif resp.status_code == 200:
                data = resp.json()
                # Pick the first URL we find from the doi response
                for v in data["values"]:
                    if v["type"] == "URL":
                        return v["data"]["value"]

                # No URLs found for this doi, what do we do?
                self.log.error("DOI {normalized_doi} doesn't point to any URLs")
                return doi
            else:
                # If we get any other status codes, raise error
                raise
        else:
            # Just return what is actulally just a URL
            return doi

    def fetch_file(self, file_ref, host, output_dir, unzip=False):
        # the assumption is that `unzip=True` means that this is the only
        # file related to a record
        file_url = deep_get(file_ref, host["download"])
        fname = deep_get(file_ref, host["filename"])
        self.log.debug(f"Downloading file {file_url} as {fname}\n")

        yield f"Requesting {file_url}\n"
        resp = self._request(file_url, stream=True)
        resp.raise_for_status()

        if path.dirname(fname):
            sub_dir = path.join(output_dir, path.dirname(fname))
            if not path.exists(sub_dir):
                yield f"Creating {sub_dir}\n"
                makedirs(sub_dir, exist_ok=True)

        dst_fname = path.join(output_dir, fname)
        with open(dst_fname, "wb") as dst:
            yield f"Fetching {fname}\n"
            for chunk in resp.iter_content(chunk_size=None):
                dst.write(chunk)

        if unzip and is_zipfile(dst_fname):
            yield f"Extracting {fname}\n"
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

            yield f"Fetched files: {os.listdir(output_dir)}\n"
