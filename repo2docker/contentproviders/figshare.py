import json
import os
import re
import shutil
from os import makedirs, path
from urllib.error import HTTPError
from urllib.request import Request
from zipfile import is_zipfile

from ..utils import copytree, deep_get
from .doi import DoiProvider


class Figshare(DoiProvider):
    """Provide contents of a Figshare article.

    See https://docs.figshare.com/#public_article for API docs.

    Examples:
      - https://doi.org/10.6084/m9.figshare.9782777
      - https://doi.org/10.6084/m9.figshare.9782777.v2
      - https://figshare.com/articles/binder-examples_requirements/9784088 (only one zipfile, no DOI)
    """

    def __init__(self):
        super().__init__()
        self.hosts = [
            {
                "hostname": [
                    "https://figshare.com/articles/",
                    "http://figshare.com/articles/",
                    "https://figshare.com/account/articles/",
                ],
                "api": "https://api.figshare.com/v2/articles/",
                "filepath": "files",
                "filename": "name",
                "download": "download_url",
            }
        ]

    # We may need to add other item types in future, see
    # https://github.com/jupyterhub/repo2docker/pull/1001#issuecomment-760107436
    # for a list
    url_regex = re.compile(r"(.*)/articles/(code/|dataset/)?([^/]+)/(\d+)(/)?(\d+)?")

    def detect(self, doi, ref=None, extra_args=None):
        """Trigger this provider for things that resolve to a Figshare article"""
        # We need the hostname (url where records are), api url (for metadata),
        # filepath (path to files in metadata), filename (path to filename in
        # metadata), download (path to file download URL), and type (path to item type in metadata)

        url = self.doi2url(doi)

        for host in self.hosts:
            if any([url.startswith(s) for s in host["hostname"]]):
                match = self.url_regex.match(url)
                if match:
                    self.article_id = match.groups()[3]
                    self.article_version = match.groups()[5]
                    if not self.article_version:
                        self.article_version = "1"
                    return {
                        "article": self.article_id,
                        "host": host,
                        "version": self.article_version,
                    }
                else:
                    return None

    def fetch(self, spec, output_dir, yield_output=False):
        """Fetch and unpack a Figshare article"""
        article_id = spec["article"]
        article_version = spec["version"]
        host = spec["host"]

        yield f"Fetching Figshare article {article_id} in version {article_version}.\n"
        resp = self.session.get(
            f'{host["api"]}{article_id}/versions/{article_version}',
            headers={"accept": "application/json"},
        )

        article = resp.json()

        files = deep_get(article, host["filepath"])
        # only fetch files where is_link_only: False
        files = [file for file in files if not file["is_link_only"]]
        only_one_file = len(files) == 1
        for file_ref in files:
            unzip = file_ref["name"].endswith(".zip") and only_one_file
            yield from self.fetch_file(file_ref, host, output_dir, unzip)

    @property
    def content_id(self):
        """The Figshare article ID"""
        return f"{self.article_id}.v{self.article_version}"
