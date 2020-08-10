# Add a new buildpack

A new buildpack is needed when a new language or a new package manager should be
supported. [Existing buildpacks](https://github.com/jupyterhub/repo2docker/tree/master/repo2docker/buildpacks)
are a good model for how new buildpacks should be structured.
See [the Buildpacks page](buildpacks) for more information about the
structure of a buildpack.

## Criteria to balance and consider

Criteria to balance are:

1. Maintenance burden on repo2docker.
2. How easy it is to use a given setup without support from repo2docker natively.
   There are two escape hatches here - `postBuild` and `Dockerfile`.
3. How widely used is this language / package manager? This is the primary tradeoff
   with point (1). We (the Binder / Jupyter team) want to make new formats
   as little as possible, so ideally we can just say "X repositories on binder already use
   this using one of the escape hatches in (2), so let us make it easy and add
   native support".

### Adding libraries or UI to existing buildpacks

Note that this doesn't apply to adding additional libraries / UI to existing
buildpacks. For example, if we had an R buildpack and it supported IRKernel,
it is much easier to
just support RStudio / Shiny with it, since those are library additions instead of entirely
new buildpacks.
