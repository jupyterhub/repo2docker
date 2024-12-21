import json
import os
import shutil
import tempfile
import time
import zipfile
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, urlunparse
from urllib.request import urlretrieve

from ..utils import is_doi
from .base import ContentProviderException
from .doi import DoiProvider


class Hydroshare(DoiProvider):
    """Provide contents of a Hydroshare resource."""

    HYDROSHARE_DOMAINS = ["www.hydroshare.org"]

    def get_version(self, resource_id: str) -> str:
        """
        Get current version of given resource_id
        """
        api_url = f"https://{self.HYDROSHARE_DOMAIN}/hsapi/resource/{resource_id}/scimeta/elements"

        json_response = self.session.get(api_url).json()
        date = next(
            item for item in json_response["dates"] if item["type"] == "modified"
        )["start_date"]
        # Hydroshare timestamp always returns the same timezone, so strip it
        date = date.split(".")[0]
        parsed_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        epoch = parsed_date.replace(tzinfo=timezone(timedelta(0))).timestamp()
        # truncate the timestamp
        return str(int(epoch))

    def detect(self, spec, ref=None, extra_args=None):
        """Trigger this provider for things that resolve to a Hydroshare resource"""
        hosts = [
            {
                "hostname": [
                    "https://www.hydroshare.org/resource/",
                    "http://www.hydroshare.org/resource/",
                ],
                "django_irods": "https://www.hydroshare.org/django_irods/download/bags/",
                "version": "",
            }
        ]

        # Our spec could be a doi that resolves to a hydroshare URL, or a hydroshare URL
        if is_doi(spec):
            url = self.doi2url(spec)
        else:
            url = spec

        parsed = urlparse(url)

        print(url)
        if parsed.netloc in self.HYDROSHARE_DOMAINS:
            return url

    def fetch(self, spec, output_dir, yield_output=False, timeout=120):
        """Fetch and unpack a Hydroshare resource"""
        url = spec
        parts = urlparse(url)
        self.resource_id = parts.path.strip("/").rsplit("/", maxsplit=1)[1]

        bag_url = urlunparse(
            parts._replace(path=f"django_irods/download/bags/{self.resource_id}")
        )

        yield f"Downloading {bag_url}.\n"

        # bag downloads are prepared on demand and may need some time
        conn = self.session.get(bag_url)
        total_wait_time = 0
        while (
            conn.status_code == 200
            and conn.headers["content-type"] != "application/zip"
        ):
            wait_time = 10
            total_wait_time += wait_time
            if total_wait_time > timeout:
                msg = "Bag taking too long to prepare, exiting now, try again later."
                yield msg
                raise ContentProviderException(msg)
            yield f"Bag is being prepared, requesting again in {wait_time} seconds.\n"
            time.sleep(wait_time)
            conn = self.session.get(bag_url)
        if conn.status_code != 200:
            msg = f"Failed to download bag. status code {conn.status_code}.\n"
            yield msg
            raise ContentProviderException(msg)
        # Bag creation seems to need a small time buffer after it says it's ready.
        time.sleep(1)
        filehandle, _ = urlretrieve(bag_url)
        zip_file_object = zipfile.ZipFile(filehandle, "r")
        yield "Downloaded, unpacking contents.\n"

        with tempfile.TemporaryDirectory() as d:
            zip_file_object.extractall(d)
            # resources store the contents in the data/contents directory, which is all we want to keep
            contents_dir = os.path.join(d, self.resource_id, "data", "contents")
            files = os.listdir(contents_dir)
            for f in files:
                shutil.move(os.path.join(contents_dir, f), output_dir)
            yield "Finished, cleaning up.\n"

    @property
    def content_id(self):
        """The HydroShare resource ID"""
        return f"{self.resource_id}"
