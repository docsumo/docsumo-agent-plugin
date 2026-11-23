---
name: product-navigation
description: Orient in the Docsumo product, covering where screens and settings live, the Home dashboard and Agents Hub (enabling, creating or duplicating document types), the case type workspace and its Inbox, product vocabulary, Sumo AI, integrations and other adjacent areas, plus official documentation lookups for features, limits and the API. Use for where-is, how-do-I and does-Docsumo-support questions.
---

# Product navigation

A document type defines fields and processing settings. Users may call it a model, agent, parser or template.
Home lists enabled/disabled agents; the Agents Hub (AI Models Hub on some accounts) enables or creates document types. A doctype workspace contains Documents,
Data Table, Analytics, Configure and Edit Fields. The Review screen shows one document beside extracted values.
Records holds reference/entity tables. Settings contains account, members, database tables, billing and integration
configuration. A case type workspace has Cases, an email Inbox and Configure.

- Enabling, creating or duplicating a doctype: [Agents Hub](references/ai-models-hub.md).
- Fields and processing controls: [doctype setup](../product-doctype-setup/SKILL.md).
- Documents, review, retries and exports: [documents and review](../product-documents-review/SKILL.md).
- Members, access, usage, webhook settings and lookup tables: [account settings](../product-account-settings/SKILL.md).
- Workflows, triggers, tests, publishing and linked cases: [product workflows](../product-workflows/SKILL.md).
- A case type's email Inbox, its emails and how they become cases: [case type Inbox](../product-inbox/SKILL.md).
- Records (formerly Tables) versus legacy CSV Database Tables: [product tables](../product-tables/SKILL.md).
- Sumo AI, integrations and adjacent UI behavior: [adjacent areas](references/other-areas.md).
- Public feature/limit/API questions: [official documentation lookup](references/support-docs.md).

Read one relevant reference. When a screen exists but no tool performs the action, say so and give the user the steps
in the app; recognizing a screen does not mean a tool can operate it.

## Explain results

Use product breadcrumbs, labels and meaningful values. Do not answer with tool names, raw JSON, IDs or unexplained
setting codes. Real amounts, page counts and DPI are meaningful numbers and must remain exact.
Resolve a setting's meaning from its live option labels. If the meaning cannot be confirmed, say so; do not guess or
echo an unexplained code. Before working in an account, confirm which account is connected
([connection setup](../connection-setup/SKILL.md)) and read each tool's live schema before its first call.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
