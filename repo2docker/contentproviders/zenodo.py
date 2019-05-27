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
        # 10.5281 is the Zenodo DOI prefix
        if doi.startswith('10.5281'):
            resp = urlopen("https://doi.org/{}".format(doi))
            self.record_id = resp.url.rsplit("/", maxsplit=1)[1]
            return {'record': self.record_id}

    def fetch(self, spec, output_dir, yield_output=False):
        record_id = spec['record']

        yield "Fetching Zenodo record {}.\n".format(record_id)
        req = Request("https://zenodo.org/api/records/{}".format(record_id),
                      headers={"accept": "application/json"})
        resp = urlopen(req)

        record = json.loads(resp.read().decode("utf-8"))

        def _fetch(file_ref, unzip=False):
            with urlopen(file_ref["links"]["download"]) as src:
                fname = file_ref["filename"]
                sub_dir = path.join(output_dir, path.dirname(fname))
                if not path.exists(sub_dir):
                    print("Creating", sub_dir)
                    makedirs(sub_dir, exist_ok=True)

                dst_fname = path.join(output_dir, fname)
                with open(dst_fname, "wb") as dst:
                    yield "Fetching {}\n".format(fname)
                    shutil.copyfileobj(src, dst)

                # first close the newly written file, then continue
                # processing it
                if unzip and is_zipfile(dst_fname):
                    zfile = ZipFile(dst_fname)
                    zfile.extractall(path=output_dir)
                    zfile.close()
                    import os
                    d = os.listdir(output_dir)[0]
                    print(output_dir)
                    print(os.listdir(output_dir))
                    copytree(path.join(output_dir, d), output_dir)
                    shutil.rmtree(sub_dir)
                    shutil.rmtree(path.join(output_dir, d))

        is_software = record["metadata"]["upload_type"] == "software"
        only_one_file = len(record["files"]) == 1
        for file_ref in record['files']:
            for line in _fetch(file_ref, unzip=is_software and only_one_file):
                yield line

        import pdb; pdb.set_trace()

    @property
    def content_id(self):
        """A unique ID to represent the version of the content.
        Uses the first seven characters of the git commit ID of the repository.
        """
        return self.record_id
