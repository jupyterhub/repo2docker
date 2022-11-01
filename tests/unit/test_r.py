from datetime import date
from unittest.mock import patch

import pytest
from requests.models import Response

from repo2docker import buildpacks


@pytest.mark.parametrize(
    "runtime_version, expected", [("", "4.2"), ("3.6", "3.6"), ("3.5.1", "3.5")]
)
def test_version_specification(tmpdir, runtime_version, expected):
    tmpdir.chdir()

    with open("runtime.txt", "w") as f:
        if runtime_version:
            runtime_version += "-"
        f.write(f"r-{runtime_version}2019-01-01")

    r = buildpacks.RBuildPack()
    assert r.r_version.startswith(expected)


def test_version_completion(tmpdir):
    tmpdir.chdir()

    with open("runtime.txt", "w") as f:
        f.write(f"r-3.6-2019-01-01")

    r = buildpacks.RBuildPack()
    assert r.r_version == "3.6.3"


@pytest.mark.parametrize(
    "runtime, expected",
    [
        ("r-2019-01-01", (2019, 1, 1)),
        ("r-3.6.1-2019-01-01", (2019, 1, 1)),
        ("r-3.5-2019-01-01", (2019, 1, 1)),
    ],
)
def test_mran_date(tmpdir, runtime, expected):
    tmpdir.chdir()

    with open("runtime.txt", "w") as f:
        f.write(runtime)

    r = buildpacks.RBuildPack()
    assert r.checkpoint_date == date(*expected)


def test_snapshot_rspm_date():
    test_dates = {
        # Even though there is no snapshot specified in the interface at https://packagemanager.rstudio.com/client/#/repos/1/overview
        # For 2021 Oct 22, the API still returns a valid URL that one can install
        # packages from - probably some server side magic that repeats our client side logic.
        # No snapshot for this date from
        date(2021, 10, 22): date(2021, 10, 22),
        # Snapshot exists for this date
        date(2022, 1, 1): date(2022, 1, 1),
    }

    r = buildpacks.RBuildPack()
    for requested, expected in test_dates.items():
        snapshot_url = r.get_rspm_snapshot_url(requested)
        assert snapshot_url.startswith(
            "https://packagemanager.rstudio.com/all/__linux__/bionic/"
            + expected.strftime("%Y-%m-%d")
        )

    with pytest.raises(ValueError):
        r.get_rspm_snapshot_url(date(1691, 9, 5))


@pytest.mark.parametrize("expected", [date(2019, 12, 29), date(2019, 12, 26)])
@pytest.mark.parametrize("requested", [date(2019, 12, 31)])
def test_snapshot_mran_date(requested, expected):
    def mock_request_head(url):
        r = Response()
        if url == "https://mran.microsoft.com/snapshot/" + expected.isoformat():
            r.status_code = 200
        else:
            r.status_code = 404
            r.reason = "Mock MRAN no snapshot"
        return r

    with patch("requests.head", side_effect=mock_request_head):
        r = buildpacks.RBuildPack()
        assert (
            r.get_mran_snapshot_url(requested)
            == f"https://mran.microsoft.com/snapshot/{expected.isoformat()}"
        )
