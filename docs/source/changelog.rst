=========
Changelog
=========

Version 0.x.x
=============

Release date: TBD

New features
------------
- Support for julia `Project.toml`, `JuliaProject.toml` and `Manifest.toml` files in :pr:`595` by
  :user:`davidanthoff`
- Set JULIA_PROJECT globally, so that every julia instance starts with the
  julia environment activated in :pr:`612` by :user:`davidanthoff`.
- Update Miniconda version to 4.5.12 and Conda version to 4.6.14 in :pr:`637` by
  :user:`jhamman`
- Install notebook into `notebook` env instead of `root`.
  Activate conda environments and shell integration via ENTRYPOINT
  in :pr:`651` by :user:`minrk`

API changes
-----------

Bug fixes
---------
- Install IJulia kernel into ${NB_PYTHON_PREFIX}/share/jupyter in :pr:`622` by
  :user:`davidanthoff`.
- Ensure git submodules are updated and initilized correctly in :pr:`639` by
  :user:`djhoese`.
- Use archive.debian.org as source for the debian jessie based legacy
  buildpack in :pr:`633` by :user:`betatim`.
- Update to version 5.7.6 of the `notebook` package used in all environments
  in :pr:`628` by :user:`betatim`.
- Switch to newer version of jupyter-server-proxy to fix websocket handling
  in :pr:`646` by :user:`betatim`.
- Update to pip v19.0.3 in :pr:`647` by :user:`betatim`.


Version 0.8.0
=============

Release date: 2019-02-21

New features
------------
- Add additional metadata to docker images about how they were built :pr:`500` by
  :user:`jrbourbeau`.
- Allow users to install global NPM packages: :pr:`573` by :user:`GladysNalvarte`.
- Add documentation on switching the user interface presented by a
  container. :pr:`568` by user:`choldgraf`.
- Increased test coverage to ~87% by :user:`betatim` and :user:`yuvipanda`.
- Documentation improvements and additions by :user:`lheagy`, :user:`choldgraf`.
- Remove f-strings from code base, repo2docker is compatible with Python 3.4+
  again by :user:`jrbourbeau` in :pr:`520`.
- Local caching of previously built repostories to speed up launch times
  by :user:`betatim` in :pr:`511`.
- Make destination of repository content in the container image configurable
  on the CLI via ``--target-repo-dir``. By :user:`yuvipanda` in :pr:`507`.
- Expose CPU limit settings for building and running containers. By
  :user:`GladysNalvarte` in :pr:`579`.
- Make Python 3.7 the default version. By :user:`yuvipanda` and :user:`minrk` in
  :pr:`539`.

API changes
-----------

Bug fixes
---------
- In some cases the version of conda installed in images was not pinned and got
  upgraded by user actions. Fixed in :pr:`576` by :user:`minrk`.
- Fix an error related to checking if debug output was enabled or not:
  :pr:`575` by :user:`yuvipanda`.
- Update nteract frontend to version 2.0.0 by :user:`yuvipanda` in :pr:`571`.
- Fix quoting issue in ``GIT_CREDENTIAL_ENV`` environment variable by
  :user:`minrk` in :pr:`572`.
- Change to using the first 8 characters of each Git commit, not the last 8,
  to tag each built docker image of repo2docker itself. :user:`minrk` in :pr:`562`.
- Allow users to select the Julia when using a ``requirements.txt`` by
  :user:`yuvipanda` in :pr:`557`.
- Set ``JULIA_DEPOT_PATH`` to install packages outside the home directory by
  :user:`yuvipanda` in :pr:`555`.
- Update to Jupyter notebook 5.7.4 :pr:`519` by :user:`minrk`.


Version 0.7.0
=============

Release date: 2018-12-12

New features
------------

- Build from sub-directory: build the image based on a sub-directory of a
  repository :pr:`413` by :user:`dsludwig`.
- Editable mode: allows editing a local repository from a live container
  :pr:`421` by :user:`evertrol`.
- Change log added :pr:`426` by :user:`evertrol`.
- Documentation: improved the documentation for contributors :pr:`453` by
  :user:`choldgraf`.
- Buildpack: added support for the nix package manager :pr:`407` by
  :user:`costrouc`.
- Log a 'success' message when push is complete :pr:`482` by
  :user:`yuvipanda`.
- Allow specifying images to reuse cache from :pr:`478` by
  :user:`yuvipanda`.
- Add JupyterHub back to base environment :pr:`476` by :user:`yuvipanda`.
- Repo2docker has a logo! by :user:`agahkarakuzu` and :user:`blairhudson`.
- Improve support for Stencila, including identifying stencila runtime from
  document context :pr:`457` by :user:`nuest`.


API changes
-----------

- Add content provider abstraction :pr:`421` by :user:`betatim`.


Bug fixes
---------

- Update to Jupyter notebook 5.7 :pr:`475` by :user:`betatim` and :user:`minrk`.



Version 0.6
===========

Released 2018-09-09


Version 0.5
===========

Released 2018-02-07


Version 0.4.1
=============

Released 2018-09-06


Version 0.2
===========

Released 2018-05-25


Version 0.1.1
=============

Released 2017-04-19


Version 0.1
===========

Released 2017-04-14
