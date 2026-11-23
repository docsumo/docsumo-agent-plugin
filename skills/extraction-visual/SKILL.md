---
name: extraction-visual
description: Diagnose Docsumo extraction failures caused by the page image or OCR, such as poor scans, handwriting, checkboxes, signatures, text the OCR missed, and the Text, Image or File extraction mode in use, by comparing original pages with OCR and output.
---

# Visual and OCR extraction failures

Start with [extraction triage](../extraction-triage/SKILL.md), including its reference-document check when continuous
learning is enabled. Reuse an existing check for the same document.

Compare the original page (`docsumo_download_document` with `format="original_file"`) with its OCR text
(`format="ocr_text"`) and the Extraction Mode in use. In Text mode, a value missing from the OCR text cannot be
extracted: fix the input (image quality, OCR on digital PDFs, orientation in Configure > Pre-processing) or, with the
user's agreement, switch to Image or File mode before tuning prompts. Image input does not guarantee legibility.
For checkboxes and signatures read [mark patterns](references/patterns.md); test both marked and unmarked examples.

Confirm the field type and the printed label and location. Do not rename fields just to reproduce a failure: names
are part of what extraction reads. Read Configure's live option labels rather than remembered values. Change one
thing at a time, save, read it back, and retry the failing document twice plus one with readable text and one with
the mark absent.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
