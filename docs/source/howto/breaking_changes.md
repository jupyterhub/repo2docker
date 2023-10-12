# Deal with breaking changes in repo2docker

Repo2docker occasionally has to make breaking changes in how repositories are built.

## Upgrade of base image from Ubuntu 18.04 to 22.04

The base image used by repo2docker was [upgraded from Ubuntu 18.04 to Ubuntu 22.04](https://github.com/jupyterhub/repo2docker/pull/1287) in version 2023.10.0 due to Ubuntu 18.04 going out of support.

This is unlikely to affect you unless you are using {ref}`apt.txt <apt.txt>`.

{ref}`apt.txt <apt.txt>` installs packages from the official Ubuntu package repositories, and is intrinsically tied to the Ubuntu version.
Many packages will be available in both Ubuntu 18.04 and Ubuntu 22.04, however some may be renamed (for example if multiple incompatible versions are available).

Some packages may be removed, or may not be compatible with the previous version.
In this case you should see if your packages can be installed using a {ref}`Conda environment.yml file <environment.yml>` using either the default [conda-forge channel](https://conda-forge.org/feedstock-outputs/) or in one of the many [third-party channels](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/channels.html).

Alternatively you can try installing the packages from source, using a {ref}`postBuild <postBuild>` script.

As a last resort you can install an older version of repo2docker locally, build your image, push it to a public container registry such as [Docker Hub](https://hub.docker.com/), [GitHub Container Registry](https://docs.github.com/en/packages/guides/about-github-container-registry) or [quay.io](https://quay.io/), and replace your repository's repo2docker configuration with a minimal {ref}`Dockerfile <dockerfile>` containing just:

```dockerfile
FROM <registry>/<username>/<image>:<tag>
```

This image will contain a frozen version of your repository at the time the image was built.
You will need to rebuild and push it everytime your repository is modified.
