# Sporadic tasks

## Upgrade default base image

repo2docker uses [Ubuntu](https://ubuntu.com/) long-term support (LTS) as the default base image because

- the default base image should have a large user base,
- the default base image should support a large number of packages, and
- the default base image should not change very often.

A new version of Ubuntu LTS is released every two years in May, more details at [Ubuntu release cycle](https://ubuntu.com/about/release-cycle).

repo2docker will upgrade to a newer version of Ubuntu LTS approximately one year after its release.

| Ubuntu LTS version | Ubuntu LTS release date | repo2docker version | repo2docker release date |
| ------------------ | ----------------------- | ------------------- | ------------------------ |
| 26.04 LTS          | April 2026              | 2027.4 (estimated)  | April 2027 (estimated)   |
| 24.04 LTS          | April 2024              | 2025.8              | August 2025              |

### Previous pull request

- [Pull request upgrading to Ubuntu 24.04 LTS](https://github.com/jupyterhub/repo2docker/pull/1417)
- [Pull request upgrading to Ubuntu 22.04 LTS](https://github.com/jupyterhub/repo2docker/pull/1287)

## Compare generated Dockerfiles between repo2docker versions

For larger refactorings it can be useful to check that the generated Dockerfiles match
between an older version of r2d and the current version. The following shell script
automates this test.

```bash
#! /bin/bash -e

current_version=$(repo2docker --version | sed s@+@-@)
echo "Comparing $(pwd) (local $current_version vs. $R2D_COMPARE_TO)"
basename="dockerfilediff"

diff_r2d_dockerfiles_with_version () {
    docker run --rm -t -v "$(pwd)":"$(pwd)" --user 1000 jupyterhub/repo2docker:"$1" repo2docker --no-build --debug "$(pwd)" &> "$basename"."$1"
    repo2docker --no-build --debug "$(pwd)" &> "$basename"."$current_version"

    # remove first line logging the path
    sed -i '/^\[Repo2Docker\]/d' "$basename"."$1"
    sed -i '/^\[Repo2Docker\]/d' "$basename"."$current_version"

    diff --strip-trailing-cr "$basename"."$1" "$basename"."$current_version" | colordiff
    rm "$basename"."$current_version" "$basename"."$1"
}

startdir="$(pwd)"
cd "$1"

#diff_r2d_dockerfiles 0.10.0-22.g4f428c3.dirty
diff_r2d_dockerfiles_with_version "$R2D_COMPARE_TO"

cd "$startdir"
```

Put the code above in a file `tests/dockerfile_diff.sh` and make it executable: `chmod +x dockerfile_diff.sh`.

Configure the repo2docker version you want to compare with your local version in the environment variable `R2D_COMPARE_TO`.
The scripts takes one input: the directory where repo2docker should be executed.

```bash
cd tests/
R2D_COMPARE_TO=0.10.0 ./dockerfile_diff.sh venv/py35/
```

Run it for all directories where there is a `verify` file:

```bash
cd tests/
R2D_COMPARE_TO=0.10.0 CMD=$(pwd)/dockerfile_diff.sh find . -name 'verify' -execdir bash -c '$CMD $(pwd)' \;
```

To keep the created Dockefilers for further inspection, comment out the deletion line in the script.
