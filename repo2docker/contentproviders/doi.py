import os
import json
import shutil
import logging

from os import makedirs
from os import path
from urllib import request  # urlopen, Request
from urllib.error import HTTPError
from zipfile import ZipFile, is_zipfile

from .base import ContentProvider
from ..utils import copytree, deep_get
from ..utils import normalize_doi, is_doi
from .. import __version__


class DoiProvider(ContentProvider):
    """Provide contents of a repository identified by a DOI and some helper functions."""

    def urlopen(self, req, headers=None):
        """A urlopen() helper"""
        # someone passed a string, not a request
        if not isinstance(req, request.Request):
            req = request.Request(req)

        req.add_header("User-Agent", "repo2docker {}".format(__version__))
        if headers is not None:
            for key, value in headers.items():
                req.add_header(key, value)

        return request.urlopen(req)

    def doi2url(self, doi):
        # Transform a DOI to a URL
        # If not a doi, assume we have a URL and return
        if is_doi(doi):
            doi = normalize_doi(doi)

            try:
                resp = self.urlopen("https://doi.org/{}".format(doi))
            # If the DOI doesn't resolve, just return URL
            except HTTPError:
                return doi
            return resp.url
        else:
            # Just return what is actulally just a URL
            return doi

    def fetch_file(self, file_ref, host, output_dir, unzip=False):
        # the assumption is that `unzip=True` means that this is the only
        # file related to a record
        file_url = deep_get(file_ref, host["download"])
        fname = deep_get(file_ref, host["filename"])
        logging.debug("Downloading file {} as {}\n".format(file_url, fname))
        with self.urlopen(file_url) as src:
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

                yield "Fetched files: {}\n".format(os.listdir(output_dir))
