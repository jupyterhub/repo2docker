=========
Changelog
=========


Upcoming release
================

Release date: TBD

New features
------------
- Add additional metadata to docker images about how they were built :pr:`500` by
  :user:`jrbourbeau`.
- Add support for repo2docker version :pr:`550` by :user:`craig-willis`

API changes
-----------

Bug fixes
---------


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
- Improve support for Stencila, including identifying stencila runtime from document context :pr:`457` by :user:`nuest`.


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
