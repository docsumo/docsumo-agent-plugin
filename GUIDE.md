# Docsumo plugin for Claude Code and Codex

The Docsumo plugin connects your AI assistant to your Docsumo account, so you can work with your documents by asking
in plain language.

Think of it as giving your assistant its own view of Docsumo. Ask *"Which invoices are waiting for review?"* or *"Add
a PO Number field to my Purchase Order document type"*, and it does the work in Docsumo for you.

It works in **Claude Code** and **Codex**. Support for claude.ai, Claude Desktop and ChatGPT is coming soon.

## What can you do with it?

- **Check documents**: see extracted values, find what's waiting in Review, approve, download and export.
- **Set up document types**: add or change fields, tables, prompts and processing settings.
- **Fix extraction issues**: ask why a value is wrong and get the cause and a fix.
- **Run workflows and cases**: build, test, publish and run workflows, and sort the emails in a case type's Inbox.
- **Manage Records**: look up and update the reference data your lookups use.
- **Get answers**: ask how a Docsumo feature works. The assistant checks the official documentation.

## How it works

The plugin gives your assistant two things:

- **A secure connection to your Docsumo account.** It uses your API key, so the assistant can see and do only what
  you can in the app.
- **Docsumo know-how.** Built-in guides teach the assistant how Docsumo works, so it uses the right screens, terms
  and steps.

## Before you start

You need a Docsumo account and your **API key**. In Docsumo, open **Settings > Webhook & API** and copy it. Keep it
private, like a password.

## Install

### Claude Code

Run this in a terminal, with your key in place of `<YOUR_API_KEY>`:

```bash
claude plugin marketplace add docsumo/docsumo-agent-plugin
claude plugin install docsumo@docsumo --config docsumo_api_key=<YOUR_API_KEY>
```

Then start a new Claude Code session, or run `/reload-plugins` in an open one. Your key is stored in your system's
secure storage.

To change the key later, run `/plugin` in Claude Code, open **Docsumo** on the **Installed** tab and choose
**Configure options**.

### Codex

Run this in a terminal, with your key in place of `<YOUR_API_KEY>`:

```bash
codex plugin marketplace add docsumo/docsumo-agent-plugin
codex plugin add docsumo@docsumo
printf 'DOCSUMO_API_KEY=%s\n' '<YOUR_API_KEY>' >> ~/.codex/.env
```

Then restart Codex. It reads the key when it starts.

To change the key later, edit the `DOCSUMO_API_KEY` line in `~/.codex/.env` and restart Codex.

## Check that it works

Ask your assistant:

> Which Docsumo account am I connected to?

It should reply with your email and organization. If it doesn't, see [Troubleshooting](#troubleshooting).

## Update

New versions add features and fixes. Update from time to time:

| Claude Code | Codex |
| --- | --- |
| `claude plugin marketplace update docsumo`<br>`claude plugin update docsumo@docsumo` | `codex plugin marketplace upgrade docsumo` |

Then start a new Claude Code session or restart Codex. In Claude Code you can also turn on automatic updates: run
`/plugin`, open **docsumo** on the **Marketplaces** tab and choose **Enable auto-update**.

## Go back to an earlier version

Each release has a version tag, such as `v0.1.0`, on the
[Releases page](https://github.com/docsumo/docsumo-agent-plugin/releases). If a new version causes a problem, install
an earlier one. The same steps install a specific version for the first time.

### Claude Code

```bash
claude plugin marketplace remove docsumo
claude plugin marketplace add docsumo/docsumo-agent-plugin#v0.1.0
claude plugin install docsumo@docsumo --config docsumo_api_key=<YOUR_API_KEY>
```

Skip the first line for a new install. Removing the marketplace also removes the plugin and your saved key, so enter
the key again. Then start a new Claude Code session.

### Codex

```bash
codex plugin remove docsumo@docsumo
codex plugin marketplace remove docsumo
codex plugin marketplace add docsumo/docsumo-agent-plugin@v0.1.0
codex plugin add docsumo@docsumo
```

Skip the first two lines for a new install, and add your key as described under [Install](#install). An existing key
stays in `~/.codex/.env`. Then restart Codex.

### Return to the latest version

A pinned version gets no updates. To return to the latest version, run the same steps without `#v0.1.0` or `@v0.1.0`.

## Remove

### Claude Code

```bash
claude plugin uninstall docsumo@docsumo
claude plugin marketplace remove docsumo
```

This also deletes your saved API key. Then start a new Claude Code session.

### Codex

Run these in this order:

```bash
codex plugin remove docsumo@docsumo
codex plugin marketplace remove docsumo
```

Then delete the `DOCSUMO_API_KEY` line from `~/.codex/.env` and restart Codex.

## Good to know

- **It works as you.** Everything happens in your account, with your permissions.
- **Credits work as in the app.** Uploads, retries, changing a document's type, applying field changes to documents
  and workflow runs that extract documents spend credits. The assistant asks you before each one.
- **One key, one account.** To work in a different Docsumo account, use that account's API key.
- **If you regenerate your API key** in Docsumo, enter the new one as described under [Install](#install).

## Troubleshooting

| Problem | What to do |
| --- | --- |
| The assistant can't find Docsumo | **Claude Code:** run `/reload-plugins` or start a new session. `claude plugin list` should show `docsumo@docsumo` as enabled. **Codex:** restart Codex. `codex plugin list` should show `docsumo@docsumo` as installed and enabled. |
| "Invalid or expired credential", or a missing API key | Copy your current key from **Settings > Webhook & API** and enter it again as described under [Install](#install). In Codex, check that `~/.codex/.env` has exactly one `DOCSUMO_API_KEY` line, then restart Codex. |
| Results don't match what you see in the app | Your key belongs to another account. Ask *"Which Docsumo account am I connected to?"* |
| "Too many requests" | Your account's API limit is shared with your other integrations. Wait a moment and try again. |
| Docsumo still works after you removed it | **Claude Code:** start a new session. **Codex:** run `codex plugin remove docsumo@docsumo` (it works even after the marketplace is removed), then restart Codex. |

## Get help

- Documentation: [support.docsumo.com](https://support.docsumo.com)
- Support: [support@docsumo.com](mailto:support@docsumo.com)
- Privacy policy: [docsumo.com/privacy-policy](https://www.docsumo.com/privacy-policy)
