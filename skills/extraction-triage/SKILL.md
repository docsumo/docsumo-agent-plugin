---
name: extraction-triage
description: Start here for any reported Docsumo extraction problem, such as a field or table value that is wrong, missing or inconsistent between documents or runs. Checks the document's continuous-learning references first when learning is enabled, then uses the document, its OCR text, the settings and the output to choose the next skill. Retrying documents to confirm a fix spends Docsumo credits: always ask the user first, even when they asked for a re-run.
---

# Extraction triage

Confirm which account is connected first ([connection setup](../connection-setup/SKILL.md)).
State the failing document/field, actual value, exact expected value and where it is printed before forming a
hypothesis. Read the doctype's continuous-learning setting. When enabled, make the
[reference-document check](references/continuous-learning.md) the first diagnostic step, before other diagnosis or
prompt tuning. Then read the OCR text (`docsumo_download_document` with `format="ocr_text"`), look at the original
page where relevant, read the saved fields and settings, and note when the document was processed relative to any
settings change.

| Evidence | Next step |
|---|---|
| Document type is a US Bank Statement type (prompts, batching and mode settings do not apply) | [US bank statement doctypes](../product-doctype-setup/references/doctype-setup.md#us-bank-statement-doctypes) |
| Missing/wrong/truncated field, wrong party, dropdown, date | [Field diagnosis](../extraction-fields/SKILL.md) |
| Missing/merged rows, shifted columns, multipage table | [Table diagnosis](../extraction-tables/SKILL.md) |
| OCR quality, handwriting, checkbox, signature, image input | [Visual diagnosis](../extraction-visual/SKILL.md) |
| Field absent from the document type, or a setting did not save | [Editing fields](../product-doctype-setup/references/editing-fields.md) |
| Values correct but Review/STP/formatting wrong | [Doctype setup](../product-doctype-setup/SKILL.md): STP, mandatory fields, validation, field type |
| Documents erroring, or a result that differs between runs | [Failure patterns](references/patterns.md) |

Compare the original page, the OCR text and the extracted result to find where the value first goes wrong.
A value absent from the OCR text limits Text mode; Image or File mode may still see it. If the value is not on the
page at all, a prompt cannot supply it. When the cause stays unclear, choose the next reading that tells the
possibilities apart, say what is uncertain, and, if needed, give the user a minimal example to send to Docsumo
support. Do not force-fit a known fix.

Prefer the smallest change the evidence supports, not a fixed ladder of increasingly expensive settings. Change one
thing at a time, save, read it back, and retry a small set of affected documents plus a document that was already
correct, to confirm the fix and catch regressions. Retries spend Docsumo credits: tell the user it spends Docsumo
credits and ask them to proceed first, even if they asked for a re-run.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
