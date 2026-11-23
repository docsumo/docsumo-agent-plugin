---
name: product-inbox
description: Explain and operate a Docsumo case type's email Inbox in product terms, covering emails sent to a case type's address, the Need review, New cases, Attached, Failed and Archived tabs, why an email failed or was not attached, attaching an email's files to a case or a new case, retry, re-check and import body, archiving and restoring, allowed senders and clean-up rules, matching emails to cases by keys found with regex or an LLM, auto split, the test address, and trying settings on a stored email before saving them. A document type's own upload email belongs to documents and review. Attaching, retrying or re-checking emails can spend Docsumo credits: always ask the user first.
---

# Case type Inbox

Every email sent to a case type's address lands in its Inbox (case type sidebar: Cases, **Inbox**, Configure). There
it becomes a new case, gets matched to an existing case for a person to attach, or waits for review. Before working in
an account, confirm which account is connected ([connection setup](../connection-setup/SKILL.md)). Then find the case
type with `docsumo_list_casetypes` and read each tool's live schema before its first call.

- Listing, searching and triaging emails, why one failed or was not attached, attaching, retrying, re-checking,
  archiving: [emails and actions](references/inbox-emails.md).
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
- Test emails (sent to the test address) are read-only. They can be archived, restored or retried, but not attached
  or relabelled.
- An accepted action is not a finished one. Read the email again until `running_action` is empty, then check
  `action_failed`.

## Explain results

Use the screen's labels from the [label table](references/inbox-emails.md#tool-values-and-screen-labels): tab names,
status chips and setting names, never enum values, IDs or raw JSON. Say who sent the email, its subject, when it
arrived, what happened to each file and which case it went to or fits. Keep counts, sizes and dates exact. If a
reason's meaning cannot be confirmed, say so; do not guess.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
