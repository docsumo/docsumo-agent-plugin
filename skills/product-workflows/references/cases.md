# Cases, sharing and artifacts

A case bundles documents and metadata under a case type with stages, fields and a checklist. Case stage and workflow
execution status are separate. Use case overview, documents, views and linked records to locate the user's issue.
An extracted-value error on a case document still goes to its doctype's
[extraction diagnosis](../../extraction-triage/SKILL.md).

A case type works on its own copies of document types: attaching a type that already exists in the account with
`docsumo_create_casetype` or `docsumo_update_casetype` adds "<title> Copy", fields included. Its
workflow and any field change made for the case type use the copy, so other workflows using the original are
unaffected; do not point the case type back at the original.

Read with `docsumo_list_casetypes`, `docsumo_list_cases`, `docsumo_get_case_overview`, `docsumo_list_case_documents`,
`docsumo_get_case_configuration`, `docsumo_get_case_view`, and `docsumo_get_case_linked_records` (the entity records a
case is about). `docsumo_get_case_validations` runs the saved validation code rather than reading a stored result;
a case type without validation code answers an empty list with a `note`. For requested changes, use current
schemas for `docsumo_create_case` (`workflow_version` `published`, or `draft` for an editor test case),
`docsumo_update_case`, `docsumo_update_case_configuration`, `docsumo_rerun_case`, `docsumo_link_case_record` /
`docsumo_unlink_case_record`, or `docsumo_update_workflow_approvals`. Case fields are read with
`docsumo_get_case_configuration` and changed with `docsumo_update_casetype` (`case_fields` add/update/delete; owners
and admins only). Documents go into a case through an upload link
([uploading files](../../product-documents-review/references/documents-and-review.md#uploading-files-from-your-computer)):
`docsumo_upload_case_document` with `casetype_id` and `file_refs` creates a case holding them, or with `case_id` (and
that case's own `casetype_id`) adds them to an existing case. When a link can't be used, the user adds them in the
app, or emails them to the case type's `upload_email` (`docsumo_get_case_configuration`). Those emails land in the case type's Inbox, which
makes a case from them or suggests the case to attach them to ([case type Inbox](../../product-inbox/SKILL.md)). Bulk case updates
and deletes take either named `case_ids` or `select_all` for the case type, never both. Read back the case/stage
and execution; changing a stage can trigger independent workflows (`docsumo_get_case_configuration` with
`include_stage_workflows` lists which).

## Rerun versus Re-process

`docsumo_rerun_case` keeps the case's stored data, reruns its workflow in the background and returns an
`execution_id` ([reruns](block-behavior.md#reruns)); wait for it with `docsumo_wait_for_workflow_runs`. Its
`cancel_running` option, which cancels a stuck case's in-flight runs first, is refused under an API key, so it is
unavailable to plugin users: a case stuck in processing is recovered from the app. It is not the case list's **Re-process**, which resets the case:
it deletes the case's validations, views (with reviewer status and remark overrides) and case-field values, moves it
to the first stage, classifies its documents again and runs the latest published version. Confirm which one the user
used before explaining lost overrides. Reviewer overrides on validation tables survive an ordinary rerun when the
table keeps its id or title and each row keeps a unique, non-empty primary value. Reruns can repeat external effects
and need an expected outcome and a bounded set of cases, not an open-ended retry loop.

## Artifacts

Artifacts are supporting files attached to a case, not necessarily documents sent through extraction. The artifact
upload accepts broader file types while excluding executables and scripts. Do not infer that an artifact gained
extracted fields or that a document-upload tool adds artifacts. No tool adds artifacts or creates share links: give
the user the steps in the app.

## Shared links

A shared link grants access to one case, not full member access. The shared view hides or disables downloads/exports,
approval/rejection and other member actions; some case-view cell edits and forward stage changes are allowed, and
Split & Classify in shared review depends on the account. Do not call the whole shared experience read-only or assume
a control a member sees is available to recipients.

For “the recipient cannot edit/download,” establish member versus share-link access, the target case, the actual
control and the error shown. Do not try to widen permissions to match what the owner sees.
