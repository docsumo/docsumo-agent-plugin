# Account and Settings

`/settings/*` is where an owner or admin manages the account. This covers identity and plan, member access, API key,
webhooks and notifications, credits and billing, retention, activity logs and database tables.

## Account identity and plan

| Need | Tool | Useful fields |
|---|---|---|
| Who am I acting as, plan, mode | `docsumo_get_account_user` | Under `data.user`: email and name, `role`, the organisation and its plan, the authorized document types |
| Allowance and usage | `docsumo_get_account_usage` (owners and admins) | Documents and pages processed over a date range (default: the last 7 days), by document type and member, with the plan and its page `allowance` (`pages_processed`, `total_pages`, `pages_left`, `overage`); list the document types themselves with `docsumo_get_document_types`. |
| Account-wide settings | `docsumo_get_account_config` | `account_type`, `plan_category`, `del_doc_after` (auto-delete window), `inactivity_timeout`, `send_token_in_review_url`, and `webhook_url` (scheme and host only). Credentials and the doctype catalog are not returned. |
| Change account-wide settings | `docsumo_update_account_config` (owners and admins only) | Only the settings given change. `straight_through_processing` turns STP on or off for the whole organisation; per-doctype STP can inherit it. `del_doc_after` is the auto-delete retention: `1days`, `7days`, `30days`, `90days`, `180days`, `365days` or `never` (the last two need a paid plan). Every day, documents whose last change is older than the window are deleted, whatever their status or folder, and a shorter window deletes the documents already older than it; check this first when documents seem to have disappeared. `temp_token_duration` is the review-link expiry in days: `0.02` (about 30 minutes), `0.125` (3 hours), `0.5`, `1`, `3` or `7`. `send_token_in_review_url` sets whether review URLs embed a token. |

Screen: Settings > Account settings (`/settings/account-settings/`).

## Members and doctype access

Roles are `owner`, `admin`, `moderator`, `member`. Each member has an **authorized doctype
list**; a doctype missing from it is invisible to that member ("the document type disappeared",
"I cannot upload to X", "my colleague sees it but I don't"). Members can request access in the product, and an
owner or admin grants it by editing the member in the app.

The tools only read members: `docsumo_list_account_members` (`query_fullname` filter, `limit`/`offset`) lists them
with their roles, each carrying `authorized_doc_types_count`, not the list. Adding, editing (role, name, document type
access) and removing a member are done in the app, at Settings > Members (`/settings/users/`); give the user the steps.

## API key

Screen: Settings > Webhook & API (`/settings/webhook-api/`). Each user has their own API key and can view and copy it
there; a user with the member role cannot regenerate it. No tool views or rotates the key, and account reads do not
return it; **never print, paste or log a key**. Regenerating **invalidates the old key**, breaking every integration
and script that uses it, including that person's Docsumo MCP connection. Treat "my API calls return 401" as: key
regenerated, wrong account or region, or member removed; point the user to the screen.

## Webhooks and notifications

A webhook fires on the document events selected in notification preferences (chiefly when a
document becomes `processed`) and carries the document JSON. Configuration:

| Item | Tool | Detail |
|---|---|---|
| Webhook target | `docsumo_get_webhook_config`, `docsumo_update_webhook_url` | The read returns `data.webhook_url` with `url` as scheme and host only (the rest `***`) and `header.key` when a custom header is set; credentials never come back, and an empty `webhook_url` means none is configured. The update changes only the fields given (`url` in full, `basic_auth`, `auth_param`, header `key` / `value`, `data_format` `v1` / `v3`); the rest keep their stored values, an empty string clears one, and the masked URL is refused. |
| Per-doctype response options | `docsumo_get_webhook_config` (`data.payload`), `docsumo_update_webhook_api_settings` | The read returns the account-wide `include_in_response` file-link and inline-contents toggles, `include_in_response_default` (the per-type value nearly every type has), and `active_doc_types`, only the types that differ from it. The update takes `doc_types`, `include_s3` / `include_base64` as `include` / `exclude`, and `action` `tick` / `untick`; `untick` clears every doctype, not only the named ones. |
| Notification preferences | (screen) | Which document, user and miscellaneous events go by email vs webhook. |
| Delivery history | `docsumo_list_activity_logs(activity_type="webhook")` | Shows attempts and failures; the user sees this as Activity > Webhook activity (`/webhookactivity`). |

"Webhook not received": check the configured destination and whether authentication is configured (never expose
credentials), that the doctype is ticked, that the document actually reached `processed` (with STP off it waits in
Review), and the webhook activity log. Delivery is tried a few times within seconds and not again later, so an
endpoint that was down at that moment misses the event: fix the endpoint, then reprocess or export the missed
documents.

## Credits, pages and billing

Screens: Settings > Billing > Overview (`/settings/billing/overview/`): plan, billing cycle,
card, invoices, overage page limits. Usage stats (`/settings/billing/usage-stats/`): pages and
documents processed per doctype and per user, credit balance and trends, a credit calculator.
Plans (`/settings/billing/plans/`): upgrade, downgrade, buy balance.

Reads: `docsumo_get_account_usage` (owners and admins) for documents and pages processed over a date range by
document type and by member, with the plan, its dates and its page allowance (the Usage stats screen); credit changes in
`docsumo_list_activity_logs(activity_type="credit")` (the UI calls this **Credit activity**, `/creditactivity`), and
the per-operation estimate `docsumo_doctype_calculate_document_credits`.
Symptoms: uploads rejected, "limit reached" banner. A document that stays unprocessed for several hours is marked
`erred` with "timeout"; retry it. Billing questions go to Docsumo; do not promise credits.

## Database tables (dropdown and CSV databases)

Settings → Database Tables (`/settings/database-table/`) is the legacy CSV source surface. No tool reads or writes
it: the user views, edits, downloads or deletes one there. Records (formerly Tables) live separately under `/tables`.
[Product tables](../../product-tables/SKILL.md) covers which is which and the lookup sources; do not assume the two
are interchangeable.

## Security, secrets, SSO

Settings > Security (`/settings/security/`): SAML SSO setup and MFA. Settings > Secrets
(`/settings/secrets/`): environment secrets used by custom code and workflows (values are
masked). No tool changes SSO, MFA or secrets; give the user the steps in the app ([security](security.md)).
No tool changes the password or deletes the account; both stay with the user.

## Activity logs

Five screens share one feed: All (`/allactivity`), Document (`/documentactivity`), User
(`/useractivity`), Credit (`/creditactivity`), Webhook (`/webhookactivity`). Each entry is
`{ activity, name, date_time }`. Tools: `docsumo_list_activity_logs` with `activity_type` =
`all` / `document` / `user` / `credit` / `webhook`, `created_date_gte` / `created_date_lte`, `q` (activity text,
matched as typed), `user_id` list, `action`, `mode`, pagination; `docsumo_get_activity_log_counts` for per-tab counts. Use it to establish **who changed what when** (a field
deleted, a setting toggled, a document deleted or reprocessed) before blaming extraction.
