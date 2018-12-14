=========
Changelog
=========


Upcoming release
================

Release date: TBD

New features
------------
- Add additional metadata to docker images about how they were built :pr:`500` by
  `@jrbourbeau`_.

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
  repository :pr:`413` by `@dsludwig`_.
- Editable mode: allows editing a local repository from a live container
  :pr:`421` by `@evertrol`_.
- Change log added :pr:`426` by `@evertrol`_.
- Documentation: improved the documentation for contributors :pr:`453` by
  `@choldgraf`_.
- Buildpack: added support for the nix package manager :pr:`407` by
  `@costrouc`_.
- Log a 'success' message when push is complete :pr:`482` by
  `@yuvipanda`_.
- Allow specifying images to reuse cache from :pr:`478` by
  `@yuvipanda`_.
- Add JupyterHub back to base environment :pr:`476` by `@yuvipanda`_.
- Repo2docker has a logo! by `@agahkarakuzu`_ and `@blairhudson`_.
- Improve support for Stencila, including identifying stencila runtime from document context :pr:`457` by `@nuest`_.


API changes
-----------

- Add content provider abstraction :pr:`421` by `@betatim`_.


Bug fixes
---------

- Update to Jupyter notebook 5.7 :pr:`475` by `@betatim`_ and `@minrk`_



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


.. _@agahkarakuzu: https://github.com/agahkarakuzu
.. _@betatim: https://github.com/betatim
.. _@blairhudson: https://github.com/blairhudson
.. _@choldgraf: https://github.com/choldgraf
.. _@costrouc: https://github.com/costrouc
.. _@dsludwig: https://github.com/dsludwig
.. _@evertrol: https://github.com/evertrol
.. _@jrbourbeau: https://github.com/jrbourbeau
.. _@minrk: https://github.com/minrk
.. _@nuest: https://github.com/nuest
.. _@yuvipanda: https://github.com/yuvipanda
