# Inbox settings: how emails become cases

Open **Inbox settings** with the gear button on the Inbox (owners and admins only; it is hidden for other roles).
Until someone saves, the defaults apply and the drawer says so (`is_saved` false). Read the settings with
`docsumo_get_inbox_settings`. Change them with `docsumo_update_inbox_settings` (owners and admins; others get
UNAUTHORIZED). Try them first with `docsumo_test_inbox_settings`.

## Addresses

- The Inbox address is the same address the case type's workflow Email block shows. It is also the case type's
  `upload_email` (`docsumo_get_case_configuration`), and Configure says "Emails to this address go to the Inbox". It
  is not a second address.
- Addresses are **per person**: each member has their own live and test address (`addresses.live`, `addresses.test`
  are the connected user's). A member who never opened the workflow gets theirs made when they open the Inbox.
- The **live** address accepts mail only once the case type's workflow is published (`workflow.is_published`).
  Before that, the Inbox says "Publish the workflow to receive emails at this address."
- The **test** address makes test cases (the draft workflow's test cases, used by workflow tests). Its emails carry a
  Test badge, and are read-only in the Inbox.
- A file must be at most 500 MB and not password-protected. Only PDF, image, Office and spreadsheet files are
  imported. A Word file is converted to PDF to be read, and some accounts refuse Word files ("Word files aren't
  supported"); then ask the sender for a PDF.
- A **document type's** upload email (Configure > Import & Export) is a different address. Its emails never reach a
  case type's Inbox or these settings: each one is listed in that document type's own Inbox tab, and its files become
  documents of the type ([document type Inbox](doctype-inbox.md)).

## General: clean-up applied to every email

| Screen label | Field | Meaning |
|---|---|---|
| Accept from: Anyone / Only allowed senders | `general.accept_from` `anyone` / `allowed_senders` | With allowed senders, mail from anyone else is not processed (Sender not allowed) |
| Allowed senders | `general.allowed_senders` | Addresses (`intake@example.com`) or whole domains (`@example.com`), up to 200 |
| Archive emails without attachments | `general.archive_no_attachments` | An email with no attachment goes straight to Archived |
| Ignore signature images | `general.ignore_signature_images` | Small images such as logos in signatures are skipped (file state ignored) |
| Import email body | `general.import_body` | Every email's body is imported as a document beside its attachments |

## Automation: what happens after clean-up

**When an email arrives** (`automation.mode`):

| Screen label | Value | Result |
|---|---|---|
| Create a new case for each email | `create_case_per_email` | Every email starts its own case (New cases tab) |
| Match emails to cases | `match` | Finds case details in each email and **suggests** the matching case; a person attaches |
| Send every email to Need review | `off` | Nothing automatic; every email waits for a person |

Matching never attaches by itself, even when exactly one case fits: the file waits with reason "Matched *case*:
check and attach". When a case is not found, **When nothing matches** (`on_no_match`) decides: **Send to Need
review** (`need_review`) or **Create a new case** (`new_case`).

**Find case details** (match mode):

- **Where to look** (`look_in`): Subject and body (`subject_body`), Attachments (`attachments`), or both.
- **Method** (`method`): **Regex** (each key's `pattern`) or **LLM** (an LLM reads the email, guided by the
  **Prompt**, `llm_prompt`, up to 10,000 characters).
- **Keys** (`keys`, up to 20): the values to find, each with a `key_id` (unique; rules refer to it), a `label`, the
  `casefield_id` it corresponds to, and for Regex a `pattern` (up to 500 characters).

**Match to cases** (`rules.groups`): the first block is **If**; the ones after it are **Else if** (up to 10 blocks,
each with 1–10 conditions joined by **and** or **or**). Each condition compares a case field with a key: **is
exactly** (`exact`) or **is approximately** (`similar`, with a `threshold` of 1–100 percent). Blocks run in order.
The first block that finds a case suggests it, and a later block is tried only when the earlier ones find nothing.
When a block finds several cases, a person picks.

**Split files that hold several documents** (`auto_split`, with **How to split**, `split_prompt`, up to 4,000
characters): only with Match emails to cases and the LLM method. It cuts a PDF that holds several cases' papers into
one part per case. The split rules are the only guidance the LLM gets for grouping pages, so they are required.
Every part waits in Need review with its own suggested case, and the original file is never attached.

## Saving changes

- Give only the fields to change; everything else keeps its saved value.
- **Lists and rules are replaced whole.** `allowed_senders`, `keys` and `rules` are saved exactly as sent. To add one
  sender or one key, read the saved list, add to it, and send the full list. Sending only the new item erases the
  rest.
- The save is checked against the case type. Key ids must be unique, a rule must use a defined key and an existing
  case field, match mode needs at least one rule, Regex needs a pattern on every key a rule uses, and auto split with
  LLM needs split rules. A failed check is VALIDATION_ERROR (on save) or INBOX_SETTINGS_INVALID (on a try), naming
  each problem; fix exactly those.
- **A save applies to emails that arrive afterwards.** Emails already in the Inbox are not re-run. To apply new
  settings to waiting emails, re-check the ones the user names ([emails and actions](inbox-emails.md#run-again-retry-re-check-import-email-body)).
  Re-check can attach files or create cases, so name them first.
- Read the settings back after saving, and report `updated_at` and who saved.

## Design or change matching: the procedure

Example request: "match incoming emails to cases by policy number".

1. **Read** `docsumo_get_inbox_settings` and `docsumo_get_casetype_schema` (the case field ids and names). Confirm
   the case field that holds the value, such as Policy number, exists and is filled on the cases. If it is missing,
   that is a case type change ([product workflows](../../product-workflows/references/cases.md)).
2. **Pick stored emails** to test on, two or three that represent the traffic: one that should match a known case,
   one that should not match, and an awkward one (the value only in an attachment, two values, a forwarded thread).
   Use `docsumo_list_inbox_emails`, preferring Need review and Attached emails whose correct case the user knows.
3. **Draft** the change. Keep the keys few and the rules simple:
   - **Regex** for fixed-format ids such as `\b[A-Z]{2}\d{8}\b`. Anchor the pattern to the format, so a phone number
     or date cannot match it. One value per key.
   - **LLM** for free-form values (a customer name, an address), for values in attachments, or for wording that
     varies. Write the prompt like the screen's example: what each key looks like and where it appears, and which
     look-alikes to ignore (the account holder, not a contact or signer).
   - **Exact** for ids. **Approximately** for names, with a threshold around 85–95. A low threshold suggests the
     wrong case.
   - Put the strongest rule in **If** (id equals id), and looser ones in **Else if** (name and date).
4. **Try** the draft on each chosen email with `docsumo_test_inbox_settings`, passing only the fields being changed.
   Nothing is saved and the email is not changed, but the automation really runs. Each try can take up to about a
   minute and a half (INBOX_TEST_TIMEOUT if longer), so run them one at a time. Read `extracted` (the values found),
   `would` and `outcome` (what would happen to the email), and `files[]` (each file's case or reason, and `parts`
   when split). Compare with the case the user expects.
5. **Adjust** and try again until every chosen email behaves as expected. If one cannot be made to behave, tell the
   user what will happen to emails like it.
6. **Propose** the change to the user as before and after, in screen labels (mode, keys, rule blocks, what happens
   when nothing matches), with the try results.
7. **Save** only after the user agrees. Read it back, then offer to re-check the waiting emails they name.

## Limits

| Item | Limit |
|---|---|
| Allowed senders | 200 |
| Keys | 20 |
| Rule blocks / conditions per block | 10 / 10 |
| Regex pattern | 500 characters |
| LLM prompt / split rules | 10,000 / 4,000 characters |
| Files read per email | 100 (more: nothing is read, every file waits) |
| File size | 500 MB |
| Emails per bulk action | 100 |
| Settings try | about 90 seconds |
