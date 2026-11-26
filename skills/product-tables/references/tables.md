# Identify and work with the right table

| Surface | Meaning |
|---|---|
| Settings → Database Tables (`/settings/database-table/`) | Legacy uploaded CSV databases used for dropdown/lookup sources. No MCP tool reads or writes them. |
| Records, formerly Tables (`/tables`, `/tables/:tableId`, record detail) | Unified reference/entity tables with typed columns, records, imports and linked records/cases; the `docsumo_*record*` tools (`table_id`) cover these. |
| Doctype Data Table | Extracted document results; see [documents/review](../../product-documents-review/SKILL.md). |
| Review line items | Rows/cells extracted from one document; review edits differ from changes to the fields or a lookup source. |

## Records tables

Choose/create a reference or entity table, define columns and its display column, then add records or import CSV/XLSX/XLS
using the import preview and header mapping. Inspect required/unique fields and column types before importing.
The UI supports search/filter/sort, column changes and record detail with linked records, cases and documents.
A linked-record cell refers to another table's record; its displayed label is not its stored identity, so write the
row id, never the label.

Column types are text, number, date, boolean, choice (needs its choices) and linked_record (needs a source table).
Text and choice uniqueness ignores case. A column's type cannot be changed while the table has rows. Deleting a row or
table can remove links to cases: check what is linked before proposing it.

A table holds at most 25,000 rows by default, counting every row, not one request: adding rows, imports and workflow
Table Write all refuse a write past it ("This table is at its 25,000-row limit."). When designing a table, multiply
rows per document by the documents it keeps. An import file is limited to about 35 MB.

For a failed import, note the file format/size, row count, header mapping, error row/column and typed values. A mapped
header missing from the file is an error only for a required or primary column; otherwise its cells stay empty without
warning. An import preview or optimistic grid edit is not proof of saved data: refresh the record, and check saved rows
after an uncertain response before retrying an import.

The MCP serves only Records tables, never Database Tables; read the live schema before each write.

Listing tables, searching, reading rows, row history and every write are for owners and admins only; for a member
they are refused. Reading one record with its cases (`docsumo_get_record`) is open to every role. Tell a member which
step needs an owner or admin instead of retrying.

| Need | Tool | Notes |
|---|---|---|
| Find a table and its columns | `docsumo_list_records_tables` (`kind`, `q` on the name) | Each table carries `table_id`, `kind`, `row_count`, `display_column` and `columns` (`column_id`, `type` text/number/date/boolean/choice/linked_record, constraints, `choices`, `source_table_id`). |
| Find a value when the table is unknown | `docsumo_search_records` (`q`, `kind`) | Rows grouped by table; linked cells stay raw `row_id`s. |
| Read or filter rows | `docsumo_get_records` (`q`, `conditions`, `match`, `row_ids`, sort) | `cells_by_name`; with `resolve_links` (default) `linked_records` gives `{row_id, display}` per linked column. Filter rather than export. |
| One record and its cases | `docsumo_get_record` (`table_id`, `row_id`) | Open to every role. Only entity rows link to cases; linked cells are not resolved here. |
| Row history | `docsumo_list_records_table_history` (`table_id`, optional `row_id`) | Inserts, updates and deletes with old/new values and the actor; not table or column changes. Rows a workflow's code wrote through the API show as the run user's own import or edit, with no workflow named: match their time against the workflow's runs. |
| Create a table | `docsumo_create_records_table` (inline rows keyed by column name) | `kind` cannot change later; a refused row fails the whole request. For values people edit by hand, prefer a choice column to boolean; a boolean cell stores true only for true, 1 or yes. |
| Change table or columns | `docsumo_update_records_table`, `docsumo_add_records_table_column`, `docsumo_update_records_table_column`, `docsumo_delete_records_table_column`, `docsumo_reorder_records_table_columns`, `docsumo_delete_records_table` | A type change is refused while the table has rows; deleting a table unlinks its cases. |
| Change rows | `docsumo_add_record`, `docsumo_update_record` (only the cells given), `docsumo_delete_record` | Cells are keyed by `column_id`. Adding an entity record does not link it to a case. |
| Case links | `docsumo_get_case_linked_records`, `docsumo_link_case_record`, `docsumo_unlink_case_record` | Entity tables only; confirm the case exists before linking. |

Importing a spreadsheet needs a file the server can read, and the hosted server reads no file on the user's computer:
`docsumo_import_records`, and `docsumo_create_records_table` with a `file_path`, are refused there. The user imports
the file on the Records screen (New Table from a file, or Import on an existing table); then read the result back with
`docsumo_get_records`. A small sheet can instead be sent as inline rows to `docsumo_create_records_table` or row by row
with `docsumo_add_record`.

## Reference spreadsheets

Import the user's reference spreadsheet as provided: the same columns and values, formula cells as their computed
values, and any blank header named and reported. Do not derive keys, merge, pack or split it into extra tables; adapt
the doctype's fields instead. Above the row limit keep the first rows up to it, report the coverage that leaves on
real documents, and ask before any other reduction. Before chaining lookups across tables, measure how many document
keys each table holds and whether shared values (vendor names, codes) are spelled alike; report gaps as data issues
rather than fuzzy-matching around them.

## Legacy Database Tables

No MCP tool reads or writes Database Tables. To look at, edit, download or delete one, the user goes to Settings >
Database Tables in the app (writes need an admin role there). Through the MCP you can still see which lookup or
dropdown uses one in the field's settings (`docsumo_field_setup_get_field_settings`).

## Lookup and workflow use

Edit Fields supports CSV and unified-table lookup sources. Confirm source kind, table, every condition (column, source
field, match type, group and connector) and the return columns. To see why a document got its value, read the field's
candidate rows with `docsumo_get_lookup_candidates`. A wrong linked display value can be a source/relationship issue
rather than an extraction prompt issue. The block's settings are in
[editing fields](../../product-doctype-setup/references/editing-fields.md#lookup-blocks).

### How a field lookup picks a row

1. **Empty sources are skipped.** A condition whose source field is empty is skipped, not failed, so a
   three-condition AND can resolve on one condition. If every condition is skipped there is no automatic match.
2. **Candidate rows contain the value.** Rows are first narrowed to those whose cell contains the source value
   (ignoring case), for exact and approximate alike: approximate tolerates a fragment, not a typo. Text is never read
   as a number ("007" is not "7").
3. **Each row is scored.** Exact means equal after ignoring case and extra spaces; approximate means a similarity at
   or above the threshold. AND takes the lowest condition score, OR the highest.
4. **One row is picked:** a reviewer's chosen row, then a stored "None", then the value already in the field if it is
   still a candidate, then the best score. Ties are not decided by row order or import order, so make sure the key is
   unique: check with `docsumo_get_records` before relying on it.
5. **Outputs are written.** The first condition's column is the field's value; return columns fill the Lookup
   Reference fields. Review offers at most 50 candidate rows plus None, ranked.

To make a condition a fallback, add a lookup on the primary condition alone and a calculation that empties the
fallback's source when that lookup found a row: an empty source skips its condition.

**Diagnosing a wrong or empty lookup:** read the field's lookup block with `docsumo_field_setup_get_field_settings`
(table, source type, conditions, connectors, match types; confirm the table and columns still exist), then
`docsumo_review_get_data` (`detail="compact"`, `fields` naming the source fields) for each source field's value, then
`docsumo_get_lookup_candidates` for the ranked rows. Explain the result by the steps above. To test a config change,
save it, then retry one document and check its value; test a reviewer's correction with
`docsumo_update_document_field`, which returns every field recomputed from the edited one. A lookup with no match leaves itself and its returned fields empty and flagged for review.

**Fixing a lookup that matches nothing.** Because rows must contain the whole source value (step 2), a document value
longer or written differently from the table's ("Acme Supply Co - North Branch" or "A.C.M.E. Supply" against "ACME
SUPPLY CO") matches at no threshold: lowering it changes nothing. Fix it in the document type, in this order, offering
the first that works:

1. **The conditions**: the column the user named (several columns as an OR group), exact or approximate, threshold.
2. **The source value**: make the field hold what the table holds, with its prompt (the name only, without branch,
   site or location), or a cleaning field that derives it and becomes the lookup's source. A cleaning field that
   normalises a value writes it the way the table's cells write it: it drops dots, commas and apostrophes, turns
   hyphens, slashes and underscores into a space, then collapses spaces ("C.N.W. Pty. Ltd." becomes "CNW Pty Ltd",
   "Sherriff-Electrical" becomes "Sherriff Electrical"). Check its result against the table's cells first.
3. **The table's rows**: a column holding the values as documents print them, added on the Records screen or with
   the Records tools.

The change applies to every document of the type: after reprocessing (which spends credits; ask first), check the
documents that missed and a few that matched with `docsumo_get_lookup_candidates`. A workflow is not a fix for a field
lookup: never offer to replace it with a workflow's Table Lookup unless the user asks for a workflow.

### Workflow Table Lookup and Table Write

Table Lookup can select entities or cases; configure the matching branch and inspect its output. Table Write inserts or
updates table records and can link cases where configured, **one record per run**: a list of line items becomes one
record, and `upsert` updates only the best match. For many rows per document, write them from a python_code block
([workflow code](../../product-workflows/references/block-behavior.md#calling-docsumo-from-workflow-code)). A Table
Write `delete` matching more than 100 rows deletes nothing. Send None, not `""`, for an empty date or number cell.

Conditions in these blocks join each row to the next by its connector, applied left to right; `==`/`!=` ignore case
on text and choice columns; a blank or unresolved value makes its condition match nothing. Entity conditions and case
filters are different, so do not reuse one shape for the other. Read actual block outputs before binding downstream
values, and do not treat a successful write count as proof the intended records changed. A successful block with zero
matches is usually a filter or input issue. Do not rerun external writes blindly. Graph editing uses the
[workflow operations](../../product-workflows/references/workflows.md).
