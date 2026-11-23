# Documents screen and Review screen

The **Documents** tab of a doctype (`/active-document/:docType/documents/:docStatus`) lists the
doctype's documents by status, with folders, filters, uploads and bulk actions. The **Review
screen** (`/review-document/:docId`) shows one document's extracted values over its page images
so a reviewer can correct, approve or skip it. Global tabs `/review`, `/skipped`, `/processed`
show the same lists across all doctypes.

## Documents screen

### What the user sees

- **Status tabs** All / Review / Skipped / Processed with counts. Failed documents show with a red badge and a
  retry action.
- **Folder view** (folders + files, folders only, or files only). Folders come from uploads
  (zip, email subject, split results) or manual creation; a folder can be downloaded as a unit.
- **Rows**: title, status, page count, uploaded by, uploaded from (UI, email, API,
  integration), folder, created/modified time, an STP marker, a marker when the document
  came out of a split, and a review link.
- **Filters**: created/modified date range, folder, uploader, free-text search (title or
  `doc_id:`), sort by created or modified date.
- **Upload**: drag-and-drop or file picker, the doctype's upload email, the API, integrations.
- **Bulk actions** on selected documents or folders: Retry, Change document type, Change owner
  (assign), Move to folder, Delete, Download.
- **Analytics** tab: volume by status over time, average processing and turnaround time, STP
  count, per-field accuracy and correction rates (needs review data to be non-empty).
- **AI Auto-Classify** tab: only on the AI Auto-Classifier document type; shows the documents it classified,
  grouped by the doctype each moved into, and the unclassified ones with the AI's suggested type (a hint
  for the user, not a target). **Manual classification**
  (`/manual-classification/:docId`) lets a user pick the target doctype; **Split & classify**
  (`/split/:originalDocId/:splitDocId`) shows proposed split points.

### MCP tools

| Need | Tool | Notes |
|---|---|---|
| List documents by tab | `docsumo_list_documents` | `doc_type` for one doctype (omit it for every doctype); `tab` = `all` / `review` / `processed` / `skipped`, or an explicit `status` list (`erred`, `new`, `processed`, `processing`, `review_required`, `review_skipped`, `reviewing`); date, `folder_id`, `user_id` (a list), search `q` (title or `doc_id:<id>`), `sort_by` (a list, such as `["created_date.desc"]`); `limit` 1-100. The default `view="files_only"` returns the documents themselves. `detail="compact"` (default) leaves out processing details; signed file URLs are never returned. |
| Tab counts | `docsumo_doctype_get_document_counts` | Same filters; returns `data.counts` all / review / processed / skipped. |
| Folders | `docsumo_list_documents` with `view="folder_only"` and `doc_type` (folders do not nest; each carries `folder_id`, `folder_name` and per-status counts), `docsumo_doctype_get_folder_detail`, `docsumo_doctype_create_folder`, `docsumo_doctype_rename_file_or_folder` (`name` with `folder_id` or `doc_id`), `docsumo_doctype_move_documents` (`dest_folder_id`, `source_folder_id`; `""` is the top level) | |
| Extracted values of one document | `docsumo_get_document_data`, `docsumo_review_get_data` | `docsumo_get_document_data` gives the API/webhook shape (sections > fields with `value`, `orig_value`, `confidence`, `review_required`, `position`; values only on an account whose webhook data format is v1); `fields` keeps named fields/columns. `docsumo_review_get_data` gives each field as Review shows it, with its id, page, `is_valid_format`, `format_message` and low-confidence marker, whatever the payload format; use `detail="compact"` with `fields` to keep named fields/columns and `flagged_only` to keep what needs review. |
| Correct a value as a reviewer | `docsumo_update_document_field` | One field or cell of a document in review (`field_id` from `docsumo_review_get_data`; `lookup_row_id` picks a lookup candidate). Returns every field recomputed from it. Approved documents are refused. A correction, not a configuration fix. |
| Download | `docsumo_download_document` (`doc_ids`, up to 25 per call, or `case_id` for a case's documents; `format` below), `docsumo_doctype_export_documents` (one of `doc_ids`, `folder_ids` or `select_all` with `doc_type` and the filters; `status: ["processed"]` is the Processed tab) | The export returns a `download_url`; save files with the host download capability and inspect them locally. |
| Retry / reprocess | `docsumo_doctype_retry_documents` | See below. |
| Change doctype | `docsumo_doctype_change_document_type` | Needs the target doctype's **numeric id** from `docsumo_get_document_types`, not the `value`. |
| Assign owner | `docsumo_doctype_change_document_user` | |
| Delete | `docsumo_doctype_delete_documents_and_folders` (`doc_ids`, `folder_ids`, or `select_all` with filters) | Destructive: confirm the exact documents with the user first. For a member, only their own documents and case documents are deleted. |
| Upload | `docsumo_create_file_upload`, then `docsumo_upload_document` (`file_ref`) or `docsumo_upload_case_document` (`file_refs`; `workflow_id` for a published workflow) | The hosted server can't read the user's files, so the file goes up through an upload link first: see [uploading files from your computer](#uploading-files-from-your-computer). |
| Analytics | `docsumo_get_doctype_analytics` (`part` = `general`, `accuracy`, or both by default) | |
| Auto-split | `docsumo_review_get_split` (`doc_id` of a split document: its groups and original document id), `docsumo_autosplit_download` (the original `doc_id`; the split documents' extracted data; admins only) | |
| Credit estimate | `docsumo_doctype_calculate_document_credits` | Optional: when the user wants the cost of a retry or type change before agreeing. |

### Uploading files from your computer

The Docsumo MCP server is hosted, so it can't read a file on the user's computer or a file attached in chat: a local
`file_path` is refused ("This server does not read files from its own filesystem"). Upload through a link instead.
This needs somewhere to run `curl` where the file is: a shell on the user's machine (Claude Code, Codex), or the code
sandbox that holds a chat attachment (Claude.ai, ChatGPT, Cowork).

1. **Confirm first.** Name the files and the target (document type, case type or published workflow), and say that
   uploading starts processing and spends Docsumo credits.
2. **Get the links:** `docsumo_create_file_upload` with each file's `filename` and, if known, `size_bytes`. It returns
   an `upload_url` and a `file_ref` per file.
3. **Send each file**, from where the file is, with the returned `Content-Type`. Quote the path:

   ```bash
   curl -sSf -X PUT -H "Content-Type: application/pdf" --data-binary @"/path/to/invoice.pdf" "<upload_url>"
   ```

   A `201` answer with `size_bytes` means the file arrived. Upload URLs expire after 15 minutes.
4. **Upload to Docsumo:** `docsumo_upload_document(doc_type=..., file_ref=...)` for one document. For a case packet,
   `docsumo_upload_case_document(casetype_id=..., file_refs=[...])`, with up to 30 files in one case. For a published
   workflow, `docsumo_upload_case_document(workflow_id=..., file_refs=[one])`.
5. Continue with the new documents (`docsumo_doctype_wait_for_documents`, `docsumo_list_documents`).

Things to know:
- A `file_ref` works once and only with the same API key. The staged copy is deleted as soon as Docsumo accepts it.
  If step 4 fails, retry it with the same `file_ref` (refs last an hour). After a success, ask for new links.
- Files over the returned `max_size_bytes` are refused (`413`). Use the app or email for those.
- If `curl` can't reach the upload URL's host from a chat sandbox, the workspace's code-execution network settings must
  allow that host. Tell the user; an admin may need to add it.
- Never print the API key, and don't try other upload APIs.

**When a link can't be used** (no shell or sandbox, the host is blocked, the file is too large, or the tool answers
that uploading "is not set up here"), ask the user to upload the files themselves:

- **In the app:** drag the files onto the document type's Documents tab, or the case's documents for a case.
- **By email to a document type:** its upload address is in Configure > Import & Export
  (`docsumo_configure_get(tab="import_export")` reads it).
- **By email to a case type:** its `upload_email` comes from `docsumo_get_case_configuration`. Those emails land in
  the case type's Inbox, where they become cases or are attached to them ([case type Inbox](../../product-inbox/SKILL.md)).

An upload starts processing and spends Docsumo credits like any other.

Downloads return short-lived links that need no credential; save one with `curl -sSfL -o <file> "<url>"` or the
host's fetch before inspecting it.

### Retry / reprocess

Retry re-runs processing for the selected documents with the doctype's **current**
Edit Fields and Configure settings. The document keeps its id, returns to `processing`, then
lands in Review or Processed (or `erred` again). It **spends Docsumo credits** per page. It is the
normal path after a configuration change ("reprocess the failed ones") and after an
`erred` state. `docsumo_doctype_retry_documents` takes `doc_ids` / `folder_ids` **or**
`select_all` with the filters and deselect lists (naming ids together with `select_all` is refused),
`retry_status` (default `all`), `batch_size`, and `trigger_workflow` to re-run the case workflow
instead of the document processing, for one named case document only. Reprocessing runs in the background;
read status with `docsumo_list_documents` or wait with `docsumo_doctype_wait_for_documents`
(`since` = the time taken just before the retry) until it reports `complete`. A retry can be refused for a file that
cannot be processed again; read the message returned. If a document errors again, note its ID, time and error
text. Wrong values go to [extraction triage](../../extraction-triage/SKILL.md); a document that keeps failing with an
error the settings cannot fix goes to Docsumo support with that information.

After a settings change, retry a few documents first to confirm the change works, then the rest once the user agrees
to spend the Docsumo credits.

### Downloads and exports

`docsumo_download_document` formats: the file itself as `original_file`, `searchable_pdf`, `images` (one per page)
or `ocr_text`; the extracted data as `json`, `csv` or `xml`. One document failing does not stop the others.
A searchable PDF exists only for some documents; when it does not, the tool says so (use `original_file`, or
`ocr_text` for the text).

The bulk export (`docsumo_doctype_export_documents`) takes `download_type`:

| Format | Content |
|---|---|
| `json` | Extracted fields with values, confidence and positions (the API/webhook shape). |
| `csv` | One row per document, columns are fields; tables flattened. |
| `csv_long` | One row per field/cell (long format); friendlier for tables. |
| `raw` | Raw extraction output (not offered for a folder download). |

A bulk download that takes too long keeps running in the background and is emailed, or offered on the All
activities page ("Download request timed out. Downloading in background…").

Sample exports for a doctype are under Configure > Import & Export
(`docsumo_configure_download_samples`). Webhook and API responses use the JSON shape; the
Data Table (see [adjacent areas](../../product-navigation/references/other-areas.md)) exports CSV or Google Sheets.

## Review screen

### What the user sees

- Page images with **bounding boxes**; selecting a field highlights where the value was read.
  Field positions are 1-based pages; raw page boxes are 0-based.
- Sections and fields with the extracted `value`, the original `orig_value`, a confidence
  score, a **low-confidence** marker, format validity, and a `review_required` marker; hidden
  fields are not shown. Mandatory fields block approval when empty.
- **Tables / line items** as a grid: add or delete rows, re-extract a table, extract similar
  tables, drill into a cell. Range selection, paste, keyboard navigation, column widths, Hide Empty Columns and
  clear actions are supported. Edits can be locked while AI work is pending. Clearing values changes review data
  only; it does not delete fields or change a lookup table.
- **Sumo AI** document chat: ask questions about the document, get table edit suggestions. Suggested table edits
  are not saved corrections until applied.
- **Reference documents** (continuous learning): matched examples the extractor used,
  which a reviewer can include or exclude.
- Bulk transforms: change the date format or year across fields; dropdown option lookup.
- **Actions**: edit values, Approve (finish review; configured exports and delivery are separate steps to verify),
  Skip (document becomes `review_skipped`), previous / next document. A document can show as **AI approved** or
  **Human approved**; neither proves delivery.
- Variants: **Spreadsheet review** (`/document-spreadsheet/:docId`) for Excel-type doctypes,
  **CSV / database-table review** (`/database-table/:docId`), **original file preview**
  (`/original-file-preview/:docId`). Some accounts see an older version of the review screen, so screenshots can
  differ.
- Review previews PDF, image, TIFF and Excel (XLSX/XLS) files. The file types an upload accepts depend on the
  upload screen; check the upload dialog or the public documentation before promising a format.
- A lookup set to **None** is a stored choice that behaves as empty when hiding empty columns or searching. A
  dropdown or text value "None" can be real data: check the field type and stored value before treating it as blank.
- Shared case review deliberately offers fewer actions than a member has, so missing buttons there are not
  automatically a fault. See [case sharing](../../product-workflows/references/cases.md).

### Through the MCP

`docsumo_update_document_field` is the reviewer's value edit; reviewer corrections and configuration fixes are
distinct actions, and correcting a value needs the user's request for that document. Read `docsumo_review_get_data`
(`detail="compact"`, with `fields` or `flagged_only` to narrow it) for values, validation state and positions,
`docsumo_get_lookup_candidates` for a lookup field's Matching records, `docsumo_review_get_references` for its
Reference documents panel, and `docsumo_download_document(doc_ids=[...], format="original_file")` to see the source.

### Common questions that start on the review screen

| Question | Usually means |
|---|---|
| "The value is highlighted in the wrong place" | Extraction picked a different occurrence; improve the field's prompt. |
| "Field is not there" | Field hidden in its settings, not in the document type, or the document was processed before the field was added (retry). |
| "Cannot approve" | Mandatory field empty, invalid format, or a validation rule; check the field's settings. |
| "Confidence is low on every field" | Poor scan quality or OCR settings (Configure > Pre-processing), or the AI model selected (Configure > Extraction). |
| "My correction did not stick for the next document" | Continuous learning is off, or a value edit was expected to change the document type's setup. |
| "Document opened in an old-looking screen" | The older version of the review screen; not a fault. |
