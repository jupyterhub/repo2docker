import json
import os
import shutil
import time
import zipfile
from datetime import datetime, timedelta, timezone
from urllib.request import urlretrieve

from .base import ContentProviderException
from .doi import DoiProvider


class Hydroshare(DoiProvider):
    """Provide contents of a Hydroshare resource."""

    def _fetch_version(self, host):
        """Fetch resource modified date and convert to epoch"""
        json_response = self.session.get(host["version"].format(self.resource_id)).json()
        date = next(
            item for item in json_response["dates"] if item["type"] == "modified"
        )["start_date"]
        # Hydroshare timestamp always returns the same timezone, so strip it
        date = date.split(".")[0]
        parsed_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        epoch = parsed_date.replace(tzinfo=timezone(timedelta(0))).timestamp()
        # truncate the timestamp
        return str(int(epoch))

    def detect(self, doi, ref=None, extra_args=None):
        """Trigger this provider for things that resolve to a Hydroshare resource"""
        hosts = [
            {
                "hostname": [
                    "https://www.hydroshare.org/resource/",
                    "http://www.hydroshare.org/resource/",
                ],
                "django_irods": "https://www.hydroshare.org/django_irods/download/bags/",
                "version": "https://www.hydroshare.org/hsapi/resource/{}/scimeta/elements",
            }
        ]
        url = self.doi2url(doi)

        for host in hosts:
            if any([url.startswith(s) for s in host["hostname"]]):
                self.resource_id = url.strip("/").rsplit("/", maxsplit=1)[1]
                self.version = self._fetch_version(host)
                return {
                    "resource": self.resource_id,
                    "host": host,
                    "version": self.version,
                }

    def _urlretrieve(self, bag_url):
        return urlretrieve(bag_url)

    def fetch(self, spec, output_dir, yield_output=False, timeout=120):
        """Fetch and unpack a Hydroshare resource"""
        resource_id = spec["resource"]
        host = spec["host"]

        bag_url = f'{host["django_irods"]}{resource_id}'

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
        filehandle, _ = self._urlretrieve(bag_url)
        zip_file_object = zipfile.ZipFile(filehandle, "r")
        yield "Downloaded, unpacking contents.\n"
        zip_file_object.extractall("temp")
        # resources store the contents in the data/contents directory, which is all we want to keep
        contents_dir = os.path.join("temp", self.resource_id, "data", "contents")
        files = os.listdir(contents_dir)
        for f in files:
            shutil.move(os.path.join(contents_dir, f), output_dir)
        yield "Finished, cleaning up.\n"
        shutil.rmtree("temp")

    @property
    def content_id(self):
        """The HydroShare resource ID"""
        return f"{self.resource_id}.v{self.version}"
