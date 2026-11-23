---
name: product-doctype-setup
description: Explain or perform Docsumo document type setup in product terms, in Edit Fields (fields, tables, columns, prompts, dropdowns, lookups) and Configure (extraction mode, model, splitting, auto-classification and other processing controls). Use for adding or changing fields and settings, building a new document type, and setup questions.
---

# Doctype setup

Use for new fields, tables, prompts, dropdowns, model settings and configuration questions.
Read [Edit Fields and Configure](references/doctype-setup.md) for surfaces and tool selection.
A requested new field is setup, not automatically an extraction problem.

1. Identify the existing doctype and intended field/output from live state; preserve existing values.
2. Explain the relevant Edit Fields or Configure location and supported controls.
3. For a requested change, follow [editing fields](references/editing-fields.md): read first, change only what was
   asked, keep every other block and column, and save without reprocessing documents.
4. Read saved values back. Existing processed documents need a separate, requested retry to show changed output.
5. After building a doctype or changing its fields, process one sample document and confirm it reaches Review, not
   `erred`, before calling the setup done.

Wrong output goes to [extraction triage](../extraction-triage/SKILL.md). Correct values that still wait in Review
usually come from the approval (STP) setting, mandatory fields, validation rules or confidence thresholds.

## Explain results

Use product breadcrumbs, labels and meaningful values. Do not answer with tool names, raw JSON, IDs or unexplained
setting codes. Real amounts, page counts and DPI are meaningful numbers and must remain exact.
Resolve a setting's meaning from its live option labels. If the meaning cannot be confirmed, say so; do not guess or
echo an unexplained code. Before working in an account, confirm which account is connected
([connection setup](../connection-setup/SKILL.md)) and read each tool's live schema before its first call.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
