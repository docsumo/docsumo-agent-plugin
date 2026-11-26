---
name: product-inbox
description: Explain and operate Docsumo's email Inboxes in product terms - a document type's Inbox (Invoice, Bank Statement, an AI Auto-Classifier...), All Inbox, and a case type's Inbox. Covers which emails need review, where an email's files went, why one was rejected or failed, archiving, restoring and retrying emails, and, for a case type, emails sent to its address, the Need review, New cases, Attached, Failed and Archived tabs, why an email failed or was not attached, attaching an email's files to a case or a new case, retry, re-check and import body, allowed senders and clean-up rules, matching emails to cases by keys found with regex or an LLM, auto split, the test address, and trying settings on a stored email before saving them. Attaching, retrying or re-checking emails can spend Docsumo credits: always ask the user first.
---

# Email Inbox

Every email sent to a case type's address lands in its Inbox (case type sidebar: Cases, **Inbox**, Configure). There
it becomes a new case, gets matched to an existing case for a person to attach, or waits for review. Every email sent
to a document type's address is one row of that type's **Inbox** tab, with the documents its files became and the
files it rejected. **All Inbox** (main nav) lists case type and document type emails together.
`docsumo_list_inbox_emails` reads all three: `casetype_id` for a case type's Inbox, `doctype_id` for a document type's,
neither for All Inbox. Before working in an account, confirm which account is connected
([connection setup](../connection-setup/SKILL.md)). Then find the case type with `docsumo_list_casetypes`, or the
document type with `docsumo_get_document_types`, and read each tool's live schema before its first call.

- A document type's Inbox and All Inbox: statuses and reasons, where an email's files went, archive, restore and
  retry: [document type Inbox](references/doctype-inbox.md).
- A case type's emails: listing, searching and triaging, why one failed or was not attached, attaching, retrying,
  re-checking, archiving: [emails and actions](references/inbox-emails.md).
- How emails become cases (clean-up, automation mode, keys, matching rules, auto split, when nothing matches),
  changing those settings and trying them first: [Inbox settings](references/inbox-settings.md).
- The case it went to, its stages and its workflow runs: [product workflows](../product-workflows/SKILL.md).
- Wrong extracted values on a document that was attached: [extraction triage](../extraction-triage/SKILL.md).

## Guardrails

- Attaching, retrying and re-checking act on live cases: they add files to a case or create cases, and the case's
  workflow may run on them and spend Docsumo credits. Name the emails and the target case, say that it can spend
  Docsumo credits, and act only on what the user confirmed after that, even if they asked for the action. One email
  failing in a bulk action does not stop the others; report each result and do not loop on failures.
- Never save settings that were not first tried on stored emails with `docsumo_test_inbox_settings`. A save applies
  only to emails that arrive afterwards, and only owners and admins can save.
- A document type's Inbox and All Inbox are for owners and admins only. When the tools refuse the user
  (UNAUTHORIZED), say that only an owner or admin can see those Inboxes; do not retry.
- Retrying a document type email, or changing a file's document type, extracts again and spends Docsumo credits:
  name the files, say so, and act only after the user confirms.
- Test emails (sent to a case type's test address) are read-only. They can be archived, restored or retried, but
  not attached or relabelled.
- An accepted action is not a finished one. Read the email again until `running_action` is empty, then check
  `action_failed`.

## Explain results

Use the screen's labels from the [label table](references/inbox-emails.md#tool-values-and-screen-labels): tab names,
status chips and setting names, never enum values, IDs or raw JSON. Say who sent the email, its subject, when it
arrived, what happened to each file and which case or document type it went to or fits, a document's status in the
product's words (still processing, in Review, Processed, Failed:
[document type Inbox](references/doctype-inbox.md#where-an-emails-files-went)). Keep counts, sizes and dates exact.
If a reason's meaning cannot be confirmed, say so; do not guess.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
