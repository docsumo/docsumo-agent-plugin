# Mark patterns

These are possible causes and fixes, not automatic changes. Confirm the cause from the page image, the saved
settings and the actual result.

## Checkbox and signature

Cause. Checkbox and Signature fields are read from the page images: every mark on the page is found and matched to
the nearest printed label by the **field name** (or the label named in its prompt). A String field asking "is it
checked" reads the OCR text instead, which usually cannot see the mark at all.

Fix order. Field type Checkbox or Signature; a field name equal to the printed label, or a prompt naming the printed
label and its location ("the 'Married' box under Marital Status"); image quality 300 DPI for faint marks; describe the
location when several boxes share a label. Checkbox and Signature fields read the page image whatever the Extraction
Mode; check other fields separately.

Verify. True on a marked document and False on an unmarked one, twice each.
