---
name: extraction-tables
description: Diagnose Docsumo line-item and table extraction problems such as missing, extra, merged or split rows, shifted or misaligned columns, repeated headers, and rows lost on multipage or long documents, after extraction-triage has checked the inputs and continuous-learning references.
---

# Table extraction failures

Start with [extraction triage](../extraction-triage/SKILL.md), including its reference-document check when continuous
learning is enabled. Reuse an existing check for the same document.

Read the matching [table pattern](references/patterns.md). Count the printed rows and compare ordered cells, columns
and totals; equal sums do not prove individual rows are correct. Read the table prompt separately from column prompts
and keep every column when editing ([editing fields](../product-doctype-setup/references/editing-fields.md)).

For PDFs, Table Batch Size is pages per call, not a row limit; Excel files are batched differently.
Check the fix on a continuation page, repeated headers, valid zero or empty cells, and duplicate rows from overlap.
Retry the failing document and one that was already correct, twice when results vary between runs. Retries spend
Docsumo credits: tell the user it spends Docsumo credits and ask them to proceed first, even if they asked for a
re-run.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
