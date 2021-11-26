import re
from tarfile import TarFile
from io import BytesIO

import requests

from .base import ContentProvider, ContentProviderException

# testing well-formedness of CID is not trivial, to do it
# properly, one should use py-cid, which can decode all CIDS
# that library however has a bunch of dependencies, so for now
# we'll go with a reged-based approximation
# this regex follows https://stackoverflow.com/a/67176726
RE_CID = re.compile(
    "Qm[1-9A-HJ-NP-Za-km-z]{44,}|"
    "b[A-Za-z2-7]{58,}|"
    "B[A-Z2-7]{58,}|"
    "z[1-9A-HJ-NP-Za-km-z]{48,}|"
    "F[0-9A-F]{50,}"
)


def is_cid(s):
    return bool(RE_CID.match(s))


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
            try:
                resp = requests.get(
                    "{}/api/v0/get?arg={}".format(gateway, cid),
                )
            except requests.ConnectionError:
                yield "could not connect to gateway {}\n".format(gateway)
                continue

            if resp.ok:
                tar = TarFile(fileobj=BytesIO(resp.content))
                tar.extractall(output_dir)
                break
            else:
                yield "could not get CID via {}: {}\n".format(gateway, resp.status_code)
        else:
            raise ContentProviderException("could not find any working IPFS gateway")
        self._cid = cid

    @property
    def content_id(self):
        """
        On IPFS, the content identifier (CID) is a hash
        of all of the referenced contents. Thus the CID
        is a good content_id :-)
        """
        return self._cid
