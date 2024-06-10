from datetime import datetime, timedelta, timezone
from os import path
from urllib.parse import parse_qs, urlparse, urlencode

from requests import Session

from .. import __version__
from .base import ContentProvider


class CKAN(ContentProvider):
    """Provide contents of a remote CKAN dataset."""

    def __init__(self):
        super().__init__()
        self.session = Session()
        self.session.headers.update(
            {
                "user-agent": f"repo2docker {__version__}",
            }
        )

    def _fetch_version(self, api_url):
        """Fetch dataset modified date and convert to epoch.
        Borrowed from the Hydroshare provider.
        """
        package_show_url = f"{api_url}package_show?id={self.dataset_id}"
        resp = self.urlopen(package_show_url).json()
        date = resp["result"]["metadata_modified"]
        parsed_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
        epoch = parsed_date.replace(tzinfo=timezone(timedelta(0))).timestamp()
        # truncate the timestamp
        return str(int(epoch))

    def _request(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    urlopen = _request

    def detect(self, source, ref=None, extra_args=None):
        """Trigger this provider for things that resolve to a CKAN dataset."""
        parsed_url = urlparse(source)
        if not parsed_url.netloc:
            return None

        url_parts_1 = parsed_url.path.split("/history/")
        url_parts_2 = url_parts_1[0].split("/")
        if url_parts_2[-2] == "dataset":
            self.dataset_id = url_parts_2[-1]
        else:
            return None

        api_url_path = "/api/3/action/"
        api_url = parsed_url._replace(
            path="/".join(url_parts_2[:-2]) + api_url_path, query=""
        ).geturl()

        status_show_url = f"{api_url}status_show"
        resp = self.urlopen(status_show_url)
        if resp.status_code == 200:

            # handle the activites
            activity_id = None
            if parse_qs(parsed_url.query).get("activity_id") is not None:
                activity_id = parse_qs(parsed_url.query).get("activity_id")[0]
            if len(url_parts_1) == 2:
                activity_id = url_parts_1[-1]

            self.version = self._fetch_version(api_url)
            return {
                "dataset_id": self.dataset_id,
                "activity_id": activity_id,
                "api_url": api_url,
                "version": self.version,
            }
        else:
            return None

    def fetch(self, spec, output_dir, yield_output=False):
        """Fetch a CKAN dataset."""
        dataset_id = spec["dataset_id"]
        activity_id = spec["activity_id"]

        yield f"Fetching CKAN dataset {dataset_id}.\n"

        # handle the activites
        if activity_id:
            fetch_url = (
                f"{spec['api_url']}activity_data_show?" + urlencode({"id": activity_id, "object_type": "package"})
            )
        else:
            fetch_url = f"{spec['api_url']}package_show?" + urlencode({"id": dataset_id})

        resp = self.urlopen(
            fetch_url,
            headers={"accept": "application/json"},
        )

        dataset = resp.json()

        yield "Fetching CKAN resources.\n"

        resources = dataset["result"]["resources"]

        for resource in resources:
            file_url = resource["url"]
            if file_url == "":
                continue
            fname = file_url.rsplit("/", maxsplit=1)[-1]
            if fname == "":
                fname = resource["id"]

            yield f"Requesting {file_url}\n"
            resp = self._request(file_url, stream=True)
            resp.raise_for_status()

            dst_fname = path.join(output_dir, fname)
            with open(dst_fname, "wb") as dst:
                yield f"Fetching {fname}\n"
                for chunk in resp.iter_content(chunk_size=None):
                    dst.write(chunk)

    @property
    def content_id(self):
        """A unique ID to represent the version of the content."""
        return f"{self.dataset_id}.v{self.version}"
