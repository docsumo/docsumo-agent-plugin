---
name: product-account-settings
description: Explain Docsumo account settings in product terms, including account identity and plan, members and doctype access, the API key screen, webhooks and notifications, credits, pages and billing, legacy database tables, inactivity sign-out, SSO and activity logs. Covers what the tools can read or change and what must be done in the app.
---

# Account and settings

Read [account settings](references/account-and-settings.md) for basic MCP reads and UI locations.
For inactivity sign-out and SSO read [security](references/security.md).
For legacy Database Tables versus Records use [product tables](../product-tables/SKILL.md).
Confirm the connected account before account-specific answers. Explain usage quantities as returned;
look up current plan limits instead of deriving them from an old reference.

Never retrieve or print credentials. For API keys, SSO material and secrets, direct the user to the product screen.
A saved webhook URL does not establish successful delivery: check the document's status and the webhook activity log.
For lookup fields use [doctype setup](../product-doctype-setup/SKILL.md). When no tool performs a requested change,
give the user the steps in the app.

## Explain results

Use product breadcrumbs, labels and meaningful values. Do not answer with tool names, raw JSON, IDs or unexplained
setting codes. Real amounts, page counts and DPI are meaningful numbers and must remain exact.
Resolve a setting's meaning from its live option labels. If the meaning cannot be confirmed, say so; do not guess or
echo an unexplained code. Before working in an account, confirm which account is connected
([connection setup](../connection-setup/SKILL.md)) and read each tool's live schema before its first call.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
