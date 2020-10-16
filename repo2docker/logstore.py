import logging
import os
from tempfile import NamedTemporaryFile
import re
from traitlets import Any, Dict, Unicode
from traitlets.config import LoggingConfigurable

try:
    import boto3

    S3_ENABLED = True
except ImportError:
    S3_ENABLED = False


"""Match all ANSI escape codes https://superuser.com/a/380778"""
ansi_escape_regex = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")


class LogStore(LoggingConfigurable):
    """Abstract interface for a class that stores a build log.
    This default implementation does nothing."""

    def write(self, s):
        """Write to the log"""
        pass

    def close(self):
        """Finish logging. Implementations may save or copy the log."""
        pass


class S3LogStore(LogStore):
    """Store a build log and upload to a S3 bucket on close

    If metadata is provided keys must be valid HTML headers, and values must be strings
    https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#object-metadata

    Example bucket policy to allow public read of objects, but prevent listing

        {
            "Version": "2012-10-17",
            "Statement": [
                {
                "Action": [
                    "s3:GetObject"
                ],
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                    "*"
                    ]
                },
                "Resource": [
                    "arn:aws:s3:::mybinder/*"
                ],
                "Sid": ""
                }
            ]
        }

    Source: https://gist.github.com/harshavardhana/400558963e4dfe3709623203222ed30c#granting-read-only-permission-to-an-anonymous-user

    """

    # Connection details
    endpoint = Unicode(help="S3 endpoint", config=True)
    access_key = Unicode(help="S3 access key ", config=True)
    secret_key = Unicode(help="S3 secret key", config=True)
    session_token = Unicode("", help="S3 session token (optional)", config=True)
    region = Unicode("", help="S3 region (optional)", config=True)

    # Where to store the log
    bucket = Unicode(help="S3 bucket", config=True)
    logname = Unicode(
        "repo2docker.log", help="The name and/or path of the log", config=True
    )

    metadata = Dict(
        {},
        help="Metadata to be associated with the log file",
        config=True,
    )

    _logfile = Any(allow_none=True)

    def __init__(self, **kwargs):
        if not S3_ENABLED:
            raise RuntimeError("S3LogStore requires the boto3 library")
        super().__init__(**kwargs)
        self.log = logging.getLogger("repo2docker")

    def _s3_credentials(self):
        creds = dict(
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region,
        )
        if self.session_token:
            creds["aws_session_token"] = self.session_token
        return creds

    def write(self, s):
        """Write a log, newlines are not automatically added,
        removes ANSI terminal escape codes"""
        if s and not self._logfile:
            self._logfile = NamedTemporaryFile("w", delete=False)
        cleaned = ansi_escape_regex.sub("", str(s))
        self._logfile.write(cleaned)

    def close(self):
        """Upload the logfile to S3"""
        if not self._logfile:
            # No log means image already exists so nothing was built
            self.log.debug("No log file")
            return
        self._logfile.close()
        self.log.info(
            f"Uploading log to {self.endpoint} bucket:{self.bucket} key:{self.logname}"
        )
        try:
            s3 = boto3.resource(
                "s3",
                config=boto3.session.Config(signature_version="s3v4"),
                **self._s3_credentials(),
            )
            s3.Bucket(self.bucket).upload_file(
                self._logfile.name,
                self.logname,
                ExtraArgs={
                    "ContentType": "text/plain; charset=utf-8",
                    "Metadata": self.metadata,
                },
            )
            os.remove(self._logfile.name)
        finally:
            self._logfile = None
