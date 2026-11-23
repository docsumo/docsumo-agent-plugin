# Inbox emails and actions

## The screen

Open a case type and pick **Inbox** in its sidebar (between Cases and Configure). The badge on Inbox counts the
emails in Need review. The header shows the address to forward to, **Start reviewing** (a queue of the Need review
emails: Attach & next, Next, Skip) and the gear button for **Inbox settings** (owners and admins only).

- **Tabs:** All, Need review, New cases, Attached, Failed, Archived. **All leaves out archived emails.** Need review
  also holds partly attached emails.
- **Rows:** sender, subject, files, status chip, the case or cases the files went to, and when the email arrived.
  Test emails carry a **Test** badge.
- **Bulk actions** on selected emails: **Attach to case…**, **Retry**, **Archive**, **Restore**.
- **Row menu:** Copy sender address, **Re-check**, **Import email body**, **Restore**.
- **Attach dialog:** search cases, or **New case** with a **New case name**, then **Create and attach**.
- **Status menu:** changes the chip by hand. It is disabled while the email is processing ("Status can be changed
  once processing finishes"), for test emails ("Test emails are read-only") and for archived emails ("Restore the
  email to change its status").

Every role can see the Inbox and act on emails. Shared case links cannot reach it.

## Tool values and screen labels

| Tool value | Screen label |
|---|---|
| tab `all` / `need_review` / `new_cases` / `attached` / `failed` / `archived` | All / Need review / New cases / Attached / Failed / Archived |
| status `processing` / `need_review` / `new_case` / `attached` / `failed` / `archived` | Processing / Need review / New case / Attached / Failed / Archived |
| status `partial` | "X of Y attached" (`file_counts.attached` of attached + review) |
| file `state` `attached` / `review` / `deleted` | Attached / Need review / Case deleted |
| file `state` `ignored` | not shown as a file (signature images skipped by Ignore signature images) |
| file `state` `split` | the original of a split file, kept for preview; its parts are the files to attach |
| `rejected_files[].reason` `unsupported_type` / `too_large` / `word_not_supported` | Unsupported file type / Larger than 500 MB / Word files aren't supported |
| `running_action` `process` / `retry` / `import_body` / `attach` | Re-checking… / Retrying… / Importing email body… / attaching (shown per file) |
| rerun action `recheck` | Re-check |
| `suggested_cases[].confidence` `high` / `medium` | every condition matched exactly / a condition matched approximately |

Use `status_message` and each file's `reason_message` as the reason's wording; they are the screen's own text. The
screen says "couldn't read this file automatically" where a message names the regex or LLM method. Do the same for a
user who is not setting up the Inbox.

## Tool for each job

| Need | Tool |
|---|---|
| One tab, searched and paged | `docsumo_list_inbox_emails` (`tab`, `q` over sender address and name, subject and file names, `test` include/exclude/only, `sort`, `limit` up to 100, `offset`; `total` is the whole tab) |
| How many emails each tab holds | the same tool with `include_counts` (adds `processing`) |
| One email in full: body, files, values found, suggested cases, history | `docsumo_get_inbox_email` |
| Let the user open or save one file | `docsumo_get_inbox_attachment_link` (`download` to save; otherwise it opens, a Word file as its PDF) |
| The addresses, whether the workflow is published, the settings | `docsumo_get_inbox_settings` |
| Attach files to a case or a new case | `docsumo_attach_inbox_emails` |
| Retry, re-check or import the body | `docsumo_rerun_inbox_email` |
| Relabel, archive or restore | `docsumo_set_inbox_email_status` |
| Find a case to attach to | `docsumo_list_cases`, or the email's `suggested_cases` |

An unknown case type is not an error: the listing is empty and the counts are zero. Confirm the case type before
saying "no emails arrived". A file link expires five minutes after it is made. Hand it to the user to open now, and
make a new one if they come back later.

## "Did the email from X arrive?"

1. List **All** with `q` set to the sender, the subject or a file name, and `test: include`.
2. Not there? List **Archived** with the same search: All leaves archived emails out, and the clean-up rules archive
   some emails on their own (Archive emails without attachments).
3. Still nothing? Read `docsumo_get_inbox_settings`:
   - `addresses.live` and `addresses.test` are the current user's own addresses. Addresses are per person, so a
     teammate's address differs. Ask which address the email was sent to.
   - When `workflow.is_published` is false, the live address refuses mail. The case type's workflow must be
     published first ([product workflows](../../product-workflows/SKILL.md)). Test mail still arrives.
   - A forwarding rule or mail filter on the sender's side is outside Docsumo. Say so rather than guess.

## "Why is this email in Failed / Need review / not attached?"

Read the email with `docsumo_get_inbox_email`. Check `running_action` first: while it is set, the email is still
being worked on. Then read `status`, `status_reason`, each attachment's `state` and `reason_message`,
`rejected_files`, `extracted` and `suggested_cases`. Match the reason to the table, then give the fix.

| `status_reason` (screen text) | What happened | Fix |
|---|---|---|
| `processing_error` (Processing failed), status Failed | Docsumo could not process the email | **Retry**. If it fails again, report the email and when it arrived |
| `sender_not_allowed` (Sender not allowed) | Accept from is set to Only allowed senders, and the sender is not on the list | Add the address or `@domain` to Allowed senders (an admin, in [settings](inbox-settings.md)), then **Restore** or move it to Need review to re-check |
| `no_attachments` (No attachments) | Archived by Archive emails without attachments | Expected. Turn on **Import email body** for emails that carry their content in the body, or import this one's body |
| `encrypted` (File is password-protected) | A file is password-protected | Ask the sender for an unprotected copy |
| `all_files_rejected` (No supported files) | Every file was rejected: see `rejected_files` | Unsupported type: only PDF, image, Office and spreadsheet files. Over 500 MB: ask the sender to split it. Word: ask for a PDF |
| `too_many_files` | More than 100 usable files, so none was read and every file waits | Attach by hand, or ask the sender to send fewer files per email |
| `not_read` (Some files weren't read automatically) | Some files could not be read: each file's `reason_message` says why (too large, time limit, unreadable, conversion failed) | Attach those files by hand |
| `automation_off` (Automatic matching is off) | The automation is set to Send every email to Need review | Attach by hand, or change the automation |
| `matching_pending` (Waiting for a person) | Waiting for a person to decide | Attach by hand |
| `no_match` (No matching case) | The rules found no case, and When nothing matches is Send to Need review | Check `extracted`: a missing value points at the keys, a value with no case points at the case data. Attach by hand, or create a new case |
| `matched` (Matched a case: check and attach) | The files matched exactly one case. **Matching never attaches by itself**: a person confirms | Show the suggested case and what it matched on; attach after the user confirms |
| `several_matches` (message names the cases) | More than one case fits the same values | Show the candidates with what each matched on; the user picks one. Tightening the rules (more conditions, exact matches) reduces this |
| `several_values` / `several_cases` | Files hold different values, or fit different cases | Show each file's suggested case (`doc_ids` on each suggestion), then attach file by file with `doc_ids` |
| `split_part` | Auto split cut a file into parts. Each part waits with its suggested case | Check each part's case and attach the parts. The original is never attached |
| `create_case_per_email` (A new case was created) | Create a new case for each email made one | Nothing to fix. The case is in `cases` |
| `test_email` (Test email: a test case was created) | Sent to the test address | Expected. Test emails are read-only |
| `manual` (Status set by a person) | Someone changed the status by hand | Read `events` for who and when |

`action_failed` set means the last person's action (attach, re-check, retry, import body) failed. Repeat it once,
then report it rather than loop. An attachment in state **Case deleted** went to a case that has since been deleted:
attach it again to another case.

## Attach by hand

1. Read the email. List its files waiting for review (`state: review`) and the `suggested_cases`, best first, each
   with its stage, its confidence, what it matched on (`matched_on`, `fields`) and, where given, which rule block
   found it (`matched_step`: 1 is the If block, 2 the first Else if). `best_match` is the one case that
   ranks strictly first, or empty when the ranking is a tie or the reason is several values, several cases, split
   part or too many files.
2. Ask the user which case, or whether to create a new one, and which files. By default every waiting file is
   attached.
3. Call `docsumo_attach_inbox_emails` with `case_id`, or `new_case: true` (and `new_case_name` for a single email).
   Pass `doc_ids` to attach only some files; this works for a single email only. The case must belong to the same
   case type.
4. The attach is queued. Read the email again until `running_action` is empty, then check `action_failed` and each
   file's state.
5. Read the case back with `docsumo_list_case_documents` and `docsumo_get_case_overview`. The attached files become
   the case's documents. Check the case's workflow runs before saying it is processed
   ([product workflows](../../product-workflows/SKILL.md)).

For many emails, pass up to 100 `email_ids` with one `case_id` or `new_case: true` (one new case per email). The
answer has one result per email (`ok`, `error_code`); one failing does not stop the others. Report which failed and
why. Test emails cannot be attached (INBOX_TEST_EMAIL_READ_ONLY).

## Run again: Retry, Re-check, Import email body

| Action | Use when | Note |
|---|---|---|
| `retry` (Retry) | The email is **Failed** | Processes it again from the start. Refused otherwise (INBOX_NOT_FAILED). The only action a test email takes |
| `recheck` (Re-check) | Files wait for review and the settings changed, or a case now exists for them | Runs the current automation again on the waiting files. **It can attach files or create cases**, so tell the user first |
| `import_body` (Import email body) | The email's body holds the document | Imports the body as a document of the email. For every future email, use the Import email body setting instead |

All three are queued: poll `docsumo_get_inbox_email` until `running_action` is empty. Only one action runs on an
email at a time.

## Status by hand: relabel, archive, restore

`docsumo_set_inbox_email_status` moves an email between tabs and **attaches nothing**. To file it, attach it.

- `need_review`, `attached` and `new_case` relabel it. Moving an email back to `need_review` re-checks its waiting
  files against the current settings.
- `archived` archives it (test emails included).
- `unarchived` restores it to the status it had before archiving. An email that the clean-up rules archived goes to
  Need review and is re-checked.
- Setting the status it already has changes nothing. A processing email cannot change status
  (INBOX_EMAIL_PROCESSING).

## Error codes

| Code | Tell the user |
|---|---|
| INBOX_EMAIL_NOT_FOUND / INBOX_FILE_NOT_FOUND | The email or file is not in this account's Inbox. Re-list to get current ids |
| INBOX_FILE_DELETED | The file was deleted, or its case was deleted with it |
| INBOX_TEST_EMAIL_READ_ONLY | Test emails can only be archived, restored or retried |
| INBOX_EMAIL_PROCESSING | The email is still being processed. Wait, then try again |
| INBOX_NOT_ARCHIVED | Only an archived email can be restored |
| INBOX_NOT_FAILED | Retry is only for failed emails. Use Re-check for waiting files |
| INBOX_FILES_NOT_IN_REVIEW | None of the chosen files is waiting for review; they were attached or ignored already |
| CASE_NOT_FOUND | The case does not exist, or belongs to another case type |
| INBOX_UPLOAD_SERVICE_ERROR / INBOX_UPLOAD_SERVICE_UNAVAILABLE | Docsumo's side failed or did not answer. Try once more later, then report it |
