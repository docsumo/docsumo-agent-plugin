#!/usr/bin/env python3
"""Check the plugin version and GitHub releases. Standard library only.

    python3 .github/scripts/plugin_version.py check                   # both manifests agree on a valid version
    python3 .github/scripts/plugin_version.py check --stable          # ...and it is not a pre-release
    python3 .github/scripts/plugin_version.py check --unreleased      # ...and it is higher than every stable v* tag
    python3 .github/scripts/plugin_version.py check --newer-than REF  # ...and higher than the version at git REF
                                                                      # (implies --unreleased)
    python3 .github/scripts/plugin_version.py version                 # print the version
    python3 .github/scripts/plugin_version.py last-release            # print the highest stable v* tag below the
                                                                      # version, or nothing
    python3 .github/scripts/plugin_version.py release                 # check a release published by hand

`release` reads the release from RELEASE_TAG, RELEASE_TITLE, RELEASE_NOTES and RELEASE_PRERELEASE ("true" or
"false"), and checks the commit that is checked out. A stable release must be on MAIN_REF (default origin/main).
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parents[2]
GIT = shutil.which("git") or "git"
MANIFESTS = (".claude-plugin/plugin.json", ".codex-plugin/plugin.json")
MARKETPLACE = ".claude-plugin/marketplace.json"
# MAJOR.MINOR.PATCH with an optional pre-release such as 0.2.0-rc.1 (semver.org, no build metadata).
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$")


def say(text, stream=sys.stdout):
    stream.write(f"{text}\n")


def fail(message: str) -> NoReturn:
    say(f"error: {message}", sys.stderr)
    sys.exit(1)


def git(*args):
    # Runs git with this script's own arguments, never a shell.
    return subprocess.run([GIT, *args], cwd=ROOT, capture_output=True, text=True)  # noqa: S603


def read_json(rel):
    try:
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"{rel}: {exc}")


def is_prerelease(version):
    return "-" in version


def precedence(version):
    """Sort key that follows semver precedence: 0.2.0-rc.1 < 0.2.0-rc.2 < 0.2.0 < 0.2.1."""
    match = SEMVER.match(version)
    if not match:
        raise ValueError(f"not a version: {version!r}")
    major, minor, patch, pre = match.groups()
    core = (int(major), int(minor), int(patch))
    if pre is None:
        return core + ((1,),)
    parts = tuple((0, int(p), "") if p.isdigit() else (1, 0, p) for p in pre.split("."))
    return core + ((0,) + parts,)


def manifest_version():
    versions = {rel: read_json(rel).get("version") for rel in MANIFESTS}
    if len(set(versions.values())) != 1:
        fail("the manifests disagree on the version: " + ", ".join(f"{k} has {v!r}" for k, v in versions.items()))
    version = versions[MANIFESTS[0]]
    if not isinstance(version, str) or not SEMVER.match(version):
        fail(f"version {version!r} is not MAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH-PRERELEASE (e.g. 0.2.0-rc.1)")
    for plugin in read_json(MARKETPLACE).get("plugins", []):
        if "version" in plugin:
            fail(
                f'{MARKETPLACE}: remove "version" from the {plugin.get("name")!r} entry; it belongs in plugin.json only'
            )
    return version


def version_at(ref):
    shown = git("show", f"{ref}:{MANIFESTS[0]}")
    if shown.returncode:
        fail(f"cannot read {MANIFESTS[0]} at {ref}: {shown.stderr.strip()}")
    try:
        version = json.loads(shown.stdout).get("version")
    except ValueError as exc:
        fail(f"{MANIFESTS[0]} at {ref}: {exc}")
    if not isinstance(version, str) or not SEMVER.match(version):
        fail(f"{MANIFESTS[0]} at {ref} has the invalid version {version!r}")
    return version


def stable_releases(exclude_tag=None):
    """Versions of the stable v* tags. Pre-release tags never block or start anything."""
    tags = git("tag", "--list", "v*")
    if tags.returncode:
        fail(f"git tag: {tags.stderr.strip()}")
    return [t[1:] for t in tags.stdout.split() if t != exclude_tag and SEMVER.match(t[1:]) and not is_prerelease(t[1:])]


def highest_release_at_or_above(version, exclude_tag=None):
    """The highest stable release whose version is >= version, or None."""
    blocking = [v for v in stable_releases(exclude_tag) if precedence(v) >= precedence(version)]
    return max(blocking, key=precedence) if blocking else None


def last_release(version):
    """The highest stable release below version, or None: where the generated release notes start."""
    lower = [v for v in stable_releases() if precedence(v) < precedence(version)]
    return max(lower, key=precedence) if lower else None


def check(version, stable, unreleased, newer_than):
    if stable and is_prerelease(version):
        fail(f"{version} is a pre-release; main takes only stable versions such as {version.split('-')[0]}")
    if newer_than is not None:
        base = version_at(newer_than)
        if precedence(version) <= precedence(base):
            fail(f"raise the version in both plugin.json files: {version} is not higher than {base} on {newer_than}")
    if unreleased or newer_than is not None:
        released = highest_release_at_or_above(version)
        if released:
            fail(f"raise the version in both plugin.json files: {version} is not higher than the released v{released}")


def release(version):
    tag = os.environ.get("RELEASE_TAG", "").strip()
    title = os.environ.get("RELEASE_TITLE", "").strip()
    notes = os.environ.get("RELEASE_NOTES", "").strip()
    prerelease = os.environ.get("RELEASE_PRERELEASE", "").strip().lower()
    main_ref = os.environ.get("MAIN_REF", "origin/main")
    if prerelease not in {"true", "false"}:
        fail(f"RELEASE_PRERELEASE must be true or false, not {prerelease!r}")
    errors = []

    if tag != f"v{version}":
        errors.append(f"the tag is {tag!r} but both plugin.json files say {version}: name the tag v{version}")
    if title and title not in {f"v{version}", version}:
        errors.append(f"the title is {title!r}: use v{version}, or leave it empty")
    if not notes:
        errors.append("the release notes are empty: describe the changes (Generate release notes fills them in)")

    if prerelease == "true":
        if not is_prerelease(version):
            errors.append(f"a pre-release needs a version such as {version}-rc.1 in both plugin.json files")
    elif is_prerelease(version):
        errors.append(f"{version} is a pre-release version: tick Pre-release, or release a stable version from main")
    else:
        on_main = git("merge-base", "--is-ancestor", "HEAD", main_ref)
        if on_main.returncode == 1:
            errors.append(
                f"a stable release must come from main, and this commit is not on {main_ref}: set Target to main"
            )
        elif on_main.returncode:
            errors.append(f"cannot check that the commit is on {main_ref}: {on_main.stderr.strip()}")

    released = highest_release_at_or_above(version, exclude_tag=tag)
    if released:
        errors.append(f"{version} is not higher than the released v{released}")

    if errors:
        for error in errors:
            say(f"error: {error}", sys.stderr)
        sys.exit(1)
    kind = "pre-release" if prerelease == "true" else "release"
    say(f"ok: {tag} is a valid {kind}")


def main(argv):
    command = argv[1] if len(argv) > 1 else "check"
    args = argv[2:]
    newer_than = None
    if "--newer-than" in args:
        at = args.index("--newer-than")
        if at + 1 >= len(args):
            fail("--newer-than needs a git ref, e.g. origin/main")
        newer_than = args[at + 1]
        del args[at : at + 2]
    unknown = set(args) - {"--stable", "--unreleased"}
    commands = {"check", "version", "last-release", "release"}
    if unknown or command not in commands or (command != "check" and (args or newer_than)):
        fail(
            f"usage: {Path(argv[0]).name} check [--stable] [--unreleased] [--newer-than REF] | version | last-release | release"
        )
    version = manifest_version()
    if command == "version":
        say(version)
    elif command == "last-release":
        previous = last_release(version)
        if previous:
            say(f"v{previous}")
    elif command == "release":
        release(version)
    else:
        unreleased = "--unreleased" in args
        check(version, "--stable" in args, unreleased, newer_than)
        compared = f"{newer_than} and every release" if newer_than else "every release" if unreleased else ""
        say(f"ok: {version}" + (f" is higher than {compared}" if compared else ""))


if __name__ == "__main__":
    main(sys.argv)
