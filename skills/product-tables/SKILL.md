---
name: product-tables
description: Explain and operate Docsumo Records (formerly Tables) in product terms, covering reference/entity Records tables versus legacy Database Tables, client reference data, columns, rows, imports, linked records, and how field lookups and workflow Table Lookup/Write use them, including why a field lookup matches nothing or the wrong row and how to fix it, through the current MCP tools.
---

# Records and lookup sources

First identify which table surface the user means: [table operations](references/tables.md). A document's line-item
extraction issue belongs to [extraction tables](../extraction-tables/SKILL.md), not this skill.

Read source type, table/column identity, sample row and intended effect before a change. The Records tools serve only
Records tables, and most need an owner or admin; Database Tables have no tools. Keep source values as they are and verify the saved row and dependent lookup behavior.
Do not equate an imported CSV database with a Records table because both appear in a dropdown.

**A field lookup that matches nothing or the wrong row:** rows are kept only when their cell contains the whole
extracted value (ignoring case), and only then scored against the threshold. A value longer or written differently
from the table's ("C.N.W. Pty. Ltd." against "CNW PTY LTD", a name with a branch after it) matches at no threshold, so
lowering it changes nothing. Fix it in the document type, in this order: the lookup's conditions, then the source
value (its prompt, or a cleaning field that normalises it and becomes the lookup's source), then the table's rows. A
workflow's Table Lookup is no fix unless the user asks for a workflow. Details:
[how a field lookup picks a row](references/tables.md#how-a-field-lookup-picks-a-row).

Workflow graph/testing belongs to [product workflows](../product-workflows/SKILL.md); field lookup configuration to
[doctype setup](../product-doctype-setup/SKILL.md). Before working in an account, confirm which account is connected
([connection setup](../connection-setup/SKILL.md)). Explain product labels and concrete values; when an operation has
no tool, say so without inventing tools or other APIs.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
