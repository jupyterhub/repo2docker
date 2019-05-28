import os
import json
import shutil

from os import makedirs
from os import path
from urllib.request import urlopen, Request
from zipfile import ZipFile, is_zipfile

from .base import ContentProvider
from ..utils import copytree


class Zenodo(ContentProvider):
    """Provide contents of a Zenodo deposit."""

    def detect(self, doi, ref=None, extra_args=None):
        doi = doi.lower()
        # 10.5281 is the Zenodo DOI prefix
        if doi.startswith("10.5281/"):
            resp = urlopen("https://doi.org/{}".format(doi))
            self.record_id = resp.url.rsplit("/", maxsplit=1)[1]
            return {"record": self.record_id}

        elif doi.startswith("https://doi.org/10.5281/") or doi.startswith(
            "http://doi.org/10.5281/"
        ):
            resp = urlopen(doi)
            self.record_id = resp.url.rsplit("/", maxsplit=1)[1]
            return {"record": self.record_id}

        elif doi.startswith("https://zenodo.org/record/") or doi.startswith(
            "http://zenodo.org/record/"
        ):
            self.record_id = doi.rsplit("/", maxsplit=1)[1]
            return {"record": self.record_id}

    def fetch(self, spec, output_dir, yield_output=False):
        record_id = spec["record"]

        yield "Fetching Zenodo record {}.\n".format(record_id)
        req = Request(
            "https://zenodo.org/api/records/{}".format(record_id),
            headers={"accept": "application/json"},
        )
        resp = urlopen(req)

        record = json.loads(resp.read().decode("utf-8"))

        def _fetch(file_ref, unzip=False):
            # the assumption is that `unzip=True` means that this is the only
            # file related to the zenodo record
            with urlopen(file_ref["links"]["download"]) as src:
                fname = file_ref["filename"]
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

        is_software = record["metadata"]["upload_type"] == "software"
        only_one_file = len(record["files"]) == 1
        for file_ref in record["files"]:
            for line in _fetch(file_ref, unzip=is_software and only_one_file):
                yield line

    @property
    def content_id(self):
        """A unique ID to represent the version of the content.
        Uses the first seven characters of the git commit ID of the repository.
        """
        return self.record_id
