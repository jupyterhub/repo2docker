import hashlib
import json
import os
import shutil
from typing import List, Tuple
from urllib.parse import parse_qs, urlparse

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

        # Used only for content_id
        self.url = url

        # At this point, we *know* this is a dataverse URL, because:
        # 1. The DOI resolved to a particular host (if using DOI)
        # 2. The host is in the list of known dataverse installations
        #
        # We don't know exactly what kind of dataverse object this is, but
        # that can be figured out during fetch as needed
        return url

    def get_dataset_id_from_file_id(self, base_url: str, file_id: str) -> str:
        """
        Return the persistent_id (DOI) that a given file_id (int or doi) belongs to
        """
        if file_id.isdigit():
            # the file_id is an integer, rather than a persistent id (DOI)
            api_url = f"{base_url}/api/files/{file_id}?returnDatasetVersion=true"
        else:
            # the file_id is a doi itself
            api_url = f"{base_url}/api/files/:persistentId?persistentId={file_id}&returnDatasetVersion=true"

        resp = self._request(api_url)
        if resp.status_code == 404:
            raise ValueError(f"File with id {file_id} not found in {base_url}")

        resp.raise_for_status()

        data = resp.json()["data"]
        return data["datasetVersion"]["datasetPersistentId"]

    def parse_dataverse_url(self, url: str) -> Tuple[str, bool]:
        """
        Parse the persistent id out of a dataverse URL

        persistent_id can point to either a dataset or a file. The second return
        value is False if we know that the persistent id is a file or a dataset,
        and True if it is ambiguous.

        Raises a ValueError if we can not parse the url
        """
        parsed_url = urlparse(url)
        path = parsed_url.path
        qs = parse_qs(parsed_url.query)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        is_ambiguous = False
        # https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/TJCLKP
        if path.startswith("/citation"):
            is_ambiguous = True
            persistent_id = qs["persistentId"][0]
        # https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/TJCLKP
        elif path.startswith("/dataset.xhtml"):
            #  https://dataverse.harvard.edu/api/access/datafile/3323458
            persistent_id = qs["persistentId"][0]
        elif path.startswith("/api/access/datafile"):
            # What we have here is an entity id, which we can use to get a persistentId
            file_id = os.path.basename(path)
            persistent_id = self.get_dataset_id_from_file_id(base_url, file_id)
        elif parsed_url.path.startswith("/file.xhtml"):
            file_persistent_id = qs["persistentId"][0]
            persistent_id = self.get_dataset_id_from_file_id(
                base_url, file_persistent_id
            )
        else:
            raise ValueError(
                f"Could not determine persistent id for dataverse URL {url}"
            )

        return persistent_id, is_ambiguous

    def get_datafiles(self, url: str) -> List[dict]:
        """
        Return a list of dataFiles for given persistent_id

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
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        persistent_id, is_ambiguous = self.parse_dataverse_url(url)

        dataset_api_url = (
            f"{base_url}/api/datasets/:persistentId?persistentId={persistent_id}"
        )
        resp = self._request(dataset_api_url, headers={"accept": "application/json"})
        if resp.status_code == 404 and is_ambiguous:
            # It's possible this is a *file* persistent_id, not a dataset one
            persistent_id = self.get_dataset_id_from_file_id(base_url, persistent_id)
            dataset_api_url = (
                f"{base_url}/api/datasets/:persistentId?persistentId={persistent_id}"
            )
            resp = self._request(
                dataset_api_url, headers={"accept": "application/json"}
            )

            if resp.status_code == 404:
                # This persistent id is just not here
                raise ValueError(f"{persistent_id} on {base_url} is not found")

        # We already handled 404, raise error for everything else
        resp.raise_for_status()

        data = resp.json()["data"]

        return data["latestVersion"]["files"]

    def fetch(self, spec, output_dir, yield_output=False):
        """Fetch and unpack a Dataverse dataset."""
        url = spec
        parsed_url = urlparse(url)
        # FIXME: Support determining API URL better
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        yield f"Fetching Dataverse record {url}.\n"

        for fobj in self.get_datafiles(url):
            file_url = (
                # without format=original you get the preservation format (plain text, tab separated)
                f'{base_url}/api/access/datafile/{deep_get(fobj, "dataFile.id")}?format=original'
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

    @property
    def content_id(self):
        """The Dataverse persistent identifier."""
        return hashlib.sha256(self.url.encode()).hexdigest()
