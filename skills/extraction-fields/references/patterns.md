# Field patterns

These are possible causes and fixes, not automatic changes. Confirm the cause from the OCR text, the page, the saved
settings and the actual result. Read only the matching pattern. Pattern numbers in "Fix order" refer to
[prompt patterns](writing-prompts.md#prompt-patterns). Changes to fields follow
[editing fields](../../product-doctype-setup/references/editing-fields.md).

## 1. Field empty

Cause. Extraction returns an empty value when nothing in the pages it was given matches the field name and prompt.
With page batching, an empty answer from one batch of pages can win over a real value in another.

Diagnose. OCR text first: is the value there? Then the field: prompt, type, multi-value setting. Then the result:
confidence and position. Compare a document where the field works.

Fix order.
1. Prompt: add the printed label words and relative location (pattern 2); add the entity definition if the name is
   generic (pattern 1).
2. If the value is in the OCR text but far from its label (label on one line, value three lines down in a column
   layout), add the layout cue ("the value appears below the label, not beside it").
3. Not in the OCR text: raise image quality to 300 DPI (Configure > Pre-processing); if the PDF is digital and text
   looks missing or garbled, set OCR on digital PDFs to complete OCR (check the live option labels first); if the
   page is rotated, turn on orientation correction.
4. The value is visual (a stamp, handwriting): Extraction Mode Image or File (Configure > Extraction).
5. Long document: make sure the Batching Configuration covers the pages that hold the value.

Don't. Add "return empty if not found"; rename the field to something the user did not ask for.

## 2. Partial value: missing cents or decimals

Cause. Numbers are kept as printed and the field type parses the separators. Cents go missing when (a) the OCR splits
`1,234` and `.56` onto different lines or columns, (b) the document uses `1.234,56` and the parser reads `,56` as a
thousands group, (c) a value pieced together from parts is rounded, or (d) a cleaning block truncates.

Diagnose. OCR text: is `.56` next to `1,234`? Field: type Number, any cleaning block, any format clause. Try two
documents with different separators.

Fix order.
1. Prompt format clause: "Output the full amount with a period as decimal separator, e.g. 1234.56; the document may
   print 1.234,56." Check the field's decimal separator setting.
2. A cleaning block only if the field type cannot handle the format.

Verify. Exact comparison on three documents including one with `,00`.

## 3. Partial value: first word only, two-word city, truncated address

Cause. Extraction returns one value and collapses whitespace. It can stop early when a line break or comma looks like
the end of the value ("New" from "New\nYork"), or when the prompt implies a single word ("city name").

Diagnose. OCR text: line breaks inside the value.

Fix order.
1. Prompt: "The city may be more than one word (New York, Salt Lake City); return the complete name." For addresses use
   the composite pattern (pattern 8) with all lines included.
2. Extraction Mode Image when the layout (columns, boxes) splits the value in the OCR text.

Verify. Full value on the failing document and unchanged value on a single-word case.

## 4. Wrong value: repeated instances

Cause. A single-value field returns one value; with several candidates it picks the most relevant, often the first in
reading order. Page batching makes it worse: each batch of pages answers separately and an earlier page's candidate
can win. Continuous learning can also teach the wrong instance if an approved reference document had it.

Diagnose. Count occurrences in the OCR text. Check: the prompt has no rule for which one; Fields Batch Size; learning
on and the wrong value matches a reference document ([reference check](../../extraction-triage/references/continuous-learning.md)).

Fix order.
1. Prompt disambiguation (pattern 3) plus a selector rule ("the amount on the line labeled 'Total Due', not 'Subtotal'
   or 'Amount Paid'"; "the most recent date").
2. Section prompt if the same rule applies to several fields ("all fields here concern the Applicant, never the
   Co-applicant").
3. If every occurrence is wanted: the field's multi-value setting (string, number and date only).
4. A Fields Batch Size that keeps the relevant pages together.
5. If a reference document carries the wrong instance: stop using that reference.

Verify. Correct instance on the failing document and on a document with a single instance.

## 5. Wrong value: from the wrong page

Cause. Pages are read in batches, and each batch is asked for every field; a plausible candidate on page 1 can beat
the real value on page 7.

Fix order. A Fields Batch Size covering the document; prompt cues ("on the final page, in the summary block") help
only when the batch contains that page.

Verify. The result's position points to the expected page.

## 6. Date and number formats

Cause. Dates and numbers are kept as printed; the **field type** then decides parsing: Date reads `03/04/2024` as
3 April, Date (MM/DD) as 4 March. Several dates near each other (issue, due, delivery) are a disambiguation problem,
not a format one. Parentheses, trailing minus, percent and currency codes are parsed; unusual formats need a cleaning
block.

Fix order. Field type first (Date (MM/DD) for US sources). Then a disambiguation clause. Then an explicit output
format clause ("Output as YYYY-MM-DD"). Cleaning block last.

Verify. Compare parsed values only if normalization is what the user needs; otherwise use exact strings; include a day
above 12 and a day of 12 or below.

## 7. Dropdown mismatch

Cause. Extraction returns text, which is then matched to an option. Wording absent from the list yields a guess or an
empty value. Options are compared as text, so `NET30` and `Net 30` differ.

Diagnose. Read the options (the dropdown block's `config.options` in `docsumo_get_doctype_schema_and_fields`, or the
Database Table behind a table-backed dropdown) and the document's wording.

Fix order. Add the missing option or fix its spelling (resend the field's whole block list) or in its source Database
Table; add mapping clauses in the prompt ("'payable within 30 days' → Net 30"). If the set of values is open-ended, the
field should be String, not Dropdown.

Verify. Returned value equals an option exactly on three documents.

## 8. Values from the wrong section or party

Cause. The same label ("Address", "Name") printed for Bill To and Ship To is a coin toss without context. Section
names and section prompts give shared party context, and duplicate field names across sections are prefixed with the
section name, which helps only if section names are meaningful.

Fix order. Section prompt ("every field in this section is the Buyer's; the Seller appears under 'From'"); a
per-field exclusion clause; improve section names only with the user's agreement (renaming changes extraction and
`<@…>` references).

Verify. One document containing both parties: both sets correct.
