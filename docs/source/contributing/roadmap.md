# The repo2docker roadmap

This roadmap collects "next steps" for repo2docker. It is about creating a
shared understanding of the project's vision and direction amongst
the community of users, contributors, and maintainers.
The goal is to communicate priorities and upcoming release plans.
It is not a aimed at limiting contributions to what is listed here.

## Using the roadmap
### Sharing Feedback on the Roadmap

All of the community is encouraged to provide feedback as well as share new
ideas with the community. Please do so by submitting an issue. If you want to
have an informal conversation first use one of the other communication channels.
After submitting the issue, others from the community will probably
respond with questions or comments they have to clarify the issue. The
maintainers will help identify what a good next step is for the issue.


### What do we mean by "next step"?

When submitting an issue, think about what "next step" category best describes
your issue:

* **now**, concrete/actionable step that is ready for someone to start work on.
These might be items that have a link to an issue or more abstract like
"decrease typos and dead links in the documentation"
* **soon**, less concrete/actionable step that is going to happen soon,
discussions around the topic are coming close to an end at which point it can
move into the "now" category
* **later**, abstract ideas or tasks, need a lot of discussion or
experimentation to shape the idea so that it can be executed. Can also
contain concrete/actionable steps that have been postponed on purpose
(these are steps that could be in "now" but the decision was taken to work on
them later)


### Reviewing and Updating the Roadmap

The roadmap will get updated as time passes (next review by 1st December) based
on discussions and ideas captured as issues.
This means this list should not be exhaustive, it should only represent
the "top of the stack" of ideas. It should
not function as a wish list, collection of feature requests or todo list.
For those please create a
[new issue](https://github.com/jupyter/repo2docker/issues/new).

The roadmap should give the reader an idea of what is happening next, what needs
input and discussion before it can happen and what has been postponed.


## The roadmap proper
### Project vision

Repo2docker is a dependable tool used by humans that reduces the complexity of
creating the environment in which a piece of software can be executed.


### Now

These "Now" items are considered active areas of focus for the project:
* reduce documentation typos and syntax errors
* add Julia Manifest support (https://docs.julialang.org/en/v1/stdlib/Pkg/index.html)
* increase test coverage (see https://codecov.io/gh/jupyter/repo2docker/tree/master/repo2docker for low coverage files)
* reduce execution time of tests
* make a new release once Pipfile and nix support have been merged


### Soon

These "Soon" items are under discussion. Once an item reaches the point of an
actionable plan, the item will be moved to the "Now" section. Typically,
these will be moved at a future review of the roadmap.
* create the contributor highway, define the route from newcomer to project lead
* add support for using ZIP files as the repo (`repo2docker https://example.com/an-archive.zip`) this will give us access to several archives (like Zenodo) that expose things as ZIP files.
* add support for Zenodo (`repo2docker 10.5281/zenodo.1476680`) so Zenodo software archives can be used as the source in addition to a git repository
* tooling to make it easier to produce good `requirements.txt`, `environment.yml`, etc files. They should help users create versions of these files that have a high chance of still working in a few months
* support for running with GPU acceleration


### Later

The "Later" items are things that are at the back of the project's mind. At this
time there is no active plan for an item. The project would like to find the
resources and time to discuss these ideas.
* repo2docker in repo2docker, to reproduce an environment users need to specify the repository and the version of repo2docker to use. Add support for repo2docker inspecting a repo and then starting a different version of itself to build the image
* support execution on a remote host (with more resources than available locally) via the command-line
