"""Configuration for gitchangelog"""

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

# gitchangelog sets current directory to the repo root
root = "."

# Helper function to return text of file relative to the repo root
def read(filename: str) -> str:
    with open(os.path.join(root, filename)) as file:
        return file.read()

# Single source the project name from pyproject.toml
name = tomllib.loads(read("pyproject.toml"))["project"]["name"]

# Single source the project version from the installed package's version
version = importlib_metadata.version(name)
try:
    # See comment conf.py near similar code for reasoning
    version = subprocess.run(
        ["hatch", "version"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
except subprocess.CalledProcessError:
    pass
unreleased_version_label = f'v{version}'

# Include tags that start with "v" and don't end with "-dev". Those tags are
# just to bump the version setuptools_scm gives.
tag_filter_regexp = r"^v[0-9].*(?<!-dev)$"

# Don't include merge commits (I think squash & merge are still included)
include_merge = False

# Ignore minor changes by adding !minor or other words
ignore_regexps = [
    r"!(minor|cosmetic|refactor|wip)",
]

# Specify sections by adding a colon after these words
section_regexps = [
    ("Added", [
        r"(?i)(add|new|feat):",
    ]),
    ("Changed", [
        r"(?i)(chg|change|use|update):",
    ]),
    ("Fixed", [
        r"(?i)(fix):",
    ]),
    ("Deprecated", [
        r"(?i)(depr|deprecate):",
    ]),
    ("Removed", [
        r"(?i)(rem|remove):",
    ]),
    ("Other",
        None  # match everything else
    ),
]

def subject_process(subject: str) -> str:
    # Remove everything before a "::" if it exists
    subject = re.sub(r"^(?:(?!::).)*::(.*)$", r"\1", subject)

    # Remove the ":" from commit types
    for _, regexps in section_regexps:
        if regexps is None:
            continue
        for regexp in regexps:
            subject = re.sub(regexp, r"\1", subject)

    # Make subject more grammatically correct (uppercase + period)
    subject = subject.strip()
    if subject and subject[0].isalpha():
        subject = f'{subject[0].upper()}{subject[1:]}'
    if subject and subject[-1].isalnum():
        subject = f'{subject}.'
    if not subject:
        subject = "No commit message."
    return subject

def post_process_commits(version):
    """Use commit trailer as subject if found and return new version info"""
    # Flatten sections back into a commit list
    commits = []
    for section in version["sections"]:
        for commit in section["commits"]:
            label = section["label"]

            # Post-process commits with a Changelog trailer
            if hasattr(commit["commit"], "trailer_changelog"):
                entry = commit["commit"].trailer_changelog
                if isinstance(entry, list):  # Use just the first entry
                    entry = entry[0]
                # Process the Changelog entry just like the subject
                if any(re.search(regexp, entry) for regexp in ignore_regexps):
                    continue
                for section_label, regexps in section_regexps:
                    if regexps is None:
                        continue  # Default to the subject's section
                    for regexp in regexps:
                        if re.search(regexp, entry):
                            label = section_label  # Overwrite commit's section
                            break
                # Update subject with changelog trailer if not empty
                new_subject = subject_process(entry)
                if new_subject != subject_process(""):
                    commit = {**commit, "subject": new_subject}

            # Append commit with (potentially different) section
            commits.append({**commit, "section": label})

    # Reverse chronological ordering of commits
    commits.sort(
        key=lambda commit: (
            # Use committer timestamp as it contains when the commit *actually*
            # gets merged
            commit["commit"].committer_date_timestamp
        ),
        reverse=True,
    )

    # Create sections and their commits (dicts are ordered also)
    new_sections = {label: [] for label, _ in section_regexps}
    for commit in commits:
        new_sections[commit["section"]].append(commit)

    # Format in gitchangelog way (list of {label: str, commits: list})
    return {
        **version,
        "sections": [
            {"label": label, "commits": commits}
            for label, commits in new_sections.items()
            if len(commits) > 0  # Exclude empty sections
        ]
    }

def output_engine(data, opts=None):
    if opts is None:
        opts = {}

    # Post-process versions' commits before outputting them
    data = {
        **data,
        "versions": (
            new_version
            for version in data["versions"]
            for new_version in [post_process_commits(version)]
            if len(new_version["sections"]) > 0  # Exclude empty versions
        )
    }

    # We're using Mako to generate the CHANGELOG
    engine = makotemplate("docs/_templates/gitchangelog/CHANGELOG.rst")

    # On Windows, the template file has CRLF endings that Mako preserves. On
    # publish, the "\n"s turn into "\r\n". We end up with "\r\r\n", so we
    # remove the LFs to fix the output back to "\r\n".
    for line in engine(data, opts):
        yield line.replace("\r", "")

# Write to the file if the environment variable is specified
def publish(lines) -> None:
    output_filename = os.environ.get("GITCHANGELOG_OUTPUT_FILENAME")
    if output_filename is None:
        return stdout(lines)

    # Ensure the directory exists and write to it
    output_path = os.path.join(root, output_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, mode="w") as file:
        file.writelines(lines)
