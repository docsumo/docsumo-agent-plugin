# Releasing

The plugin uses the same branches as docllm:

- `develop`: work is merged here first. Testers can install it.
- `master`: what clients install. A merge into `master` with a higher version ships and is released automatically.

Nothing is built or deployed: clients read the plugin straight from the branch and update when the `version` in
`plugin.json` changes. A release adds a `v<version>` tag that people can pin to and roll back to, and a page of notes.

## Version

Raise `version` in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` (they must match; never add a
version to `marketplace.json`). Patch for fixes and wording, minor for new skills or tools, major for breaking changes
such as a new sign-in method. A pull request into `master` fails the Validate check unless the version is stable and
higher than the one on `master` and every release.

## Stable release (automatic)

Open a pull request from `develop` into `master` with the stable version and merge it. The Release workflow creates the
`v<version>` tag on the merge commit and a GitHub Release marked **Latest**, with notes that list the pull requests
merged since the last stable release. Edit the notes on the release page if they need more context.

If the publish job fails, fix the cause and re-run it from the **Actions** tab, or publish the release by hand with
**Target** set to `master`.

## Testing before a release

Testers can follow `develop` with `claude plugin marketplace add docsumo/docsumo-agent-plugin#develop` or
`codex plugin marketplace add docsumo/docsumo-agent-plugin@develop`. They only get a change when the version changes,
so give `develop` a pre-release version such as `0.2.0-rc.1` and raise it (`0.2.0-rc.2`) when they should get the
latest changes.

To share a fixed copy instead, publish a pre-release from `develop` or any branch:

1. Open **Releases > Draft a new release**. Set **Target** to the branch and create the tag `v` plus its version, for
   example `v0.2.0-rc.1`.
2. Leave the title empty or set it to the tag, click **Generate release notes**, select **Pre-release** and publish.
3. Testers install it with `#v0.2.0-rc.1` (Claude Code) or `@v0.2.0-rc.1` (Codex) in the commands above.

The Release workflow checks every release published by hand and fails when:

- the tag is not `v` plus the version in both `plugin.json` files, or the title is something other than the tag;
- the notes are empty;
- a pre-release has a version without a pre-release part;
- a stable release is not on `master` or has a pre-release version;
- the version is not higher than every stable release.

If the check fails, delete the release and its tag (`gh release delete v0.2.0-rc.1 --cleanup-tag`), fix the problem
and publish again.

## Rolling back

Revert the change, raise the version (for example `0.2.1`), and merge it into `master`. Its release follows
automatically. Don't set `master` back to an older version number: always move forward. Someone who needs an older
release right away can pin it, as described in GUIDE.md.

## Check locally

Before opening a pull request into `master`:

```bash
git fetch origin --tags
python3 .github/scripts/plugin_version.py check --stable --newer-than origin/master
```
