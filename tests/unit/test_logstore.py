"""
Test S3LogStore
"""
# botocore includes a stub
# https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html
# but it doesn't work with upload_file so use mock instead
# https://sgillies.net/2017/10/19/mock-is-magic.html
from unittest.mock import patch
from repo2docker import logstore


@patch("repo2docker.logstore.boto3")
def test_s3logstore_upload(boto3):
    store = logstore.S3LogStore(
        endpoint="http://localhost:9000",
        access_key="access",
        secret_key="secret",
        bucket="bucket",
        keyprefix="prefix/",
        logname="test/build.log",
    )

    store.write("hello\n")
    r = store.close()

    boto3.resource.assert_called_with(
        "s3",
        config=boto3.session.Config(signature_version="s3v4"),
        endpoint_url="http://localhost:9000",
        aws_access_key_id="access",
        aws_secret_access_key="secret",
        region_name="",
    )
    boto3.resource().Bucket.assert_called_with("bucket")
    boto3.resource().Bucket().upload_file.assert_called_with(
        store._logfile.name,
        "prefix/test/build.log",
        ExtraArgs={"ContentType": "text/plain; charset=utf-8", "ACL": "public-read"},
    )


@patch("repo2docker.logstore.boto3")
def test_s3logstore_empty(boto3):
    store = logstore.S3LogStore(
        endpoint="http://localhost:9000",
        access_key="access",
        secret_key="secret",
        bucket="bucket",
        keyprefix="prefix/",
        logname="test/build.log",
    )

    r = store.close()

    assert not boto3.resource.called
    assert not boto3.resource().Bucket.called
    assert not boto3.resource().Bucket().upload_file.called
