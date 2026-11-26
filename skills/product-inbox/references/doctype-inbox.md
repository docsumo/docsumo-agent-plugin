# Document type Inbox and All Inbox

## The screens

- **A document type's Inbox** (the Inbox tab of a document type, `/active-document/<type>/inbox`): one row per email
  sent to the type's address (`upload_email` from `docsumo_get_document_types`; each person has their own). A row
  shows the sender, the subject, the files, and a status with its reason under it. Tabs: All, Need review, Attached
  and Archived. All leaves out archived emails, and an email still processing shows only under All. An AI
  Auto-Classifier has an Inbox too. An email whose files it sorted also shows in the Inbox of each type a file went
  to, and stays there after the file moves to yet another type.
- **All Inbox** (main nav, `/inbox`): case type and document type emails together. Tabs: All, Need review, New
  cases, Attached, Failed and Archived. New cases and Failed hold only case type emails. Filters: Agent (the case or
  document type), Attached To (nowhere yet, a case, or a document type) and Status.
- **Opening an email** shows the message, its files and a Document panel. A file's ⋮ menu has Change document type,
  Assign user, Retry and Download. Bulk actions on ticked emails: Archive, Restore and Retry.
- **Who sees them:** owners and admins only. Members and moderators have neither screen, and the tools refuse them
  (UNAUTHORIZED). A case type's own Inbox is unchanged and open to every role.
- **Since when:** only emails that arrived after these Inboxes shipped (24 Nov 2026) are listed. An older email is
  not missing: it predates the screen. Its documents are on the type's Documents tab.

## Reading them

| Need | Tool |
|---|---|
| A document type's Inbox, one tab at a time | `docsumo_list_inbox_emails` with `doctype_id` (`tab` all, need_review, attached or archived; `q` over sender, subject and file names; `include_counts` for each tab's count) |
| All Inbox | `docsumo_list_inbox_emails` with neither `doctype_id` nor `casetype_id`; narrow with `kind` (case_type or doc_type), `agents` (`doc_type:<doctype_id>`, `case_type:<casetype_id>`), `statuses` and `attached_to` (`none`, `case`, `doc_type:<doctype_id>`) |
| One email in full: its files and where they went, rejected files, folder, history | `docsumo_get_inbox_email` |
| Let the user open or save one file | `docsumo_get_inbox_attachment_link` with a `doc_id` from `documents` or `split_parts` |
| The address to send a type's documents to | `upload_email` in `docsumo_get_document_types` |

The user's screen is the scope: on All Inbox a question about "the Inbox" means All Inbox, on a document type's Inbox
tab it means that type's.

## Status and reason

Use `status_message` as the reason's wording: it is the screen's own text.

| Status (screen) | `status_reason` | What happened | Fix |
|---|---|---|---|
| Attached | none | Every file became a document of the type | Nothing to fix |
| Need review | `files_rejected` ("N files rejected") | Some files became documents and the rest were refused: `rejected_files` gives each name and reason (wrong file type, outside the size limit, an email body that could not be converted). The sender got a reply listing them | Ask the sender for a supported copy; once the email is handled, set it to Attached or archive it |
| Need review | `files_failed` ("N files failed") | A document's processing failed (`state: failed`, `doc_status: erred`) | **Retry** the email: its failed files are processed again, and a successful retry returns it to Attached |
| Need review | `no_supported_files` (No supported files) | Every file was refused; no document was made | As for rejected files |
| Need review | `processing_error` (Couldn't process this email) | Docsumo could not process the email | Report the email and when it arrived; resending it is the user's call |
| Archived | `no_attachments` (No attachments) | Nothing to import: no file and no body to import. The sender got a reply | Expected. The type's Parse email body setting imports the body of emails that carry their content there |
| any | `manual` | A person set the status by hand | Read `events` for who and when |

## Where an email's files went

Read the email with `docsumo_get_inbox_email`. Each entry of `documents` is one file as its document stands now:

- `doc_type_title` is the type it is in now. "Unclassified" means a classifier still holds it and did not sort it.
- `state`: `attached` (a document of that type), `failed` (its processing failed: Retry) or `deleted` (the document
  was deleted since).
- `doc_status` is its status in Documents. Say it as the product does: `new` or `processing` is still processing,
  `review_required` or `reviewing` is in Review, `review_skipped` is Skipped, `processed` is Processed, `erred` is
  Failed, `splitted` is split into parts. Right after a retry the email's status and message can still say a file
  failed until its documents finish; the files' own `state` and `doc_status` are current.
- A split file is an entry whose `split_parts` lists its parts. Each part is a document of its own, with its own type,
  state and status; the original is only the file that was split.
- `folder` is the folder its documents were put in (Create folder from subject), or empty.
- `rejected_files` are files that never became documents.

## Acting on them

| Need | Tool |
|---|---|
| Archive, restore or relabel one or many emails (up to 100) | `docsumo_set_inbox_email_status` with `email_ids` and `archived`, `unarchived`, `need_review` or `attached` (`new_case` is for case type emails only). One email failing does not stop the others: report each result |
| Retry an email's failed files | `docsumo_rerun_inbox_email` with `retry`. It retries only the files whose `state` is `failed`, split parts included, and spends credits as an extraction does. An email with none is INBOX_NOTHING_TO_RETRY. Re-check and Import email body are for case type emails only (INBOX_NOT_A_CASE_EMAIL) |
| Move a file to another document type, or assign it to a member | `docsumo_doctype_change_document_type` or `docsumo_doctype_change_document_user` with its `doc_id` ([documents and review](../../product-documents-review/references/documents-and-review.md)) |

Archiving, restoring and relabelling act on live mail: name the emails before you do it. A retry and a change of
document type extract again and spend Docsumo credits: say so and act only after the user confirms. After a retry,
read the email again later to see each file's new `state` and `doc_status`.

A document type's Inbox settings (the gear on its Inbox: Parse email body, Create folder from subject, Upload to
existing folder, Notify on upload failure) are its Configure settings:
[document type setup](../../product-doctype-setup/SKILL.md).
