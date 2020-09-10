import os
import json
import shutil

from urllib.request import Request
from urllib.parse import urlparse, urlunparse, parse_qs

from .doi import DoiProvider
from ..utils import copytree, deep_get


class Dataverse(DoiProvider):
    """
    Provide contents of a Dataverse dataset.

    This class loads a a list of existing Dataverse installations from the internal
    file dataverse.json. This file is manually updated with the following command:

        python setup.py generate_dataverse_file
    """

    def __init__(self):
        data_file = os.path.join(os.path.dirname(__file__), "dataverse.json")
        with open(data_file, "r") as fp:
            self.hosts = json.load(fp)["installations"]
        super().__init__()

    def detect(self, doi, ref=None, extra_args=None):
        """Trigger this provider for things that resolve to a Dataverse dataset.

        Handles:
        - DOI pointing to {siteURL}/dataset.xhtml?persistentId={persistentId}
        - DOI pointing to {siteURL}/file.xhtml?persistentId={persistentId}&...
        - URL {siteURL}/api/access/datafile/{fileId}

        Examples:
        - https://dataverse.harvard.edu/api/access/datafile/3323458
        - doi:10.7910/DVN/6ZXAGT
        - doi:10.7910/DVN/6ZXAGT/3YRRYJ

        """
        url = self.doi2url(doi)
        # Parse the url, to get the base for later API calls
        parsed_url = urlparse(url)

        # Check if the url matches any known Dataverse installation, bail if not.
        host = next(
            (
                host
                for host in self.hosts
                if urlparse(host["url"]).netloc == parsed_url.netloc
            ),
            None,
        )
        if host is None:
            return

        query_args = parse_qs(parsed_url.query)

        # Corner case handling
        if parsed_url.path.startswith("/file.xhtml"):
            # There's no way of getting file information using its persistentId, the only thing we can do is assume that doi
            # is structured as "doi:<dataset_doi>/<file_doi>" and try to handle dataset that way.
            new_doi = doi.rsplit("/", 1)[0]
            if new_doi == doi:
                # tough luck :( Avoid inifite recursion and exit.
                return
            return self.detect(new_doi)
        elif parsed_url.path.startswith("/api/access/datafile"):
            # Raw url pointing to a datafile is a typical output from an External Tool integration
            entity_id = os.path.basename(parsed_url.path)
            search_query = "q=entityId:" + entity_id + "&type=file"
            # Knowing the file identifier query search api to get parent dataset
            search_url = urlunparse(
                parsed_url._replace(path="/api/search", query=search_query)
            )
            self.log.debug("Querying Dataverse: " + search_url)
            resp = self.urlopen(search_url).read()
            data = json.loads(resp.decode("utf-8"))["data"]
            if data["count_in_response"] != 1:
                self.log.debug(
                    "Dataverse search query failed!\n - doi: {}\n - url: {}\n - resp: {}\n".format(
                        doi, url, json.dump(data)
                    )
                )
                return

            self.record_id = deep_get(data, "items.0.dataset_persistent_id")
        elif (
            parsed_url.path.startswith("/dataset.xhtml")
            and "persistentId" in query_args
        ):
            self.record_id = deep_get(query_args, "persistentId.0")

        if hasattr(self, "record_id"):
            return {"record": self.record_id, "host": host}

    def fetch(self, spec, output_dir, yield_output=False):
        """Fetch and unpack a Dataverse dataset."""
        record_id = spec["record"]
        host = spec["host"]

        yield "Fetching Dataverse record {}.\n".format(record_id)
        req = Request(
            "{}/api/datasets/:persistentId?persistentId={}".format(
                host["url"], record_id
            ),
            headers={"accept": "application/json"},
        )
        resp = self.urlopen(req)
        record = json.loads(resp.read().decode("utf-8"))["data"]

        for fobj in deep_get(record, "latestVersion.files"):
            file_url = "{}/api/access/datafile/{}".format(
                host["url"], deep_get(fobj, "dataFile.id")
            )
            filename = os.path.join(fobj.get("directoryLabel", ""), fobj["label"])

            file_ref = {"download": file_url, "filename": filename}
            fetch_map = {key: key for key in file_ref.keys()}

            for line in self.fetch_file(file_ref, fetch_map, output_dir):
                yield line

        new_subdirs = os.listdir(output_dir)
        # if there is only one new subdirectory move its contents
        # to the top level directory
        if len(new_subdirs) == 1 and os.path.isdir(new_subdirs[0]):
            d = new_subdirs[0]
            copytree(os.path.join(output_dir, d), output_dir)
            shutil.rmtree(os.path.join(output_dir, d))

    @property
    def content_id(self):
        """The Dataverse persistent identifier."""
        return self.record_id
