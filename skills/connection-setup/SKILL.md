---
name: connection-setup
description: Connect, reconnect or troubleshoot the Docsumo MCP server in Claude Code or Codex. Use when the user asks to connect Docsumo, or to change or switch their API key or account, and for Docsumo tools not showing, invalid or expired credential errors, the wrong account connected, rate limits and refused local file uploads. Needs no working account.
---

# Connection setup

The Docsumo MCP is a hosted server at `https://mcp.docsumo.com/mcp`. Each person connects with their own Docsumo API
key (in Docsumo: Settings > Webhook & API), and every call acts as that key's user in that one account. Use an API
key, not a token copied from a browser session.
Regenerating a key invalidates the old one everywhere it is used, so prefer copying the existing key.

Never repeat a key in full: refer to it by its last four characters, and write it nowhere except the client's own
configuration. When the user gives you the key to set up the plugin, use it only in the commands or file below. Do
not ask for it otherwise.

## Install and change the key

The plugin brings the server with it, so there is nothing to add by hand. Both clients install it in two steps: add
the marketplace (`docsumo/docsumo-agent-plugin`, the GitHub repository), then install the plugin with the key.

- **Claude Code**: `claude plugin marketplace add docsumo/docsumo-agent-plugin`, then
  `claude plugin install docsumo@docsumo --config docsumo_api_key=<key>`. The key goes to the system's secure
  storage. To change it, the user runs `/plugin configure docsumo@docsumo` in a session. From a shell, pipe the
  value in: `printf '{"docsumo_api_key":"%s"}' '<key>' | claude plugin configure docsumo@docsumo --values-stdin`
  (without `--values-stdin` the command only lists the options). Then run `/reload-plugins` or start a new session.
- **Codex**: `codex plugin marketplace add docsumo/docsumo-agent-plugin`, then `codex plugin add docsumo@docsumo`, and the line
  `DOCSUMO_API_KEY=<key>` in `~/.codex/.env` (create the file if needed, replace an existing `DOCSUMO_API_KEY` line,
  keep the others). Codex reads that file, or a `DOCSUMO_API_KEY` shell variable, when it starts, so restart Codex
  after a change. `codex plugin list` shows whether `docsumo@docsumo` is installed and enabled.

Do not also add a separate `docsumo` server with `claude mcp add`, `codex mcp add` or in a config file while the
plugin is enabled: two servers under one name cause confusing results. If the user already has such an entry from an
earlier manual setup, tell them, and remove it only with their agreement (`claude mcp get docsumo` or
`codex mcp get docsumo` shows it; `claude mcp remove docsumo -s <scope>` or `codex mcp remove docsumo` removes it).

**Verify:** call `docsumo_get_account_user`. It returns the connected email, role, organisation and plan. Confirm it
is the intended account before any account work.

## Troubleshoot

| Symptom | Likely cause | Fix |
|---|---|---|
| No Docsumo tools | The connection loads only at session start; the plugin is disabled; a separate `docsumo` server entry overrides it | Claude Code: run `/reload-plugins` or start a new session, check the plugin is enabled in `/plugin`, check `claude mcp list`. Codex: restart Codex, check `codex plugin list` and `codex mcp list` |
| "No Docsumo API key came with this request" (older servers: "found on this request") | The key was not entered | Claude Code: set it with `/plugin configure docsumo@docsumo` or the `--values-stdin` command above. Codex: see the next row |
| Codex: "Environment variable DOCSUMO_API_KEY for MCP server 'docsumo' is empty" | No key in `~/.codex/.env` or the shell Codex started from | Add `DOCSUMO_API_KEY=<key>` to `~/.codex/.env` and restart Codex |
| "Invalid or expired credential" or 401 on every tool | Regenerated key, removed member, a typo in the key | Copy the current API key from Settings > Webhook & API and enter it again |
| Results empty or unlike what the user sees | The key belongs to a different account | Run `docsumo_get_account_user`; connect the right account's key |
| 429 errors | The account-wide rate limit (10 requests per second, shared with the account's other API integrations) | Slow down or batch, then retry |
| Local file upload refused ("does not read files from its own filesystem") | The hosted server cannot see the user's files | Upload through a link: `docsumo_create_file_upload`, `curl` the file to its `upload_url`, then pass the `file_ref`. See [uploading files](../product-documents-review/references/documents-and-review.md#uploading-files-from-your-computer). A Records import has no link yet: import in the app |
| `docsumo_create_file_upload` says uploading "is not set up here" | The server doesn't have uploads switched on yet | The user uploads in the Docsumo app or by email: the document type's upload address (`upload_email` in `docsumo_get_document_types`, or `docsumo_configure_get(tab="import_export")`) or the case type's `upload_email` (`docsumo_get_case_configuration`) |
| `curl` to the `upload_url` fails to connect, from a chat sandbox | The workspace's code-execution network settings block the upload host | An admin allows the upload URL's host in the code-execution network settings, or the user uploads in the app |
| A `file_ref` is refused as already used | A ref works once; that file already reached Docsumo | Check the documents list before uploading again; for another copy, call `docsumo_create_file_upload` again |
| An upload timed out | Large documents take a while | Check whether the document arrived before uploading again, to avoid duplicates |
| A tool named in a skill is missing | The server version differs from the skill | Use the tools the server lists and tell the user what is not available; do not call other APIs instead |

## Switching accounts

One key is one account. To work in another account, enter that account's key as above, start a new session and
confirm the identity again with `docsumo_get_account_user` before reading or changing anything.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
