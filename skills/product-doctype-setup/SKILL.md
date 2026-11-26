---
name: product-doctype-setup
description: Explain or perform Docsumo document type setup in product terms, in Edit Fields (fields, tables, columns, prompts, dropdowns, lookups, and why a lookup matches nothing or the wrong row) and Configure (extraction mode, model, splitting, auto-classification and other processing controls). Use for adding or changing fields and settings, building a new document type, and setup questions. Processing documents and field saves that re-extract them spend Docsumo credits: always ask the user first.
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

**Credits:** processing or retrying documents, and a field save that extracts (`docsumo_field_setup_save` with a
`doc_id`, or with `save_type: "all"`), spend Docsumo credits. Before each, ask the user to proceed, saying it spends
Docsumo credits, and wait for a yes, even when their request already names the action. Give the credits only if you
already know them; don't make an extra call to find out.

**A field lookup that matches nothing or the wrong row:** rows are kept only when their cell contains the whole
extracted value (ignoring case), and only then scored against the threshold. A value longer or written differently
from the table's ("C.N.W. Pty. Ltd." against "CNW PTY LTD", a name with a branch after it) matches at no threshold, so
lowering it changes nothing. Fix it in the document type, in this order: the lookup's conditions, then the source
value (its prompt, or a cleaning field that normalises it and becomes the lookup's source), then the table's rows. A
workflow's Table Lookup is no fix unless the user asks for a workflow. Details and how to check the result:
[how a field lookup picks a row](../product-tables/references/tables.md#how-a-field-lookup-picks-a-row).

Wrong output goes to [extraction triage](../extraction-triage/SKILL.md). Correct values that still wait in Review
usually come from the approval (STP) setting, mandatory fields, validation rules or confidence thresholds.

## Explain results

Use product breadcrumbs, labels and meaningful values. Do not answer with tool names, raw JSON, IDs or unexplained
setting codes. Real amounts, page counts and DPI are meaningful numbers and must remain exact.
Resolve a setting's meaning from its live option labels. If the meaning cannot be confirmed, say so; do not guess or
echo an unexplained code. Before working in an account, confirm which account is connected
([connection setup](../connection-setup/SKILL.md)) and read each tool's live schema before its first call.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
