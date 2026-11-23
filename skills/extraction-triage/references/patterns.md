# Failure patterns

These are possible causes and fixes, not automatic changes. Confirm the cause from the OCR text, the page, the
saved settings and the actual processing result. Field and table patterns are in
[field patterns](../../extraction-fields/references/patterns.md) and
[table patterns](../../extraction-tables/references/patterns.md).

## Documents erroring

Causes. A double colon (`::`) in a prompt; an invalid value in Configure > Additional Parameters; a field setup that
breaks the block chain rules; a file too large to process; custom post-processing code that fails. Very long
documents do not error: pages past the processing limit are not read.

Diagnose. `docsumo_list_documents` (`status=["erred"]`) or `docsumo_doctype_wait_for_documents` give the
`err_message`. Check every prompt for `::` and any unusual Additional Parameters; check whether one document or all
fail; check whether the Post-processing tab holds custom code (do not edit it). No tool runs the setup on one
document as a test: to see which field step fails, save a candidate fix, then retry the failing document and read its
error or values.

Fix order. Remove the `::`; revert the Additional Parameters change; repair the block chain
([editing fields](../../product-doctype-setup/references/editing-fields.md#blocks)). Failures in custom
post-processing code go to Docsumo support.

Verify. Retry one document and check that it extracts again and reaches the expected Review or Processed state; then a
document that was already correct.

## The reported document fails but a retry does not (or the other way round)

When continuous learning is enabled, first do the [reference-document check](continuous-learning.md): references can
differ between runs as new documents are approved.

Other causes: a setting or prompt changed between runs (check the activity log for who changed what and when); an
older trained-model document type; account-level defaults such as STP or confidence thresholds. Compare the current
fields and Configure values with what the user expected, field by field, and check
`docsumo_review_get_references` for the references each run used. Missing evidence is a stated gap, not a cause.
