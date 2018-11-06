# The repo2docker roadmap

This roadmap collects "next steps" for the project. The goal is to
communicate where the current priorities are and where the project is heading.
It is not a list aimed at limiting contributions to what is listed here. If
something is not listed here please do bring it up in a new issue or start
work on it.

Each "next step" should fit into one of the following three categories:

* **now**, concrete/actionable step that is ready for someone to start work on.
These might be items that have a link to an issue or more abstract like
"decrease typos and dead links in the documentation"
* **soon**, less concrete/actionable step that is going to happen soon,
discussions around the topic are coming close to an end at which point it can
move into the "now" category
* **later**, abstract ideas or tasks, need a lot of discussion or
experimentation to shape the idea so that it can be discussed. Should also
contain concrete/actionable steps that have been postponed on purpose
(these are steps that could be in "now" but the decision was taken to work on
them later)

The roadmap will get updated as time passes (next review by 1st December).
This means this list should not be exhaustive, it should only represent
the "top of the stack" of ideas. It should
not function as a wish list, collection of feature requests or todo list.
For those please create a
[new issue](https://github.com/jupyter/repo2docker/issues/new).

The roadmap should give the reader an idea of what is happening next, what needs
input and discussion before it can happen and what has been postponed.


## Guiding thought for the next months
Repo2docker is a dependable tool used by humans that reduces the complexity of creating the environment in which a piece of software can be executed.


## Now
* reduce documentation typos and syntax errors
* add Julia Manifest support (https://docs.julialang.org/en/v1/stdlib/Pkg/index.html)
* increase test coverage (see https://codecov.io/gh/jupyter/repo2docker/tree/master/repo2docker for low coverage files)
* reduce execution time of tests
* make a new release once Pipfile and nix support have been merged

## Soon
* create the contributor highway, define the route from newcomer to project lead
* add support for using ZIP files as the repo (`repo2docker https://example.com/an-archive.zip`) this will give us access to several archives (like Zenodo) that expose things as ZIP files.
* add support for Zenodo (`repo2docker 10.5281/zenodo.1476680`) so Zenodo software archives can be used as the source in addition to a git repository
* tooling to make it easier to produce good `requirements.txt`, `environment.yml`, etc files. They should help users create versions of these files that have a high chance of still working in a few months
* support for running with GPU acceleration

## Later
* repo2docker in repo2docker, to reproduce an environment users need to specify the repository and the version of repo2docker to use. Add support for repo2docker inspecting a repo and then starting a different version of itself to build the image
* support execution on a remote host (with more resources than available locally) via the command-line
