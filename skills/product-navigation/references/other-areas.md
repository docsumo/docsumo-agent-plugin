# Adjacent areas: recognise and hand off

Use these routes to identify the surface and choose the right skill. Tool availability and the user's role govern
operations; recognizing a screen alone does not mean a tool can operate it.

## Cases and workflows

Workflows include case-attached and independent graphs, with manual, schedule, case-event and combined upload
triggers. Cases bundle documents under a case type; a case-event run can reference a case without owning its type.
Use [product workflows](../../product-workflows/SKILL.md) for navigation, supported setup/test/publish operations,
runs, linked cases, sharing and artifacts. Do not substitute a case upload for a trigger run that no tool supports.

## Records and legacy Database Tables

**Records** (`/tables`, formerly Tables) contains reference/entity tables and linked records. Settings → Database Tables is the older CSV
source surface. Neither is a document's extracted Data Table nor its line items. Use
[product tables](../../product-tables/SKILL.md) for source selection, imports, typed records and lookup/write
behavior.

## Sumo AI

The product assistant is **Sumo AI**, with full-page `/ai/:threadId` conversations and an in-product panel.
Conversation files and unapplied table suggestions are distinct from saved document corrections. See
[review guidance](../../product-documents-review/references/documents-and-review.md).

## Data Table (grid view)

The **Data Table** tab (`/active-document/:docType/data-table`, or `/all-data/:docType/data-table`
across doctypes) shows extracted values as a spreadsheet: rows are documents, columns are the
doctype's fields plus metadata (status, uploaded by, dates), with drill-down into line-item
tables, smart (AI) filters, confidence and reasoning per cell, column show/hide/rename, and
bulk actions (approve, validate, delete, retry with a credit estimate, rerun one column) and
export to CSV or Google Sheets. It reads the same extraction data as the review screen, so a
wrong value here is a doctype setup question. A grid that does not load, a stale column set after a
change to the fields, or an export failure goes to Docsumo support. No tool targets the grid itself;
use `docsumo_get_document_data` for the underlying values.

## Integrations

**Integrations** (`/integration/connector-library`, `/integration/my-integrations`,
`/integration/trigger`) connect external systems for **import** (documents in) and **export**
(extracted data out) through **triggers**: Google Drive, Google Sheets, OneDrive, SharePoint,
Dropbox, Box, Amazon S3, Zapier, Email, API, Custom Code, Salesforce. Each connected integration
has an auth type (OAuth or credential-based) and a status; each trigger maps doctype
fields to destination columns and has its own activity log. Vocabulary: connector, trigger,
mapping, re-authenticate, consent. `docsumo_list_integrations` (owners and admins) reads each connection's status
(connected, active, disabled, error, authentication_error) and its last few log messages, and each trigger's
direction, document type, last run and error message; it never returns credentials or the connected account. Files
that stopped arriving usually show as an authentication error after a revoked or expired grant, which the user
fixes by reconnecting on the screen. Documents that arrive via an integration show `uploaded_from` accordingly on the
Documents screen; extraction problems on them are doctype questions, while failed exports, mapping errors and
connector faults go to Docsumo support with the trigger name, status, log messages and timestamps. For setup
questions use the [public docs](support-docs.md).

## Case assistant and collaboration

Chat, comments, tasks and request forms attached to a case are not available through these tools; give the user
the steps in the app.
