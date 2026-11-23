# Table patterns

These are possible causes and fixes, not automatic changes. Confirm the cause from the OCR text, the page, the saved
settings and the actual result. Read only the matching pattern. Prompt guidance is in
[writing prompts](../../extraction-fields/references/writing-prompts.md); changes to fields follow
[editing fields](../../product-doctype-setup/references/editing-fields.md).

## 1. Table rows missing

Cause. Table extraction leaves out total/summary rows, folds wrapped sub-lines into the row above, and leaves a cell
empty when unsure. Rows disappear when: they look like totals; the page is dense and too many rows are asked for in
one call; continuation-page header rows are skipped together with the row beneath; or the table starts on a page its
batch did not include. On long or dense documents the loss can vary between runs: two runs at identical settings
return different rows, or a whole table comes back empty.

Diagnose. OCR text: count the rows on the page. Settings: Table Batch Size, Overlap, Table Page Selection, the table
prompt.

Fix order.
1. If identical runs differ or the table returns empty: turn Overlap on and Reasoning Effort to High (Configure >
   Extraction) before prompt work.
2. Table prompt: define a row ("every line with a quantity and an amount is a row; include zero-amount rows; exclude
   only the final Total/Subtotal/Tax lines").
3. Reduce Table Batch Size if multi-page output is cut short; one dense page can still be too much for one call.
4. Overlap on when rows straddle page breaks.

Verify. Row count equals the printed count on two documents; no duplicate rows (overlap can repeat a row). When
results vary, process the same configuration twice and compare.

## 2. Table rows merged or split

Cause. Folding wrapped lines into the row above is right for multi-line descriptions and wrong when each line is an
item without its own header cues. Splitting is the mirror image: continuation lines become rows with empty quantity
or amount.

Fix. Table prompt with a row anchor rule ("a row has exactly one amount; description lines without an amount belong to
the row above", or "each line with a quantity is a separate row even if descriptions repeat").

Verify. No rows with an empty amount when splitting was the issue; per-row amounts match when merging was.

## 3. Wrong column mapping

Cause. Printed headers are mapped to your column names by meaning. Two similar numeric columns (Unit Price / Amount,
Qty / Units), two-line or merged headers, and headers that differ per vendor cause swaps.

Fix order.
1. Column prompt naming the printed header words and the exclusion ("the line total under 'Amount' or 'Ext. Price';
   not the unit price").
2. Column type (Number for amounts) so the type reinforces the mapping.
3. Extraction Mode Image when the alignment is visual (merged or two-line headers).
4. Table prompt describing the column order as printed when it is stable.

Verify. Five rows × all columns on two layouts.

## 4. Multi-page tables

Cause. Tables are extracted per batch of pages and joined; a row split by the page break is half-seen twice; repeated
headers on continuation pages can become data rows; "balance brought forward" or per-page subtotals look like rows.

Fix order. Overlap on; table prompt ("skip repeated header rows on continuation pages; skip 'brought forward' and
per-page subtotal lines"); a Table Batch Size covering the table if it is short; Table Page Selection with a clear
document description for long documents.

Verify. Continuous row sequence across the break; column sums match the printed total.

## 5. Rows built from column headers

Cause. In transposed grids (visit or period schedules, tiered rate cards) each row's label is a column header that may
stack several lines (code, day, week, translation) under banners spanning several columns (cycle, arm, period).
Unguided, extraction joins everything, inserts a banner mid-label or keeps one line, so labels differ from the
expected text across layouts.

Fix. The label column's prompt states the layout rule: from a row list take the label cell only and move day/week/
window values to a description column; from grid columns join that column's own header lines in order, leaving out
multi-column banners and tolerance lines. State whether bilingual headers keep one language.

Verify. Labels on one row-list and one grid document.

## 6. Placeholder text and rows without amounts

Cause. For an empty numeric cell, extraction may write the literal "None", "N/A" or "-" instead of leaving it empty.
It can also emit header or schedule lines (visit-column headers, tick-only assessment rows) as rows with no amount.

Fix. Numeric column prompts: "leave the cell empty; never write None, N/A, null or a dash". Table prompt: "every row
carries a printed amount; skip lines with no price".

Verify. Search the export for literal placeholder strings; count rows with an empty amount.
