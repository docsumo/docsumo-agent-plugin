# Editing fields safely

Read the live tool schemas before use. The rules below keep an edit from losing the user's existing setup or
reprocessing documents they did not ask to reprocess.

## Read a document type first

1. `docsumo_get_document_types`: find the doctype; note its `doc_type` string (e.g. `invoice__abc12`) and numeric `id`.
2. `docsumo_get_doctype_schema_and_fields` (`doctype_id`): the saved setup in one read — sections, fields, `type`,
   `blocks` (with their whole `config`, lookups included), named optional settings, `columns`, and the extraction
   settings. This is the source of truth for a change proposal.
3. `docsumo_field_setup_get` (`doc_type`, `include_block_settings: true`): the Edit Fields view, one entry per field or
   table column with its `path` (`Section___Field` / `Section___Table___Column`), `field_id` and `blocks`. It opens
   Edit Fields like the app does, so **any unsaved draft is discarded**; use `docsumo_get_doctype_schema_and_fields`
   (it reads the open draft, `read_from: "draft"`) to check a draft edit without losing it. `docsumo_field_setup_get_field_settings` (`doc_type`, `field_id`) returns
   one field's full optional settings and its `block_settings`.
4. Section and table prompts are in the same read: each section's `config.prompt`, each table field's `table_prompt`.
5. `docsumo_configure_get` (`tab="extraction"` for one tab, `setting_name` for one setting) for Configure values, with
   `value_label` for coded options.
6. `docsumo_get_doctype_analytics` (`part="accuracy"`) shows which fields reviewers correct most.

Keep a note of the current description, section names and prompts, every field's type and prompt, dropdown options,
table columns and table prompts, and lookup settings before changing anything, so the change can be checked and
undone.

## Field and column types

| Type | Use | Notes |
|---|---|---|
| String | Free text | Multi-line values come back as one line. |
| Number | Amounts, quantities | Printed `$`, commas and parentheses are parsed; decimal separator and decimals are field settings. |
| Date / Date (MM/DD) | Dates | The type decides how an ambiguous `03/04/2024` is read. |
| Dropdown | One of a fixed list | Options come from a list or a Database Table column. |
| Checkbox | Ticked or not | True/False, matched to the printed label nearest the mark. Allowed as a column. |
| Signature | Signed or not | True/False. Fields only. |
| Table | Line items | No field-level blocks; columns carry them. One table prompt per table. |
| Lookup | A row of a reference table | Matches extracted fields against a table (see [lookup blocks](#lookup-blocks)). Its type is locked once set. |
| Lookup Reference | Another column of the matched row | Created from the lookup's return columns; never added by hand. |

Columns take every type except Table and Signature. The multi-value setting (string, number and date only) returns a
list for a field that occurs several times. The field name is part of what extraction reads: renaming a field
changes extraction.

## Blocks

| Block | Purpose | Placement |
|---|---|---|
| Extraction | Read the value from the document; its `config.prompt` is the field's prompt | First; once per field |
| Cleaning | Normalise the value's format when built-in parsing is not enough | After extraction, or first |
| Calculation | Derive the value from other fields, columns or document metadata | After extraction/cleaning/validation, or first |
| Validation | Check the field's own value and flag it for review (rule-based with code, or AI-assisted with a prompt) | Never first |
| User validation | A True/False check across other fields | Alone |
| Dropdown | Categorical pick (`tagging_type: options` with `options`, or `table` with a table and column) | First |
| Lookup | Table-row match | First |
| Lookup Reference | A column of the matched row | First; created for you |

Chain rules: at most 10 blocks per field. Extraction, lookup, lookup reference, dropdown and user validation must come
first; validation never comes first; extraction, lookup, dropdown and user validation appear once. Allowed next
blocks: extraction → cleaning, calculation or validation; cleaning → calculation or validation; calculation →
validation; validation → calculation; dropdown, lookup and lookup reference → cleaning, calculation or validation;
user validation → nothing. Any other order makes every document fail, so the tool refuses it.

A field whose first block is not extraction (calculation, lookup, lookup reference) is not read from the page. A failed validation flags its field and leaves every field computed from it empty, so put
validations on fields nothing else reads. Every block should feed the field's value: a code block that never reads
the field's own value starts over, and the blocks before it run for nothing.

### Code blocks need code

Cleaning, calculation, validation and user validation blocks run their `custom_code`, not their prompt. A block saved
with a prompt alone never runs and its field stays empty. Generate the code with `docsumo_field_setup_generate_code`
(`doc_type`, `field_id`, `block_type`, `prompt`) — the app's "Generate and Run" — check it, then save it in the block's
`config.custom_code`. Do not run generated code on the local computer.

In prompts, refer to a field as `<@Section Name___Field Name>` and a column as
`<@Section Name___Table Name___Column Name>` (three underscores); a whole table cannot be referenced. List every field
a code block reads in the field's `references`, or it can run before its inputs and is not recomputed after a review
edit. A field with more than one block is read-only in Review unless its own id is in `references`.

Document metadata that is not on the page can be read in code blocks:

| Placeholder | Value |
|---|---|
| `<@__filename__>` | The uploaded file name |
| `<@__doc_meta_data__>` | The `doc_meta_data` string sent with an API upload, usually JSON (`json.loads(data["__doc_meta_data__"])`) |
| `<@__user_doc_id__>` | The `user_doc_id` sent with the upload |
| `<@__upload_date__>` | Upload date (in the field's date format for a date field) |
| `<@__username__>`, `<@__user_email__>` | The uploader's name and email |

An upload in the Docsumo app sets no metadata, so test a metadata reference with an upload that sends it:
`docsumo_upload_document` with a `file_ref` and `user_doc_id` / `doc_meta_data`
([uploading files](../../product-documents-review/references/documents-and-review.md#uploading-files-from-your-computer)),
or a document sent through the API with its metadata.

### Lookup blocks

A lookup's config holds `source_type` (`csv_table` for a Database Table, `unified_table` for a Records table), `table_id`,
`group_connector` (`and` / `or`), `condition_groups` and, only when adding return columns, `columns_to_added`:

```json
{ "source_type": "unified_table", "table_id": "…", "group_connector": "or",
  "condition_groups": [
    { "id": "grp_seller", "connector": "and", "sub_conditions": [
        { "id": "sub_1", "column": "<column id; header name for a Database Table>", "source": 9001001,
          "match": { "type": "exact" } },
        { "id": "sub_2", "column": "…", "source": 9001002, "match": { "type": "approximate", "threshold": 80 } } ] } ],
  "columns_to_added": [ { "column_id": "…", "label": "Vendor Code" } ] }
```

- Every group and condition needs an `id`; connectors are lowercase; a group holds conditions only. Approximate takes a
  threshold of 0–100 (the app offers 0–99, default 80).
- The first condition's column is the value the field shows; reordering conditions changes the output.
- `columns_to_added` holds header names for a Database Table and `{column_id, label}` for a Records table. Each entry creates a
  Lookup Reference field, so send it only when adding them.
- A header-field lookup takes header fields as sources; a column lookup only columns of its own table. To match a
  column against a header value, add a calculation column that copies it.

How matching picks a row: [lookup matching](../../product-tables/references/tables.md#how-a-field-lookup-picks-a-row).

## Build fields

1. A new custom type starts with one section, `Section 1`, holding a string field `Key Field`: rename them
   (`docsumo_field_setup_rename_section`; `docsumo_field_setup_rename_field` with `field_type: "field"`, or
   `"column"` for a column) or delete the field once others exist. For an existing type,
   `docsumo_field_setup_get` (`include_block_settings: false`) opens the draft.
2. Add sections with `docsumo_field_setup_add_section` and fields or columns with `docsumo_field_setup_add_field`
   (`parent_id`, `label`, `field_type`). A table (`field_type: line_item`) starts with one string column,
   `Column 01`; add columns with the table's id as `parent_id`. Deleting a table's last column deletes the table.
3. Give each field its blocks with `docsumo_field_setup_update_field_settings`. Read
   `docsumo_field_setup_get_field_settings` first and send back its whole optional settings list, changed, the full
   `block_settings` list (every surviving block, not just the one you changed) and the `references` the blocks read.
   Find the prompt by the block's type (`extraction`), not its position. A dropdown without options stops the save
   ("Dropdown field '<name>' must be setup").
4. Save with the settings-only scope (see [save scope](#save-scope)), read it back with
   `docsumo_get_doctype_schema_and_fields`, and retry one sample document and check it in Review.

Other edits:

- Section and table prompts: `docsumo_update_doctype_fields` (`doctype_id`) with `section_prompts`
  (`[{section, prompt}]`) or `table_prompts` (`[{section, table, prompt}]`), each the whole new text (`""` clears it).
  The table prompt is the place for row rules (what counts as a row, continuation lines, summary rows). With Edit
  Fields open the change goes to the draft (`applied_to: "draft"`) and is live only once saved; read each back.
- Document description: Configure > General "Description", through `docsumo_update_doctype_configuration`
  (`doctype_description`).
- Field type change: `docsumo_field_setup_change_field_type` with `change_type` retain, reset or reset_blocks (to or
  from a table always resets; to or from a dropdown resets the blocks); read back to confirm blocks and options.
- Delete with `docsumo_field_setup_delete` (`field_ids` or `section_ids`, in separate calls; a table takes its
  columns). A lookup with reference fields, or a field a lookup reads, cannot be deleted until those go; rewrite any
  `<@…>` reference to the field first.

## Configure settings

Pick one way to write each setting and read it back:

- `docsumo_update_doctype_configuration` writes Configure settings: `settings=[…]`, each by `setting_name` (as
  `docsumo_configure_get` names it), for any setting; `doctype_title` renames the type; `doctype_description` and the
  main extraction settings named in its schema can go in the same call. Its `updated_settings`, `failed_settings` and
  `warnings` say what applied; compare a read-back with what you sent.
- Disabling uses `docsumo_configure_disable_doctype`.

Never change the Post-processing tab's custom code.

## An open draft and changes saved elsewhere

The Edit Fields draft is a snapshot taken when an editing session opens and kept until it is saved or cancelled,
even days later. A change saved elsewhere after the draft opened (a colleague's save in the app, or another tool) is
not in that snapshot, and saving the older draft would replace it.

When the draft may be old: `docsumo_field_setup_cancel`, then `docsumo_field_setup_get`
(`include_block_settings: false`) to rebuild the draft from saved state, confirm one field with
`docsumo_field_setup_get_field_settings`, then make the edits, save, and compare the read-back with the intended
change. An error "specified field does not exist" for a valid field means no draft is open; rebuild it the same way.
If the user has Edit Fields open in the app, ask them to close or reload it first, so they do not save an older copy.

## Save scope

`docsumo_field_setup_save` saves the whole draft and can also touch documents:

- `save_type: "one", doc_id: "", status: "processed"` saves the settings only.
- `save_type: "all"` reprocesses **every** document of the doctype, approved ones included, and spends their credits.
  Use it only when the user asked to reprocess the whole document type.

Prefer the settings-only save, then retry the documents the user named with `docsumo_doctype_retry_documents`.

## Names and prompts

- Names cannot contain `\ / : * ? " < > |`; avoid `#`, `@`, `.`, `___` and other symbols. Use letters, digits and
  single spaces in Title Case. Names are case-sensitive and unique within their section or table.
- Do not use a double colon (`::`) in a prompt.
- Change only the fields the user asked about, by id; if two fields share a name, stop and ask.

## Check before saving

1. Fields were built as above; names are unique and allowed.
2. Every block chain follows the chain rules.
3. Every `<@…>` reference resolves, and every code block has code and its references.
4. Every dropdown has options or a table and column, and its field type is Dropdown.
5. Multi-value only on string, number and date; no Lookup Reference added by hand.
6. No prompt contains `::`.
7. After saving, read back with `docsumo_get_doctype_schema_and_fields` and `docsumo_field_setup_get_field_settings`
   and compare with the intended change.
