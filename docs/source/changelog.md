# Changelog

## Version 2024.03.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/2023.06.0...2024.01.03))

### New features added

- Implement support for dockerignore and containerignore [#1205](https://github.com/jupyterhub/repo2docker/pull/1205) ([@sgaist](https://github.com/sgaist))

### Enhancements made

- rstudio: log-level info to stderr [#1317](https://github.com/jupyterhub/repo2docker/pull/1317) ([@manics](https://github.com/manics))

### Bugs fixed

- Get Zenodo working again [#1315](https://github.com/jupyterhub/repo2docker/pull/1315) ([@manics](https://github.com/manics))

### Maintenance and upkeep improvements

- Update mamba to 1.5.7 from 1.5.1, and conda to 24.3.0 from 23.7.4 [#1337](https://github.com/jupyterhub/repo2docker/pull/1337) ([@SylvainCorlay](https://github.com/SylvainCorlay))
- Dockerfile: bump alpine from 3.17 to 3.19 and Python 3.10 to 3.11 [#1332](https://github.com/jupyterhub/repo2docker/pull/1332) ([@yuvipanda](https://github.com/yuvipanda))
- Upgrade base image from to Ubuntu 22.04 from 18.04 [#1287](https://github.com/jupyterhub/repo2docker/pull/1287) ([@yuvipanda](https://github.com/yuvipanda))

### Documentation improvements

- Add Ubuntu 22.04 upgrade guide [#1309](https://github.com/jupyterhub/repo2docker/pull/1309) ([@manics](https://github.com/manics))
- Update version of R available [#1288](https://github.com/jupyterhub/repo2docker/pull/1288) ([@yuvipanda](https://github.com/yuvipanda))
- Add changelog for 2023.06.0 [#1286](https://github.com/jupyterhub/repo2docker/pull/1286) ([@yuvipanda](https://github.com/yuvipanda))

### Other merged PRs

- [pre-commit.ci] pre-commit autoupdate [#1333](https://github.com/jupyterhub/repo2docker/pull/1333) ([@pre-commit-ci](https://github.com/pre-commit-ci))
- build(deps): bump codecov/codecov-action from 3 to 4 [#1331](https://github.com/jupyterhub/repo2docker/pull/1331) ([@dependabot](https://github.com/dependabot))
- Support pytest=8 [#1330](https://github.com/jupyterhub/repo2docker/pull/1330) ([@manics](https://github.com/manics))
- Update versioneer [#1329](https://github.com/jupyterhub/repo2docker/pull/1329) ([@TimoRoth](https://github.com/TimoRoth))
- build(deps): bump actions/setup-python from 4 to 5 [#1328](https://github.com/jupyterhub/repo2docker/pull/1328) ([@dependabot](https://github.com/dependabot))
- build(deps): bump actions/upload-artifact from 3 to 4 [#1327](https://github.com/jupyterhub/repo2docker/pull/1327) ([@dependabot](https://github.com/dependabot))
- Add NYCU Dataverse [#1326](https://github.com/jupyterhub/repo2docker/pull/1326) ([@twtw](https://github.com/twtw))
- [pre-commit.ci] pre-commit autoupdate [#1322](https://github.com/jupyterhub/repo2docker/pull/1322) ([@pre-commit-ci](https://github.com/pre-commit-ci))
- New domain for Edmond MPG repository [#1321](https://github.com/jupyterhub/repo2docker/pull/1321) ([@haarli](https://github.com/haarli))
- [pre-commit.ci] pre-commit autoupdate [#1319](https://github.com/jupyterhub/repo2docker/pull/1319) ([@pre-commit-ci](https://github.com/pre-commit-ci))
- [MRG] docs: Add base_image parameter example. [#1318](https://github.com/jupyterhub/repo2docker/pull/1318) ([@hiroyuki-sato](https://github.com/hiroyuki-sato))
- Upgrade mamba and refreeze [#1313](https://github.com/jupyterhub/repo2docker/pull/1313) ([@manics](https://github.com/manics))
- r: Bump version of rsession-proxy [#1310](https://github.com/jupyterhub/repo2docker/pull/1310) ([@yuvipanda](https://github.com/yuvipanda))
- build(deps): bump actions/checkout from 3 to 4 [#1308](https://github.com/jupyterhub/repo2docker/pull/1308) ([@dependabot](https://github.com/dependabot))
- build(deps): bump docker/build-push-action from 4 to 5 [#1307](https://github.com/jupyterhub/repo2docker/pull/1307) ([@dependabot](https://github.com/dependabot))
- build(deps): bump docker/setup-qemu-action from 2 to 3 [#1306](https://github.com/jupyterhub/repo2docker/pull/1306) ([@dependabot](https://github.com/dependabot))
- build(deps): bump docker/setup-buildx-action from 2 to 3 [#1305](https://github.com/jupyterhub/repo2docker/pull/1305) ([@dependabot](https://github.com/dependabot))
- Update conda and mamba [#1299](https://github.com/jupyterhub/repo2docker/pull/1299) ([@SylvainCorlay](https://github.com/SylvainCorlay))
- Point to official documentation for handling JupyterLab workspace [#1294](https://github.com/jupyterhub/repo2docker/pull/1294) ([@fcollonval](https://github.com/fcollonval))
- Fix rstudio-build selection [#1293](https://github.com/jupyterhub/repo2docker/pull/1293) ([@yamaton](https://github.com/yamaton))
- [pre-commit.ci] pre-commit autoupdate [#1291](https://github.com/jupyterhub/repo2docker/pull/1291) ([@pre-commit-ci](https://github.com/pre-commit-ci))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2023-06-13&to=2024-03-28&type=c))

[@annakrystalli](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aannakrystalli+updated%3A2023-06-13..2024-03-28&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2023-06-13..2024-03-28&type=Issues) | [@bollwyvl](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abollwyvl+updated%3A2023-06-13..2024-03-28&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2023-06-13..2024-03-28&type=Issues) | [@dependabot](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adependabot+updated%3A2023-06-13..2024-03-28&type=Issues) | [@dolfinus](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adolfinus+updated%3A2023-06-13..2024-03-28&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Afcollonval+updated%3A2023-06-13..2024-03-28&type=Issues) | [@felder](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Afelder+updated%3A2023-06-13..2024-03-28&type=Issues) | [@haarli](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ahaarli+updated%3A2023-06-13..2024-03-28&type=Issues) | [@hiroyuki-sato](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ahiroyuki-sato+updated%3A2023-06-13..2024-03-28&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2023-06-13..2024-03-28&type=Issues) | [@mathieuboudreau](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amathieuboudreau+updated%3A2023-06-13..2024-03-28&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2023-06-13..2024-03-28&type=Issues) | [@pre-commit-ci](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apre-commit-ci+updated%3A2023-06-13..2024-03-28&type=Issues) | [@rgaiacs](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Argaiacs+updated%3A2023-06-13..2024-03-28&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aryanlovett+updated%3A2023-06-13..2024-03-28&type=Issues) | [@sgaist](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Asgaist+updated%3A2023-06-13..2024-03-28&type=Issues) | [@SylvainCorlay](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ASylvainCorlay+updated%3A2023-06-13..2024-03-28&type=Issues) | [@TimoRoth](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ATimoRoth+updated%3A2023-06-13..2024-03-28&type=Issues) | [@twtw](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atwtw+updated%3A2023-06-13..2024-03-28&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awelcome+updated%3A2023-06-13..2024-03-28&type=Issues) | [@yamaton](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayamaton+updated%3A2023-06-13..2024-03-28&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2023-06-13..2024-03-28&type=Issues)

## Version 2023.06.0

([full changelog](https://github.com/jupyterhub/repo2docker/compare/2022.10.0...2023.06.0))

### Breaking changes

- JupyterHub version installed by default upgraded from 1.5 to 3.1.1
- Microsoft [killed MRAN](https://techcommunity.microsoft.com/t5/azure-sql-blog/microsoft-r-application-network-retirement/ba-p/3707161), so all package snapshots now come from [Posit Package Manager](https://packagemanager.posit.co/client/). Snapshots from before 2018-12-07 are now no longer available, so you might have to update the snapshot date in your `runtime.txt`.

### New features added

- Support Python 3.11 and upgrade jupyterhub from 1.5.0 to 3.1.1 [#1239](https://github.com/jupyterhub/repo2docker/pull/1239) ([@minrk](https://github.com/minrk))
- allow user to specify a single port with default command [#918](https://github.com/jupyterhub/repo2docker/pull/918) ([@minrk](https://github.com/minrk))
- Let `FROM <base_image>` in the Dockerfile template be configurable [#909](https://github.com/jupyterhub/repo2docker/pull/909) ([@yuvipanda](https://github.com/yuvipanda))

### Enhancements made

- Update to mamba 1.4.0 [#1256](https://github.com/jupyterhub/repo2docker/pull/1256) ([@SylvainCorlay](https://github.com/SylvainCorlay))
- [MRG] download original file formats from Dataverse #1242 [#1253](https://github.com/jupyterhub/repo2docker/pull/1253) ([@pdurbin](https://github.com/pdurbin))
- Add optional registry credentials to push() [#1245](https://github.com/jupyterhub/repo2docker/pull/1245) ([@manics](https://github.com/manics))
- Add ARM64 support where possible [#1228](https://github.com/jupyterhub/repo2docker/pull/1228) ([@manics](https://github.com/manics))
- Switch default python to 3.10 [#1219](https://github.com/jupyterhub/repo2docker/pull/1219) ([@yuvipanda](https://github.com/yuvipanda))

### Bugs fixed

- Microsoft killed MRAN, stop relying on it [#1285](https://github.com/jupyterhub/repo2docker/pull/1285) ([@minrk](https://github.com/minrk))
- Update the location of R packagemanager [#1273](https://github.com/jupyterhub/repo2docker/pull/1273) ([@Xarthisius](https://github.com/Xarthisius))
- missing `f` in julia fetch error f-string [#1264](https://github.com/jupyterhub/repo2docker/pull/1264) ([@minrk](https://github.com/minrk))
- avoid duplicate log statements by memoizing getters [#1248](https://github.com/jupyterhub/repo2docker/pull/1248) ([@minrk](https://github.com/minrk))
- Add Conda env library path to RStudio configuration [#1237](https://github.com/jupyterhub/repo2docker/pull/1237) ([@TimStewartJ](https://github.com/TimStewartJ))
- Create Julia projects based on binder/Project.toml when found [#1216](https://github.com/jupyterhub/repo2docker/pull/1216) ([@frankier](https://github.com/frankier))
- Allow REPO_DIR to be a non-existing folder by creating it and providing the user with permissions [#976](https://github.com/jupyterhub/repo2docker/pull/976) ([@bollwyvl](https://github.com/bollwyvl))

### Maintenance and upkeep improvements

- Microsoft killed MRAN, stop relying on it [#1285](https://github.com/jupyterhub/repo2docker/pull/1285) ([@minrk](https://github.com/minrk))
- Relax pins to major versions and refreeze, introduce explicit jupyter_server v1 pin [#1283](https://github.com/jupyterhub/repo2docker/pull/1283) ([@consideRatio](https://github.com/consideRatio))
- fix github link templates [#1276](https://github.com/jupyterhub/repo2docker/pull/1276) ([@minrk](https://github.com/minrk))
- dependabot: monthly updates of github actions [#1262](https://github.com/jupyterhub/repo2docker/pull/1262) ([@consideRatio](https://github.com/consideRatio))
- Remove deprecated nteract_on_jupyter [#1259](https://github.com/jupyterhub/repo2docker/pull/1259) ([@yuvipanda](https://github.com/yuvipanda))
- disable codecov failures [#1251](https://github.com/jupyterhub/repo2docker/pull/1251) ([@minrk](https://github.com/minrk))
- Support Python 3.11 and upgrade jupyterhub from 1.5.0 to 3.1.1 [#1239](https://github.com/jupyterhub/repo2docker/pull/1239) ([@minrk](https://github.com/minrk))
- pre-commit update to fix ci [#1238](https://github.com/jupyterhub/repo2docker/pull/1238) ([@minrk](https://github.com/minrk))
- Upgrade to mamba 1.1 and enable rich SAT error messages [#1232](https://github.com/jupyterhub/repo2docker/pull/1232) ([@SylvainCorlay](https://github.com/SylvainCorlay))
- Upgrade to mamba 1.0 [#1213](https://github.com/jupyterhub/repo2docker/pull/1213) ([@SylvainCorlay](https://github.com/SylvainCorlay))
- docker image: update alpine to 3.16 [#1212](https://github.com/jupyterhub/repo2docker/pull/1212) ([@consideRatio](https://github.com/consideRatio))
- reconcile CLI/config priority [#1211](https://github.com/jupyterhub/repo2docker/pull/1211) ([@minrk](https://github.com/minrk))
- pipfile: pass --clear flag, and do it separetely to not be ignored [#1208](https://github.com/jupyterhub/repo2docker/pull/1208) ([@consideRatio](https://github.com/consideRatio))
- run submodule test over https [#1204](https://github.com/jupyterhub/repo2docker/pull/1204) ([@minrk](https://github.com/minrk))
- pre-commit: add pyupgrade, isort, and prettier for .md files [#1202](https://github.com/jupyterhub/repo2docker/pull/1202) ([@consideRatio](https://github.com/consideRatio))
- Create wheels with the build package, stop calling setup.py directly [#1199](https://github.com/jupyterhub/repo2docker/pull/1199) ([@consideRatio](https://github.com/consideRatio))
- Add check-tmp step to local repo tests [#1126](https://github.com/jupyterhub/repo2docker/pull/1126) ([@minrk](https://github.com/minrk))
- Set default, type, and help method for engine in argparse [#1073](https://github.com/jupyterhub/repo2docker/pull/1073) ([@jgarte](https://github.com/jgarte))

### Documentation improvements

- Fix links to jupyterlab-demo postBuild file [#1282](https://github.com/jupyterhub/repo2docker/pull/1282) ([@fcollonval](https://github.com/fcollonval))
- Recreate changelog as markdown [#1281](https://github.com/jupyterhub/repo2docker/pull/1281) ([@yuvipanda](https://github.com/yuvipanda))
- fix github link templates [#1276](https://github.com/jupyterhub/repo2docker/pull/1276) ([@minrk](https://github.com/minrk))
- update docs for default and supported Python versions [#1250](https://github.com/jupyterhub/repo2docker/pull/1250) ([@minrk](https://github.com/minrk))
- docs: add devenv, linkcheck, and refresh misc config etc [#1197](https://github.com/jupyterhub/repo2docker/pull/1197) ([@consideRatio](https://github.com/consideRatio))

### Other merged PRs

- build(deps): bump pypa/gh-action-pypi-publish from 1.8.5 to (edit) release/v1 [#1279](https://github.com/jupyterhub/repo2docker/pull/1279) ([@dependabot](https://github.com/dependabot))
- [pre-commit.ci] pre-commit autoupdate [#1270](https://github.com/jupyterhub/repo2docker/pull/1270) ([@pre-commit-ci](https://github.com/pre-commit-ci))
- build(deps): bump pypa/gh-action-pypi-publish from 1.8.4 to 1.8.5 [#1263](https://github.com/jupyterhub/repo2docker/pull/1263) ([@dependabot](https://github.com/dependabot))
- [pre-commit.ci] pre-commit autoupdate [#1261](https://github.com/jupyterhub/repo2docker/pull/1261) ([@pre-commit-ci](https://github.com/pre-commit-ci))
- build(deps): bump pypa/gh-action-pypi-publish from 1.8.3 to 1.8.4 [#1260](https://github.com/jupyterhub/repo2docker/pull/1260) ([@dependabot](https://github.com/dependabot))
- build(deps): bump pypa/gh-action-pypi-publish from 1.6.4 to 1.8.3 [#1257](https://github.com/jupyterhub/repo2docker/pull/1257) ([@dependabot](https://github.com/dependabot))
- [pre-commit.ci] pre-commit autoupdate [#1252](https://github.com/jupyterhub/repo2docker/pull/1252) ([@pre-commit-ci](https://github.com/pre-commit-ci))
- Ensure `BuildPack.python_version` is specified [#1249](https://github.com/jupyterhub/repo2docker/pull/1249) ([@minrk](https://github.com/minrk))
- Update install-nix.bash [#1244](https://github.com/jupyterhub/repo2docker/pull/1244) ([@robertodr](https://github.com/robertodr))
- build(deps): bump docker/build-push-action from 3 to 4 [#1241](https://github.com/jupyterhub/repo2docker/pull/1241) ([@dependabot](https://github.com/dependabot))
- Update to `jupyter-resource-usage==0.7.0` [#1236](https://github.com/jupyterhub/repo2docker/pull/1236) ([@jtpio](https://github.com/jtpio))
- Also install dev requirements on Gitpod [#1235](https://github.com/jupyterhub/repo2docker/pull/1235) ([@jtpio](https://github.com/jtpio))
- Bump to Node 18 [#1234](https://github.com/jupyterhub/repo2docker/pull/1234) ([@jtpio](https://github.com/jtpio))
- [pre-commit.ci] pre-commit autoupdate [#1229](https://github.com/jupyterhub/repo2docker/pull/1229) ([@pre-commit-ci](https://github.com/pre-commit-ci))
- Quick-fix for Docker image build [#1227](https://github.com/jupyterhub/repo2docker/pull/1227) ([@manics](https://github.com/manics))
- Fix tests/external/reproductions.repos.yaml [#1226](https://github.com/jupyterhub/repo2docker/pull/1226) ([@manics](https://github.com/manics))
- Fix typo [#1224](https://github.com/jupyterhub/repo2docker/pull/1224) ([@fkohrt](https://github.com/fkohrt))
- build(deps): bump pypa/gh-action-pypi-publish from 1.5.1 to 1.6.4 [#1223](https://github.com/jupyterhub/repo2docker/pull/1223) ([@dependabot](https://github.com/dependabot))
- [pre-commit.ci] pre-commit autoupdate [#1222](https://github.com/jupyterhub/repo2docker/pull/1222) ([@pre-commit-ci](https://github.com/pre-commit-ci))
- ci: cleanup no longer used test logic related to memlimit [#1218](https://github.com/jupyterhub/repo2docker/pull/1218) ([@consideRatio](https://github.com/consideRatio))
- [pre-commit.ci] pre-commit autoupdate [#1217](https://github.com/jupyterhub/repo2docker/pull/1217) ([@pre-commit-ci](https://github.com/pre-commit-ci))
- ci: use non-deprecated codecov uploader [#1209](https://github.com/jupyterhub/repo2docker/pull/1209) ([@consideRatio](https://github.com/consideRatio))
- ci: stop running pre-commit in gha, rely on pre-commit.ci [#1200](https://github.com/jupyterhub/repo2docker/pull/1200) ([@consideRatio](https://github.com/consideRatio))
- Initial changelog for 2022.10.0 [#1194](https://github.com/jupyterhub/repo2docker/pull/1194) ([@manics](https://github.com/manics))

### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/repo2docker/graphs/contributors?from=2022-10-18&to=2023-06-13&type=c))

[@AliMirlou](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AAliMirlou+updated%3A2022-10-18..2023-06-13&type=Issues) | [@betatim](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abetatim+updated%3A2022-10-18..2023-06-13&type=Issues) | [@bollwyvl](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Abollwyvl+updated%3A2022-10-18..2023-06-13&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acholdgraf+updated%3A2022-10-18..2023-06-13&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AconsideRatio+updated%3A2022-10-18..2023-06-13&type=Issues) | [@craig-willis](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Acraig-willis+updated%3A2022-10-18..2023-06-13&type=Issues) | [@dependabot](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Adependabot+updated%3A2022-10-18..2023-06-13&type=Issues) | [@fcollonval](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Afcollonval+updated%3A2022-10-18..2023-06-13&type=Issues) | [@fkohrt](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Afkohrt+updated%3A2022-10-18..2023-06-13&type=Issues) | [@frankier](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Afrankier+updated%3A2022-10-18..2023-06-13&type=Issues) | [@jgarte](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajgarte+updated%3A2022-10-18..2023-06-13&type=Issues) | [@jhamman](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajhamman+updated%3A2022-10-18..2023-06-13&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ajtpio+updated%3A2022-10-18..2023-06-13&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Amanics+updated%3A2022-10-18..2023-06-13&type=Issues) | [@meeseeksmachine](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ameeseeksmachine+updated%3A2022-10-18..2023-06-13&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Aminrk+updated%3A2022-10-18..2023-06-13&type=Issues) | [@nuest](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Anuest+updated%3A2022-10-18..2023-06-13&type=Issues) | [@pdurbin](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apdurbin+updated%3A2022-10-18..2023-06-13&type=Issues) | [@pre-commit-ci](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Apre-commit-ci+updated%3A2022-10-18..2023-06-13&type=Issues) | [@robertodr](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Arobertodr+updated%3A2022-10-18..2023-06-13&type=Issues) | [@SylvainCorlay](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ASylvainCorlay+updated%3A2022-10-18..2023-06-13&type=Issues) | [@TimStewartJ](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3ATimStewartJ+updated%3A2022-10-18..2023-06-13&type=Issues) | [@trybik](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Atrybik+updated%3A2022-10-18..2023-06-13&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awelcome+updated%3A2022-10-18..2023-06-13&type=Issues) | [@westurner](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Awesturner+updated%3A2022-10-18..2023-06-13&type=Issues) | [@Xarthisius](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3AXarthisius+updated%3A2022-10-18..2023-06-13&type=Issues) | [@yamaton](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayamaton+updated%3A2022-10-18..2023-06-13&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Frepo2docker+involves%3Ayuvipanda+updated%3A2022-10-18..2023-06-13&type=Issues)

## Version 2022.10.0

[Full changelog](https://github.com/jupyterhub/repo2docker/compare/2022.02.0...2022.10.0)

### New features

- Update Jupyter dependencies {pr}`1193` by {user}`jtpio`
- add Python 3.10 base environment {pr}`1175` by {user}`minrk`
- Bump default R version to 4.2 from 4.1, and let R 3.4 go from 3.4.0 to 3.4.4 {pr}`1165` by {user}`yuvipanda`
- Support pulling from zenodo sandbox too {pr}`1169` by {user}`yuvipanda`
- Add MPDL Dataverse {pr}`1167` by {user}`wilhelmfrank`
- Add JPL Dataverse {pr}`1163` by {user}`foobarbecue`
- upgrade RStudio Server to v2022.02.1 {pr}`1148` by {user}`aplamada`
- Pass build_args to `render()` during `--no-build` for consistency with regular builds {pr}`1135` by {user}`yoogottamk`

### Documentation improvements

- Update 'how to get R' section {pr}`1147` by {user}`yuvipanda`
- Post release fixes {pr}`1133` by {user}`manics`

### API changes

### Bug fixes

- consistent log handling when not using JSON loggers {pr}`1177` by {user}`minrk`
- Fix Read-Only filesystem permission issue for log file {pr}`1156` by {user}`timeu`
- handle permission issue writing .jupyter-server-log.txt in REPO_DIR {pr}`1151` by {user}`pymonger`
- handle r version being unspecified in environment.yml {pr}`1141` by {user}`minrk`

### Other merged PRs

- Remove conda buildpacks pin of r-irkernel to 1.2 {pr}`1191` by {user}`consideRatio`
- ci: refactor julia/r/conda tests - now ~25 min instead of ~50 min {pr}`1188` by {user}`consideRatio`
- ci: general refresh of github workflows, update gha versions and let dependabot do it, etc. {pr}`1186` by {user}`consideRatio`
- Use enum to standardise `phase` {pr}`1185` by {user}`manics`
- fail on unsupported Python {pr}`1184` by {user}`minrk`
- mount wheels from build stage instead of copying them {pr}`1182` by {user}`minrk`
- get CI working again {pr}`1178` by {user}`minrk`
- explicitly build linux/amd64 images {pr}`1176` by {user}`minrk`
- Freeze.py update {pr}`1173` by {user}`manics`
- Bump version of nodejs {pr}`1172` by {user}`yuvipanda`
- Update mamba {pr}`1171` by {user}`SylvainCorlay`
- ci: switch to using a 2fa enabled accounts pypi api-token {pr}`1166` by {user}`consideRatio`
- Get R from RStudio provided apt packages (.deb files) {pr}`1161` by {user}`yuvipanda`
- Shallow clone HEAD {pr}`1160` by {user}`daradib`
- Update black version {pr}`1150` by {user}`yuvipanda`
- Update base notebook packages {pr}`1149` by {user}`yuvipanda`
- Update Dockerfile to current Alpine (ALPINE_VERSION=3.15.0) {pr}`1136` by {user}`holzman`
- update Python in some dockerfile tests {pr}`1130` by {user}`minrk`

## Version 2022.02.0

[Full changelog](https://github.com/jupyterhub/repo2docker/compare/2021.08.0...2022.02.0)

### New features

- Update ipywidgets jupyter-offlinenotebook jupyterlab {pr}`1127` by {user}`manics`
- Allow passing in extra args to Docker initialization {pr}`1124` by {user}`yuvipanda`
- Allow passing in traitlets via commandline {pr}`1123` by {user}`yuvipanda`
- Bump default R version to 4.1 {pr}`1107` by {user}`yuvipanda`
- Update jupyterlab 3.2.5 jupyter-resource-usage 0.6.1 {pr}`1105` by {user}`manics`
- Get binary R packages from packagemanager.rstudio.com {pr}`1104` by {user}`yuvipanda`
- Support R 4.1 {pr}`1102` by {user}`yuvipanda`
- Add command line option to pass extra build args {pr}`1100` by {user}`TimoRoth`
- Set labels when building image from Dockerfile {pr}`1097` by {user}`TimoRoth`
- jupyterlab 3.1.17 {pr}`1092` by {user}`minrk`
- Bump JupyterLab to 3.1.11 {pr}`1081` by {user}`choldgraf`
- Bootstrap base env with micromamba {pr}`1062` by {user}`wolfv`
- Default UI to JupyterLab {pr}`1035` by {user}`SylvainCorlay`

### API changes

### Bug fixes

### Other merged PRs

- Put micromamba in /usr/local/bin and use mamba for installs {pr}`1128` by {user}`minrk`
- Remove deprecated calls to distutils {pr}`1122` by {user}`minrk`
- Delete /tmp/downloaded_packages after running install.R {pr}`1119` by {user}`yuvipanda`
- Use a smaller R library in our tests {pr}`1118` by {user}`yuvipanda`
- Only get R itself (r-base-core) from apt, not CRAN packages {pr}`1117` by {user}`minrk`
- set USER root after each directive block {pr}`1115` by {user}`minrk`
- Say 'apt repository' rather than PPA {pr}`1111` by {user}`yuvipanda`
- add tests for R conda {pr}`1108` by {user}`aplamada`
- Add help message to freeze.py {pr}`1106` by {user}`manics`
- Quieter R builds {pr}`1103` by {user}`yuvipanda`
- update user_interface doc to reflect that lab is default {pr}`1085` by {user}`minrk`
- Updates to dev docs + Recommonmark -> MyST Parser {pr}`1082` by {user}`choldgraf`
- Fix Docker build (again) {pr}`1078` by {user}`manics`
- \[mrg\] \_\_init\_\_.py: r_version: fixed description {pr}`1074` by {user}`magnush0lm`
- Typo fix in utils docstring {pr}`1072` by {user}`jgarte`
- Rename requirements.py-3.5.txt to requirements.py-3.5.pip {pr}`1061` by {user}`manics`
- Remove nodesource' nodejs {pr}`847` by {user}`yuvipanda`

## Version 2021.08.0

[Full changelog](https://github.com/jupyterhub/repo2docker/compare/2021.03.0...2021.08.0)

The repo2docker container image has moved to [quay.io/jupyterhub/repo2docker](https://quay.io/repository/jupyterhub/repo2docker?tab=tags)

### New features

- always unpack a single zenodo zip {pr}`1043` by {user}`akhmerov`
- Refreeze with conda-lock {pr}`1024` by {user}`minrk`
- Refine buffered output debugging {pr}`1016` by {user}`minrk`
- reimplement entrypoint in Python {pr}`1014` by {user}`minrk`
- Fetch available Julia versions from hosted json {pr}`994` by {user}`tomyun`
- Define an interface for Container engines {pr}`848` by {user}`manics`

### API changes

### Bug fixes

- Workaround docker-py dependency's failure to import six {pr}`1066:` by {user}`consideratio`
- fix: add chardet, a not explicitly declared dependency {pr}`1064` by {user}`johnhoman`
- Add build-base to build stage of docker image {pr}`1051` by {user}`yuvipanda`
- Fix regression in hydroshare introduced after moving to requests {pr}`1034` by {user}`MridulS`

### Other merged PRs

- Update README quay.io URL, Add docker latest tag {pr}`1075` by {user}`manics`
- GitHub workflow build and push to Docker hub {pr}`1071` by {user}`manics`
- Rename master branch to main {pr}`1068` by {user}`manics`
- Remove Pipfile & Pipfile.lock {pr}`1054` by {user}`yuvipanda`
- Remove CircleCI docs build {pr}`1053` by {user}`yuvipanda`
- Pin doc requirements to avoid CI breakages {pr}`1052` by {user}`manics`
- Stop using deprecated add_stylesheet in sphinx {pr}`1050` by {user}`yuvipanda`
- Add study participation notice to readme {pr}`1046` by {user}`sgibson91`
- Bump urllib3 from 1.26.4 to 1.26.5 {pr}`1045` by {user}`dependabot`
- State newly used installation command {pr}`1040` by {user}`fkohrt`
- Bump pyyaml from 5.1.1 to 5.4 {pr}`1029` by {user}`dependabot`
- Set default Julia version to 1.6 {pr}`1028` by {user}`tomyun`
- Fix logo URL in README {pr}`1027` by {user}`betatim`

## Version 2021.03.0

[Full changelog](https://github.com/jupyterhub/repo2docker/compare/2021.01.0...2021.03.0)

### New features

- freeze with mamba, add 3.9 {pr}`1017` by {user}`minrk`
- Add GH workflow to push releases to PYPi and introduce CalVer {pr}`1004` by {user}`betatim`
- Add entrypoint script which automatically propagates \*\_PROXY env vars… {pr}`1003` (\[@g-braeunlich\](<https://github.com/g-braeunlich>))
- Update to JupyterLab 3.0 {pr}`996` by {user}`jtpio`
- Fetch available Julia versions from hosted json {pr}`994` by {user}`tomyun`
- Add a contentprovider for Software Heritage persistent ID (SWHID) {pr}`988` by {user}`douardda`
- Stream jupyter server logs to a file {pr}`987` by {user}`betatim`
- add 4.0, 4.0.2 to list of supported R versions {pr}`960` by {user}`minrk`

### API changes

### Bug fixes

- fix dataverse regression introduced in last release {pr}`1011` by {user}`MridulS`
- buildpacks.r: dont use apt-key directly to respect \*\_proxy env vars {pr}`1019` (\[@g-braeunlich\](<https://github.com/g-braeunlich>))

### Other merged PRs

- Cleanup install_requires including duplicates {pr}`1020` by {user}`manics`
- bump docker action version {pr}`1018` by {user}`minrk`
- bump python in circleci test {pr}`1013` by {user}`minrk`
- Investigating the missing logs {pr}`1008` by {user}`betatim`
- Experiment with different install mechanism to get code coverage stats again {pr}`982` by {user}`betatim`

## Version 2021.01.0

[Full changelog](https://github.com/jupyterhub/repo2docker/compare/0.11.0...2021.01.0)

### New features

- Replace urllib by requests in contentproviders {pr}`993` by {user}`douardda`
- Use mambaforge instead of miniforge {pr}`992` by {user}`SylvainCorlay`
- buildpacks/nix: 2.3 -> 2.3.9 {pr}`991` by {user}`FRidh`
- Drop support for stencila {pr}`985` by {user}`minrk`
- Add Julia 1.5.3 support {pr}`984` by {user}`tomyun`
- Update to node 14 {pr}`983` by {user}`jtpio`
- Mamba 0.6.1 {pr}`979` by {user}`minrk`
- Ensure REPO_DIR owned by NB_USER {pr}`975` by {user}`tomyun`
- Add Julia 1.5.2 support {pr}`965` by {user}`tomyun`
- Mamba number three {pr}`962` by {user}`SylvainCorlay`
- Add a Mercurial contentprovider {pr}`950` by {user}`paugier`
- Add Julia 1.5.1 support {pr}`949` by {user}`tomyun`
- Handle requirements.txt with `--pre` lines {pr}`943` by {user}`betatim`
- Add Julia 1.5.0 support {pr}`938` by {user}`tomyun`
- Update JupyterLab to 2.2.0 {pr}`933` by {user}`manics`
- Bump nix version to 2.3 {pr}`915` by {user}`jboynyc`
- Add nbresuse==0.3.3 (full freeze.py) {pr}`904` by {user}`manics`
- Add Julia 1.4.2 support {pr}`899` by {user}`davidanthoff`
- Bump version of irkernel for R 4.0 {pr}`892` by {user}`betatim`
- chmod start script from repo2docker-entrypoint {pr}`886` by {user}`danlester`
- pypi jupyter-offlinenotebook==0.1.0 {pr}`880` by {user}`manics`
- Add support for Julia 1.4.1 {pr}`878` by {user}`davidanthoff`
- Change --env option to work like docker's {pr}`874` by {user}`hwine`
- Add support for Julia 1.4.0 {pr}`870` by {user}`davidanthoff`
- Update server proxy and rsession proxy {pr}`869` by {user}`betatim`
- Use miniforge instead of miniconda to get conda {pr}`859` by {user}`yuvipanda`
- If looking for latest MRAN URL try earlier snapshots too {pr}`851` by {user}`manics`
- Add jupyter-offlinenotebook extension {pr}`845` by {user}`betatim`

### API changes

- Bump Python requirement to 3.6 from 3.5 {pr}`951` by {user}`betatim`

### Bug fixes

- buildpacks/nix: disable sandboxing (bugfix) {pr}`990` by {user}`FRidh`
- avoid deprecated import of collections.abc {pr}`924` by {user}`minrk`
- Add missing “:” for R code {pr}`900` by {user}`adamhsparks`
- Fix RShiny proxy {pr}`893` by {user}`betatim`
- Work around a Julia bug {pr}`879` by {user}`davidanthoff`
- Fix typo {pr}`862` by {user}`jtpio`

### Other merged PRs

- Fix figshare test {pr}`1001` by {user}`manics`
- Weekly test of master to check for external failures {pr}`998` by {user}`manics`
- Remove reference to `master` branch from CLI doc {pr}`977` by {user}`betatim`
- add chown to COPY commands to reduce layer count {pr}`969` by {user}`bollwyvl`
- set TIMEFORMAT for timed bash conda commands {pr}`966` by {user}`manics`
- Disable jupyterlab extension build minimize {pr}`963` by {user}`manics`
- Bump Black version to 20.8b1 and use --target-version=py36 {pr}`955` by {user}`paugier`
- Add workflow to build Docker image {pr}`954` by {user}`manics`
- Crosslink 'Configuring your repository' with usage {pr}`952` by {user}`manics`
- Add `www-frame-origin=same` to /etc/rstudio/rserver.conf {pr}`944` (\[@rkevin-arch\](<https://github.com/rkevin-arch>))
- GitHub Actions {pr}`942` by {user}`minrk`
- stop running tests on travis {pr}`940` by {user}`minrk`
- update repo URLs for jupyterhub/repo2docker {pr}`939` by {user}`minrk`
- Upgrade custom test infrastructure for pytest 6.0.0 {pr}`936` by {user}`betatim`
- validate_image_name: mention lowercase, fix formatting {pr}`934` by {user}`manics`
- Update snapshot date for simple R test {pr}`930` by {user}`betatim`
- little improvement for testing binder_dir {pr}`928` by {user}`bitnik`
- update docs for config dirs {pr}`927` by {user}`bitnik`
- doc: runtime.txt installs python x.y (& concise rewording) {pr}`914` by {user}`mdeff`
- doc: environment.yml installs a conda env, not only python {pr}`913` by {user}`mdeff`
- Make the memory limit test simpler {pr}`912` by {user}`betatim`
- Add gitpod.io config for docs {pr}`908` by {user}`betatim`
- fix repo2docker logo in Sphinx docs {pr}`906` by {user}`trallard`
- Update Dockerfile to add Docker {pr}`896` by {user}`hamelsmu`
- Document test failure workarounds {pr}`890` by {user}`hwine`
- Workaround Docker issue impacting some tests on macOS {pr}`882` by {user}`hwine`
- \[docs\] fix grammatical error in section title {pr}`872` by {user}`jameslamb`
- Fix long form args requirements {pr}`866` by {user}`betatim`
- Adopt new Sphinx theme name {pr}`864` by {user}`xhochy`
- Document loose conda export with --from-history {pr}`863` by {user}`xhochy`
- utils.execute_cmd flush buffer if no EOL {pr}`850` by {user}`manics`
- Update black 19.10b0, target Python 3.5 {pr}`849` by {user}`manics`
- docs: postBuild warn about shell script errors being ignored {pr}`844` by {user}`manics`
- Update changelog for 0.11.0 {pr}`842` by {user}`betatim`

## Version 0.11.0

Release date: 2020-02-05

### New features

- Add support for Figshare in {pr}`788` by {user}`nuest`.
- Add support for Dataverse in {pr}`739` by {user}`Xarthisius`.
- Add support for configuring the version of R installed in {pr}`772` by
  {user}`betatim`.
- Add support for Julia 1.2.0 in {pr}`768` by {user}`davidanthoff`.
- Add support for Julia 1.3.0 and 1.0.5 in {pr}`822` by {user}`davidanthoff`.
- Add support for Julia 1.3.1 in {pr}`831` by {user}`davidanthoff`.
- Update Miniconda to 4.7.10 in {pr}`769` by {user}`davidrpugh`.
- Update IRKernel to 1.0.2 in {pr}`770` by {user}`GeorgianaElena`.
- Update RStudio to 1.2 in {pr}`803` by {user}`pablobernabeu`.
- Switch to "pandas" sphinx theme for documentation in {pr}`816` by {user}`choldgraf`.
- Add content provider documentation in {pr}`824` by {user}`choldgraf`.
- Remove legacy buildpack in {pr}`829` by {user}`betatim`.
- Add support for automatic RStudio install when using R packages via conda
  in {pr}`838` by {user}`xhochy`.
- Add support for Python 3.8 in {pr}`840` by {user}`minrk`.
- Add Hydroshare as content provider in {pr}`800` by {user}`sblack-usu`.
- Update to Jupyter Notebook 6 and Lab 1.2 in {pr}`839` by {user}`minrk`.

### Bug fixes

- Fix for submodule check out in {pr}`809` by {user}`davidbrochart`.
- Handle `requirements.txt` files with different encodings in {pr}`771`
  by {user}`GeorgianaElena`.
- Update to nteract-on-jupyter 2.1.3 in {pr}`2.1.3 by :user:`betatim`.
- Use `useradd --no-log-init` to fix exhausting disk space in {pr}`804` by
  {user}`manics.`
- Add help text for commandline arguments in {pr}`517` by {user}`yuvipanda`.
- Fix submodule checkout in {pr}`809` by {user}`davidbrochart`.

## Version 0.10.0

Release date: 2019-08-07

### New features

- Increased minimum Python version supported for running `repo2docker` itself
  to Python 3.5 in {pr}`684` by {user}`betatim`.
- Support for `Pipfile` and `Pipfile.lock` implemented in {pr}`649` by
  {user}`consideratio`.
- Use only conda packages for our base environments in {pr}`728` by
  {user}`scottyhq`.
- Fast rebuilds when repo dependencies haven't changed by {user}`minrk` and
  {user}`betatim` in {pr}`743`, {pr}`752`, {pr}`718` and {pr}`716`.
- Add support for Zenodo in {pr}`693` by {user}`betatim`.
- Add support for general Invenio repositories in {pr}`704` by {user}`tmorrell`.
- Add support for julia 1.0.4 and 1.1.1 in {pr}`710` by {user}`davidanthoff`.
- Bump Conda from 4.6.14 to 4.7.5 in {pr}`719` by {user}`davidrpugh`.

### API changes

### Bug fixes

- Prevent building the image as root if --user-id and --user-name are not specified
  in {pr}`676` by {user}`Xarthisius`.
- Add bash to Dockerfile to fix usage of private repos with git-crendential-env in
  {pr}`738` by {user}`eexwhyzee`.
- Fix memory limit enforcement in {pr}`677` by {user}`betatim`.

## Version 0.9.0

Release date: 2019-05-05

### New features

- Support for julia `Project.toml`, `JuliaProject.toml` and `Manifest.toml` files in {pr}`595` by
  {user}`davidanthoff`
- Set JULIA_PROJECT globally, so that every julia instance starts with the
  julia environment activated in {pr}`612` by {user}`davidanthoff`.
- Update Miniconda version to 4.6.14 and Conda version to 4.6.14 in {pr}`637` by
  {user}`jhamman`
- Install notebook into `notebook` env instead of `root`.
  Activate conda environments and shell integration via ENTRYPOINT
  in {pr}`651` by {user}`minrk`
- Support for `.binder` directory in addition to `binder` directory for location of
  configuration files, in {pr}`653` by {user}`jhamman`.
- Updated contributor guide and issue templates for bugs, feature requests,
  and support questions in {pr}`654` and {pr}`655` by {user}`KirstieJane` and
  {user}`betatim`.
- Create a page naming and describing the "Reproducible Execution
  Environment Specification" (the specification used by repo2docker)
  in {pr}`662` by {user}`choldgraf`.

### API changes

### Bug fixes

- Install IJulia kernel into \$\{NB_PYTHON_PREFIX}/share/jupyter in {pr}`622` by
  {user}`davidanthoff`.
- Ensure git submodules are updated and initilized correctly in {pr}`639` by
  {user}`djhoese`.
- Use archive.debian.org as source for the debian jessie based legacy
  buildpack in {pr}`633` by {user}`betatim`.
- Update to version 5.7.6 of the `notebook` package used in all environments
  in {pr}`628` by {user}`betatim`.
- Update to version 5.7.8 of the `notebook` package and version 2.0.12 of
  `nteract-on-jupyter` in {pr}`650` by {user}`betatim`.
- Switch to newer version of jupyter-server-proxy to fix websocket handling
  in {pr}`646` by {user}`betatim`.
- Update to pip version 19.0.3 in {pr}`647` by {user}`betatim`.
- Ensure ENTRYPOINT is an absolute path in {pr}`657` by {user}`yuvipanda`.
- Fix handling of `--build-memory-limit` values without a postfix in {pr}`652`
  by {user}`betatim`.

## Version 0.8.0

Release date: 2019-02-21

### New features

- Add additional metadata to docker images about how they were built {pr}`500` by
  {user}`jrbourbeau`.
- Allow users to install global NPM packages: {pr}`573` by {user}`GladysNalvarte`.
- Add documentation on switching the user interface presented by a
  container. {pr}`568` by user:`choldgraf`.
- Increased test coverage to ~87% by {user}`betatim` and {user}`yuvipanda`.
- Documentation improvements and additions by {user}`lheagy`, {user}`choldgraf`.
- Remove f-strings from code base, repo2docker is compatible with Python 3.4+
  again by {user}`jrbourbeau` in {pr}`520`.
- Local caching of previously built repostories to speed up launch times
  by {user}`betatim` in {pr}`511`.
- Make destination of repository content in the container image configurable
  on the CLI via `--target-repo-dir`. By {user}`yuvipanda` in {pr}`507`.
- Expose CPU limit settings for building and running containers. By
  {user}`GladysNalvarte` in {pr}`579`.
- Make Python 3.7 the default version. By {user}`yuvipanda` and {user}`minrk` in
  {pr}`539`.

### API changes

### Bug fixes

- In some cases the version of conda installed in images was not pinned and got
  upgraded by user actions. Fixed in {pr}`576` by {user}`minrk`.
- Fix an error related to checking if debug output was enabled or not:
  {pr}`575` by {user}`yuvipanda`.
- Update nteract frontend to version 2.0.0 by {user}`yuvipanda` in {pr}`571`.
- Fix quoting issue in `GIT_CREDENTIAL_ENV` environment variable by
  {user}`minrk` in {pr}`572`.
- Change to using the first 8 characters of each Git commit, not the last 8,
  to tag each built docker image of repo2docker itself. {user}`minrk` in {pr}`562`.
- Allow users to select the Julia when using a `requirements.txt` by
  {user}`yuvipanda` in {pr}`557`.
- Set `JULIA_DEPOT_PATH` to install packages outside the home directory by
  {user}`yuvipanda` in {pr}`555`.
- Update to Jupyter notebook 5.7.4 {pr}`519` by {user}`minrk`.

## Version 0.7.0

Release date: 2018-12-12

### New features

- Build from sub-directory: build the image based on a sub-directory of a
  repository {pr}`413` by {user}`dsludwig`.
- Editable mode: allows editing a local repository from a live container
  {pr}`421` by {user}`evertrol`.
- Change log added {pr}`426` by {user}`evertrol`.
- Documentation: improved the documentation for contributors {pr}`453` by
  {user}`choldgraf`.
- Buildpack: added support for the nix package manager {pr}`407` by
  {user}`costrouc`.
- Log a 'success' message when push is complete {pr}`482` by
  {user}`yuvipanda`.
- Allow specifying images to reuse cache from {pr}`478` by
  {user}`yuvipanda`.
- Add JupyterHub back to base environment {pr}`476` by {user}`yuvipanda`.
- Repo2docker has a logo! by {user}`agahkarakuzu` and {user}`blairhudson`.
- Improve support for Stencila, including identifying stencila runtime from
  document context {pr}`457` by {user}`nuest`.

### API changes

- Add content provider abstraction {pr}`421` by {user}`betatim`.

### Bug fixes

- Update to Jupyter notebook 5.7 {pr}`475` by {user}`betatim` and {user}`minrk`.

## Version 0.6

Released 2018-09-09

## Version 0.5

Released 2018-02-07

## Version 0.4.1

Released 2018-09-06

## Version 0.2

Released 2018-05-25

## Version 0.1.1

Released 2017-04-19

## Version 0.1

Released 2017-04-14
