---
name: extraction-fields
description: Diagnose wrong, missing, partial or misplaced extracted field values in Docsumo, such as the wrong party's name or tax ID, dates, amounts, ZIP codes losing leading zeros, or dropdown values that do not match, and write better field prompts, after extraction-triage has checked the inputs and continuous-learning references.
---

# Field extraction failures

Start with [extraction triage](../extraction-triage/SKILL.md), including its reference-document check when continuous
learning is enabled. Reuse an existing check for the same document.

Read the matching [field pattern](references/patterns.md) and, when the wording of a prompt is involved,
[writing prompts](references/writing-prompts.md). Tell apart a value that is not on the page, a wrong choice between
similar values, a value from the wrong page, a formatting issue from the field type, and a value calculated from other
fields. Read the OCR text before changing a prompt. For upload metadata or calculated values use
[editing fields](../product-doctype-setup/references/editing-fields.md#code-blocks-need-code); do not ask extraction to
invent an unprinted value.

Use exact expected values, including leading zeros and dropdown spelling. Compare dates and numbers as normalized
values only when that is what the user needs; otherwise compare strings exactly. Check the same field on another
layout too, and both ambiguous and unambiguous dates where relevant. Change one thing at a time, save, read it back,
and retry the failing document and one that was already correct. Retries spend Docsumo credits: tell the user it
spends Docsumo credits and ask them to proceed first, even if they asked for a re-run.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
