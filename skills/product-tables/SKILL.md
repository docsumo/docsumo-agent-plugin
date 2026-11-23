---
name: product-tables
description: Explain and operate Docsumo Records (formerly Tables) in product terms, covering reference/entity Records tables versus legacy Database Tables, client reference data, columns, rows, imports, linked records, and how field lookups and workflow Table Lookup/Write use them, through the current MCP tools.
---

# Records and lookup sources

First identify which table surface the user means: [table operations](references/tables.md). A document's line-item
extraction issue belongs to [extraction tables](../extraction-tables/SKILL.md), not this skill.

Read source type, table/column identity, sample row and intended effect before a change. The Records tools serve only
Records tables, and most need an owner or admin; Database Tables have no tools. Keep source values as they are and verify the saved row and dependent lookup behavior.
Do not equate an imported CSV database with a Records table because both appear in a dropdown.

Workflow graph/testing belongs to [product workflows](../product-workflows/SKILL.md); field lookup configuration to
[doctype setup](../product-doctype-setup/SKILL.md). Before working in an account, confirm which account is connected
([connection setup](../connection-setup/SKILL.md)). Explain product labels and concrete values; when an operation has
no tool, say so without inventing tools or other APIs.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
