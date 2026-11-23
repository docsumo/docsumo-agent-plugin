# Writing extraction prompts

A field's prompt is the Extraction block's `config.prompt`, written with `docsumo_field_setup_update_field_settings`
and saved as in [editing fields](../../product-doctype-setup/references/editing-fields.md#build-fields). In the app it
is the field's prompt in Edit Fields.

## How extraction already behaves (do not repeat it in prompts)

Fields:
- Returns exactly **one most relevant value** per single-value field even if many candidates exist. This is why
  repeated values pick "the wrong one" without guidance.
- Returns an empty value when the field is absent — never `N/A` or `null`. Do not add "return empty if not found".
- Keeps zeros (`0`, `0.00`).
- Collapses whitespace to single spaces: multi-line values come back as one line.
- Multi-value fields always return a list; single-value fields never do.
- A dropdown sees its options verbatim.

Tables:
- Extracts every row in order, each cell under its column, with **wrapped sub-lines folded into the same cell**; never
  invents new columns.
- Leaves out rows that total or summarise the whole table.
- Leaves a cell empty when unsure, and keeps numbers as printed (numeric cells can still need a prompt against
  placeholder text: see table patterns).

Checkboxes and signatures are read from the page image: every mark is found, judged marked or unmarked, and matched to
the nearest printed label by the field name.

Asking for a value in a different format than printed (`1,234.00` → `1234.00`) can lose its highlight on the page
and lower its confidence; ask for reformatting only when needed.

## Prompt patterns

Every sentence must add something the document does not already make obvious. Prefer 2–5 lines. Ground labels in
real, common wording, never in one sample's layout.

1. **Entity / role** — define the entity, list synonym labels, name exclusions.
   `The Vendor is the company issuing the invoice and receiving payment. Labels: "Supplier", "From", "Sold By". Not the Bill To / Ship To party. Company name only; no address or tax id.`
2. **Label + relative location** — `Look for "Reference No.", "Ref #", "Document ID". Take the value after the label. If several, use the one nearest the top of the first page.`
3. **Disambiguation** — `This document has amounts for several parties. Extract only the Applicant's monthly income; not the Co-applicant's, which appears under "Co-borrower".`
4. **Format** — `Digits and one decimal point only (1400.00); no currency symbols or thousands separators.` For dates: `Output as YYYY-MM-DD; the document prints dates as MM/DD/YYYY.`
5. **Empty handling** — say nothing (empty is the default). Only for a required, possibly-absent field add one clause:
   `Only extract if clearly stated; if absent leave empty and do not infer from headings or the closest-looking text.`
6. **Yes/No verification** — `Check whether the document carries a "PAID" stamp or handwritten "paid". Respond "Yes" or "No".`
7. **Examples** — `Examples: "Total Due: $1,234.56" → 1234.56; "Grand Total USD 500" → 500.00`
8. **Composite / template** — `Full mailing address as: [Street], [City], [State] [Postal Code], [Country]. Include suite lines; exclude the recipient name.`
9. **Multi-word values** — `The city may be more than one word (e.g. "New York", "Salt Lake City"); return the complete city name, not the first word.`
10. **Checkbox** — name the printed label: `The "I agree to the terms" checkbox at the bottom of page 2.`
11. **Signature** — `Applicant's signature in the "Signature of Applicant" box on the last page.`

Refinement order when a prompt already exists: disambiguate → locate → format → repeated-instance rule →
possibly-absent clause. One change at a time.

## Where each instruction goes

| Level | Reaches | Where | Use for |
|---|---|---|---|
| Document description | The whole document | Configure > General > Description (`docsumo_update_doctype_configuration` `doctype_description`) | What the document is, and how to tell it from look-alikes. One or two lines. |
| Section prompt | Every field in the section | `docsumo_update_doctype_fields` (`section_prompts`) | Shared disambiguation ("everything here is the Buyer"), domain facts ("Net 30 EOM = 30 days after month end"), shared constraints ("amounts exclude VAT"). |
| Field prompt | That field only | The Extraction block's `config.prompt` | Everything specific to the field. |
| Table prompt | Every column of that table | `docsumo_update_doctype_fields` (`table_prompts`) | Row rules: what is a row, skip repeated headers on continuation pages, leave out "brought forward" lines and VAT/summary rows. |
| Column prompt | That column only | The column's Extraction block `config.prompt` | Which printed header maps here, format, exclusions. |

Never restate the document or the field list at a higher level; when in doubt, leave a level empty.

## Repeated instances (the value occurs several times)

Pick one deliberately:
- **Single value + selector rule** when a general rule identifies the right one ("the most recent date", "the amount
  on the totals line", "the first page's").
- **Multi-value setting** when every occurrence is wanted and no companion data is needed.
- **Table** when each occurrence carries two or more related values that must stay together.

With page batching, an earlier page's candidate can also win; keep the relevant pages in one batch.

## Don'ts

- No cross-document references ("must match the bank statement"); extraction sees one document.
- No sample-specific section titles; use labels and relative location.
- No validation or arithmetic in extraction prompts; use validation and calculation blocks.
- No "return empty if not found" boilerplate.
- No invented labels; do not overfit to one sample.
- No repeating the same instruction at several levels.
- Do not paste a whole business rulebook into a field prompt; long prompts dilute the few cues that matter.
- Do not use a double colon (`::`) in a prompt.

## Checklist for each prompt

- [ ] Says what entity, how to disambiguate, and the output format only if the default is wrong.
- [ ] Says where to look only in relative terms.
- [ ] A repeated-instance rule is chosen explicitly when the value can repeat.
- [ ] No `::`.
- [ ] Block chain valid; references resolve; a dropdown has options.
- [ ] One thing changed versus the previous version, and the previous version is noted so it can be restored.
