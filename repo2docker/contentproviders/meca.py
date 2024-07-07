from .base import ContentProvider
from requests import Session
import os
from hashlib import md5
from os import path
import tempfile
import shutil
import xml.etree.ElementTree as ET
from zipfile import ZipFile, is_zipfile
from urllib.parse import urlparse, urlunparse

def get_hashed_slug(url, changes_with_content):
    """Return a unique slug that is invariant to query parameters in the url"""
    parsed_url = urlparse(url)
    stripped_url = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "", "")
    )

    return "meca-" + md5(f"{stripped_url}-{changes_with_content}".encode()).hexdigest()

def fetch_zipfile(session, url, dst_dir):
    resp = session.get(url, headers={"accept": "application/zip"}, stream=True)
    resp.raise_for_status()

    dst_filename = path.join(dst_dir, "meca.zip")
    with open(dst_filename, "wb") as dst:
        for chunk in resp.iter_content(chunk_size=128):
            dst.write(chunk)

    return dst_filename


def handle_items(_, item):
    print(item)


def extract_validate_and_identify_bundle(zip_filename, dst_dir):
    if not os.path.exists(zip_filename):
        raise RuntimeError("Download MECA bundle not found")

    if not is_zipfile(zip_filename):
        raise RuntimeError("MECA bundle is not a zip file")

    with ZipFile(zip_filename, "r") as zip_ref:
        zip_ref.extractall(dst_dir)

    try:
        manifest = path.join(dst_dir, "manifest.xml")
        if not os.path.exists(manifest):
            raise RuntimeError("MECA bundle is missing manifest.xml")
        article_source_dir = "bundle/"

        tree = ET.parse(manifest)
        root = tree.getroot()

        bundle_instance = root.findall(
            "{*}item[@item-type='article-source-directory']/{*}instance"
        )
        for attr in bundle_instance[0].attrib:
            if attr.endswith("href"):
                article_source_dir = bundle_instance[0].get(attr)

        return True, path.join(dst_dir, article_source_dir)
    except:
        return False, dst_dir


class Meca(ContentProvider):
    """A repo2docker content provider for MECA bundles"""

    def __init__(self):
        super().__init__()
        self.session = Session()
        self.session.headers.update(
            {
                "user-agent": f"repo2docker MECA",
            }
        )

    def detect(self, spec, ref=None, extra_args=None):
        """`spec` contains a faux protocol of meca+http[s] for detection purposes
        and we assume `spec` trusted as a reachable MECA bundle from an allowed origin
        (binderhub RepoProvider class already checking for this).

        An other HEAD check in made here in order to get the content-length header
        """
        parsed = urlparse(spec)
        if not parsed.scheme.endswith("+meca"):
            return None
        parsed = parsed._replace(scheme=parsed.scheme[:-5])
        url = urlunparse(parsed)

        r = self.session.head(url)
        changes_with_content = r.headers.get("ETag") or r.headers.get("Content-Length")

        self.hashed_slug = get_hashed_slug(url, changes_with_content)

        return {"url": url, "slug": self.hashed_slug}

    def fetch(self, spec, output_dir, yield_output=False):
        hashed_slug = spec["slug"]
        url = spec["url"]

        yield f"Creating temporary directory.\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            yield f"Temporary directory created at {tmpdir}.\n"

            yield f"Fetching MECA Bundle {url}.\n"
            zip_filename = fetch_zipfile(self.session, url, tmpdir)

            yield f"Extracting MECA Bundle {zip_filename}.\n"
            is_meca, bundle_dir = extract_validate_and_identify_bundle(
                zip_filename, tmpdir
            )

            if not is_meca:
                yield f"This doesn't look like a meca bundle, extracting everything.\n"

            yield f"Copying MECA Bundle at {bundle_dir} to {output_dir}.\n"
            files = os.listdir(bundle_dir)
            for f in files:
                shutil.move(os.path.join(bundle_dir, f), output_dir)

            yield f"Removing temporary directory.\n"

        yield f"MECA Bundle {hashed_slug} fetched and unpacked.\n"

    @property
    def content_id(self):
        return self.hashed_slug
