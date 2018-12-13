Version x.y.z (unreleased)
==========================

Release date: the-future

New features
------------
- Add additional metadata to docker images about how they were built `#500`_ by
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
  repository `#413`_ by `@dsludwig`_.
- Editable mode: allows editing a local repository from a live container
  `#421`_ by `@evertrol`_.
- Change log added `#426`_ by `@evertrol`_.
- Documentation: improved the documentation for contributors `#453`_ by
  `@choldgraf`_.
- Buildpack: added support for the nix package manager `#407`_ by
  `@costrouc`_.
- Log a 'success' message when push is complete `#482`_ by
  `@yuvipanda`_.
- Allow specifying images to reuse cache from `#478`_ by
  `@yuvipanda`_.
- Add JupyterHub back to base environment `#467`_ by
  `@yuvipanda`_.
- Repo2docker has a logo! by `@agahkarakuzu`_ and `@blairhudson`_.
- Improve support for Stencila, including identifying stencila runtime from document context `#457`_ by `@nuest`_.


API changes
-----------

- Add content provider abstraction `#421`_ by `@betatim`_.


Bug fixes
---------

- Update to Jupyter notebook 5.7 `#475`_ by `@betatim`_ and `@minrk`_



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


.. _#242: https://github.com/jupyter/repo2docker/pull/242
.. _#407: https://github.com/jupyter/repo2docker/pull/407
.. _#413: https://github.com/jupyter/repo2docker/pull/413
.. _#421: https://github.com/jupyter/repo2docker/pull/421
.. _#426: https://github.com/jupyter/repo2docker/pull/426
.. _#453: https://github.com/jupyter/repo2docker/pull/453
.. _#457: https://github.com/jupyter/repo2docker/pull/457
.. _#475: https://github.com/jupyter/repo2docker/pull/475
.. _#478: https://github.com/jupyter/repo2docker/pull/478
.. _#482: https://github.com/jupyter/repo2docker/pull/482
.. _#500: https://github.com/jupyter/repo2docker/pull/500

.. _@agahkarakuzu: https://github.com/agahkarakuzu
.. _@betatim: https://github.com/betatim
.. _@blairhudson: https://github.com/blairhudson
.. _@choldgraf: https://github.com/choldgraf
.. _@costrouc: https://github.com/costrouc
.. _@dsludwig: https://github.com/dsludwig
.. _@evertrol: https://github.com/evertrol
.. _@minrk: https://github.com/minrk
.. _@nuest: https://github.com/nuest
.. _@yuvipanda: https://github.com/yuvipanda
.. _@jrbourbeau: https://github.com/jrbourbeau
