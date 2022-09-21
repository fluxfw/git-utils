#!/usr/bin/env python
from datetime import datetime
from json import dumps, load
from os import getcwd
from os.path import exists, join
from re import sub

folder = getcwd()

_metadata_json_file = join(folder, "metadata.json")
_composer_json_file = join(folder, "composer.json")
_package_json_file = join(folder, "package.json")
if exists(_metadata_json_file):
    metadata_json_file = _metadata_json_file
else:
    if exists(_composer_json_file):
        metadata_json_file = _composer_json_file
    else:
        if exists(_package_json_file):
            metadata_json_file = _package_json_file
        else:
            metadata_json_file = _metadata_json_file

changelog_md_file = join(folder, "CHANGELOG.md")
plugin_php_file = join(folder, "plugin.php")

metadata = None
if exists(metadata_json_file):
    with open(metadata_json_file, "r") as fp:
        metadata = load(fp)

if metadata is None:
    metadata = {}

date = datetime.now()
new_version_date = f"{date.year}-{date.month:0>2}-{date.day:0>2}"

old_version = None
if "version" in metadata:
    old_version = metadata["version"]

new_version_increment = 0
if old_version is not None:
    if old_version.startswith(new_version_date):
        new_version_increment = int(old_version[len(new_version_date) + 1:])

new_version_increment += 1
new_version = f"{new_version_date}-{new_version_increment}"

metadata["version"] = new_version

with open(metadata_json_file, "w") as fp:
    fp.write(f"{dumps(metadata, indent=4)}\n")

changelog = None
if exists(changelog_md_file):
    with open(changelog_md_file, "r") as fp:
        changelog = fp.read()

if changelog is None or changelog.strip() == "":
    changelog = f"""# Changelog

## latest

Changes:

\-
"""

latest_start_position = changelog.find("## latest")
if latest_start_position == -1:
    latest_start_position = 0
old_latest_changelog = changelog[latest_start_position:]

latest_end_position = old_latest_changelog.find("\n## ")
if latest_end_position != -1:
    old_latest_changelog = old_latest_changelog[:latest_end_position]

new_version_changelog = old_latest_changelog.replace("latest", f"v{new_version}")

new_latest_changelog = sub(r"Changes\s*:\s*(.+\n)+\n*", "Changes:\n\n\-\n", old_latest_changelog)

changelog = changelog.replace(old_latest_changelog, f"""{new_latest_changelog}
{new_version_changelog}""")

with open(changelog_md_file, "w") as fp:
    fp.write(changelog)

if exists(plugin_php_file):
    plugin = ""
    with open(plugin_php_file, "r") as fp:
        plugin = fp.read()

    plugin_new_version = new_version_date.replace("-", ".")

    plugin = sub("\$version\s*=\s*[\"'][0-9.]+[\"']", f"$version = \"{plugin_new_version}\"", plugin)

    with open(plugin_php_file, "w") as fp:
        fp.write(plugin)
