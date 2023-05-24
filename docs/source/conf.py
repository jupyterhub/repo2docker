# Configuration file for Sphinx to build our documentation to HTML.
#
# Configuration reference: https://www.sphinx-doc.org/en/master/usage/configuration.html
#
import datetime

# -- Project information -----------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
#
project = "repo2docker"
copyright = f"{datetime.date.today().year}, Project Jupyter Contributors"
author = "Project Jupyter Contributors"


# -- General Sphinx configuration ---------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
#
extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx.ext.extlinks",
    "sphinxcontrib.autoprogram",
    "sphinxext.opengraph",
    "sphinxext.rediraffe",
]
root_doc = "index"
source_suffix = [".md", ".rst"]
default_role = "literal"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
templates_path = ["_templates"]
extlinks = {
    "issue": ("https://github.com/jupyterhub/repo2docker/issues/%s", "Issue #%s"),
    "pr": ("https://github.com/jupyterhub/repo2docker/pull/%s", "PR #%s"),
    "user": ("https://github.com/%s", "@%s"),
}


# -- General MyST configuration -----------------------------------------------------
# ref: https://myst-parser.readthedocs.io/en/latest/configuration.html
#
myst_enable_extensions = [
    "colon_fence",
]


# -- Referenceable variables --------------------------------------------------
#
# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
import repo2docker

version = repo2docker.__version__
# The full version, including alpha/beta/rc tags.
release = version

from repo2docker.buildpacks.conda import CondaBuildPack

default_python = CondaBuildPack.major_pythons["3"]

rst_prolog = f"""
.. |default_python| replace:: **Python {default_python}**
.. |default_python_version| replace:: {default_python}
"""


# -- Options for HTML output -------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
#
html_logo = "_static/images/logo.png"
html_favicon = "_static/images/favicon.ico"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# pydata_sphinx_theme reference: https://pydata-sphinx-theme.readthedocs.io/en/latest/
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "use_edit_page_button": True,
    "github_url": "https://github.com/jupyterhub/repo2docker",
}
html_context = {
    "github_user": "jupyterhub",
    "github_repo": "repo2docker",
    "github_version": "main",
    "doc_path": "docs/source",
}


# -- Options for linkcheck builder -------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder
#
linkcheck_ignore = [
    r"(.*)github\.com(.*)#",  # javascript based anchors
    r"(.*)/#%21(.*)/(.*)",  # /#!forum/jupyter - encoded anchor edge case
    r"https://github.com/[^/]*$",  # too many github usernames / searches in changelog
    "https://github.com/jupyterhub/repo2docker/pull/",  # too many PRs in changelog
    "https://github.com/jupyterhub/repo2docker/compare/",  # too many comparisons in changelog
]
linkcheck_anchors_ignore = [
    "/#!",
    "/#%21",
]


# -- Options for the opengraph extension -------------------------------------
# ref: https://github.com/wpilibsuite/sphinxext-opengraph#options
#
# This extension help others provide better thumbnails and link descriptions
# when they link to this documentation from other websites, such as
# https://discourse.jupyter.org.
#
# ogp_site_url is set automatically by RTD
ogp_image = "_static/images/logo.png"
ogp_use_first_image = True


# -- Options for the rediraffe extension -------------------------------------
# ref: https://github.com/wpilibsuite/sphinxext-rediraffe#readme
#
# This extensions help us relocated content without breaking links. If a
# document is moved internally, we should configure a redirect like below.
#
rediraffe_branch = "main"
rediraffe_redirects = {
    # "old-file": "new-folder/new-file-name",
}
