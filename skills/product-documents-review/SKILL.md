---
name: product-documents-review
description: Explain and act on Docsumo documents in product terms, covering the Documents screen and statuses, the Review screen and approvals, retry and reprocessing, uploads, downloads and exports, and other document actions through the available MCP tools.
---

# Documents and review

Read [documents and Review](references/documents-and-review.md) for product locations and basic MCP operations.
Use the product's tab names (All, Review, Skipped, Processed) and distinguish extraction completion from approval.

Read the selected document and its current state before explaining a failure. Retrying spends processing credits:
estimate the cost with the credit tool, tell the user, and retry only the documents they asked for.
A settings save does not prove old documents were reprocessed. A downloadable result does not prove webhook delivery.
Wrong or missing extracted values go to [extraction triage](../extraction-triage/SKILL.md). Correct values that still
wait in Review usually come from the document type's approval settings: see [doctype setup](../product-doctype-setup/SKILL.md).

## Explain results

Use product breadcrumbs, labels and meaningful values. Do not answer with tool names, raw JSON, IDs or unexplained
setting codes. Real amounts, page counts and DPI are meaningful numbers and must remain exact.
Resolve a setting's meaning from its live option labels. If the meaning cannot be confirmed, say so; do not guess or
echo an unexplained code. Before working in an account, confirm which account is connected
([connection setup](../connection-setup/SKILL.md)) and read each tool's live schema before its first call.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
