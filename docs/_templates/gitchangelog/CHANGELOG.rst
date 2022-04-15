<%
def indent(indent: str, string: str):
    """Indents all lines but the first with the given string"""
    return "".join(
        line if i == 0 else indent + line
        for i, line in enumerate(string.splitlines(keepends=True))
    )
def underline(char: str, string: str):
    """Returns the string followed by a line of the given char"""
    assert len(char) == 1
    return f'{string}\n{char * len(string)}'
%>\
% if data["title"]:
${underline("=", data["title"])}
% endif
% for version in data["versions"]:
<%
tag = version.get("tag")
if tag is not None:
    ref = tag
    title = f'{tag} ({version["date"]})'
else:
    ref = "Unreleased"
    title = f'{opts["unreleased_version_label"]} (Unreleased)'
%>\

.. _${ref}:

${underline("-", title)}
% for section in version["sections"]:
% if section["label"] != "Other" or len(version["sections"]) > 1:

.. _${ref}-${section["label"]}:

${underline("~", section["label"])}
% endif
% for commit in section["commits"]:
- ${indent("  ", commit["subject"])} [${", ".join(commit["authors"])}]
% endfor
% endfor
% endfor
