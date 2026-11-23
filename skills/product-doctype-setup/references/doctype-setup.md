# Edit Fields and Configure

## Edit Fields

The section/field tree, source preview and settings panel define what to extract. Fields have types, prompts,
optional settings and ordered blocks; tables have columns and a separate table prompt. A section prompt can
provide shared party/context instructions. A document description becomes extraction context, not just tile text.

Field types: String, Number, Date (DD/MM/YYYY or MM/DD/YYYY), Dropdown, Checkbox, Signature, Table and Lookup; table
columns take the same except Signature and Table. Lookup Reference fields are created from a lookup's chosen columns,
never added by hand. Every field is built in Edit Fields ([building fields](editing-fields.md#build-fields)).

| Need | Basic MCP reads/actions (read the live schemas) |
|---|---|
| Definition, fields, prompts | `docsumo_get_doctype_schema_and_fields` (`summary` for names, ids and types only), `docsumo_field_setup_get` |
| Tree and one field's settings | `docsumo_field_setup_get` (`include_block_settings: false` for the tree), `docsumo_field_setup_get_field_settings` |
| Check an unsaved edit | `docsumo_get_doctype_schema_and_fields` reads the open Field Setup draft without discarding it (`read_from` is `draft`) |
| Section/table prompt | `docsumo_get_doctype_schema_and_fields`: a section's `config.prompt`, a table field's `table_prompt` |
| Options/types/lookup fields | `docsumo_field_setup_get_settings_options`, `docsumo_field_setup_get_data_types`, `docsumo_field_setup_get_lookup_fields` |
| Editing session | `docsumo_field_setup_start_session`, `docsumo_field_setup_save`, `docsumo_field_setup_cancel` |
| Test a change | No tool runs a draft on a document. Save, then retry one document (`docsumo_doctype_retry_documents`) and check its values. |
| Add fields, columns, sections, tables | `docsumo_field_setup_add_field`, `docsumo_field_setup_add_section`; remove with `docsumo_field_setup_delete` |
| Field/type/prompt changes | `docsumo_field_setup_update_field_settings`, `docsumo_field_setup_change_field_type`; section and table prompts with `docsumo_update_doctype_fields` (`section_prompts` `[{section, prompt}]`, `table_prompts` `[{section, table, prompt}]`, the whole new text) |
| Dropdown options | Read the `drop_down` block's `config.options` in `docsumo_get_doctype_schema_and_fields`; change them in the field's blocks with `docsumo_field_setup_update_field_settings` (its `block_settings` replaces the whole list). CSV-backed options are Database Tables, which no tool reads: the user checks them in Settings > Database Tables. |

When the user's process works on a row-level export (one spreadsheet row per line item), add each derived value as a
column of that line-item table, computed from sibling columns or copied from a header field, not as a header field.

Read current state, keep unaffected blocks/columns, save the intended session and read the saved state back.
A draft is not proof of a save, and opening Edit Fields discards an unsaved draft
([draft rules](editing-fields.md#an-open-draft-and-changes-saved-elsewhere)).
A save can also reprocess documents depending on its [save scope](editing-fields.md#save-scope); never assume that
every old document reran or that saving has no processing effect.

## Configure

Read with `docsumo_configure_get` (`tab` for one tab, `setting_name` for one setting). Write with
`docsumo_update_doctype_configuration` (`settings=[…]` by `setting_name`, `doctype_title` for the name), then read it back.
Reads carry `value_label` for settings with fixed options: use those labels, never a remembered code.

| Tab | Controls and their meaning |
|---|---|
| General | Name; document description/context; AI Document Approval/STP; assigned users and notifications |
| Pre-processing | Image quality (DPI); orientation; OCR on digital PDFs; split type and its parameters (page count, pattern, custom API URL, split prompt); Additional Parameters |
| Extraction | AI extractor/model; Text/Image/File modes; continuous learning with Template Priority, Template Threshold and Number of Templates; Batching Configuration with page selection, batch sizes and overlap; reasoning effort |
| Import & Export | Upload email; parse email body; folder behavior; upload failure notification; sample JSON/CSV exports |
| Post-processing | Custom processing code set up with Docsumo; read it only to know it exists and never change it |

For PDF extraction, the fields and table batch sizes are pages per call, not a number of fields or rows.
Excel files are batched differently. A batch size of zero does not mean the whole document is read at once.

## Route the symptom

- Blank/wrong values or missing table rows: [extraction triage](../../extraction-triage/SKILL.md).
- Correct values but Review/approval unexpected: the STP setting, mandatory fields, field validation and confidence
  thresholds.
- Wrong date/decimal presentation: the field type and its format settings before prompt edits.
- Blur, rotation or missing OCR: [visual diagnosis](../../extraction-visual/SKILL.md).
- Split or classification setup: the sections below. The resulting documents and the manual-classification screen are
  in [documents and review](../../product-documents-review/SKILL.md); workflows and lookup sources have their own skills.
- Integration delivery: [integrations](../../product-navigation/references/other-areas.md#integrations).

Example wording: “In Invoice → Configure → Extraction, the model is Advanced.”
Keep meaningful numbers: “Image quality is 200 DPI.” Unknown values: “I could not confirm what the saved
extraction mode means.” Do not give an unexplained code as the answer.

## Setup guidance

Current templates offer Standard and Advanced models; Basic is no longer selectable there. Do not silently change an
old saved Basic value. Extraction Mode offers Text, Image and File. Model tier and reading mode are different controls.
New custom doctypes start with continuous learning off and Image mode; copied or older doctypes keep their own
choices, so read them back rather than assuming defaults.

Batching Configuration includes Fields Batch Size, Table Page Selection, Table Batch Size and Overlap. The current
table default is 10 pages. Page selection uses table context to choose relevant pages before batching; it does not
limit rows. Values in Additional Parameters can override visible settings, so read both when behavior differs from
the UI. Do not turn on learning or page selection as an automatic fix without evidence from the documents.

Use the table's separate prompt for table-wide row/continuation/summary instructions and per-column prompts for column
meaning. Save the table prompt and read it back separately.

A lookup field picks one row of a Database Table or a Records table (the Lookup Table picker groups them as Database, Entity
and Reference) by one or more conditions, each "is exactly" or "is approximately" a document field, joined by AND or OR
in groups. The first condition's column is the value shown, and each Return column adds a field with another column of
the matched row. In Review, the field's Matching records panel lists every candidate row, with Search candidates.
[Records](../../product-tables/SKILL.md) covers the tables themselves and how matching works; the block's settings
are in [editing fields](editing-fields.md#lookup-blocks).

## Splitting and the AI Auto-Classifier

Classifying and splitting are separate features. Set up only what the user's files need: many accounts need just one
of them.

| The files | Set up |
|---|---|
| One document per file, of one of several types | The AI Auto-Classifier with its target types. Its split type stays None, so each file is classified whole. |
| Several documents of one type back to back in each file (statements, invoices, one bill per account) | Split with AI on that type, with a Split prompt saying where one document ends. Files are uploaded to that type; no classifier. |
| Pages of several types in one file (a cover with its bills, a packet of forms), or pages to leave out | Split with AI on the AI Auto-Classifier: it gives every page a target type or leaves it unclassified. |
| Both: mixed types, and one type's pages hold several documents | Split with AI on the AI Auto-Classifier, plus Split with AI on each target type whose pages must be cut into several documents. |

**How an AI split runs.** On the AI Auto-Classifier the model first labels every page with a target type, or
unclassified, from the classifier's Split prompt and each target's own Document Description. Adjacent pages with one
label form one part: two runs of the same type with another type between them are two parts, and unclassified pages
stay on the classifier as their own documents. Then a part of two or more pages is cut into documents only if its
target type has Split with AI and its own Split prompt. That prompt, with the classifier's Split prompt as general
instructions, decides where each document starts. A target without its own AI split keeps each part whole, whatever
the classifier's prompt says. A file uploaded straight to a type with Split with AI is all that type, and only goes
through the cutting step. Both steps read a limited window of pages at a time (about 20, overlapping the previous
window by a few pages), each window on its own.

So each prompt has one job:

- **The classifier's Split prompt**: which pages belong to which type, and which to leave unclassified.
- **A target's Document Description**: what that type is, so its pages are recognised. It is also that type's
  extraction context, so never replace or trim it: put one sentence saying what the document is and how its pages look
  in front of the text already there, even when that text looks generic.
- **A target's own Split prompt**: where one document of that type ends and the next begins, and what must stay
  together.

**Write rules a page can answer.** Every page is judged inside its own window, so tell the model what a page
shows and what that means: the signs a page carries (an identifier that belongs to one document, such as an account,
invoice or policy number with its own amounts; a table listing many such documents; a notice, terms or blank page with
nothing of its own) and the type or cut each sign gets, with a page that carries no sign of its own following its
neighbour. Never make a page depend on the whole file ("if the file has one account", "every page before the first
invoice"): in a long file no window sees the whole file, so such a rule comes out differently in each window. Name
document features, never a file, vendor or page number.

Rules for cutting one type's pages go in that type's own Split prompt: in the classifier's they change nothing unless
the type has its own split. Put each type's description in its own Document Description.

**Split with AI is the split type to set up.** The other types — Fixed Number, Text Pattern, Custom API — are
deterministic and suit only boundaries that really are fixed: a constant page count per document, or a separator
string every bundle carries. Keep a working AI split as it is. Turn **Create folder on split** on whenever a split is in use so the parts stay
together; on the AI Auto-Classifier it turns itself on when the split type becomes AI.

**Checking a split**: upload a few real files through a link
([uploading files](../../product-documents-review/references/documents-and-review.md#uploading-files-from-your-computer)),
or have the user upload them in the app or by the type's upload email, wait for them, then read each original's parts with `docsumo_review_get_split` (its split
groups: each part's type and pages, and the original document id), or with `docsumo_autosplit_download` (admins only:
the extracted data of every part). When the user gives the expected parts,
compare every file. On a miss, change the prompt that owns it, with a rule about what the missed pages show: a page
with the wrong type needs the classifier's Split prompt or the types' descriptions; a part that holds two documents,
or one document cut in two, needs that type's own split. Then have all the files you compare uploaded again, not only the one
that missed, since a rule for one file can break another (a retry or reprocess does not split a file again: its parts
keep the old cut, so only a new upload tests a change), and compare, and repeat while the results improve. Report what
still misses and what those pages show. If fresh uploads keep missing in a way prompts cannot fix, the user can
contact Docsumo support with example files.

**AI Auto-Classify** is a document type of its own (`auto_classify_ai`, "AI Auto-Classifier" on Home and in the Agents
Hub). It sorts uploads into other document types instead of extracting, so its Configure screen has General,
Pre-processing, Import & Export and Post-processing but no Extraction tab, and it has no fields to edit.

- **Classification Type** on General is General or Custom. General considers every document type in the account;
  Custom considers only the ones picked in the Edit dialog, which can also create new type names. Switching to Custom
  and back keeps types that already hold documents. Set Custom's targets with one write of `classifier_doc_types`
  listing every target: a type left out stops being one. Send only active targets. An inactive entry in the list is a
  former target that documents were classified into: it routes nothing and needs no cleanup. When the user names the types to route to, select
  Custom with exactly those: General lets every type of the account compete.
- **Auto-classifier description** on General describes the sorting job as a whole. It is read when the classifier's
  split type is None. With Split with AI it is not read: the classifier's Split prompt takes its place. Each candidate
  type is told apart by its own **Document Description** either way.
- **Split type None** on the classifier classifies each file whole: one target type for the whole file, or
  unclassified, and the target's own split does not run. **Split with AI** labels pages and cuts files as described
  above.
- **Classify documents using custom model** switches from the AI to a trained classifier, and only once training has
  produced a model; start it with the training action. Training problems go to Docsumo support. Without a trained
  model the AI classifies every upload: training is optional, never a prerequisite.
- **Where a file ends up is the result.** A file the classifier places moves into that target type: it leaves AI
  Auto-Classify's list, its `type` becomes the target and its `source_type` keeps the classifier. A file it cannot
  place keeps the classifier's own type (unclassified) and waits in Review. Most unclassified files also carry a
  **suggested type**: the AI's own name for the file, never one of the active targets, shown on the AI Auto-Classify
  tab and in Manual classification to help the user pick a type by hand. It never moves the file, so it is normal
  output, not a classification and nothing to fix with the description or settings.
- **Testing a classifier**: have the user upload a few samples of each target type and of other kinds, wait for them
  (`docsumo_doctype_wait_for_documents` on the classifier finds each one wherever it went), and judge each by its
  `type`. A target-type sample left unclassified, or another kind moved into a target, is a miss. Every other kind left
  unclassified is correct, even when its suggested type names a document type of the account, inactive or former
  targets included: the classifier routes only into its active targets, and which types to target is the user's
  choice, not a fix.

Workflow Split and Document Type Classifier blocks are the same idea inside a workflow and are configured there
([workflows](../../product-workflows/SKILL.md)).

## US bank statement doctypes

The US Bank Statement doctype (and its duplicates) is extracted differently from other document types.
Configure → Extraction adds Fraud Analysis, Transaction categorization and Analytics Type (None, Basic, Cashflow, MCA);
transactions are categorised only when categorization is on and Analytics Type is not None. The model, Extraction Mode,
batching, reasoning effort, learning and document description controls do not change its extraction, and Auto-extract
fields is unavailable. Renaming a custom document type does not make it a bank statement type. The older upload screen
allows 75 MB files for this type (35 MB otherwise), and Review offers “Update date format” on its date columns.
