# Changelog

## 2022.10.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/e40242c...e0d5b9b))

### Maintenance and upkeep improvements

- Use enum to standardise `phase` [#1185](https://github.com/jupyterhub/repo2docker/pull/1185) ([@manics](https://github.com/manics))
- get CI working again [#1178](https://github.com/jupyterhub/repo2docker/pull/1178) ([@minrk](https://github.com/minrk))
- Freeze.py update [#1173](https://github.com/jupyterhub/repo2docker/pull/1173) ([@manics](https://github.com/manics))
- Bump default R version to 4.2 from 4.1, and let R 3.4 go from 3.4.0 to 3.4.4 [#1165](https://github.com/jupyterhub/repo2docker/pull/1165) ([@yuvipanda](https://github.com/yuvipanda))

### Documentation improvements

- Post release fixes [#1133](https://github.com/jupyterhub/repo2docker/pull/1133) ([@manics](https://github.com/manics))

### Other merged PRs

- Initial changelog for 2022.10.0 [#1194](https://github.com/jupyterhub/repo2docker/pull/1194) ([@manics](https://github.com/manics))
- [MRG] Update Jupyter dependencies [#1193](https://github.com/jupyterhub/repo2docker/pull/1193) ([@jtpio](https://github.com/jtpio))
- Remove conda buildpacks pin of r-irkernel to 1.2 [#1191](https://github.com/jupyterhub/repo2docker/pull/1191) ([@consideRatio](https://github.com/consideRatio))
- ci: refactor julia/r/conda tests - now ~25 min instead of ~50 min [#1188](https://github.com/jupyterhub/repo2docker/pull/1188) ([@consideRatio](https://github.com/consideRatio))
- ci: general refresh of github workflows, update gha versions and let dependabot do it, etc. [#1186](https://github.com/jupyterhub/repo2docker/pull/1186) ([@consideRatio](https://github.com/consideRatio))
- fail on unsupported Python [#1184](https://github.com/jupyterhub/repo2docker/pull/1184) ([@minrk](https://github.com/minrk))
- mount wheels from build stage instead of copying them [#1182](https://github.com/jupyterhub/repo2docker/pull/1182) ([@minrk](https://github.com/minrk))
- consistent log handling when not using JSON loggers [#1177](https://github.com/jupyterhub/repo2docker/pull/1177) ([@minrk](https://github.com/minrk))
- explicitly build linux/amd64 images [#1176](https://github.com/jupyterhub/repo2docker/pull/1176) ([@minrk](https://github.com/minrk))
- add Python 3.10 base environment [#1175](https://github.com/jupyterhub/repo2docker/pull/1175) ([@minrk](https://github.com/minrk))
- Bump version of nodejs [#1172](https://github.com/jupyterhub/repo2docker/pull/1172) ([@yuvipanda](https://github.com/yuvipanda))
- Update mamba [#1171](https://github.com/jupyterhub/repo2docker/pull/1171) ([@SylvainCorlay](https://github.com/SylvainCorlay))
- Support pulling from zenodo sandbox too [#1169](https://github.com/jupyterhub/repo2docker/pull/1169) ([@yuvipanda](https://github.com/yuvipanda))
- Add MPDL Dataverse [#1167](https://github.com/jupyterhub/repo2docker/pull/1167) ([@wilhelmfrank](https://github.com/wilhelmfrank))
- ci: switch to using a 2fa enabled accounts pypi api-token [#1166](https://github.com/jupyterhub/repo2docker/pull/1166) ([@consideRatio](https://github.com/consideRatio))
- Add JPL Dataverse [#1163](https://github.com/jupyterhub/repo2docker/pull/1163) ([@foobarbecue](https://github.com/foobarbecue))
- Get R from RStudio provided apt packages (.deb files) [#1161](https://github.com/jupyterhub/repo2docker/pull/1161) ([@yuvipanda](https://github.com/yuvipanda))
- [MRG] Shallow clone HEAD [#1160](https://github.com/jupyterhub/repo2docker/pull/1160) ([@daradib](https://github.com/daradib))
- Fix Read-Only filesystem permission issue for log file [#1156](https://github.com/jupyterhub/repo2docker/pull/1156) ([@timeu](https://github.com/timeu))
- handle permission issue writing .jupyter-server-log.txt in REPO_DIR [#1151](https://github.com/jupyterhub/repo2docker/pull/1151) ([@pymonger](https://github.com/pymonger))
- Update black version [#1150](https://github.com/jupyterhub/repo2docker/pull/1150) ([@yuvipanda](https://github.com/yuvipanda))
- Update base notebook packages [#1149](https://github.com/jupyterhub/repo2docker/pull/1149) ([@yuvipanda](https://github.com/yuvipanda))
- [MRG] upgrade RStudio Server to v2022.02.1 [#1148](https://github.com/jupyterhub/repo2docker/pull/1148) ([@aplamada](https://github.com/aplamada))
- Update 'how to get R' section [#1147](https://github.com/jupyterhub/repo2docker/pull/1147) ([@yuvipanda](https://github.com/yuvipanda))
- handle r version being unspecified in environment.yml [#1141](https://github.com/jupyterhub/repo2docker/pull/1141) ([@minrk](https://github.com/minrk))
- [MRG] Update Dockerfile to current Alpine (ALPINE_VERSION=3.15.0) [#1136](https://github.com/jupyterhub/repo2docker/pull/1136) ([@holzman](https://github.com/holzman))
- [MRG] Pass build_args to `render()` during `--no-build` for consistency with regular builds [#1135](https://github.com/jupyterhub/repo2docker/pull/1135) ([@yoogottamk](https://github.com/yoogottamk))
- Update Changelog for release 2022.02.0 [#1113](https://github.com/jupyterhub/repo2docker/pull/1113) ([@manics](https://github.com/manics))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2022-02-06&to=2022-10-18&type=c))

[@aplamada](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aaplamada+updated%3A2022-02-06..2022-10-18&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2022-02-06..2022-10-18&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2022-02-06..2022-10-18&type=Issues) | [@daradib](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adaradib+updated%3A2022-02-06..2022-10-18&type=Issues) | [@foobarbecue](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Afoobarbecue+updated%3A2022-02-06..2022-10-18&type=Issues) | [@holzman](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aholzman+updated%3A2022-02-06..2022-10-18&type=Issues) | [@jameshowison](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajameshowison+updated%3A2022-02-06..2022-10-18&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajtpio+updated%3A2022-02-06..2022-10-18&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2022-02-06..2022-10-18&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2022-02-06..2022-10-18&type=Issues) | [@pymonger](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apymonger+updated%3A2022-02-06..2022-10-18&type=Issues) | [@SylvainCorlay](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ASylvainCorlay+updated%3A2022-02-06..2022-10-18&type=Issues) | [@timeu](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atimeu+updated%3A2022-02-06..2022-10-18&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awelcome+updated%3A2022-02-06..2022-10-18&type=Issues) | [@wilhelmfrank](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awilhelmfrank+updated%3A2022-02-06..2022-10-18&type=Issues) | [@yoogottamk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayoogottamk+updated%3A2022-02-06..2022-10-18&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2022-02-06..2022-10-18&type=Issues)

## 2022.02.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/c73321c...e40242c))

### Enhancements made

- Update jupyterlab 3.2.5 jupyter-resource-usage 0.6.1 [#1105](https://github.com/jupyterhub/repo2docker/pull/1105) ([@manics](https://github.com/manics))

### Maintenance and upkeep improvements

- Add help message to freeze.py [#1106](https://github.com/jupyterhub/repo2docker/pull/1106) ([@manics](https://github.com/manics))

### Documentation improvements

- [MRG] Release 2021.08.0 [#1067](https://github.com/jupyterhub/repo2docker/pull/1067) ([@manics](https://github.com/manics))

### Other merged PRs

- put micromamba in /usr/local/bin and use mamba for installs [#1128](https://github.com/jupyterhub/repo2docker/pull/1128) ([@minrk](https://github.com/minrk))
- Update ipywidgets jupyter-offlinenotebook jupyterlab [#1127](https://github.com/jupyterhub/repo2docker/pull/1127) ([@manics](https://github.com/manics))
- Allow passing in extra args to Docker initialization [#1124](https://github.com/jupyterhub/repo2docker/pull/1124) ([@yuvipanda](https://github.com/yuvipanda))
- Allow passing in traitlets via commandline [#1123](https://github.com/jupyterhub/repo2docker/pull/1123) ([@yuvipanda](https://github.com/yuvipanda))
- Delete /tmp/downloaded_packages after running install.R [#1119](https://github.com/jupyterhub/repo2docker/pull/1119) ([@yuvipanda](https://github.com/yuvipanda))
- Use a smaller R library in our tests [#1118](https://github.com/jupyterhub/repo2docker/pull/1118) ([@yuvipanda](https://github.com/yuvipanda))
- Only get R itself (r-base-core) from apt, not CRAN packages [#1117](https://github.com/jupyterhub/repo2docker/pull/1117) ([@minrk](https://github.com/minrk))
- set USER root after each directive block [#1115](https://github.com/jupyterhub/repo2docker/pull/1115) ([@minrk](https://github.com/minrk))
- Update Changelog for release 2022.02.0 [#1113](https://github.com/jupyterhub/repo2docker/pull/1113) ([@manics](https://github.com/manics))
- Say 'apt repository' rather than PPA [#1111](https://github.com/jupyterhub/repo2docker/pull/1111) ([@yuvipanda](https://github.com/yuvipanda))
- Bump default R version to 4.1 [#1107](https://github.com/jupyterhub/repo2docker/pull/1107) ([@yuvipanda](https://github.com/yuvipanda))
- Get binary R packages from packagemanager.rstudio.com [#1104](https://github.com/jupyterhub/repo2docker/pull/1104) ([@yuvipanda](https://github.com/yuvipanda))
- Quieter R builds [#1103](https://github.com/jupyterhub/repo2docker/pull/1103) ([@yuvipanda](https://github.com/yuvipanda))
- Support R 4.1 [#1102](https://github.com/jupyterhub/repo2docker/pull/1102) ([@yuvipanda](https://github.com/yuvipanda))
- Add command line option to pass extra build args [#1100](https://github.com/jupyterhub/repo2docker/pull/1100) ([@TimoRoth](https://github.com/TimoRoth))
- Set labels when building image from Dockerfile [#1097](https://github.com/jupyterhub/repo2docker/pull/1097) ([@TimoRoth](https://github.com/TimoRoth))
- jupyterlab 3.1.17 [#1092](https://github.com/jupyterhub/repo2docker/pull/1092) ([@minrk](https://github.com/minrk))
- update user_interface doc to reflect that lab is default [#1085](https://github.com/jupyterhub/repo2docker/pull/1085) ([@minrk](https://github.com/minrk))
- Updates to dev docs + Recommonmark -> MyST Parser [#1082](https://github.com/jupyterhub/repo2docker/pull/1082) ([@choldgraf](https://github.com/choldgraf))
- Bump JupyterLab to 3.1.11 [#1081](https://github.com/jupyterhub/repo2docker/pull/1081) ([@choldgraf](https://github.com/choldgraf))
- Fix Docker build (again) [#1078](https://github.com/jupyterhub/repo2docker/pull/1078) ([@manics](https://github.com/manics))
- Typo fix in utils docstring [#1072](https://github.com/jupyterhub/repo2docker/pull/1072) ([@jgarte](https://github.com/jgarte))
- Rename requirements.py-3.5.txt to requirements.py-3.5.pip [#1061](https://github.com/jupyterhub/repo2docker/pull/1061) ([@manics](https://github.com/manics))
- Default UI to JupyterLab [#1035](https://github.com/jupyterhub/repo2docker/pull/1035) ([@SylvainCorlay](https://github.com/SylvainCorlay))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2021-08-24&to=2022-02-06&type=c))

[@andrewjohnlowe](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aandrewjohnlowe+updated%3A2021-08-24..2022-02-06&type=Issues) | [@aplamada](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aaplamada+updated%3A2021-08-24..2022-02-06&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2021-08-24..2022-02-06&type=Issues) | [@bollwyvl](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abollwyvl+updated%3A2021-08-24..2022-02-06&type=Issues) | [@cboettig](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acboettig+updated%3A2021-08-24..2022-02-06&type=Issues) | [@ccordoba12](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Accordoba12+updated%3A2021-08-24..2022-02-06&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2021-08-24..2022-02-06&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2021-08-24..2022-02-06&type=Issues) | [@d70-t](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ad70-t+updated%3A2021-08-24..2022-02-06&type=Issues) | [@daroczig](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adaroczig+updated%3A2021-08-24..2022-02-06&type=Issues) | [@exaexa](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aexaexa+updated%3A2021-08-24..2022-02-06&type=Issues) | [@jgarte](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajgarte+updated%3A2021-08-24..2022-02-06&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajtpio+updated%3A2021-08-24..2022-02-06&type=Issues) | [@kkmann](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Akkmann+updated%3A2021-08-24..2022-02-06&type=Issues) | [@mael-le-gal](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amael-le-gal+updated%3A2021-08-24..2022-02-06&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2021-08-24..2022-02-06&type=Issues) | [@mattwigway](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amattwigway+updated%3A2021-08-24..2022-02-06&type=Issues) | [@meeseeksmachine](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ameeseeksmachine+updated%3A2021-08-24..2022-02-06&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2021-08-24..2022-02-06&type=Issues) | [@petersudmant](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apetersudmant+updated%3A2021-08-24..2022-02-06&type=Issues) | [@RaoOfPhysics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ARaoOfPhysics+updated%3A2021-08-24..2022-02-06&type=Issues) | [@sje30](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asje30+updated%3A2021-08-24..2022-02-06&type=Issues) | [@SylvainCorlay](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ASylvainCorlay+updated%3A2021-08-24..2022-02-06&type=Issues) | [@TimoRoth](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ATimoRoth+updated%3A2021-08-24..2022-02-06&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awelcome+updated%3A2021-08-24..2022-02-06&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2021-08-24..2022-02-06&type=Issues)

## 2021.08.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/71eb805...c73321c))

### Bugs fixed

- fix: add chardet, a not explicitly declared dependency [#1064](https://github.com/jupyterhub/repo2docker/pull/1064) ([@johnhoman](https://github.com/johnhoman))

### Documentation improvements

- [MRG] Release 2021.08.0 [#1067](https://github.com/jupyterhub/repo2docker/pull/1067) ([@manics](https://github.com/manics))

### Other merged PRs

- Update README quay.io URL, Add docker latest tag [#1075](https://github.com/jupyterhub/repo2docker/pull/1075) ([@manics](https://github.com/manics))
- GitHub workflow build and push to Docker hub [#1071](https://github.com/jupyterhub/repo2docker/pull/1071) ([@manics](https://github.com/manics))
- Bump environment [#1069](https://github.com/jupyterhub/repo2docker/pull/1069) ([@manics](https://github.com/manics))
- Rename master branch to main [#1068](https://github.com/jupyterhub/repo2docker/pull/1068) ([@manics](https://github.com/manics))
- Workaround docker-py dependency's failure to import six [#1066](https://github.com/jupyterhub/repo2docker/pull/1066) ([@consideRatio](https://github.com/consideRatio))
- Remove Pipfile & Pipfile.lock [#1054](https://github.com/jupyterhub/repo2docker/pull/1054) ([@yuvipanda](https://github.com/yuvipanda))
- Remove CircleCI docs build [#1053](https://github.com/jupyterhub/repo2docker/pull/1053) ([@yuvipanda](https://github.com/yuvipanda))
- Pin doc requirements to avoid CI breakages [#1052](https://github.com/jupyterhub/repo2docker/pull/1052) ([@manics](https://github.com/manics))
- Stop using deprecated add_stylesheet in sphinx [#1050](https://github.com/jupyterhub/repo2docker/pull/1050) ([@yuvipanda](https://github.com/yuvipanda))
- Add study participation notice to readme [#1046](https://github.com/jupyterhub/repo2docker/pull/1046) ([@sgibson91](https://github.com/sgibson91))
- Bump urllib3 from 1.26.4 to 1.26.5 [#1045](https://github.com/jupyterhub/repo2docker/pull/1045) ([@dependabot](https://github.com/dependabot))
- always unpack a single zenodo zip [#1043](https://github.com/jupyterhub/repo2docker/pull/1043) ([@akhmerov](https://github.com/akhmerov))
- State newly used installation command [#1040](https://github.com/jupyterhub/repo2docker/pull/1040) ([@fkohrt](https://github.com/fkohrt))
- Fix regression in hydroshare introduced after moving to requests [#1034](https://github.com/jupyterhub/repo2docker/pull/1034) ([@MridulS](https://github.com/MridulS))
- Bump pyyaml from 5.1.1 to 5.4 [#1029](https://github.com/jupyterhub/repo2docker/pull/1029) ([@dependabot](https://github.com/dependabot))
- Set default Julia version to 1.6 [#1028](https://github.com/jupyterhub/repo2docker/pull/1028) ([@tomyun](https://github.com/tomyun))
- Fix logo URL in README [#1027](https://github.com/jupyterhub/repo2docker/pull/1027) ([@betatim](https://github.com/betatim))
- Refine buffered output debugging [#1016](https://github.com/jupyterhub/repo2docker/pull/1016) ([@minrk](https://github.com/minrk))
- reimplement entrypoint in Python [#1014](https://github.com/jupyterhub/repo2docker/pull/1014) ([@minrk](https://github.com/minrk))
- [MRG] Define an interface for Container engines [#848](https://github.com/jupyterhub/repo2docker/pull/848) ([@manics](https://github.com/manics))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2021-03-12&to=2021-08-24&type=c))

[@akhmerov](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aakhmerov+updated%3A2021-03-12..2021-08-24&type=Issues) | [@aplamada](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aaplamada+updated%3A2021-03-12..2021-08-24&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2021-03-12..2021-08-24&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2021-03-12..2021-08-24&type=Issues) | [@civodul](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acivodul+updated%3A2021-03-12..2021-08-24&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2021-03-12..2021-08-24&type=Issues) | [@dependabot](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adependabot+updated%3A2021-03-12..2021-08-24&type=Issues) | [@dkleissa](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adkleissa+updated%3A2021-03-12..2021-08-24&type=Issues) | [@fkohrt](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Afkohrt+updated%3A2021-03-12..2021-08-24&type=Issues) | [@johnhoman](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajohnhoman+updated%3A2021-03-12..2021-08-24&type=Issues) | [@jzf2101](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajzf2101+updated%3A2021-03-12..2021-08-24&type=Issues) | [@ltetrel](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Altetrel+updated%3A2021-03-12..2021-08-24&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2021-03-12..2021-08-24&type=Issues) | [@meeseeksmachine](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ameeseeksmachine+updated%3A2021-03-12..2021-08-24&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2021-03-12..2021-08-24&type=Issues) | [@MridulS](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AMridulS+updated%3A2021-03-12..2021-08-24&type=Issues) | [@ocefpaf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aocefpaf+updated%3A2021-03-12..2021-08-24&type=Issues) | [@paugier](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apaugier+updated%3A2021-03-12..2021-08-24&type=Issues) | [@rnestler](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Arnestler+updated%3A2021-03-12..2021-08-24&type=Issues) | [@sgibson91](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asgibson91+updated%3A2021-03-12..2021-08-24&type=Issues) | [@SylvainCorlay](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ASylvainCorlay+updated%3A2021-03-12..2021-08-24&type=Issues) | [@tomyun](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atomyun+updated%3A2021-03-12..2021-08-24&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awelcome+updated%3A2021-03-12..2021-08-24&type=Issues) | [@willingc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awillingc+updated%3A2021-03-12..2021-08-24&type=Issues) | [@xhochy](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Axhochy+updated%3A2021-03-12..2021-08-24&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2021-03-12..2021-08-24&type=Issues)

## 2021.03.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/40f475f...71eb805))

### Merged PRs

- [MRG] Cleanup install_requires including duplicates [#1020](https://github.com/jupyterhub/repo2docker/pull/1020) ([@manics](https://github.com/manics))
- buildpacks.r: dont use apt-key directly to respect *_proxy env vars [#1019](https://github.com/jupyterhub/repo2docker/pull/1019) ([@g-braeunlich](https://github.com/g-braeunlich))
- freeze with mamba, add 3.9 [#1017](https://github.com/jupyterhub/repo2docker/pull/1017) ([@minrk](https://github.com/minrk))
- bump python in circleci  test [#1013](https://github.com/jupyterhub/repo2docker/pull/1013) ([@minrk](https://github.com/minrk))
- fix dataverse regression introduced in last release [#1011](https://github.com/jupyterhub/repo2docker/pull/1011) ([@MridulS](https://github.com/MridulS))
- Add GH workflow to push releases to PYPi and introduce CalVer [#1004](https://github.com/jupyterhub/repo2docker/pull/1004) ([@betatim](https://github.com/betatim))
- Add entrypoint script which automatically propagates *_PROXY env vars… [#1003](https://github.com/jupyterhub/repo2docker/pull/1003) ([@g-braeunlich](https://github.com/g-braeunlich))
- Update to JupyterLab 3.0 [#996](https://github.com/jupyterhub/repo2docker/pull/996) ([@jtpio](https://github.com/jtpio))
- Add a contentprovider for Software Heritage persistent ID (SWHID) [#988](https://github.com/jupyterhub/repo2docker/pull/988) ([@douardda](https://github.com/douardda))
- [MRG] Stream jupyter server logs to a file [#987](https://github.com/jupyterhub/repo2docker/pull/987) ([@betatim](https://github.com/betatim))
- [MRG] Experiment with different install mechanism to get code coverage stats again [#982](https://github.com/jupyterhub/repo2docker/pull/982) ([@betatim](https://github.com/betatim))
- add 4.0, 4.0.2 to list of supported R versions [#960](https://github.com/jupyterhub/repo2docker/pull/960) ([@minrk](https://github.com/minrk))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2021-01-23&to=2021-03-12&type=c))

[@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2021-01-23..2021-03-12&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2021-01-23..2021-03-12&type=Issues) | [@ctr26](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Actr26+updated%3A2021-01-23..2021-03-12&type=Issues) | [@douardda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adouardda+updated%3A2021-01-23..2021-03-12&type=Issues) | [@g-braeunlich](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ag-braeunlich+updated%3A2021-01-23..2021-03-12&type=Issues) | [@jabbera](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajabbera+updated%3A2021-01-23..2021-03-12&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajtpio+updated%3A2021-01-23..2021-03-12&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2021-01-23..2021-03-12&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2021-01-23..2021-03-12&type=Issues) | [@MridulS](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AMridulS+updated%3A2021-01-23..2021-03-12&type=Issues) | [@scottyhq](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ascottyhq+updated%3A2021-01-23..2021-03-12&type=Issues) | [@SylvainCorlay](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ASylvainCorlay+updated%3A2021-01-23..2021-03-12&type=Issues) | [@trybik](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atrybik+updated%3A2021-01-23..2021-03-12&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awelcome+updated%3A2021-01-23..2021-03-12&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2021-01-23..2021-03-12&type=Issues)

## 2021.01.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/2e477dd...40f475f))

### Merged PRs

- MRG: Fix figshare test [#1001](https://github.com/jupyterhub/repo2docker/pull/1001) ([@manics](https://github.com/manics))
- [MRG] Weekly test of master to check for external failures [#998](https://github.com/jupyterhub/repo2docker/pull/998) ([@manics](https://github.com/manics))
- Replace urllib by requests in contentproviders [#993](https://github.com/jupyterhub/repo2docker/pull/993) ([@douardda](https://github.com/douardda))
- Use mambaforge instead of miniforge [#992](https://github.com/jupyterhub/repo2docker/pull/992) ([@SylvainCorlay](https://github.com/SylvainCorlay))
- buildpacks/nix: 2.3 -> 2.3.9 [#991](https://github.com/jupyterhub/repo2docker/pull/991) ([@FRidh](https://github.com/FRidh))
- buildpacks/nix: disable sandboxing (bugfix) [#990](https://github.com/jupyterhub/repo2docker/pull/990) ([@FRidh](https://github.com/FRidh))
- Add Julia 1.5.3 support [#984](https://github.com/jupyterhub/repo2docker/pull/984) ([@tomyun](https://github.com/tomyun))
- [MRG] Update to node 14 [#983](https://github.com/jupyterhub/repo2docker/pull/983) ([@jtpio](https://github.com/jtpio))
- Mamba 0.6.1 [#979](https://github.com/jupyterhub/repo2docker/pull/979) ([@minrk](https://github.com/minrk))
- [MRG] Remove reference to `master` branch from CLI doc [#977](https://github.com/jupyterhub/repo2docker/pull/977) ([@betatim](https://github.com/betatim))
- [MRG] Ensure REPO_DIR owned by NB_USER [#975](https://github.com/jupyterhub/repo2docker/pull/975) ([@tomyun](https://github.com/tomyun))
- add chown to COPY commands to reduce layer count [#969](https://github.com/jupyterhub/repo2docker/pull/969) ([@bollwyvl](https://github.com/bollwyvl))
- MRG: set TIMEFORMAT for timed bash conda commands [#966](https://github.com/jupyterhub/repo2docker/pull/966) ([@manics](https://github.com/manics))
- MRG: Disable jupyterlab extension build minimize [#963](https://github.com/jupyterhub/repo2docker/pull/963) ([@manics](https://github.com/manics))
- Bump Black version to 20.8b1 and use --target-version=py36 [#955](https://github.com/jupyterhub/repo2docker/pull/955) ([@paugier](https://github.com/paugier))
- MRG: Add workflow to build Docker image [#954](https://github.com/jupyterhub/repo2docker/pull/954) ([@manics](https://github.com/manics))
- [MRG] Crosslink 'Configuring your repository' with usage [#952](https://github.com/jupyterhub/repo2docker/pull/952) ([@manics](https://github.com/manics))
- [MRG] Bump Python requirement to 3.6 from 3.5 [#951](https://github.com/jupyterhub/repo2docker/pull/951) ([@betatim](https://github.com/betatim))
- [MRG] Add a Mercurial contentprovider [#950](https://github.com/jupyterhub/repo2docker/pull/950) ([@paugier](https://github.com/paugier))
- [MRG] Handle requirements.txt with `--pre` lines [#943](https://github.com/jupyterhub/repo2docker/pull/943) ([@betatim](https://github.com/betatim))
- GitHub Actions [#942](https://github.com/jupyterhub/repo2docker/pull/942) ([@minrk](https://github.com/minrk))
- stop running tests on travis [#940](https://github.com/jupyterhub/repo2docker/pull/940) ([@minrk](https://github.com/minrk))
- update repo URLs for jupyterhub/repo2docker [#939](https://github.com/jupyterhub/repo2docker/pull/939) ([@minrk](https://github.com/minrk))
- Add Julia 1.5.0 support [#938](https://github.com/jupyterhub/repo2docker/pull/938) ([@tomyun](https://github.com/tomyun))
- Upgrade custom test infrastructure for pytest 6.0.0 [#936](https://github.com/jupyterhub/repo2docker/pull/936) ([@betatim](https://github.com/betatim))
- validate_image_name: mention lowercase, fix formatting [#934](https://github.com/jupyterhub/repo2docker/pull/934) ([@manics](https://github.com/manics))
- Update JupyterLab to 2.2.0 [#933](https://github.com/jupyterhub/repo2docker/pull/933) ([@manics](https://github.com/manics))
- [MRG] Update snapshot date for simple R test [#930](https://github.com/jupyterhub/repo2docker/pull/930) ([@betatim](https://github.com/betatim))
- little improvement for testing binder_dir [#928](https://github.com/jupyterhub/repo2docker/pull/928) ([@bitnik](https://github.com/bitnik))
- update docs for config dirs [#927](https://github.com/jupyterhub/repo2docker/pull/927) ([@bitnik](https://github.com/bitnik))
- avoid deprecated import of collections.abc [#924](https://github.com/jupyterhub/repo2docker/pull/924) ([@minrk](https://github.com/minrk))
- Bump nix version to 2.3 [#915](https://github.com/jupyterhub/repo2docker/pull/915) ([@jboynyc](https://github.com/jboynyc))
- doc: runtime.txt installs python x.y (& concise rewording) [#914](https://github.com/jupyterhub/repo2docker/pull/914) ([@mdeff](https://github.com/mdeff))
- doc: environment.yml installs a conda env, not only python [#913](https://github.com/jupyterhub/repo2docker/pull/913) ([@mdeff](https://github.com/mdeff))
- [MRG] Add gitpod.io config for docs [#908](https://github.com/jupyterhub/repo2docker/pull/908) ([@betatim](https://github.com/betatim))
- [MRG] - fix repo2docker logo in Sphinx docs [#906](https://github.com/jupyterhub/repo2docker/pull/906) ([@trallard](https://github.com/trallard))
- [MRG] Add nbresuse==0.3.3 (full freeze.py) [#904](https://github.com/jupyterhub/repo2docker/pull/904) ([@manics](https://github.com/manics))
- Add missing “:” for R code [#900](https://github.com/jupyterhub/repo2docker/pull/900) ([@adamhsparks](https://github.com/adamhsparks))
- Add Julia 1.4.2 support [#899](https://github.com/jupyterhub/repo2docker/pull/899) ([@davidanthoff](https://github.com/davidanthoff))
- Update Dockerfile to add Docker [#896](https://github.com/jupyterhub/repo2docker/pull/896) ([@hamelsmu](https://github.com/hamelsmu))
- [MRG] Fix RShiny proxy [#893](https://github.com/jupyterhub/repo2docker/pull/893) ([@betatim](https://github.com/betatim))
- [MRG] Bump version of irkernel for R 4.0 [#892](https://github.com/jupyterhub/repo2docker/pull/892) ([@betatim](https://github.com/betatim))
- [MRG] chmod start script from repo2docker-entrypoint [#886](https://github.com/jupyterhub/repo2docker/pull/886) ([@danlester](https://github.com/danlester))
- [MRG] Workaround Docker issue impacting some tests on macOS [#882](https://github.com/jupyterhub/repo2docker/pull/882) ([@hwine](https://github.com/hwine))
- [MRG] pypi jupyter-offlinenotebook==0.1.0 [#880](https://github.com/jupyterhub/repo2docker/pull/880) ([@manics](https://github.com/manics))
- Work around a Julia bug [#879](https://github.com/jupyterhub/repo2docker/pull/879) ([@davidanthoff](https://github.com/davidanthoff))
- [MRG] Change --env option to work like docker's [#874](https://github.com/jupyterhub/repo2docker/pull/874) ([@hwine](https://github.com/hwine))
- [docs] fix grammatical error in section title [#872](https://github.com/jupyterhub/repo2docker/pull/872) ([@jameslamb](https://github.com/jameslamb))
- Add support for Julia 1.4.0 [#870](https://github.com/jupyterhub/repo2docker/pull/870) ([@davidanthoff](https://github.com/davidanthoff))
- [MRG] Update server proxy and rsession proxy [#869](https://github.com/jupyterhub/repo2docker/pull/869) ([@betatim](https://github.com/betatim))
- Adopt new Sphinx theme name [#864](https://github.com/jupyterhub/repo2docker/pull/864) ([@xhochy](https://github.com/xhochy))
- Document loose conda export with --from-history [#863](https://github.com/jupyterhub/repo2docker/pull/863) ([@xhochy](https://github.com/xhochy))
- Fix typo [#862](https://github.com/jupyterhub/repo2docker/pull/862) ([@jtpio](https://github.com/jtpio))
- Use miniforge instead of miniconda to get conda [#859](https://github.com/jupyterhub/repo2docker/pull/859) ([@yuvipanda](https://github.com/yuvipanda))
- [MRG] If looking for latest MRAN URL try earlier snapshots too [#851](https://github.com/jupyterhub/repo2docker/pull/851) ([@manics](https://github.com/manics))
- [MRG] Update black 19.10b0, target Python 3.5 [#849](https://github.com/jupyterhub/repo2docker/pull/849) ([@manics](https://github.com/manics))
- [MRG] Add jupyter-offlinenotebook extension [#845](https://github.com/jupyterhub/repo2docker/pull/845) ([@betatim](https://github.com/betatim))
- docs: postBuild warn about shell script errors being ignored [#844](https://github.com/jupyterhub/repo2docker/pull/844) ([@manics](https://github.com/manics))
- [MRG] Update changelog for 0.11.0 [#842](https://github.com/jupyterhub/repo2docker/pull/842) ([@betatim](https://github.com/betatim))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2020-02-05&to=2021-01-23&type=c))

[@adamhsparks](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aadamhsparks+updated%3A2020-02-05..2021-01-23&type=Issues) | [@AliMirlou](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AAliMirlou+updated%3A2020-02-05..2021-01-23&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2020-02-05..2021-01-23&type=Issues) | [@bitnik](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abitnik+updated%3A2020-02-05..2021-01-23&type=Issues) | [@blink1073](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ablink1073+updated%3A2020-02-05..2021-01-23&type=Issues) | [@bollwyvl](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abollwyvl+updated%3A2020-02-05..2021-01-23&type=Issues) | [@cboettig](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acboettig+updated%3A2020-02-05..2021-01-23&type=Issues) | [@ccordoba12](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Accordoba12+updated%3A2020-02-05..2021-01-23&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2020-02-05..2021-01-23&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2020-02-05..2021-01-23&type=Issues) | [@danlester](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adanlester+updated%3A2020-02-05..2021-01-23&type=Issues) | [@davidanthoff](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adavidanthoff+updated%3A2020-02-05..2021-01-23&type=Issues) | [@dolfinus](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adolfinus+updated%3A2020-02-05..2021-01-23&type=Issues) | [@douardda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adouardda+updated%3A2020-02-05..2021-01-23&type=Issues) | [@FRidh](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AFRidh+updated%3A2020-02-05..2021-01-23&type=Issues) | [@gracinet](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Agracinet+updated%3A2020-02-05..2021-01-23&type=Issues) | [@hamelsmu](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ahamelsmu+updated%3A2020-02-05..2021-01-23&type=Issues) | [@hwine](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ahwine+updated%3A2020-02-05..2021-01-23&type=Issues) | [@ivergara](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aivergara+updated%3A2020-02-05..2021-01-23&type=Issues) | [@jameslamb](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajameslamb+updated%3A2020-02-05..2021-01-23&type=Issues) | [@jasongrout](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajasongrout+updated%3A2020-02-05..2021-01-23&type=Issues) | [@jboynyc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajboynyc+updated%3A2020-02-05..2021-01-23&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajtpio+updated%3A2020-02-05..2021-01-23&type=Issues) | [@jzf2101](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajzf2101+updated%3A2020-02-05..2021-01-23&type=Issues) | [@kkmann](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Akkmann+updated%3A2020-02-05..2021-01-23&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2020-02-05..2021-01-23&type=Issues) | [@mdeff](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amdeff+updated%3A2020-02-05..2021-01-23&type=Issues) | [@meeseeksmachine](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ameeseeksmachine+updated%3A2020-02-05..2021-01-23&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2020-02-05..2021-01-23&type=Issues) | [@nokome](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Anokome+updated%3A2020-02-05..2021-01-23&type=Issues) | [@nuest](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Anuest+updated%3A2020-02-05..2021-01-23&type=Issues) | [@ocefpaf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aocefpaf+updated%3A2020-02-05..2021-01-23&type=Issues) | [@paugier](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apaugier+updated%3A2020-02-05..2021-01-23&type=Issues) | [@scottyhq](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ascottyhq+updated%3A2020-02-05..2021-01-23&type=Issues) | [@sgibson91](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asgibson91+updated%3A2020-02-05..2021-01-23&type=Issues) | [@support](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asupport+updated%3A2020-02-05..2021-01-23&type=Issues) | [@SylvainCorlay](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ASylvainCorlay+updated%3A2020-02-05..2021-01-23&type=Issues) | [@tomyun](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atomyun+updated%3A2020-02-05..2021-01-23&type=Issues) | [@trallard](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atrallard+updated%3A2020-02-05..2021-01-23&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awelcome+updated%3A2020-02-05..2021-01-23&type=Issues) | [@westurner](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awesturner+updated%3A2020-02-05..2021-01-23&type=Issues) | [@willingc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awillingc+updated%3A2020-02-05..2021-01-23&type=Issues) | [@xhochy](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Axhochy+updated%3A2020-02-05..2021-01-23&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2020-02-05..2021-01-23&type=Issues)

## 0.11.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/69c09ae...2e477dd))

### Enhancements made

- [MRG] Allow absolute paths in build_script_files [#681](https://github.com/jupyterhub/repo2docker/pull/681) ([@Xarthisius](https://github.com/Xarthisius))

### Maintenance and upkeep improvements

- adduser: useradd --no-log-init to reduce lastlog size [#804](https://github.com/jupyterhub/repo2docker/pull/804) ([@manics](https://github.com/manics))
- [MRG] Bumped conda version to 4.7.12 [#802](https://github.com/jupyterhub/repo2docker/pull/802) ([@davidrpugh](https://github.com/davidrpugh))
- Use port 80 to download GPG keys to avoid firewall problems [#797](https://github.com/jupyterhub/repo2docker/pull/797) ([@betatim](https://github.com/betatim))
- [MRG] Update nteract-on-jupyter to 2.1.3 [#794](https://github.com/jupyterhub/repo2docker/pull/794) ([@betatim](https://github.com/betatim))
- use getpass.getuser instead of os.getlogin [#789](https://github.com/jupyterhub/repo2docker/pull/789) ([@minrk](https://github.com/minrk))
- Add baseline infra for Azure Pipelines [#787](https://github.com/jupyterhub/repo2docker/pull/787) ([@willingc](https://github.com/willingc))
- [MRG] Restore the hooks directory when building the docker image [#786](https://github.com/jupyterhub/repo2docker/pull/786) ([@betatim](https://github.com/betatim))
- Add script to compare Dockerfiles generated by current and older… [#785](https://github.com/jupyterhub/repo2docker/pull/785) ([@nuest](https://github.com/nuest))
- Print Dockerfile to stdout when --no-build [#784](https://github.com/jupyterhub/repo2docker/pull/784) ([@minrk](https://github.com/minrk))
- add hooks to dockerignore [#782](https://github.com/jupyterhub/repo2docker/pull/782) ([@minrk](https://github.com/minrk))
- add explicit log message on failing Docker connection [#779](https://github.com/jupyterhub/repo2docker/pull/779) ([@nuest](https://github.com/nuest))
- [WIP] Upgrade IRKernel version to 1.0.2 [#770](https://github.com/jupyterhub/repo2docker/pull/770) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Bump Miniconda from 4.6.14 to 4.7.10 [#769](https://github.com/jupyterhub/repo2docker/pull/769) ([@davidrpugh](https://github.com/davidrpugh))
- Add support for Julia 1.2.0 [#768](https://github.com/jupyterhub/repo2docker/pull/768) ([@davidanthoff](https://github.com/davidanthoff))
- include full docker progress events in push progress events [#727](https://github.com/jupyterhub/repo2docker/pull/727) ([@minrk](https://github.com/minrk))

### Documentation improvements

- [MRG] Add docs for Figshare and Dataverse; update Dataverse installations file formatting [#796](https://github.com/jupyterhub/repo2docker/pull/796) ([@nuest](https://github.com/nuest))
- Provide help text for commandline arguments [#517](https://github.com/jupyterhub/repo2docker/pull/517) ([@yuvipanda](https://github.com/yuvipanda))

### Other merged PRs

- [MRG] Update changelog for 0.11.0 [#842](https://github.com/jupyterhub/repo2docker/pull/842) ([@betatim](https://github.com/betatim))
- Merge pull request #840 from minrk/py38 [#840](https://github.com/jupyterhub/repo2docker/pull/840) ([@minrk](https://github.com/minrk))
- [MRG] update base environment [#839](https://github.com/jupyterhub/repo2docker/pull/839) ([@minrk](https://github.com/minrk))
- Start RStudio if R is installed via conda [#838](https://github.com/jupyterhub/repo2docker/pull/838) ([@xhochy](https://github.com/xhochy))
- Merge pull request #834 from GeorgianaElena/new_badge [#834](https://github.com/jupyterhub/repo2docker/pull/834) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Add support for Julia 1.3.1 [#831](https://github.com/jupyterhub/repo2docker/pull/831) ([@davidanthoff](https://github.com/davidanthoff))
- [WIP] r build-pack: when using ppa install r-recommended [#830](https://github.com/jupyterhub/repo2docker/pull/830) ([@manics](https://github.com/manics))
- [MRG] Deprecate legacy buildpack [#829](https://github.com/jupyterhub/repo2docker/pull/829) ([@betatim](https://github.com/betatim))
- [MRG] Fix a broken link, update favicon [#826](https://github.com/jupyterhub/repo2docker/pull/826) ([@betatim](https://github.com/betatim))
- adding instructions for contentprovider extension [#824](https://github.com/jupyterhub/repo2docker/pull/824) ([@choldgraf](https://github.com/choldgraf))
- Add support for Julia 1.0.5 and 1.3.0 [#822](https://github.com/jupyterhub/repo2docker/pull/822) ([@davidanthoff](https://github.com/davidanthoff))
- updating theme to pandas sphinx [#816](https://github.com/jupyterhub/repo2docker/pull/816) ([@choldgraf](https://github.com/choldgraf))
- [MRG] Fixes link rendering [#811](https://github.com/jupyterhub/repo2docker/pull/811) ([@arokem](https://github.com/arokem))
- [MRG] Remove explicit checkout when ref given [#810](https://github.com/jupyterhub/repo2docker/pull/810) ([@betatim](https://github.com/betatim))
- [MRG] Fix submodule check out [#809](https://github.com/jupyterhub/repo2docker/pull/809) ([@davidbrochart](https://github.com/davidbrochart))
- [MRG] add Hydroshare as a content provider [#800](https://github.com/jupyterhub/repo2docker/pull/800) ([@sblack-usu](https://github.com/sblack-usu))
- [MRG] Add support for installing different versions of R [#772](https://github.com/jupyterhub/repo2docker/pull/772) ([@betatim](https://github.com/betatim))
- Handle different file encodings [#771](https://github.com/jupyterhub/repo2docker/pull/771) ([@GeorgianaElena](https://github.com/GeorgianaElena))
- Tiny typo in docs/source/index.rst [#760](https://github.com/jupyterhub/repo2docker/pull/760) ([@AartGoossens](https://github.com/AartGoossens))
- [MRG] Dataverse content provider [#739](https://github.com/jupyterhub/repo2docker/pull/739) ([@Xarthisius](https://github.com/Xarthisius))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2019-08-07&to=2020-02-05&type=c))

[@AartGoossens](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AAartGoossens+updated%3A2019-08-07..2020-02-05&type=Issues) | [@andrewjohnlowe](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aandrewjohnlowe+updated%3A2019-08-07..2020-02-05&type=Issues) | [@arokem](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aarokem+updated%3A2019-08-07..2020-02-05&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2019-08-07..2020-02-05&type=Issues) | [@cboettig](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acboettig+updated%3A2019-08-07..2020-02-05&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2019-08-07..2020-02-05&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2019-08-07..2020-02-05&type=Issues) | [@daroczig](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adaroczig+updated%3A2019-08-07..2020-02-05&type=Issues) | [@davidanthoff](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adavidanthoff+updated%3A2019-08-07..2020-02-05&type=Issues) | [@davidbrochart](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adavidbrochart+updated%3A2019-08-07..2020-02-05&type=Issues) | [@davidrpugh](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adavidrpugh+updated%3A2019-08-07..2020-02-05&type=Issues) | [@dlowenberg](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adlowenberg+updated%3A2019-08-07..2020-02-05&type=Issues) | [@DominikGlodzik](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ADominikGlodzik+updated%3A2019-08-07..2020-02-05&type=Issues) | [@GeorgianaElena](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AGeorgianaElena+updated%3A2019-08-07..2020-02-05&type=Issues) | [@jchesterpivotal](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajchesterpivotal+updated%3A2019-08-07..2020-02-05&type=Issues) | [@jdblischak](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajdblischak+updated%3A2019-08-07..2020-02-05&type=Issues) | [@jhamman](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajhamman+updated%3A2019-08-07..2020-02-05&type=Issues) | [@juanesarango](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajuanesarango+updated%3A2019-08-07..2020-02-05&type=Issues) | [@jzf2101](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajzf2101+updated%3A2019-08-07..2020-02-05&type=Issues) | [@karthik](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Akarthik+updated%3A2019-08-07..2020-02-05&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2019-08-07..2020-02-05&type=Issues) | [@meeseeksmachine](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ameeseeksmachine+updated%3A2019-08-07..2020-02-05&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2019-08-07..2020-02-05&type=Issues) | [@NHDaly](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ANHDaly+updated%3A2019-08-07..2020-02-05&type=Issues) | [@nuest](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Anuest+updated%3A2019-08-07..2020-02-05&type=Issues) | [@pablobernabeu](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apablobernabeu+updated%3A2019-08-07..2020-02-05&type=Issues) | [@pat-s](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apat-s+updated%3A2019-08-07..2020-02-05&type=Issues) | [@pdurbin](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apdurbin+updated%3A2019-08-07..2020-02-05&type=Issues) | [@psychemedia](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apsychemedia+updated%3A2019-08-07..2020-02-05&type=Issues) | [@rdbisme](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ardbisme+updated%3A2019-08-07..2020-02-05&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aryanlovett+updated%3A2019-08-07..2020-02-05&type=Issues) | [@saulshanabrook](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asaulshanabrook+updated%3A2019-08-07..2020-02-05&type=Issues) | [@sblack-usu](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asblack-usu+updated%3A2019-08-07..2020-02-05&type=Issues) | [@scottyhq](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ascottyhq+updated%3A2019-08-07..2020-02-05&type=Issues) | [@trallard](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atrallard+updated%3A2019-08-07..2020-02-05&type=Issues) | [@travigd](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atravigd+updated%3A2019-08-07..2020-02-05&type=Issues) | [@willingc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awillingc+updated%3A2019-08-07..2020-02-05&type=Issues) | [@Xarthisius](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AXarthisius+updated%3A2019-08-07..2020-02-05&type=Issues) | [@xhochy](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Axhochy+updated%3A2019-08-07..2020-02-05&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2019-08-07..2020-02-05&type=Issues)

## 0.10.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/734664a...69c09ae))

### Enhancements made

- [MRG/REVIEW] Support Pipfile / Pipfile.lock with pipenv [#649](https://github.com/jupyterhub/repo2docker/pull/649) ([@consideRatio](https://github.com/consideRatio))

### Maintenance and upkeep improvements

- [MRG] Rewrite tests in test_semver.py #615 [#757](https://github.com/jupyterhub/repo2docker/pull/757) ([@Geektrovert](https://github.com/Geektrovert))
- [MRG] switch pip packages to conda-forge in conda buildpack [#728](https://github.com/jupyterhub/repo2docker/pull/728) ([@scottyhq](https://github.com/scottyhq))

### Other merged PRs

- [MRG] Call parent preassemble scripts methods [#752](https://github.com/jupyterhub/repo2docker/pull/752) ([@betatim](https://github.com/betatim))
- parse pipfiles to determine Python version [#748](https://github.com/jupyterhub/repo2docker/pull/748) ([@minrk](https://github.com/minrk))
- typo in doi regexp [#746](https://github.com/jupyterhub/repo2docker/pull/746) ([@minrk](https://github.com/minrk))
- refreeze 2019-07-16 [#745](https://github.com/jupyterhub/repo2docker/pull/745) ([@minrk](https://github.com/minrk))
- [MRG] preassembly for conda/python [#743](https://github.com/jupyterhub/repo2docker/pull/743) ([@minrk](https://github.com/minrk))
- [MRG] Adding bash to Dockerfile to fix git-credential-env [#738](https://github.com/jupyterhub/repo2docker/pull/738) ([@eexwhyzee](https://github.com/eexwhyzee))
- bump xeus-cling in tests [#735](https://github.com/jupyterhub/repo2docker/pull/735) ([@minrk](https://github.com/minrk))
- [MRG] Switch to binder-examples/requirements for our tests [#732](https://github.com/jupyterhub/repo2docker/pull/732) ([@betatim](https://github.com/betatim))
- [MRG] Remove print statement and unused import [#730](https://github.com/jupyterhub/repo2docker/pull/730) ([@betatim](https://github.com/betatim))
- [MRG] Handle root user case more gracefully. Fixes #696 [#723](https://github.com/jupyterhub/repo2docker/pull/723) ([@Xarthisius](https://github.com/Xarthisius))
- Update target_repo_dir docstring [#721](https://github.com/jupyterhub/repo2docker/pull/721) ([@fmaussion](https://github.com/fmaussion))
- [WIP] Version bump Conda from 4.6.14 to 4.7.5 [#719](https://github.com/jupyterhub/repo2docker/pull/719) ([@davidrpugh](https://github.com/davidrpugh))
- [MRG] Install APT packages before copying the repo contents [#716](https://github.com/jupyterhub/repo2docker/pull/716) ([@betatim](https://github.com/betatim))
- updated link for the community edition of docker [#715](https://github.com/jupyterhub/repo2docker/pull/715) ([@johnjarmitage](https://github.com/johnjarmitage))
- Revert "[MRG] Remove more files during the image build to slimdown the image" [#712](https://github.com/jupyterhub/repo2docker/pull/712) ([@betatim](https://github.com/betatim))
- Add support for julia 1.0.4 and 1.1.1 [#710](https://github.com/jupyterhub/repo2docker/pull/710) ([@davidanthoff](https://github.com/davidanthoff))
- [MRG] Remove more files during the image build to slimdown the image [#709](https://github.com/jupyterhub/repo2docker/pull/709) ([@betatim](https://github.com/betatim))
- base docker image on alpine [#705](https://github.com/jupyterhub/repo2docker/pull/705) ([@minrk](https://github.com/minrk))
- [MRG] Generalize Zenodo content provider to support other Invenio repositories [#704](https://github.com/jupyterhub/repo2docker/pull/704) ([@tmorrell](https://github.com/tmorrell))
- add `git-lfs` to dockerfile used for the repo2docker image [#703](https://github.com/jupyterhub/repo2docker/pull/703) ([@minrk](https://github.com/minrk))
- [MRG] Add auto-formatting setup [#699](https://github.com/jupyterhub/repo2docker/pull/699) ([@betatim](https://github.com/betatim))
- [MRG] Update verification of Node install [#695](https://github.com/jupyterhub/repo2docker/pull/695) ([@betatim](https://github.com/betatim))
- [MRG] Zenodo content provider [#693](https://github.com/jupyterhub/repo2docker/pull/693) ([@betatim](https://github.com/betatim))
- Adding contentprovider documentation [#692](https://github.com/jupyterhub/repo2docker/pull/692) ([@choldgraf](https://github.com/choldgraf))
- set CONDA_DEFAULT_ENV [#690](https://github.com/jupyterhub/repo2docker/pull/690) ([@minrk](https://github.com/minrk))
- Switch Travis CI to Ubuntu Xenial 16.04 [#689](https://github.com/jupyterhub/repo2docker/pull/689) ([@jrbourbeau](https://github.com/jrbourbeau))
- [MRG] Drop support for Python 3.4 [#684](https://github.com/jupyterhub/repo2docker/pull/684) ([@betatim](https://github.com/betatim))
- [MRG] Use getpass instead of pwd to fetch username [#683](https://github.com/jupyterhub/repo2docker/pull/683) ([@betatim](https://github.com/betatim))
- Do not try to build the image with root as the primary user [#679](https://github.com/jupyterhub/repo2docker/pull/679) ([@Xarthisius](https://github.com/Xarthisius))
- Revert "[MRG] Do not try to build the image with root as the primary user." [#678](https://github.com/jupyterhub/repo2docker/pull/678) ([@betatim](https://github.com/betatim))
- [MRG] Update base image used for memory limit checks [#677](https://github.com/jupyterhub/repo2docker/pull/677) ([@betatim](https://github.com/betatim))
- [MRG] Do not try to build the image with root as the primary user. [#676](https://github.com/jupyterhub/repo2docker/pull/676) ([@Xarthisius](https://github.com/Xarthisius))
- bumping release date [#669](https://github.com/jupyterhub/repo2docker/pull/669) ([@choldgraf](https://github.com/choldgraf))
- [MRG] release info updates [#668](https://github.com/jupyterhub/repo2docker/pull/668) ([@choldgraf](https://github.com/choldgraf))
- [MRG] Remove the conda package cache as we can't hardlink to it [#666](https://github.com/jupyterhub/repo2docker/pull/666) ([@betatim](https://github.com/betatim))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2019-05-05&to=2019-08-07&type=c))

[@AliMirlou](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AAliMirlou+updated%3A2019-05-05..2019-08-07&type=Issues) | [@arnavs](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aarnavs+updated%3A2019-05-05..2019-08-07&type=Issues) | [@arokem](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aarokem+updated%3A2019-05-05..2019-08-07&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2019-05-05..2019-08-07&type=Issues) | [@cboettig](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acboettig+updated%3A2019-05-05..2019-08-07&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2019-05-05..2019-08-07&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2019-05-05..2019-08-07&type=Issues) | [@davidanthoff](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adavidanthoff+updated%3A2019-05-05..2019-08-07&type=Issues) | [@davidrpugh](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adavidrpugh+updated%3A2019-05-05..2019-08-07&type=Issues) | [@eexwhyzee](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aeexwhyzee+updated%3A2019-05-05..2019-08-07&type=Issues) | [@fmaussion](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Afmaussion+updated%3A2019-05-05..2019-08-07&type=Issues) | [@Geektrovert](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AGeektrovert+updated%3A2019-05-05..2019-08-07&type=Issues) | [@henchc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ahenchc+updated%3A2019-05-05..2019-08-07&type=Issues) | [@jchesterpivotal](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajchesterpivotal+updated%3A2019-05-05..2019-08-07&type=Issues) | [@jlperla](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajlperla+updated%3A2019-05-05..2019-08-07&type=Issues) | [@johnjarmitage](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajohnjarmitage+updated%3A2019-05-05..2019-08-07&type=Issues) | [@jrbourbeau](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajrbourbeau+updated%3A2019-05-05..2019-08-07&type=Issues) | [@jzf2101](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajzf2101+updated%3A2019-05-05..2019-08-07&type=Issues) | [@mael-le-gal](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amael-le-gal+updated%3A2019-05-05..2019-08-07&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2019-05-05..2019-08-07&type=Issues) | [@MattF-NSIDC](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AMattF-NSIDC+updated%3A2019-05-05..2019-08-07&type=Issues) | [@meeseeksmachine](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ameeseeksmachine+updated%3A2019-05-05..2019-08-07&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2019-05-05..2019-08-07&type=Issues) | [@nuest](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Anuest+updated%3A2019-05-05..2019-08-07&type=Issues) | [@pdurbin](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apdurbin+updated%3A2019-05-05..2019-08-07&type=Issues) | [@psychemedia](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apsychemedia+updated%3A2019-05-05..2019-08-07&type=Issues) | [@saulshanabrook](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asaulshanabrook+updated%3A2019-05-05..2019-08-07&type=Issues) | [@scopatz](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ascopatz+updated%3A2019-05-05..2019-08-07&type=Issues) | [@scottyhq](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ascottyhq+updated%3A2019-05-05..2019-08-07&type=Issues) | [@sgibson91](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asgibson91+updated%3A2019-05-05..2019-08-07&type=Issues) | [@SylvainCorlay](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ASylvainCorlay+updated%3A2019-05-05..2019-08-07&type=Issues) | [@tmorrell](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atmorrell+updated%3A2019-05-05..2019-08-07&type=Issues) | [@trallard](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atrallard+updated%3A2019-05-05..2019-08-07&type=Issues) | [@willingc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awillingc+updated%3A2019-05-05..2019-08-07&type=Issues) | [@Xarthisius](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AXarthisius+updated%3A2019-05-05..2019-08-07&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2019-05-05..2019-08-07&type=Issues) | [@zmackie](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Azmackie+updated%3A2019-05-05..2019-08-07&type=Issues)

## 0.9.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/b6c4e7e...734664a))

### Merged PRs

- [MRG] Update change log in preparation for releasing v0.9.0 [#664](https://github.com/jupyterhub/repo2docker/pull/664) ([@betatim](https://github.com/betatim))
- tweak language to make clear `exec "$@"` works [#663](https://github.com/jupyterhub/repo2docker/pull/663) ([@fomightez](https://github.com/fomightez))
- specification info page [#662](https://github.com/jupyterhub/repo2docker/pull/662) ([@choldgraf](https://github.com/choldgraf))
- add note to changelog [#659](https://github.com/jupyterhub/repo2docker/pull/659) ([@jhamman](https://github.com/jhamman))
- Make sure ENTRYPOINT is an absolute path [#657](https://github.com/jupyterhub/repo2docker/pull/657) ([@yuvipanda](https://github.com/yuvipanda))
- [MRG] Update contributing guidelines and issue templates [#655](https://github.com/jupyterhub/repo2docker/pull/655) ([@KirstieJane](https://github.com/KirstieJane))
- [MRG] Update issue templates [#654](https://github.com/jupyterhub/repo2docker/pull/654) ([@betatim](https://github.com/betatim))
- Support .binder directory [#653](https://github.com/jupyterhub/repo2docker/pull/653) ([@jhamman](https://github.com/jhamman))
- [MRG] Fix handling of memory limit command line argument [#652](https://github.com/jupyterhub/repo2docker/pull/652) ([@betatim](https://github.com/betatim))
- [MRG] install notebook in its own env [#651](https://github.com/jupyterhub/repo2docker/pull/651) ([@minrk](https://github.com/minrk))
- [MRG] Bump nteract-on-jupyter to 2.0.12 and notebook to 5.7.8 [#650](https://github.com/jupyterhub/repo2docker/pull/650) ([@betatim](https://github.com/betatim))
- [MRG] Unpin pip again [#647](https://github.com/jupyterhub/repo2docker/pull/647) ([@betatim](https://github.com/betatim))
- [MRG] Fix up the server proxy package to get websockets back [#646](https://github.com/jupyterhub/repo2docker/pull/646) ([@betatim](https://github.com/betatim))
- mentioning s2i in faq [#642](https://github.com/jupyterhub/repo2docker/pull/642) ([@choldgraf](https://github.com/choldgraf))
- [MRG] Update change log [#641](https://github.com/jupyterhub/repo2docker/pull/641) ([@betatim](https://github.com/betatim))
- [MRG] Fix sphinx deprecation for recommonmark [#640](https://github.com/jupyterhub/repo2docker/pull/640) ([@betatim](https://github.com/betatim))
- [MRG] Ensure git submodules are updated and initialized [#639](https://github.com/jupyterhub/repo2docker/pull/639) ([@djhoese](https://github.com/djhoese))
- [MRG] Remove conda package directory [#638](https://github.com/jupyterhub/repo2docker/pull/638) ([@betatim](https://github.com/betatim))
- [MRG] Update the source links used by the legacy buildpack [#633](https://github.com/jupyterhub/repo2docker/pull/633) ([@betatim](https://github.com/betatim))
- [MRG] Python 3.7 as the default in the docs [#631](https://github.com/jupyterhub/repo2docker/pull/631) ([@jtpio](https://github.com/jtpio))
- [MRG] Bump notebook package version [#628](https://github.com/jupyterhub/repo2docker/pull/628) ([@betatim](https://github.com/betatim))
- [MRG] Add issue template [#624](https://github.com/jupyterhub/repo2docker/pull/624) ([@betatim](https://github.com/betatim))
- [MRG] Julia: Two small doc updates [#623](https://github.com/jupyterhub/repo2docker/pull/623) ([@fredrikekre](https://github.com/fredrikekre))
- Install IJulia kernel into proper directory [#622](https://github.com/jupyterhub/repo2docker/pull/622) ([@davidanthoff](https://github.com/davidanthoff))
- added some debug for R shiny [#614](https://github.com/jupyterhub/repo2docker/pull/614) ([@drmowinckels](https://github.com/drmowinckels))
- [MRG] Add tests for Julia semver matching [#613](https://github.com/jupyterhub/repo2docker/pull/613) ([@betatim](https://github.com/betatim))
- Use JULIA_PROJECT env variable to activate julia env [#612](https://github.com/jupyterhub/repo2docker/pull/612) ([@davidanthoff](https://github.com/davidanthoff))
- [MRG] Add PR template with links to contrib docs and less focus on code contributions [#607](https://github.com/jupyterhub/repo2docker/pull/607) ([@betatim](https://github.com/betatim))
- [MRG] Reopen change log [#606](https://github.com/jupyterhub/repo2docker/pull/606) ([@betatim](https://github.com/betatim))
- [MRG] Add FAQ entry and Howto on exporting conda environments [#598](https://github.com/jupyterhub/repo2docker/pull/598) ([@betatim](https://github.com/betatim))
- [MRG] Add tests for setting Python version during freeze [#592](https://github.com/jupyterhub/repo2docker/pull/592) ([@betatim](https://github.com/betatim))
- Fix release date of 0.8.0 [#590](https://github.com/jupyterhub/repo2docker/pull/590) ([@betatim](https://github.com/betatim))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2019-02-21&to=2019-05-05&type=c))

[@alimanfoo](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aalimanfoo+updated%3A2019-02-21..2019-05-05&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2019-02-21..2019-05-05&type=Issues) | [@captainsafia](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acaptainsafia+updated%3A2019-02-21..2019-05-05&type=Issues) | [@cboettig](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acboettig+updated%3A2019-02-21..2019-05-05&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2019-02-21..2019-05-05&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2019-02-21..2019-05-05&type=Issues) | [@davidanthoff](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adavidanthoff+updated%3A2019-02-21..2019-05-05&type=Issues) | [@djhoese](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adjhoese+updated%3A2019-02-21..2019-05-05&type=Issues) | [@drmowinckels](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adrmowinckels+updated%3A2019-02-21..2019-05-05&type=Issues) | [@fomightez](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Afomightez+updated%3A2019-02-21..2019-05-05&type=Issues) | [@fredrikekre](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Afredrikekre+updated%3A2019-02-21..2019-05-05&type=Issues) | [@Geektrovert](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AGeektrovert+updated%3A2019-02-21..2019-05-05&type=Issues) | [@jdblischak](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajdblischak+updated%3A2019-02-21..2019-05-05&type=Issues) | [@jhamman](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajhamman+updated%3A2019-02-21..2019-05-05&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajtpio+updated%3A2019-02-21..2019-05-05&type=Issues) | [@karthik](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Akarthik+updated%3A2019-02-21..2019-05-05&type=Issues) | [@KirstieJane](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AKirstieJane+updated%3A2019-02-21..2019-05-05&type=Issues) | [@LucianaMarques](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ALucianaMarques+updated%3A2019-02-21..2019-05-05&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2019-02-21..2019-05-05&type=Issues) | [@meeseeksmachine](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ameeseeksmachine+updated%3A2019-02-21..2019-05-05&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2019-02-21..2019-05-05&type=Issues) | [@NHDaly](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ANHDaly+updated%3A2019-02-21..2019-05-05&type=Issues) | [@nuest](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Anuest+updated%3A2019-02-21..2019-05-05&type=Issues) | [@pat-s](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apat-s+updated%3A2019-02-21..2019-05-05&type=Issues) | [@rabernat](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Arabernat+updated%3A2019-02-21..2019-05-05&type=Issues) | [@rgbkrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Argbkrk+updated%3A2019-02-21..2019-05-05&type=Issues) | [@trallard](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atrallard+updated%3A2019-02-21..2019-05-05&type=Issues) | [@willingc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awillingc+updated%3A2019-02-21..2019-05-05&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2019-02-21..2019-05-05&type=Issues)

## 0.8.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/72d7634...b6c4e7e))

### Merged PRs

- Fix release date of 0.8.0 [#590](https://github.com/jupyterhub/repo2docker/pull/590) ([@betatim](https://github.com/betatim))
- Fix up double label trouble in the config file docs [#588](https://github.com/jupyterhub/repo2docker/pull/588) ([@betatim](https://github.com/betatim))
- fix "Possible nested set" warning [#587](https://github.com/jupyterhub/repo2docker/pull/587) ([@minrk](https://github.com/minrk))
- regen Pipfile.lock [#586](https://github.com/jupyterhub/repo2docker/pull/586) ([@minrk](https://github.com/minrk))
- [MRG] Update documentation with more cross references [#585](https://github.com/jupyterhub/repo2docker/pull/585) ([@betatim](https://github.com/betatim))
- install: one-liner to install most recent upstream code [#583](https://github.com/jupyterhub/repo2docker/pull/583) ([@haraldschilly](https://github.com/haraldschilly))
- pin conda during Python-switch step [#576](https://github.com/jupyterhub/repo2docker/pull/576) ([@minrk](https://github.com/minrk))
- Check if '--debug' is set properly [#575](https://github.com/jupyterhub/repo2docker/pull/575) ([@yuvipanda](https://github.com/yuvipanda))
- npm installation [#573](https://github.com/jupyterhub/repo2docker/pull/573) ([@GladysNalvarte](https://github.com/GladysNalvarte))
- missing quotes in GIT_CREDENTIAL_ENV [#572](https://github.com/jupyterhub/repo2docker/pull/572) ([@minrk](https://github.com/minrk))
- Update conf.py [#569](https://github.com/jupyterhub/repo2docker/pull/569) ([@lheagy](https://github.com/lheagy))
- updating interfaces page and adding jupyterlab workspaces page [#568](https://github.com/jupyterhub/repo2docker/pull/568) ([@choldgraf](https://github.com/choldgraf))
- fix docker commit tag [#562](https://github.com/jupyterhub/repo2docker/pull/562) ([@minrk](https://github.com/minrk))
- Set JULIA_DEPOT_PATH [#555](https://github.com/jupyterhub/repo2docker/pull/555) ([@yuvipanda](https://github.com/yuvipanda))
- Updated log info for local content provider [#551](https://github.com/jupyterhub/repo2docker/pull/551) ([@GladysNalvarte](https://github.com/GladysNalvarte))
- Fixes Travis build errors related to pytest and Sphinx  [#547](https://github.com/jupyterhub/repo2docker/pull/547) ([@craig-willis](https://github.com/craig-willis))
- Spurious comment in `Dockerfile` #543 [#544](https://github.com/jupyterhub/repo2docker/pull/544) ([@benjaminr](https://github.com/benjaminr))
- Bump default python version to 3.7 [#539](https://github.com/jupyterhub/repo2docker/pull/539) ([@yuvipanda](https://github.com/yuvipanda))
- Use a minimal hand-crafted Dockerfile for speed [#536](https://github.com/jupyterhub/repo2docker/pull/536) ([@betatim](https://github.com/betatim))
- [MRG] Add tests for port mapping conversion [#534](https://github.com/jupyterhub/repo2docker/pull/534) ([@betatim](https://github.com/betatim))
- adding a roadmap link to the root [#532](https://github.com/jupyterhub/repo2docker/pull/532) ([@choldgraf](https://github.com/choldgraf))
- Minor howto doc fixes [#531](https://github.com/jupyterhub/repo2docker/pull/531) ([@jrbourbeau](https://github.com/jrbourbeau))
- fix commit hash truncation on docker images [#530](https://github.com/jupyterhub/repo2docker/pull/530) ([@minrk](https://github.com/minrk))
- Run docker builds on docker hub [#527](https://github.com/jupyterhub/repo2docker/pull/527) ([@minrk](https://github.com/minrk))
- Add tag command snippet [#526](https://github.com/jupyterhub/repo2docker/pull/526) ([@minrk](https://github.com/minrk))
- Remove f-strings [#520](https://github.com/jupyterhub/repo2docker/pull/520) ([@jrbourbeau](https://github.com/jrbourbeau))
- refreeze with notebook 5.7.4 [#519](https://github.com/jupyterhub/repo2docker/pull/519) ([@minrk](https://github.com/minrk))
- Update RTD to install repo2docker [#518](https://github.com/jupyterhub/repo2docker/pull/518) ([@jrbourbeau](https://github.com/jrbourbeau))
- Fix cache-busting when running tests locally [#509](https://github.com/jupyterhub/repo2docker/pull/509) ([@yuvipanda](https://github.com/yuvipanda))
- Copy repo to ${REPO_DIR} rather than ${HOME} [#507](https://github.com/jupyterhub/repo2docker/pull/507) ([@yuvipanda](https://github.com/yuvipanda))
- Fix typos and syntax errors in the documentation [#505](https://github.com/jupyterhub/repo2docker/pull/505) ([@betatim](https://github.com/betatim))
- fix push-tags condition [#501](https://github.com/jupyterhub/repo2docker/pull/501) ([@minrk](https://github.com/minrk))
- Add repo2docker Dockerfile labels [#500](https://github.com/jupyterhub/repo2docker/pull/500) ([@jrbourbeau](https://github.com/jrbourbeau))
- push tagged images on travis [#499](https://github.com/jupyterhub/repo2docker/pull/499) ([@minrk](https://github.com/minrk))
- Update changelog in preparation for releasing v0.7.0 [#498](https://github.com/jupyterhub/repo2docker/pull/498) ([@betatim](https://github.com/betatim))
- Make repo2docker easier to use as a library - Part 1 [#496](https://github.com/jupyterhub/repo2docker/pull/496) ([@yuvipanda](https://github.com/yuvipanda))
- Make apt-get install be quiet [#483](https://github.com/jupyterhub/repo2docker/pull/483) ([@yuvipanda](https://github.com/yuvipanda))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2018-12-12&to=2019-02-21&type=c))

[@alimanfoo](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aalimanfoo+updated%3A2018-12-12..2019-02-21&type=Issues) | [@annakrystalli](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aannakrystalli+updated%3A2018-12-12..2019-02-21&type=Issues) | [@benjaminr](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abenjaminr+updated%3A2018-12-12..2019-02-21&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2018-12-12..2019-02-21&type=Issues) | [@captainsafia](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acaptainsafia+updated%3A2018-12-12..2019-02-21&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2018-12-12..2019-02-21&type=Issues) | [@craig-willis](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acraig-willis+updated%3A2018-12-12..2019-02-21&type=Issues) | [@GladysNalvarte](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AGladysNalvarte+updated%3A2018-12-12..2019-02-21&type=Issues) | [@haraldschilly](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aharaldschilly+updated%3A2018-12-12..2019-02-21&type=Issues) | [@jrbourbeau](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajrbourbeau+updated%3A2018-12-12..2019-02-21&type=Issues) | [@lheagy](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Alheagy+updated%3A2018-12-12..2019-02-21&type=Issues) | [@LucianaMarques](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ALucianaMarques+updated%3A2018-12-12..2019-02-21&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2018-12-12..2019-02-21&type=Issues) | [@MatthewBM](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AMatthewBM+updated%3A2018-12-12..2019-02-21&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2018-12-12..2019-02-21&type=Issues) | [@psychemedia](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apsychemedia+updated%3A2018-12-12..2019-02-21&type=Issues) | [@rgbkrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Argbkrk+updated%3A2018-12-12..2019-02-21&type=Issues) | [@VladimirVisnovsky](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AVladimirVisnovsky+updated%3A2018-12-12..2019-02-21&type=Issues) | [@WillKoehrsen](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AWillKoehrsen+updated%3A2018-12-12..2019-02-21&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2018-12-12..2019-02-21&type=Issues)

## 0.7.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/1b8e16a...72d7634))

### Merged PRs

- Update changelog in preparation for releasing v0.7.0 [#498](https://github.com/jupyterhub/repo2docker/pull/498) ([@betatim](https://github.com/betatim))
- Remove duplicate codecov config [#495](https://github.com/jupyterhub/repo2docker/pull/495) ([@betatim](https://github.com/betatim))
- Bump nbrsessionproxy version [#493](https://github.com/jupyterhub/repo2docker/pull/493) ([@yuvipanda](https://github.com/yuvipanda))
- Add codecov configuration [#492](https://github.com/jupyterhub/repo2docker/pull/492) ([@betatim](https://github.com/betatim))
- Update the roadmap [#491](https://github.com/jupyterhub/repo2docker/pull/491) ([@betatim](https://github.com/betatim))
- Log a 'success' message when push is complete [#482](https://github.com/jupyterhub/repo2docker/pull/482) ([@yuvipanda](https://github.com/yuvipanda))
- Revert "[MRG] Start reusing existing docker images if content hasn't changed" [#481](https://github.com/jupyterhub/repo2docker/pull/481) ([@yuvipanda](https://github.com/yuvipanda))
- Make apt be quieter [#479](https://github.com/jupyterhub/repo2docker/pull/479) ([@yuvipanda](https://github.com/yuvipanda))
- Allow specifying images to reuse cache from [#478](https://github.com/jupyterhub/repo2docker/pull/478) ([@yuvipanda](https://github.com/yuvipanda))
- removing note that env.yml is needed for julia [#477](https://github.com/jupyterhub/repo2docker/pull/477) ([@choldgraf](https://github.com/choldgraf))
- [MRG] Tweak docstring to make it more understandable [#474](https://github.com/jupyterhub/repo2docker/pull/474) ([@betatim](https://github.com/betatim))
- Ensure Python3 before reading README with encoding arg [#472](https://github.com/jupyterhub/repo2docker/pull/472) ([@nokome](https://github.com/nokome))
- Add space between logo and title in README [#468](https://github.com/jupyterhub/repo2docker/pull/468) ([@willingc](https://github.com/willingc))
- Add jupyterhub to base environment [#467](https://github.com/jupyterhub/repo2docker/pull/467) ([@yuvipanda](https://github.com/yuvipanda))
- [MRG] Add a first roadmap [#465](https://github.com/jupyterhub/repo2docker/pull/465) ([@betatim](https://github.com/betatim))
- Update CHANGES.rst [#464](https://github.com/jupyterhub/repo2docker/pull/464) ([@betatim](https://github.com/betatim))
- [MRG] Add and use new logo [#463](https://github.com/jupyterhub/repo2docker/pull/463) ([@betatim](https://github.com/betatim))
- [MRG] Start reusing existing docker images if content hasn't changed [#461](https://github.com/jupyterhub/repo2docker/pull/461) ([@betatim](https://github.com/betatim))
- Updates for Stencila [#457](https://github.com/jupyterhub/repo2docker/pull/457) ([@nuest](https://github.com/nuest))
- Update changelog [#454](https://github.com/jupyterhub/repo2docker/pull/454) ([@betatim](https://github.com/betatim))
- adding back sidebars [#451](https://github.com/jupyterhub/repo2docker/pull/451) ([@choldgraf](https://github.com/choldgraf))
- [MRG] Switch to BaseImage for nix build pack [#448](https://github.com/jupyterhub/repo2docker/pull/448) ([@betatim](https://github.com/betatim))
- [MRG] Pipfile for repo2Docker [#447](https://github.com/jupyterhub/repo2docker/pull/447) ([@trallard](https://github.com/trallard))
- adding circleci preview and jupyterhub docs theme [#446](https://github.com/jupyterhub/repo2docker/pull/446) ([@choldgraf](https://github.com/choldgraf))
- [MRG] Change back into main repository directory [#436](https://github.com/jupyterhub/repo2docker/pull/436) ([@betatim](https://github.com/betatim))
- PEP8 styling [#435](https://github.com/jupyterhub/repo2docker/pull/435) ([@betatim](https://github.com/betatim))
- [MRG] Switch to right sub-directory for coverage reports [#432](https://github.com/jupyterhub/repo2docker/pull/432) ([@betatim](https://github.com/betatim))
- Add pip install doc-requirements.txt to setup of virtual environment instructions [#431](https://github.com/jupyterhub/repo2docker/pull/431) ([@matthewfeickert](https://github.com/matthewfeickert))
- [MRG] Only check beginning of name of Python shared library [#429](https://github.com/jupyterhub/repo2docker/pull/429) ([@betatim](https://github.com/betatim))
- Adjust css for header links [#428](https://github.com/jupyterhub/repo2docker/pull/428) ([@evertrol](https://github.com/evertrol))
- [MRG] Update the contributing docs [#427](https://github.com/jupyterhub/repo2docker/pull/427) ([@betatim](https://github.com/betatim))
- Add a change log [#426](https://github.com/jupyterhub/repo2docker/pull/426) ([@evertrol](https://github.com/evertrol))
- Change faq to rst [#425](https://github.com/jupyterhub/repo2docker/pull/425) ([@evertrol](https://github.com/evertrol))
- Fix documentation: avoid clashing markup [#422](https://github.com/jupyterhub/repo2docker/pull/422) ([@evertrol](https://github.com/evertrol))
- Add an edit-mode option [#421](https://github.com/jupyterhub/repo2docker/pull/421) ([@evertrol](https://github.com/evertrol))
- Speed up cloning by using a depth of 1 if there is no refspec [#420](https://github.com/jupyterhub/repo2docker/pull/420) ([@evertrol](https://github.com/evertrol))
- fix my heading mistake in the docs for DESCRIPTION files [#418](https://github.com/jupyterhub/repo2docker/pull/418) ([@gedankenstuecke](https://github.com/gedankenstuecke))
- Subdirectory support [#413](https://github.com/jupyterhub/repo2docker/pull/413) ([@dsludwig](https://github.com/dsludwig))
- updating index, usage, and install docs [#409](https://github.com/jupyterhub/repo2docker/pull/409) ([@choldgraf](https://github.com/choldgraf))
- Adding support for nix buildpack in repo2docker [#407](https://github.com/jupyterhub/repo2docker/pull/407) ([@costrouc](https://github.com/costrouc))
- add R DESCRIPTION support [#406](https://github.com/jupyterhub/repo2docker/pull/406) ([@gedankenstuecke](https://github.com/gedankenstuecke))
- Support python 3.7 [#405](https://github.com/jupyterhub/repo2docker/pull/405) ([@minrk](https://github.com/minrk))
- [MRG] Make travis fail when pytest fails [#401](https://github.com/jupyterhub/repo2docker/pull/401) ([@betatim](https://github.com/betatim))
- Fix relative location of the start script [#400](https://github.com/jupyterhub/repo2docker/pull/400) ([@giovannipizzi](https://github.com/giovannipizzi))
- Add more details to our setup() command [#394](https://github.com/jupyterhub/repo2docker/pull/394) ([@betatim](https://github.com/betatim))
- Julia v1.0 support: Add option to specify julia version in REQUIRE [#393](https://github.com/jupyterhub/repo2docker/pull/393) ([@NHDaly](https://github.com/NHDaly))
- Bump nteract-on-jupyter version [#390](https://github.com/jupyterhub/repo2docker/pull/390) ([@yuvipanda](https://github.com/yuvipanda))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2018-09-09&to=2018-12-12&type=c))

[@agahkarakuzu](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aagahkarakuzu+updated%3A2018-09-09..2018-12-12&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2018-09-09..2018-12-12&type=Issues) | [@blairhudson](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ablairhudson+updated%3A2018-09-09..2018-12-12&type=Issues) | [@cboettig](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acboettig+updated%3A2018-09-09..2018-12-12&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2018-09-09..2018-12-12&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2018-09-09..2018-12-12&type=Issues) | [@costrouc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acostrouc+updated%3A2018-09-09..2018-12-12&type=Issues) | [@craig-willis](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acraig-willis+updated%3A2018-09-09..2018-12-12&type=Issues) | [@ctr26](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Actr26+updated%3A2018-09-09..2018-12-12&type=Issues) | [@davidanthoff](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adavidanthoff+updated%3A2018-09-09..2018-12-12&type=Issues) | [@dsludwig](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adsludwig+updated%3A2018-09-09..2018-12-12&type=Issues) | [@evertrol](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aevertrol+updated%3A2018-09-09..2018-12-12&type=Issues) | [@gedankenstuecke](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Agedankenstuecke+updated%3A2018-09-09..2018-12-12&type=Issues) | [@giovannipizzi](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Agiovannipizzi+updated%3A2018-09-09..2018-12-12&type=Issues) | [@jhamman](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajhamman+updated%3A2018-09-09..2018-12-12&type=Issues) | [@jzf2101](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajzf2101+updated%3A2018-09-09..2018-12-12&type=Issues) | [@karthik](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Akarthik+updated%3A2018-09-09..2018-12-12&type=Issues) | [@KristofferC](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AKristofferC+updated%3A2018-09-09..2018-12-12&type=Issues) | [@ltalirz](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Altalirz+updated%3A2018-09-09..2018-12-12&type=Issues) | [@ltetrel](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Altetrel+updated%3A2018-09-09..2018-12-12&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2018-09-09..2018-12-12&type=Issues) | [@matthewfeickert](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amatthewfeickert+updated%3A2018-09-09..2018-12-12&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2018-09-09..2018-12-12&type=Issues) | [@NHDaly](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ANHDaly+updated%3A2018-09-09..2018-12-12&type=Issues) | [@nokome](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Anokome+updated%3A2018-09-09..2018-12-12&type=Issues) | [@nuest](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Anuest+updated%3A2018-09-09..2018-12-12&type=Issues) | [@pdurbin](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apdurbin+updated%3A2018-09-09..2018-12-12&type=Issues) | [@psychemedia](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apsychemedia+updated%3A2018-09-09..2018-12-12&type=Issues) | [@rbavery](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Arbavery+updated%3A2018-09-09..2018-12-12&type=Issues) | [@rgbkrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Argbkrk+updated%3A2018-09-09..2018-12-12&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aryanlovett+updated%3A2018-09-09..2018-12-12&type=Issues) | [@spMohanty](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AspMohanty+updated%3A2018-09-09..2018-12-12&type=Issues) | [@tgeorgeux](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atgeorgeux+updated%3A2018-09-09..2018-12-12&type=Issues) | [@trallard](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atrallard+updated%3A2018-09-09..2018-12-12&type=Issues) | [@trybik](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atrybik+updated%3A2018-09-09..2018-12-12&type=Issues) | [@willingc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awillingc+updated%3A2018-09-09..2018-12-12&type=Issues) | [@WillKoehrsen](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AWillKoehrsen+updated%3A2018-09-09..2018-12-12&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2018-09-09..2018-12-12&type=Issues)

## 0.6.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/d97eee9...1b8e16a))

### Documentation improvements

- Add architecture document [#235](https://github.com/jupyterhub/repo2docker/pull/235) ([@yuvipanda](https://github.com/yuvipanda))

### Other merged PRs

- Add more details to our setup() command [#394](https://github.com/jupyterhub/repo2docker/pull/394) ([@betatim](https://github.com/betatim))
- Bump conda version to 4.5.11 [#391](https://github.com/jupyterhub/repo2docker/pull/391) ([@yuvipanda](https://github.com/yuvipanda))
- Issue #388 - Use bash echo for git-credential-env [#389](https://github.com/jupyterhub/repo2docker/pull/389) ([@zymergen-luke](https://github.com/zymergen-luke))
- Change PyPI deploy account to mybinderteam [#385](https://github.com/jupyterhub/repo2docker/pull/385) ([@betatim](https://github.com/betatim))
- [MRG] Update contributing documentation [#384](https://github.com/jupyterhub/repo2docker/pull/384) ([@betatim](https://github.com/betatim))
- Update to JupyterLab 0.34 [#378](https://github.com/jupyterhub/repo2docker/pull/378) ([@blink1073](https://github.com/blink1073))
- [MRG] Escape environment variable when using Python string formatting [#377](https://github.com/jupyterhub/repo2docker/pull/377) ([@betatim](https://github.com/betatim))
- Split out tests, tweak docs, and a style change [#375](https://github.com/jupyterhub/repo2docker/pull/375) ([@betatim](https://github.com/betatim))
- remove conda-meta/history [#373](https://github.com/jupyterhub/repo2docker/pull/373) ([@minrk](https://github.com/minrk))
- Fix warnings in the documentation build and add to CI [#372](https://github.com/jupyterhub/repo2docker/pull/372) ([@betatim](https://github.com/betatim))
- adding message and changing header characters for config files [#370](https://github.com/jupyterhub/repo2docker/pull/370) ([@choldgraf](https://github.com/choldgraf))
- Install nodejs/npm from nodesource [#364](https://github.com/jupyterhub/repo2docker/pull/364) ([@GladysNalvarte](https://github.com/GladysNalvarte))
- Add launch script [#363](https://github.com/jupyterhub/repo2docker/pull/363) ([@jhamman](https://github.com/jhamman))
- Specify custom_display_url argument [#358](https://github.com/jupyterhub/repo2docker/pull/358) ([@GladysNalvarte](https://github.com/GladysNalvarte))
- Switch from PyDataScienceHandbook to Pytudes [#355](https://github.com/jupyterhub/repo2docker/pull/355) ([@betatim](https://github.com/betatim))
- bump versions and refreeze [#354](https://github.com/jupyterhub/repo2docker/pull/354) ([@minrk](https://github.com/minrk))
- [MRG] Add version argument [#352](https://github.com/jupyterhub/repo2docker/pull/352) ([@vsoch](https://github.com/vsoch))
- Add CircleCI Deploy Option [#351](https://github.com/jupyterhub/repo2docker/pull/351) ([@vsoch](https://github.com/vsoch))
- from traitlets import TraitError in utils.py [#348](https://github.com/jupyterhub/repo2docker/pull/348) ([@cclauss](https://github.com/cclauss))
- scinece -> science [#347](https://github.com/jupyterhub/repo2docker/pull/347) ([@danielleberre](https://github.com/danielleberre))
- Fix some rst weirdness in the uage docs [#346](https://github.com/jupyterhub/repo2docker/pull/346) ([@betatim](https://github.com/betatim))
- Add DockerSpawner command in JupyterHub config [#344](https://github.com/jupyterhub/repo2docker/pull/344) ([@rprimet](https://github.com/rprimet))
- Test that images can start notebook servers in all the builders  [#343](https://github.com/jupyterhub/repo2docker/pull/343) ([@GladysNalvarte](https://github.com/GladysNalvarte))
- Setup auto releasing on GitHub tagging [#342](https://github.com/jupyterhub/repo2docker/pull/342) ([@betatim](https://github.com/betatim))
- documentation improvements based on reviews for walkthrough and configuration details [#338](https://github.com/jupyterhub/repo2docker/pull/338) ([@jzf2101](https://github.com/jzf2101))
- Tweaking Docs for Readability  [#335](https://github.com/jupyterhub/repo2docker/pull/335) ([@jzf2101](https://github.com/jzf2101))
- Include LICENSE file in wheels [#327](https://github.com/jupyterhub/repo2docker/pull/327) ([@toddrme2178](https://github.com/toddrme2178))
- Switch to miniconda v4.5.1 [#324](https://github.com/jupyterhub/repo2docker/pull/324) ([@betatim](https://github.com/betatim))
- Support shiny apps [#320](https://github.com/jupyterhub/repo2docker/pull/320) ([@ryanlovett](https://github.com/ryanlovett))
- prefer R to conda in buildpack order [#317](https://github.com/jupyterhub/repo2docker/pull/317) ([@minrk](https://github.com/minrk))
- Use XDG standard ~/.local for user software installs [#313](https://github.com/jupyterhub/repo2docker/pull/313) ([@yuvipanda](https://github.com/yuvipanda))
- To add the user bin folder to the path [#311](https://github.com/jupyterhub/repo2docker/pull/311) ([@aborruso](https://github.com/aborruso))
- stencila support [#309](https://github.com/jupyterhub/repo2docker/pull/309) ([@minrk](https://github.com/minrk))
- Add links to the front page and modify travis [#308](https://github.com/jupyterhub/repo2docker/pull/308) ([@betatim](https://github.com/betatim))
- Bump nteract jupyter extension [#306](https://github.com/jupyterhub/repo2docker/pull/306) ([@yuvipanda](https://github.com/yuvipanda))
- remove _nb_ext_conf from legacy env [#303](https://github.com/jupyterhub/repo2docker/pull/303) ([@minrk](https://github.com/minrk))
- bump base image to ubuntu 18.04 [#302](https://github.com/jupyterhub/repo2docker/pull/302) ([@minrk](https://github.com/minrk))
- Documentation and warning improvements [#300](https://github.com/jupyterhub/repo2docker/pull/300) ([@choldgraf](https://github.com/choldgraf))
- Fix two typos [#299](https://github.com/jupyterhub/repo2docker/pull/299) ([@darabos](https://github.com/darabos))
- Always install Python with conda [#298](https://github.com/jupyterhub/repo2docker/pull/298) ([@minrk](https://github.com/minrk))
- split  post build script command in Docker file [#294](https://github.com/jupyterhub/repo2docker/pull/294) ([@bitnik](https://github.com/bitnik))
- Add guidelines on merging work [#292](https://github.com/jupyterhub/repo2docker/pull/292) ([@betatim](https://github.com/betatim))
- Support setup.py in Python buildpacks [#289](https://github.com/jupyterhub/repo2docker/pull/289) ([@GladysNalvarte](https://github.com/GladysNalvarte))
- Use travis_retry to run tests [#288](https://github.com/jupyterhub/repo2docker/pull/288) ([@betatim](https://github.com/betatim))
- Add a test to select Python 3 via runtime.txt [#287](https://github.com/jupyterhub/repo2docker/pull/287) ([@betatim](https://github.com/betatim))
- Enables Python2 just with runtime.txt file [#284](https://github.com/jupyterhub/repo2docker/pull/284) ([@GladysNalvarte](https://github.com/GladysNalvarte))
- Add note about os support and update example repo [#283](https://github.com/jupyterhub/repo2docker/pull/283) ([@willingc](https://github.com/willingc))
- Add codecov configuration to enable PR comments [#279](https://github.com/jupyterhub/repo2docker/pull/279) ([@betatim](https://github.com/betatim))
- fixing python2 search [#277](https://github.com/jupyterhub/repo2docker/pull/277) ([@choldgraf](https://github.com/choldgraf))
- Freeze legacy environment  [#276](https://github.com/jupyterhub/repo2docker/pull/276) ([@GladysNalvarte](https://github.com/GladysNalvarte))
- Refreeze environments [#274](https://github.com/jupyterhub/repo2docker/pull/274) ([@willingc](https://github.com/willingc))
- add docstrings to docker buildpack [#272](https://github.com/jupyterhub/repo2docker/pull/272) ([@willingc](https://github.com/willingc))
- add docstrings for conda buildpack [#271](https://github.com/jupyterhub/repo2docker/pull/271) ([@willingc](https://github.com/willingc))
- add docstrings for legacy buildpack [#270](https://github.com/jupyterhub/repo2docker/pull/270) ([@willingc](https://github.com/willingc))
- Add docstrings to python3 and python2 buildpacks [#265](https://github.com/jupyterhub/repo2docker/pull/265) ([@willingc](https://github.com/willingc))
- Add doc for new buildpacks [#264](https://github.com/jupyterhub/repo2docker/pull/264) ([@willingc](https://github.com/willingc))
- Fix detecting dependency files in binder/ subidr [#261](https://github.com/jupyterhub/repo2docker/pull/261) ([@betatim](https://github.com/betatim))
- refreeze environments [#260](https://github.com/jupyterhub/repo2docker/pull/260) ([@minrk](https://github.com/minrk))
- Adding unzip to base packages [#259](https://github.com/jupyterhub/repo2docker/pull/259) ([@kmader](https://github.com/kmader))
- Revert "Add shiny-server." [#258](https://github.com/jupyterhub/repo2docker/pull/258) ([@yuvipanda](https://github.com/yuvipanda))
- make sure there's a newline before each 'File: ' heading [#255](https://github.com/jupyterhub/repo2docker/pull/255) ([@ctb](https://github.com/ctb))
- [MRG] Setup R libraries path for RStudio [#254](https://github.com/jupyterhub/repo2docker/pull/254) ([@betatim](https://github.com/betatim))
- upgrade nteract_on_jupyter to 1.5.0 [#252](https://github.com/jupyterhub/repo2docker/pull/252) ([@rgbkrk](https://github.com/rgbkrk))
- remove -v from conda env update [#248](https://github.com/jupyterhub/repo2docker/pull/248) ([@minrk](https://github.com/minrk))
- [WIP] Specify plans for stability in repo2docker dependency [#244](https://github.com/jupyterhub/repo2docker/pull/244) ([@betatim](https://github.com/betatim))
- Do not require postBuild to be executable [#241](https://github.com/jupyterhub/repo2docker/pull/241) ([@yuvipanda](https://github.com/yuvipanda))
- Add shiny-server. [#239](https://github.com/jupyterhub/repo2docker/pull/239) ([@ryanlovett](https://github.com/ryanlovett))
- clone recursively [#233](https://github.com/jupyterhub/repo2docker/pull/233) ([@minrk](https://github.com/minrk))
- instantiate Repo2Docker to run tests [#229](https://github.com/jupyterhub/repo2docker/pull/229) ([@minrk](https://github.com/minrk))
- do not reuse BuildPack instances [#228](https://github.com/jupyterhub/repo2docker/pull/228) ([@minrk](https://github.com/minrk))
- Bump jupyterlab and jupyter notebook to latest versions [#225](https://github.com/jupyterhub/repo2docker/pull/225) ([@betatim](https://github.com/betatim))
- Add a CONTRIBUTING.md [#224](https://github.com/jupyterhub/repo2docker/pull/224) ([@yuvipanda](https://github.com/yuvipanda))
- Install from wheel when testing in travis [#222](https://github.com/jupyterhub/repo2docker/pull/222) ([@yuvipanda](https://github.com/yuvipanda))
- Bump version to v0.5 [#221](https://github.com/jupyterhub/repo2docker/pull/221) ([@yuvipanda](https://github.com/yuvipanda))
- Switch freeze guidance to not be a directive [#220](https://github.com/jupyterhub/repo2docker/pull/220) ([@rgbkrk](https://github.com/rgbkrk))
- pin nteract_on_jupyter to 1.4.0 [#219](https://github.com/jupyterhub/repo2docker/pull/219) ([@rgbkrk](https://github.com/rgbkrk))
- Add docstrings and minor style fixes for application files and JuliaBuildPack [#213](https://github.com/jupyterhub/repo2docker/pull/213) ([@willingc](https://github.com/willingc))
- Add native R + IRKernel + RStudio support [#210](https://github.com/jupyterhub/repo2docker/pull/210) ([@yuvipanda](https://github.com/yuvipanda))
- Fix Python version detection for conda [#209](https://github.com/jupyterhub/repo2docker/pull/209) ([@minrk](https://github.com/minrk))
- Clarify that --debug and --no-build are for debugging only [#205](https://github.com/jupyterhub/repo2docker/pull/205) ([@yuvipanda](https://github.com/yuvipanda))
- Remove outdated builder info from docs [#204](https://github.com/jupyterhub/repo2docker/pull/204) ([@yuvipanda](https://github.com/yuvipanda))
- Add nteract jupyter extension to requirements.txt based setups [#200](https://github.com/jupyterhub/repo2docker/pull/200) ([@yuvipanda](https://github.com/yuvipanda))
- Emergency Bump to artful [#197](https://github.com/jupyterhub/repo2docker/pull/197) ([@yuvipanda](https://github.com/yuvipanda))
- Refreeze conda environment [#193](https://github.com/jupyterhub/repo2docker/pull/193) ([@yuvipanda](https://github.com/yuvipanda))
- refreeze conda environments [#187](https://github.com/jupyterhub/repo2docker/pull/187) ([@minrk](https://github.com/minrk))
- Provide a flag to pass environment variables at runtime [#186](https://github.com/jupyterhub/repo2docker/pull/186) ([@rprimet](https://github.com/rprimet))
- Stop using alpine base images [#183](https://github.com/jupyterhub/repo2docker/pull/183) ([@yuvipanda](https://github.com/yuvipanda))
- Fix indentation causing only last line of apt.txt to be parsed [#181](https://github.com/jupyterhub/repo2docker/pull/181) ([@nmih](https://github.com/nmih))
- Fixed run argument check for mounting volumes.  [#179](https://github.com/jupyterhub/repo2docker/pull/179) ([@mukundans91](https://github.com/mukundans91))
- Add default command to base Dockerfile template [#176](https://github.com/jupyterhub/repo2docker/pull/176) ([@AaronWatters](https://github.com/AaronWatters))
- Added regex pattern based validation for image name argument [#175](https://github.com/jupyterhub/repo2docker/pull/175) ([@mukundans91](https://github.com/mukundans91))
- Allow mounting arbitrary volumes into the repo2docker container [#172](https://github.com/jupyterhub/repo2docker/pull/172) ([@yuvipanda](https://github.com/yuvipanda))
- adding runtime to preparing + improving config section [#168](https://github.com/jupyterhub/repo2docker/pull/168) ([@choldgraf](https://github.com/choldgraf))
- improving docs [#165](https://github.com/jupyterhub/repo2docker/pull/165) ([@choldgraf](https://github.com/choldgraf))
- Remove symlink & just copy postBuild file instead [#161](https://github.com/jupyterhub/repo2docker/pull/161) ([@yuvipanda](https://github.com/yuvipanda))
- Set limits for how much memory docker build can use [#159](https://github.com/jupyterhub/repo2docker/pull/159) ([@yuvipanda](https://github.com/yuvipanda))
- update venv freeze and conda versions [#158](https://github.com/jupyterhub/repo2docker/pull/158) ([@minrk](https://github.com/minrk))
- don't run tests in parallel on travis [#157](https://github.com/jupyterhub/repo2docker/pull/157) ([@minrk](https://github.com/minrk))
- Use a frozen requirements.txt for base install in venv buildpacks [#156](https://github.com/jupyterhub/repo2docker/pull/156) ([@yuvipanda](https://github.com/yuvipanda))
- Split detector.py into multiple files [#155](https://github.com/jupyterhub/repo2docker/pull/155) ([@yuvipanda](https://github.com/yuvipanda))
- Make conda env update be verbose [#153](https://github.com/jupyterhub/repo2docker/pull/153) ([@choldgraf](https://github.com/choldgraf))
- Suggest editable install when installed from source [#152](https://github.com/jupyterhub/repo2docker/pull/152) ([@GladysNalvarte](https://github.com/GladysNalvarte))
- fixing empty lines and comments in apt.txt [#151](https://github.com/jupyterhub/repo2docker/pull/151) ([@GladysNalvarte](https://github.com/GladysNalvarte))
- Bump notebook version to 5.2.2 [#150](https://github.com/jupyterhub/repo2docker/pull/150) ([@yuvipanda](https://github.com/yuvipanda))
- Make all bash verify scripts fail on error [#147](https://github.com/jupyterhub/repo2docker/pull/147) ([@yuvipanda](https://github.com/yuvipanda))
- Add tests for binder/apt.txt and binder/postBuild [#145](https://github.com/jupyterhub/repo2docker/pull/145) ([@oschuett](https://github.com/oschuett))
- Fix binder/apt.txt detection [#140](https://github.com/jupyterhub/repo2docker/pull/140) ([@oschuett](https://github.com/oschuett))
- RFC: Ignore "julia" in REQUIRE file when precompiling [#137](https://github.com/jupyterhub/repo2docker/pull/137) ([@darwindarak](https://github.com/darwindarak))
- Fully remove jupyterhub references [#132](https://github.com/jupyterhub/repo2docker/pull/132) ([@yuvipanda](https://github.com/yuvipanda))
- Revert "[MRG] Add limit on git clone depth" [#131](https://github.com/jupyterhub/repo2docker/pull/131) ([@yuvipanda](https://github.com/yuvipanda))
- Revert "Add handling for no ref being provided" [#130](https://github.com/jupyterhub/repo2docker/pull/130) ([@yuvipanda](https://github.com/yuvipanda))
- Add handling for no ref being provided [#128](https://github.com/jupyterhub/repo2docker/pull/128) ([@betatim](https://github.com/betatim))
- Add 'repo2docker' as a script alias [#121](https://github.com/jupyterhub/repo2docker/pull/121) ([@yuvipanda](https://github.com/yuvipanda))
- [MRG] Use stdlib tempfile module [#118](https://github.com/jupyterhub/repo2docker/pull/118) ([@betatim](https://github.com/betatim))
- Add a basic FAQ doc + 1 entry [#117](https://github.com/jupyterhub/repo2docker/pull/117) ([@yuvipanda](https://github.com/yuvipanda))
- adding jupyter logos [#112](https://github.com/jupyterhub/repo2docker/pull/112) ([@choldgraf](https://github.com/choldgraf))
- Remove jupyterhub from default installs [#111](https://github.com/jupyterhub/repo2docker/pull/111) ([@willingc](https://github.com/willingc))
- Add doc badge [#108](https://github.com/jupyterhub/repo2docker/pull/108) ([@willingc](https://github.com/willingc))
- reorganizing arguments [#107](https://github.com/jupyterhub/repo2docker/pull/107) ([@choldgraf](https://github.com/choldgraf))
- Replace theme with alabaster [#106](https://github.com/jupyterhub/repo2docker/pull/106) ([@willingc](https://github.com/willingc))
- Attempt to add some info about design principles [#105](https://github.com/jupyterhub/repo2docker/pull/105) ([@yuvipanda](https://github.com/yuvipanda))
- Only parse `REQUIRE` file in `binder` (if exists) [#104](https://github.com/jupyterhub/repo2docker/pull/104) ([@darwindarak](https://github.com/darwindarak))
- Remove intermediate containers in failed builds [#101](https://github.com/jupyterhub/repo2docker/pull/101) ([@yuvipanda](https://github.com/yuvipanda))
- Upgrade to jupyterlab 0.28.0 [#99](https://github.com/jupyterhub/repo2docker/pull/99) ([@gnestor](https://github.com/gnestor))
- avoid producing non-JSON output on errors [#97](https://github.com/jupyterhub/repo2docker/pull/97) ([@minrk](https://github.com/minrk))
- docs type-o [#95](https://github.com/jupyterhub/repo2docker/pull/95) ([@choldgraf](https://github.com/choldgraf))
- Updating postBuild docs + doc build script [#90](https://github.com/jupyterhub/repo2docker/pull/90) ([@choldgraf](https://github.com/choldgraf))
- Add git to the repo2docker docker image [#89](https://github.com/jupyterhub/repo2docker/pull/89) ([@yuvipanda](https://github.com/yuvipanda))
- Explicitly echo what image is built in travis [#88](https://github.com/jupyterhub/repo2docker/pull/88) ([@yuvipanda](https://github.com/yuvipanda))
- Switch base image to alpine + fix typo causing CI to fail [#87](https://github.com/jupyterhub/repo2docker/pull/87) ([@yuvipanda](https://github.com/yuvipanda))
- make binder directory visible [#86](https://github.com/jupyterhub/repo2docker/pull/86) ([@minrk](https://github.com/minrk))
- Look in .binder directory for files [#83](https://github.com/jupyterhub/repo2docker/pull/83) ([@minrk](https://github.com/minrk))
- Update virtualenv base to use jupyterlab 0.27 [#81](https://github.com/jupyterhub/repo2docker/pull/81) ([@ellisonbg](https://github.com/ellisonbg))
- Update JupyterLab to 0.27 [#80](https://github.com/jupyterhub/repo2docker/pull/80) ([@ellisonbg](https://github.com/ellisonbg))
- document `--debug` [#79](https://github.com/jupyterhub/repo2docker/pull/79) ([@choldgraf](https://github.com/choldgraf))
- make JUPYTERHUB_VERSION a build arg [#76](https://github.com/jupyterhub/repo2docker/pull/76) ([@minrk](https://github.com/minrk))
- typo: --print-dockerfile ended up falling under --debug [#75](https://github.com/jupyterhub/repo2docker/pull/75) ([@minrk](https://github.com/minrk))
- don't install requirements.txt if environment.yml is present [#74](https://github.com/jupyterhub/repo2docker/pull/74) ([@minrk](https://github.com/minrk))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2017-09-06&to=2018-09-09&type=c))

[@AaronWatters](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AAaronWatters+updated%3A2017-09-06..2018-09-09&type=Issues) | [@aborruso](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aaborruso+updated%3A2017-09-06..2018-09-09&type=Issues) | [@akarve](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aakarve+updated%3A2017-09-06..2018-09-09&type=Issues) | [@arokem](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aarokem+updated%3A2017-09-06..2018-09-09&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2017-09-06..2018-09-09&type=Issues) | [@bitnik](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abitnik+updated%3A2017-09-06..2018-09-09&type=Issues) | [@blink1073](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ablink1073+updated%3A2017-09-06..2018-09-09&type=Issues) | [@brooksambrose](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abrooksambrose+updated%3A2017-09-06..2018-09-09&type=Issues) | [@Carreau](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ACarreau+updated%3A2017-09-06..2018-09-09&type=Issues) | [@cboettig](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acboettig+updated%3A2017-09-06..2018-09-09&type=Issues) | [@cclauss](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acclauss+updated%3A2017-09-06..2018-09-09&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2017-09-06..2018-09-09&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2017-09-06..2018-09-09&type=Issues) | [@ctb](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Actb+updated%3A2017-09-06..2018-09-09&type=Issues) | [@danielleberre](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adanielleberre+updated%3A2017-09-06..2018-09-09&type=Issues) | [@darabos](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adarabos+updated%3A2017-09-06..2018-09-09&type=Issues) | [@darwindarak](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adarwindarak+updated%3A2017-09-06..2018-09-09&type=Issues) | [@davidanthoff](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adavidanthoff+updated%3A2017-09-06..2018-09-09&type=Issues) | [@dkleissa](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adkleissa+updated%3A2017-09-06..2018-09-09&type=Issues) | [@DominikGlodzik](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ADominikGlodzik+updated%3A2017-09-06..2018-09-09&type=Issues) | [@ellisonbg](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aellisonbg+updated%3A2017-09-06..2018-09-09&type=Issues) | [@evertrol](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aevertrol+updated%3A2017-09-06..2018-09-09&type=Issues) | [@GladysNalvarte](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AGladysNalvarte+updated%3A2017-09-06..2018-09-09&type=Issues) | [@gnestor](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Agnestor+updated%3A2017-09-06..2018-09-09&type=Issues) | [@hydrosquall](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ahydrosquall+updated%3A2017-09-06..2018-09-09&type=Issues) | [@jasongrout](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajasongrout+updated%3A2017-09-06..2018-09-09&type=Issues) | [@jhamman](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajhamman+updated%3A2017-09-06..2018-09-09&type=Issues) | [@juanesarango](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajuanesarango+updated%3A2017-09-06..2018-09-09&type=Issues) | [@jzf2101](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajzf2101+updated%3A2017-09-06..2018-09-09&type=Issues) | [@kmader](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Akmader+updated%3A2017-09-06..2018-09-09&type=Issues) | [@KristofferC](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AKristofferC+updated%3A2017-09-06..2018-09-09&type=Issues) | [@Madhu94](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AMadhu94+updated%3A2017-09-06..2018-09-09&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2017-09-06..2018-09-09&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2017-09-06..2018-09-09&type=Issues) | [@mpacer](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ampacer+updated%3A2017-09-06..2018-09-09&type=Issues) | [@mrustl](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amrustl+updated%3A2017-09-06..2018-09-09&type=Issues) | [@mukundans91](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amukundans91+updated%3A2017-09-06..2018-09-09&type=Issues) | [@NHDaly](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ANHDaly+updated%3A2017-09-06..2018-09-09&type=Issues) | [@nmih](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Anmih+updated%3A2017-09-06..2018-09-09&type=Issues) | [@nuest](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Anuest+updated%3A2017-09-06..2018-09-09&type=Issues) | [@oschuett](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aoschuett+updated%3A2017-09-06..2018-09-09&type=Issues) | [@psychemedia](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apsychemedia+updated%3A2017-09-06..2018-09-09&type=Issues) | [@RaoOfPhysics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ARaoOfPhysics+updated%3A2017-09-06..2018-09-09&type=Issues) | [@remram44](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aremram44+updated%3A2017-09-06..2018-09-09&type=Issues) | [@rgbkrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Argbkrk+updated%3A2017-09-06..2018-09-09&type=Issues) | [@rnestler](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Arnestler+updated%3A2017-09-06..2018-09-09&type=Issues) | [@rprimet](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Arprimet+updated%3A2017-09-06..2018-09-09&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aryanlovett+updated%3A2017-09-06..2018-09-09&type=Issues) | [@sje30](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asje30+updated%3A2017-09-06..2018-09-09&type=Issues) | [@slayoo](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aslayoo+updated%3A2017-09-06..2018-09-09&type=Issues) | [@spendyala](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aspendyala+updated%3A2017-09-06..2018-09-09&type=Issues) | [@SylvainCorlay](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ASylvainCorlay+updated%3A2017-09-06..2018-09-09&type=Issues) | [@taylorreiter](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ataylorreiter+updated%3A2017-09-06..2018-09-09&type=Issues) | [@toddrme2178](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atoddrme2178+updated%3A2017-09-06..2018-09-09&type=Issues) | [@trallard](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atrallard+updated%3A2017-09-06..2018-09-09&type=Issues) | [@vsoch](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Avsoch+updated%3A2017-09-06..2018-09-09&type=Issues) | [@willingc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awillingc+updated%3A2017-09-06..2018-09-09&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2017-09-06..2018-09-09&type=Issues) | [@zymergen-luke](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Azymergen-luke+updated%3A2017-09-06..2018-09-09&type=Issues)

## v0.4.1

([full changelog](https://github.com/jupyterhub/repo2docker/compare/e7674ce...d97eee9))

### Merged PRs

- Add --debug & --no-build options [#68](https://github.com/jupyterhub/repo2docker/pull/68) ([@yuvipanda](https://github.com/yuvipanda))
- Moved old COPYING.md to LICENSE, and updated with current language. [#67](https://github.com/jupyterhub/repo2docker/pull/67) ([@tdalseide](https://github.com/tdalseide))
- Add license - Issue #64 [#65](https://github.com/jupyterhub/repo2docker/pull/65) ([@sumalaika](https://github.com/sumalaika))
- Include package_data in setup.py [#59](https://github.com/jupyterhub/repo2docker/pull/59) ([@yuvipanda](https://github.com/yuvipanda))
- Include package_data in setup.py [#58](https://github.com/jupyterhub/repo2docker/pull/58) ([@yuvipanda](https://github.com/yuvipanda))
- Add npm to base image [#57](https://github.com/jupyterhub/repo2docker/pull/57) ([@yuvipanda](https://github.com/yuvipanda))
- config file for RTD [#56](https://github.com/jupyterhub/repo2docker/pull/56) ([@choldgraf](https://github.com/choldgraf))
- fixing RTD build [#54](https://github.com/jupyterhub/repo2docker/pull/54) ([@choldgraf](https://github.com/choldgraf))
- updating autogen examples [#53](https://github.com/jupyterhub/repo2docker/pull/53) ([@choldgraf](https://github.com/choldgraf))
- adding doc generation from the tests [#51](https://github.com/jupyterhub/repo2docker/pull/51) ([@choldgraf](https://github.com/choldgraf))
- Validate that Julia is using our pre-installed conda [#50](https://github.com/jupyterhub/repo2docker/pull/50) ([@yuvipanda](https://github.com/yuvipanda))
- Cleanup conda [#49](https://github.com/jupyterhub/repo2docker/pull/49) ([@yuvipanda](https://github.com/yuvipanda))
- Add back --no-clean support [#48](https://github.com/jupyterhub/repo2docker/pull/48) ([@yuvipanda](https://github.com/yuvipanda))
- Add a little more info to README [#47](https://github.com/jupyterhub/repo2docker/pull/47) ([@yuvipanda](https://github.com/yuvipanda))
- Print stdout for all the tests! [#46](https://github.com/jupyterhub/repo2docker/pull/46) ([@yuvipanda](https://github.com/yuvipanda))
- Fix legacy dockerfile support and add tests [#43](https://github.com/jupyterhub/repo2docker/pull/43) ([@yuvipanda](https://github.com/yuvipanda))
- Fix dockerfile builds and add tests for them [#42](https://github.com/jupyterhub/repo2docker/pull/42) ([@yuvipanda](https://github.com/yuvipanda))
- fix the python2 kernelspec [#35](https://github.com/jupyterhub/repo2docker/pull/35) ([@minrk](https://github.com/minrk))
- julia version bump [#30](https://github.com/jupyterhub/repo2docker/pull/30) ([@choldgraf](https://github.com/choldgraf))
- Add support for Julia buildpack [#29](https://github.com/jupyterhub/repo2docker/pull/29) ([@yuvipanda](https://github.com/yuvipanda))
- Add initial sphinx docs [#26](https://github.com/jupyterhub/repo2docker/pull/26) ([@willingc](https://github.com/willingc))
- Add JupyterLab to the default environment for venv + conda builders [#22](https://github.com/jupyterhub/repo2docker/pull/22) ([@yuvipanda](https://github.com/yuvipanda))
- Cleanup docker pull hack [#21](https://github.com/jupyterhub/repo2docker/pull/21) ([@yuvipanda](https://github.com/yuvipanda))
- Add a default build pack [#20](https://github.com/jupyterhub/repo2docker/pull/20) ([@yuvipanda](https://github.com/yuvipanda))
- add LegacyBinderDockerfile buildpack [#16](https://github.com/jupyterhub/repo2docker/pull/16) ([@minrk](https://github.com/minrk))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2017-05-25&to=2017-09-06&type=c))

[@arokem](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aarokem+updated%3A2017-05-25..2017-09-06&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2017-05-25..2017-09-06&type=Issues) | [@cboettig](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acboettig+updated%3A2017-05-25..2017-09-06&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2017-05-25..2017-09-06&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2017-05-25..2017-09-06&type=Issues) | [@dpsanders](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adpsanders+updated%3A2017-05-25..2017-09-06&type=Issues) | [@jzf2101](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajzf2101+updated%3A2017-05-25..2017-09-06&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2017-05-25..2017-09-06&type=Issues) | [@rprimet](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Arprimet+updated%3A2017-05-25..2017-09-06&type=Issues) | [@sje30](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asje30+updated%3A2017-05-25..2017-09-06&type=Issues) | [@sumalaika](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asumalaika+updated%3A2017-05-25..2017-09-06&type=Issues) | [@taylorreiter](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ataylorreiter+updated%3A2017-05-25..2017-09-06&type=Issues) | [@tdalseide](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atdalseide+updated%3A2017-05-25..2017-09-06&type=Issues) | [@tkelman](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atkelman+updated%3A2017-05-25..2017-09-06&type=Issues) | [@willingc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awillingc+updated%3A2017-05-25..2017-09-06&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2017-05-25..2017-09-06&type=Issues)

## 0.2.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/efd55a9...e7674ce))

### Merged PRs

- line endings! [#14](https://github.com/jupyterhub/repo2docker/pull/14) ([@minrk](https://github.com/minrk))
- bundle s2i in wheels [#12](https://github.com/jupyterhub/repo2docker/pull/12) ([@minrk](https://github.com/minrk))
- Add builder creation doc [#11](https://github.com/jupyterhub/repo2docker/pull/11) ([@willingc](https://github.com/willingc))
- Use same port in host and docker container [#10](https://github.com/jupyterhub/repo2docker/pull/10) ([@yuvipanda](https://github.com/yuvipanda))
- support repo as positional arg [#8](https://github.com/jupyterhub/repo2docker/pull/8) ([@minrk](https://github.com/minrk))
- further simplify s2i buildpacks [#7](https://github.com/jupyterhub/repo2docker/pull/7) ([@minrk](https://github.com/minrk))
- add conda detector [#2](https://github.com/jupyterhub/repo2docker/pull/2) ([@minrk](https://github.com/minrk))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2017-04-19&to=2017-05-25&type=c))

[@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2017-04-19..2017-05-25&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2017-04-19..2017-05-25&type=Issues) | [@willingc](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awillingc+updated%3A2017-04-19..2017-05-25&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2017-04-19..2017-05-25&type=Issues)

