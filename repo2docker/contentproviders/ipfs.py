from tarfile import TarFile
from io import BytesIO

import requests
from cid import is_cid

from .base import ContentProvider, ContentProviderException


class IPFS(ContentProvider):
    """Provide contents of an IPFS CID."""

    def __init__(self):
        super().__init__()
        self.gateways = [
            "http://127.0.0.1:8080",
            "https://ipfs.io",
            "https://dweb.link",
            "https://gateway.pinata.cloud",
            "https://cloudflare-ipfs.com",
            "https://ipfs.fleek.co",
        ]

    def detect(self, cid, ref=None, extra_args=None):
        if is_cid(cid):
            return {"cid": cid}

    def fetch(self, spec, output_dir, yield_output=False):
        """Fetch and unpack directory tree behind a CID"""
        cid = spec["cid"]

        for gateway in self.gateways:
            yield "Fetching CID {} via {}.\n".format(cid, gateway)
            # the following url may change once ?format=tar
            # is implemented on the gateway
            # see also: https://github.com/ipfs/go-ipfs/issues/8234
            resp = requests.get(
                "{}/api/v0/get?arg={}".format(gateway, cid),
            )
            if resp.ok:
                tar = TarFile(fileobj=BytesIO(resp.content))
                tar.extractall(output_dir)
                break
            else:
                yield "could not get CID via {}: {}".format(
                        gateway, resp.status_code)
        else:
            raise ContentProviderException(
                    "could not find any working IPFS gateway")
        self._cid = cid

    @property
    def content_id(self):
        """
        On IPFS, the content identifier (CID) is a hash
        of all of the referenced contents. Thus the CID
        is a good content_id :-)
        """
        return self._cid
