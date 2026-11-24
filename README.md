<img src="assets/logo.svg" alt="Docsumo" width="220">

# Docsumo plugin for Claude Code and Codex

Work with [Docsumo](https://www.docsumo.com) from your AI coding agent. Read documents' extracted data, review and
approve them, set up document types and fields, build and run workflows, triage case Inbox emails, manage Records, and get answers from the
[Docsumo documentation](https://support.docsumo.com).

New to the plugin? Start with the [user guide](GUIDE.md).

This plugin bundles:

- **The hosted Docsumo MCP server** (`https://mcp.docsumo.com/mcp`), which acts in your Docsumo account with your
  own API key.
- **Skills** that teach the agent how Docsumo works: documents and review, document type setup, workflows and
  cases, the case type email Inbox, Records, account settings, extraction troubleshooting, and connection help.

## Before you start

You need a Docsumo account and your API key. In Docsumo, open **Settings > Webhook & API** and copy your key.
Every action the agent takes runs as you, in that one account, with your permissions. Uploads, retries and other
actions that extract documents spend credits as they would in the app, and the agent asks before each one.

The hosted server cannot read files on your computer directly. To upload one, the agent asks the server for a
short-lived upload link and sends the file to it with `curl`. That works from your shell, or from the code sandbox
holding a file you attached in chat. The file waits on Docsumo's side only until it is uploaded to your account, and
is then deleted. In Claude.ai or ChatGPT, code execution must be on and allowed to reach `mcp.docsumo.com`. You can
always upload in the Docsumo app or by email instead, and the agent works with the documents once they arrive.

## Install

Installing takes the same two steps in Claude Code and Codex: add the Docsumo marketplace, then install the plugin
with your API key.

### Let your agent set it up

Paste this into Claude Code or Codex, with your API key in place of `<YOUR_API_KEY>`:

```text
Set up the Docsumo plugin for me from the docsumo/docsumo-agent-plugin GitHub repository
using my Docsumo API key: <YOUR_API_KEY>

In Claude Code, run:
  claude plugin marketplace add docsumo/docsumo-agent-plugin
  claude plugin install docsumo@docsumo --config docsumo_api_key=<the key>
In Codex, run:
  codex plugin marketplace add docsumo/docsumo-agent-plugin
  codex plugin add docsumo@docsumo
  then set DOCSUMO_API_KEY=<the key> in ~/.codex/.env (create the file if needed, replace any
  existing DOCSUMO_API_KEY line, keep the other lines).
Do not repeat the key back to me. When done, tell me to run /reload-plugins (Claude Code) or
restart Codex, then confirm the connected account with docsumo_get_account_user.
```

The key you paste stays in that conversation's history. To keep it out, run the commands yourself instead.

### Or run the commands yourself

In a terminal, with your API key in place of `<YOUR_API_KEY>`:

**Claude Code**

```
claude plugin marketplace add docsumo/docsumo-agent-plugin
claude plugin install docsumo@docsumo --config docsumo_api_key=<YOUR_API_KEY>
```

Claude Code keeps the key in your system's secure storage. Run `/reload-plugins` in an open session, or start a new
one. To change the key later, run `/plugin` in Claude Code, open **Docsumo** on the **Installed** tab and choose
**Configure options**.

**Codex**

```
codex plugin marketplace add docsumo/docsumo-agent-plugin
codex plugin add docsumo@docsumo
printf 'DOCSUMO_API_KEY=%s\n' '<YOUR_API_KEY>' >> ~/.codex/.env
```

Codex reads the key from `~/.codex/.env` when it starts, so restart Codex after installing. To change the key
later, edit that line and restart Codex.

## Remove

**Claude Code** (this also deletes the saved key):

```
claude plugin uninstall docsumo@docsumo
claude plugin marketplace remove docsumo
```

**Codex**, in this order (removing the marketplace first leaves the plugin active):

```
codex plugin remove docsumo@docsumo
codex plugin marketplace remove docsumo
```

Then delete the `DOCSUMO_API_KEY` line from `~/.codex/.env`. Start a new Claude Code session or restart Codex.

## Try it

- "Show me the extracted values of the latest document in my Invoice document type."
- "Which documents are waiting in Review?"
- "Which emails in my Claims Inbox are waiting for review, and which case does each fit?"
- "Add a field for the PO number to my Purchase Order document type."
- "Why is the total on this document wrong?"

## Repository layout

| Path | Purpose |
| --- | --- |
| `.claude-plugin/plugin.json`, `.mcp.json` | Claude Code plugin manifest and MCP server |
| `.claude-plugin/marketplace.json` | Marketplace entry, read by both Claude Code and Codex |
| `.codex-plugin/plugin.json`, `.codex-plugin/mcp.json` | Codex plugin manifest and MCP server |
| `skills/` | Skills shared by every client |
| `assets/` | Docsumo icon and logo |

## Support

Documentation: [support.docsumo.com](https://support.docsumo.com).

## License

MIT, see [LICENSE](LICENSE). The Docsumo name and logos are trademarks of Docsumo Inc. and are not licensed under
MIT.
