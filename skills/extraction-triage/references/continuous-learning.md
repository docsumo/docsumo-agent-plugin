# Check continuous-learning references first

## When

For any reported extraction issue on a document type with continuous learning enabled, do this check before other
diagnosis or prompt tuning. It applies to fields, table cells and checkbox/signature marks. If learning is disabled,
continue ordinary triage. If the setting cannot be confirmed, say so and continue without assuming either state.

Continuous learning uses earlier approved documents of the same type as **reference documents**: examples the
extractor follows for similar layouts. A reference with a wrong reviewed value, or one that only looks similar, can
teach the wrong answer.

## Procedure

1. **Find the references.** Read the setting with `docsumo_configure_get(tab="extraction")` (continuous learning, Template
   Priority, Template Threshold, Number of Templates). Read the failing document's references with
   `docsumo_review_get_references`: best matches were used; potential matches were not. Note the failing document,
   field, actual and exact expected value, and where the value is printed. A confirmed empty reference list is
   different from a list that could not be read.
2. **Check each used reference for similarity.** Compare its original pages with the failing document: layout,
   labels, field location and surrounding context; for tables, headers and row structure; for marks, the label and
   mark region. Record **similar**, **dissimilar** or **uncertain** for each, with what you saw. A matching document
   type, file name or match score alone is not enough.
3. **For similar references, compare the field.** Find the reference's own printed value and its reviewed value
   (`docsumo_get_document_data`). A reviewed value that is wrong, or that follows a different rule than the failing
   document needs, is a likely cause — but still a hypothesis until a retry confirms it.
4. **Decide the next step.** Dissimilar references point at reference selection, not prompts. For mixed references,
   assess each separately. If references are suitable and consistent, continue with field, table or visual diagnosis.
   If the document used no references, say so and continue ordinary triage.

## Fixes

This check is diagnostic. Do not automatically exclude references, disable learning or rewrite prompts. Supported
changes, made only when the user agrees:

- Stop using one confirmed-bad reference with `docsumo_review_set_reference_eligibility` (`doc_id` of the reference
  document, `use_as_reference: false`; the Reference documents panel in Review does the same).
- Set Template Priority to **Human Approved Only** so only documents a person approved become references.

Do not change approved documents' values to fix a reference. Then retry the failing document and one that was already correct, and compare.

## Example

A failing invoice prints buyer tax ID `BUY-204` but returns seller tax ID `SELL-901`. A similarly laid-out reference
prints buyer ID `BUY-108`, but its approved value is the seller's `SELL-802`. The reference is teaching the seller's
ID: stop using that reference, then retry the failing invoice.
