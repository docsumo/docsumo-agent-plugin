# Releasing

Clients install the plugin from `main` and update when the `version` in `plugin.json` changes. Nothing is built or
deployed: a merge into `main` with a higher version is what ships. A release adds a `v<version>` tag that people can
pin to and roll back to, and a page of notes.

## Version

Raise `version` in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` (they must match; never add a
version to `marketplace.json`). Patch for fixes and wording, minor for new skills or tools, major for breaking changes
such as a new sign-in method. A pull request into `main` fails the Validate check unless the version is stable and
higher than the one on `main` and every release.

## Stable release (automatic)

Merge the pull request into `main`. The Release workflow creates the `v<version>` tag on the merge commit and a GitHub
Release marked **Latest**, with notes that list the pull requests merged since the last stable release. Edit the notes
on the release page if they need more context. The first release, `v0.1.0`, is created the same way when `main` is
first pushed.

If the publish job fails, fix the cause and re-run it from the **Actions** tab, or publish the release by hand with
**Target** set to `main`.

## Pre-release (by hand, from any branch)

1. On your branch, set a pre-release version such as `0.2.0-rc.1` in both `plugin.json` files and push.
2. Open **Releases > Draft a new release**. Set **Target** to your branch and create the tag `v0.2.0-rc.1`. Leave the
   title empty or set it to the tag, click **Generate release notes**, select **Pre-release** and publish.
3. Testers install it with `claude plugin marketplace add docsumo/docsumo-agent-plugin#v0.2.0-rc.1` or
   `codex plugin marketplace add docsumo/docsumo-agent-plugin@v0.2.0-rc.1`. Nobody else gets it.

Set the stable version (`0.2.0`) before the branch is merged into `main`.

The Release workflow checks every release published by hand and fails when:

- the tag is not `v` plus the version in both `plugin.json` files, or the title is something other than the tag;
- the notes are empty;
- a pre-release has a version without a pre-release part;
- a stable release is not on `main` or has a pre-release version;
- the version is not higher than every stable release.

If the check fails, delete the release and its tag (`gh release delete v0.2.0-rc.1 --cleanup-tag`), fix the problem
and publish again.

## Rolling back

Revert the change, raise the version (for example `0.2.1`), and merge it into `main`. Its release follows
automatically. Don't set `main` back to an older version number: always move forward. Someone who needs an older
release right away can pin it, as described in GUIDE.md.

## Check locally

Before opening a pull request into `main`:

```bash
git fetch origin --tags
python3 .github/scripts/plugin_version.py check --stable --newer-than origin/main
```
