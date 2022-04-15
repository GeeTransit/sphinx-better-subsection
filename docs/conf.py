"""Configuration for the Sphinx documentation builder"""

import os
import re
import subprocess
import sys

if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

# - Project config

# Repo root relative to this file's directory
root = ".."

# Helper function to return text of file relative to the repo root
def read(filename: str) -> str:
    with open(os.path.join(root, filename)) as file:
        return file.read()

# Single source the project name from pyproject.toml
project = tomllib.loads(read("pyproject.toml"))["project"]["name"]

# Single source copyright. The format is ([] denoting optional parts):
# Copyright [(c)] [2022[-present]] John Doe [<email>] [(website)]
year, holder = re.search(
    r'''
        Copyright[ ]*  # Locate "Copyright"
        (?:(?:\(c\)|\N{COPYRIGHT SIGN})[ ]*)?  # Optional sign
        # Year ranges separated by commas
        (?:
            (
                (?:\d+(?:[ ]*-[ ]*(?:\d+))?,[ ]*)*
                \d+(?:[ ]*-[ ]*(?:\d+|present))?
            )
            ,?
        )?
        [ ]*
        (?:by[ ]*)?
        (
            [^ \n,.]+
            (?:
                [ ]*[,.]?[ ]*
                (?!
                    [^ @]+@  # Don't match emails (have @ in them)
                    |All rights reserved  # Don't match boilerplate text
                    |[^ :]+://  # Don't match websites
                    |[<(]  # Don't match <email> or (website)
                )
                [^ \n,.]+
            )*
            [.]?
        )
    ''',
    read("LICENSE"),
    re.MULTILINE | re.VERBOSE | re.IGNORECASE,
).groups()
author = holder.strip()
copyright = f"{year}, {author}" if year else author

# Single source the project version from the installed package's version
version = importlib_metadata.version(project)
try:
    # Try getting the package's version from Hatch's CLI if possible. The
    # version is different when a new commit is added but the installed package
    # isn't updated (editable installs don't have dynamic versions).
    version = subprocess.run(
        ["hatch", "version"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
except subprocess.CalledProcessError:
    pass
release = version

# - Sphinx config

# Allow less verbose references (e.g. `list` instead of :py:class:`list`)
default_role = "any"

# Add last updated timestamp
html_last_updated_fmt = "%B %d, %Y"  # strftime format

templates_path = ["_templates"]
exclude_patterns = ["_build"]

# - Extension config

extensions = []

# Custom extensions are located in _extensions
# sys.path.append(os.path.abspath("_extensions"))

# View code from the docs
extensions += ["sphinx.ext.viewcode"]

# Set section permalink
extensions += ["sphinx_better_subsection"]

# Recursively generate docs using autosummary
extensions += ["sphinx.ext.autosummary"]
# Always generate missing summaries (located in _generated/api)
autosummary_generate = True

# Generate docs from docstrings
extensions += ["sphinx.ext.autodoc"]
# Combine __init__ with class docstring
autoclass_content = "both"

# Support Google style docstrings and type annotations
extensions += ["sphinx.ext.napoleon", "sphinx_autodoc_typehints"]
# Disable separate "Return type" field
napoleon_use_rtype = False
typehints_use_rtype = False
# Show default values after the argument type - like "(int, default=-1)"
typehints_defaults = "comma"
# Show argument types even if the docstring has no "Arguments" field
always_document_param_types = True

# - HTML output config

html_theme = "alabaster"
html_static_path = ["_static"]
html_css_files = [
    # Contains some minor CSS improvements to Alabaster
    "custom.css",
]
html_theme_options = {
    # Allow larger windows to have wider text (default is a hardcoded width)
    "page_width": "auto",
    "body_max_width": "auto",
    # Don't have a minimum width
    "body_min_width": "0",
    # Add GitHub "Watch" button
    "github_button": True,
    "github_user": "GeeTransit",
    "github_repo": "sphinx-better-subsection",
    "github_type": "star",
}
html_permalinks_icon = "#"  # More consistent with other sites
