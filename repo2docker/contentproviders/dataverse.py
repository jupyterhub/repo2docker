import json
import os
import shutil
from urllib.parse import parse_qs, urlparse, urlunparse

from ..utils import copytree, deep_get, is_doi
from .doi import DoiProvider


class Dataverse(DoiProvider):
    """
    Provide contents of a Dataverse dataset.

    This class loads a a list of existing Dataverse installations from the internal
    file dataverse.json. This file is manually updated with the following command:

        python setup.py generate_dataverse_file
    """

    def __init__(self):
        data_file = os.path.join(os.path.dirname(__file__), "dataverse.json")
        with open(data_file) as fp:
            self.hosts = json.load(fp)["installations"]
        super().__init__()

    def detect(self, spec, ref=None, extra_args=None):
        """
        Detect if given spec is hosted on dataverse

        The spec can be:
        - DOI pointing to {siteURL}/dataset.xhtml?persistentId={persistentId}
        - DOI pointing to {siteURL}/file.xhtml?persistentId={persistentId}&...
        - URL {siteURL}/api/access/datafile/{fileId}

        Examples:
        - https://dataverse.harvard.edu/api/access/datafile/3323458
        - doi:10.7910/DVN/6ZXAGT
        - doi:10.7910/DVN/6ZXAGT/3YRRYJ
        """
        if is_doi(spec):
            url = self.doi2url(spec)
        else:
            url = spec
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

        # At this point, we *know* this is a dataverse URL, because:
        # 1. The DOI resolved to a particular host (if using DOI)
        # 2. The host is in the list of known dataverse installations
        #
        # We don't know exactly what kind of dataverse object this is, but
        # that can be figured out during fetch as needed
        return {"host": host, "url": url}

    def get_persistent_id_from_url(self, url: str) -> str:
        """
        Return the persistentId for given dataverse URL.

        Supports the following *dataset* URL styles:
        - /citation: https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/TJCLKP
        - /dataset.xhtml: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/TJCLKP

        Supports the following *file* URL styles:
        - /api/access/datafile: https://dataverse.harvard.edu/api/access/datafile/3323458

        Supports a subset of the following *file* URL styles:
        - /file.xhtml: https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/6ZXAGT/3YRRYJ

        If a URL can not be parsed, throw an exception
        """
        parsed_url = urlparse(url)
        path = parsed_url.path
        qs = parse_qs(parsed_url.query)

        # https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/TJCLKP
        # https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/TJCLKP
        if path.startswith("/citation") or path.startswith("/dataset.xhtml"):
            return qs["persistentId"][0]
        #  https://dataverse.harvard.edu/api/access/datafile/3323458
        elif path.startswith("/api/access/datafile"):
            # What we have here is an entity id, which we can use to get a persistentId
            entity_id = os.path.basename(parsed_url.path)
            # FIXME: Should we be URL Encoding something here to protect from path traversal
            # or similar attacks?
            search_query = f"q=entityId:{entity_id}&type=file"
            search_api_url = urlunparse(
                parsed_url._replace(path="/api/search", query=search_query)
            )
            self.log.debug("Querying Dataverse: " + search_api_url)
            data = self.urlopen(search_api_url).json()["data"]
            if data["count_in_response"] != 1:
                raise ValueError(
                    f"Dataverse search query failed!\n - url: {url}\n - resp: {json.dumps(data)}\n"
                )
            return data["items"][0]["dataset_persistent_id"]
        elif parsed_url.path.startswith("/file.xhtml"):
            file_persistent_id = qs['persistentId'][0]
            dataset_persistent_id = file_persistent_id.rsplit("/", 1)[0]
            if file_persistent_id == dataset_persistent_id:
                # We can't figure this one out, throw an error
                raise ValueError(f"Could not find dataset id for {url}")
            return dataset_persistent_id

        raise ValueError(f"Could not determine persistent id for dataverse URL {url}")

    def fetch(self, spec, output_dir, yield_output=False):
        """Fetch and unpack a Dataverse dataset."""
        url = spec["url"]
        host = spec["host"]

        persistent_id = self.get_persistent_id_from_url(url)

        yield f"Fetching Dataverse record {persistent_id}.\n"
        url = f'{host["url"]}/api/datasets/:persistentId?persistentId={persistent_id}'

        resp = self.urlopen(url, headers={"accept": "application/json"})
        print(resp.json())
        record = resp.json()["data"]

        for fobj in deep_get(record, "latestVersion.files"):
            file_url = (
                # without format=original you get the preservation format (plain text, tab separated)
                f'{host["url"]}/api/access/datafile/{deep_get(fobj, "dataFile.id")}?format=original'
            )
            filename = fobj["label"]
            original_filename = fobj["dataFile"].get("originalFileName", None)
            if original_filename:
                # replace preservation format filename (foo.tab) with original filename (foo.dta)
                filename = original_filename

            filename_with_path = os.path.join(fobj.get("directoryLabel", ""), filename)

            file_ref = {"download": file_url, "filename": filename_with_path}
            fetch_map = {key: key for key in file_ref.keys()}

            yield from self.fetch_file(file_ref, fetch_map, output_dir)

        new_subdirs = os.listdir(output_dir)
        # if there is only one new subdirectory move its contents
        # to the top level directory
        if len(new_subdirs) == 1 and os.path.isdir(new_subdirs[0]):
            d = new_subdirs[0]
            copytree(os.path.join(output_dir, d), output_dir)
            shutil.rmtree(os.path.join(output_dir, d))


        # Save persistent id
        self.persitent_id = persistent_id

    @property
    def content_id(self):
        """The Dataverse persistent identifier."""
        return self.persistent_id
