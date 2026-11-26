# Block behavior, large inputs and reruns

Use the numbers here for sizing, and confirm a limit that shapes the design with one small run.

## Every block

A block step that runs too long is retried before it fails, so a stuck block can hold a run for a while. Cancelling a run stops the workflow, not work already started: extraction jobs finish, write their results and
use page credits. Cancel once and let them finish; do not cancel and restart large runs repeatedly.

Blocks after extraction take longer as the run's total pages and rows grow, whatever the block itself reads. When a
block after extraction times out on a very large case, test with a trivial block first; if that also times out, the
case is too large: split the input or contact Docsumo support with the page and row counts and run IDs.

## References between blocks

Block configs and prompts read earlier output as `<@path#doctype>`. `.3` or `[3]` index a list; `[i]` means each
item. Pitfalls that fail silently:

- `#doctype` filters only a list of items that carry `doc_type`; applied to the usual top-level data it changes
  nothing. `#invoice` also keeps items with no type.
- In text, a list becomes its items joined with ", " and an unresolved reference becomes "" — no error. Case Update
  values take the first element instead.
- Output keys differ by block: code and widget blocks under `output`, an LLM block `output.response`, AI categorizer
  `output.tags` (`[]` when its answer could not be read), Table Lookup `Matched rows.<Column>`, a case lookup
  `matched_cases`.
- python_code, widget, view and export blocks see upstream blocks by name only, so renaming a block breaks their code.

## Blocks with no input

A block whose input has no documents is skipped and marked `skipped`, and the run still completes: after every
document erred upstream, the rest of the graph does nothing. A conditional edge forwards only the documents routed to
its branch. Manual, schedule and case-event runs, and payload-only API runs, have no documents by design and do not
skip, so router and lookup branches may all run. Confirm with one run before relying on it either way.

## Split

The Split block reads up to the first 300 pages of each file. Very large files can be slow to split or time out:
upload them one at a time, check the split step's status before waiting on extraction, and contact Docsumo support
about a file that keeps timing out, with its page count and run ID. A fixed-page or text-pattern split names each part
`<parent name>_<start>_<end><ext>`, gives it no document type until the extractor assigns one, and replaces the parent.
AI split parts carry their classified document type. Code after extraction should take the case's documents rather
than filter on the split's document type, and restore page order from the title range.

## Data Extraction

Extraction reads at most 300 pages of a document. Documents are extracted in batches, and each batch finishes before
the next starts, so one slow part delays its batch. Chunk a single document longer than 300 pages with the Split block
on fixed pages — the one case a fixed split is the right tool, since there are no document boundaries to find. A file
holding several documents is split with AI.

## Python code blocks

- The entry point is `execute(data)` and its return value must be JSON-serializable. Judge a run by the block's
  output and its `std_err` log, not only its status: an error in the code shows as output `None` with the traceback in
  `std_err`, and output `{"error": ...}` means the run itself failed or timed out.
- Limits per call: about 5 minutes including package install, and about 512 MB of memory. HTTPS requests are allowed;
  plain HTTP is blocked.
- Packages come from the imports in the saved code. Only these install: numpy, pandas, scipy, scikit-learn,
  matplotlib, requests, python-dateutil, pytz, regex, openpyxl, xlsxwriter, xlrd, beautifulsoup4, lxml, pillow,
  pydantic, rapidfuzz, torch, pymupdf, boto3. Any other import returns a dependency error without running.
- `data` holds `documents` (metadata plus `extracted_data` and `ocr_text`), `case`, and one key per upstream block by
  block name (code and widget blocks as `{"output": ...}`); a manual or scheduled run has no documents and no case.
  python_code, validation and export blocks, and external API calls, also receive `secrets`: the account's Environment
  Secrets (Settings > Secrets, owner or admin) as `secrets.<NAME>`, a test run getting a secret's test value when it
  has one, and `secrets.account.DOCSUMO_API_KEY`, the API key of whoever started the run, or None when that user has
  none. Code reads keys from there: never write a key into code or ask the user to paste one, and never print or
  return it.

## Widget, View and validation code

Widget blocks (summary cards, summary text, charts, tables, validation tables), the View and validation blocks run
code too, and the case screen draws only the value their type expects: code that runs without an error can still show
"No data found". Before writing one, read `docsumo_get_block_schema` for its type: `code_output` gives the value
`execute` must return (`returns`), an `example`, the `rules` and, for most, `helpers` to paste into the code.

- A chart gives each bar or line series its own `color` ('#RRGGBB') and a pie one color per label in `colors`. Set
  the block's chart type setting to the chart's type: while it is unset, the block's settings show Pie.
- After a run, `output_problems` on a block (run history, waiting for runs, test outcomes) means the screen cannot
  draw it (errors) or draws it incomplete (warnings). Fix them and run again before calling the work done;
  `docsumo_get_case_view` reports `renders: false` with the problems for a case's view.
- Where the plan says nothing about a missing or unreadable value, it is data, not an error: leave it blank and let
  the check it feeds need review, naming the value (a Warning on a validation table, neither a Pass nor a Fail). Never
  count it as 0 or another default: a blank tax is not a zero tax. One document's gap then never stops the block for
  the others.

## Calling Docsumo from workflow code

When no block does the job (reading or reassigning documents, reading members, writing many table rows), a
python_code block can call Docsumo's public API. This is for code that runs inside the user's workflow; the agent
itself uses the MCP tools. Use the routes in the API Reference at support.docsumo.com
([documentation lookup](../../product-navigation/references/support-docs.md)), the base address `api_base_url` from
`docsumo_get_account_user`, and `secrets.account.DOCSUMO_API_KEY` in the `apikey` header, with an explicit
`User-Agent` header. The key acts with its user's role.

Code that changes records must be safe to run again: pick what to change from the current state on every run (only
documents still held by someone, rows not yet written), so a second run changes nothing more. A table import appends,
so for a write that survives reruns, delete the rows written earlier for the same key before importing again.

## Reruns

A case reruns the draft when it is a test case and the published version otherwise; the case's test flag decides, not
a mode parameter. Rerunning from a block continues from the workflow's latest test run, so rerun a test case in full
first, and do not rerun from a block while another test case of the workflow is running.
