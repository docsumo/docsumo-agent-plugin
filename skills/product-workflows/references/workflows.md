# Build, test and diagnose workflows

## Choose the right workflow

Workflows are executable block graphs, not only post-extraction actions. Navigate to Workflows (`/workflows`), use
All / Case / Independent type tabs, open the editor, and inspect Runs (`/workflows/runs`). Blank drafts can be untyped.
A case workflow owns a case type; an independent workflow does not. An independent run may still reference existing
cases or carry the case that caused a case event. Missing `case_id` is not by itself a failed run.

| Trigger | Product behavior |
|---|---|
| Manual | Starts an independent run without requiring a file or a new case. |
| Schedule | Starts independent runs on a configured UTC cron schedule once published; inspect next run and overlap behavior. |
| Case event | Watches selected target stages for a case type; remains independent and uses the triggering case as context. |
| Upload | Combines email, API and file sources. “Upload as case type” creates cases; “nothing” processes inputs independently without persisting a case. For a case workflow, emails to the Email block's address arrive in the case type's [Inbox](../../product-inbox/SKILL.md), whose settings decide whether they make cases. |
| API | Starts an independent run from an HTTP call carrying a JSON payload and/or files. |
| Document event | Starts an independent run when a document of a chosen type changes status, is uploaded, assigned or deleted. |

Independent workflows disable Documents/Preview rather than requiring an editor case. Run history identifies each
execution; case workflows' test lists can group by case. Do not deduplicate independent rows by a null case ID.
Draft edits do not change the published graph. Published workflow type and trigger restrictions matter when changing
an existing workflow: inspect saved/published state before suggesting conversion.

## Supported operations

Read live schemas before use. A tool being listed does not prove every new block type is accepted.

| Need | Callable tools / boundary |
|---|---|
| Inspect | `docsumo_list_workflows`, `docsumo_get_workflow` (`include_config` adds the case type it feeds and the email addresses documents can be sent to), `docsumo_list_workflow_blocks` |
| Create/edit draft | `docsumo_create_workflow`, `docsumo_create_workflow_from_template`, `docsumo_edit_workflow_graph` (block and edge edits; `replace_graph` with `expected_revision` replaces the whole draft graph unchecked). `docsumo_get_workflow` omits canvas positions; a block written back without one keeps its saved position. |
| Versions | `docsumo_list_workflow_versions`, `docsumo_get_workflow_version`, `docsumo_duplicate_workflow`, `docsumo_restore_workflow_draft` |
| Tests | `docsumo_run_workflow_test` (the draft on its test cases, or on its own for an independent workflow; real effects wait for `confirm`), `docsumo_run_workflow_trigger` (arms the next `email` or `api` document to run the draft as a test; the user sends that document to the test address from `docsumo_get_workflow(include_config)`); check mode and side effects. New files for a test are uploaded through a link ([uploading files](../../product-documents-review/references/documents-and-review.md#uploading-files-from-your-computer)), or come from the user in the app or by email |
| Independent runs | `docsumo_run_independent_workflow`: the editor's Run for a manual, schedule or case-event workflow; `draft` by default, `case_id` with `casetype_id` for a case-event workflow; answers the `execution_id` |
| Publish | `docsumo_check_workflow_publishable`, then `docsumo_publish_workflow` when the user asked to publish; read the resulting published version |
| Results | `docsumo_list_workflow_executions` (`status` `processing` / `success` / `error`, `mode`, `trigger`), `docsumo_get_workflow_execution_history` (a run's status and per-block traces), `docsumo_wait_for_workflow_runs` (waits on `execution_id`s or case ids until the runs stop; call again while `complete` is false), `docsumo_get_execution_dag`, `docsumo_list_workflow_test_cases` |
| Control | `docsumo_cancel_workflow_execution`, `docsumo_update_workflow_approvals` when applicable to the actual run/case; `docsumo_set_workflow_schedule_enabled` for the list's schedule switch |
| Documents and members (workflows that read or assign documents) | `docsumo_list_account_members` (`include_doc_types` for who may use which type), `docsumo_list_documents` (every folder; `doc_type` for one type), `docsumo_doctype_change_document_user` (owner, admin or moderator for any document; a member only their own) |

`docsumo_run_workflow_trigger` accepts only `email` and `api`. It arms ingestion; the run starts when that document
arrives. For a case workflow, a test email shows up in the case type's Inbox with a Test badge
(`docsumo_list_inbox_emails` with `test: only`): check there whether it arrived and what it made. For a manual, schedule or case-event workflow use `docsumo_run_independent_workflow`: it records a hand run,
so it runs while the schedule is off, is refused while an earlier run is still going, and executes every block's real
effects. If the server does not offer it, give the editor/list Run steps and say the tool is unavailable. Wait for a
run with `docsumo_wait_for_workflow_runs` rather than restarting a run that is still going.
Do not invent enum values or use a file-upload tool to simulate a manual run.

## Test a workflow that changes live data

Every test run executes the graph's real effects. When the workflow changes records people work with (documents and
who holds them, cases, table rows):

1. Prove the logic without effects first: a dry-run switch makes the code report what it would change instead of
   changing it, such as an Environment Secret whose test value turns it on (test runs read test values), or a flag
   removed before the final test.
2. Then make live test runs only on records the user named or allowed, with their state read before.
3. Put back what the tests changed with the tools (document holders, table rows, rows the runs themselves wrote)
   and read it back; leave it to the user only when no tool can.
4. Keep the code safe to run again ([workflow code](block-behavior.md#calling-docsumo-from-workflow-code)),
   and report what the live runs changed and what was restored.

## Design for the input size

Before wiring, size the input: pages per file, files per case, rows each document produces, and which blocks run
after extraction. Use the native block for each platform job: Split for a file holding several documents (with AI,
which also classifies the parts) or, where the file is one long document past the extraction page limit, Split by
fixed pages purely to chunk it; Table Write for one record per run; a python_code block with the table row import for
many records. Propose any custom-code replacement for a native block to the user before building it. Limits are in
[block behavior](block-behavior.md). Test on the smallest representative files first, estimate page credits as
pages × runs and ask the user before each round, and have very large files uploaded one at a time.

## Setup or fix procedure

1. Read type, trigger, saved graph and block catalog. Identify expected inputs/outputs, intended run mode and side effects.
2. Keep unrelated blocks/edges and save the smallest draft edit that does what was asked. Read it back. If the user
   has the workflow editor open, ask them to reload it before they click Run or Save there, so the editor works on the
   latest draft, and read the draft again after any action in the app.
3. Run the appropriate supported test; if unavailable, keep the tested/untested distinction explicit and provide UI steps.
   Rerun a test case in full before rerunning from a block, and never from a block while other test cases run
   ([reruns](block-behavior.md#reruns)).
4. Inspect completion, block errors/output and expected downstream result. An accepted run is not a completed run.
5. For requested publishing, check publishability after the final edit, publish, and read the frozen version. The
   check compares every block's config, edge and order with the last full run; a partial `docsumo_rerun_case` with
   `block_id` does not satisfy it. Do not publish an untested changed graph or force a case upload for a workflow that
   has no case.

For a schedule that does not fire, inspect published trigger, enabled state, cron/minimum interval, next run, overlap
policy, production versus test workspace, and execution history. Schedules fire in the production workspace only, and
missed runs are skipped rather than made up later. The enable switch (`docsumo_set_workflow_schedule_enabled`)
controls unattended scheduling; disabling it does not unpublish or prevent a manual run, and turning it back on
schedules the next run from now rather than making up missed ones. Do not promise delivery at an exact wall-clock
second.
