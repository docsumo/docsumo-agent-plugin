# Home dashboard and Agents Hub

**Home** (`/`) lists every doctype and casetype in the account as **agents**: tiles with title,
category, upload email and counts, grouped into enabled and a collapsible **disabled** section,
with tabs All / Documents / Cases. The **Agents Hub** (`/model-hub/`; named **AI Models Hub** on accounts without
Cases and Workflows) is the catalog of pretrained models and the entry point for a custom document type.

## Home dashboard

| Need | Tool | Notes |
|---|---|---|
| All doctypes with metadata | `docsumo_get_document_types` | Active types under `data.document`, each with `doc_type` (the string other tools take), numeric `id`, `title`, `category`, `can_upload`, `created_at`, `upload_email` (the address that emails documents into the type, its Inbox's address; each person has their own) and `doc_counts`; `data.disabled_doc_types` lists the disabled ones. Search with `q` and page with `limit` / `offset` rather than reading several hundred types. The upload email is on Configure > Import & Export. |
| Account models with upload status | `docsumo_agents_hub_list_models(scope="account")` | The same active types with plan and catalog metadata (`user_value`, `is_authorized`, `plan`), no counts; `mode` = `prod` (default) or `test`, `q`, `limit` / `offset`. |
| Document counts per doctype | `docsumo_get_document_types` (`doc_counts`), `docsumo_doctype_get_document_counts` (with filters) | |
| Casetypes | `docsumo_list_casetypes` | Case types and their cases are operated through [product workflows](../../product-workflows/SKILL.md). |
| Disable / re-enable a doctype | `docsumo_configure_disable_doctype(doc_type, enabled)` | A disabled doctype rejects uploads and sits in the disabled section. |

Common questions: "the tile is gone" (disabled, or the member lost access to the doctype; see
[account settings](../../product-account-settings/references/account-and-settings.md)), "I don't see Cases/Workflows" (not enabled for the
account; the account owner can ask Docsumo), "the count is wrong" (documents inside cases are counted under the case).

## Agents Hub

### Pretrained vs custom

| | Pretrained model | Custom document type |
|---|---|---|
| Created from | Agents Hub catalog, "Add" | Agents Hub "Custom document type" card |
| Doctype id (`value`) | a slug such as `invoice`, `acord25`, `us_cheque`, `bank_statement` | `others__<5 chars>`, e.g. `others__abc12` |
| Initial definition | Docsumo-maintained sections and fields; bundled sample document uploaded on add | Blank; fields are added in Edit Fields (auto-extraction helps propose them) |
| Editable | Yes, in Edit Fields and Configure | Yes |
| Add again | "Add" works once per model value; re-adding means **duplicate** | Create another custom type or duplicate |

The catalog groups 50+ models by category (ID, statements, lending, bills, compliance, tax
forms, procurement, insurance) with tags and a popularity rank.

### Tools

| Need | Tool | Notes |
|---|---|---|
| Catalog | `docsumo_agents_hub_list_models` (`scope="catalog"`, the default) | `mode` `prod` / `test`, `q` to search; returns numeric `id`, `value`, `title`, `category`, tags. |
| Can this model be added? | `docsumo_agents_hub_check_model_status` | Keyed by **value** (`invoice`), the only Agents Hub call that is. |
| Add a pretrained model | `docsumo_agents_hub_enable_model` | Admins only. Numeric catalog `id` as `service_id`; optional `title`, `can_upload`, settings; `upload_sample` (default true) adds the bundled sample as a second, best-effort step (`sample_upload` reports it). Returns only the enabled model's entry. |
| Duplicate a doctype | `docsumo_agents_hub_duplicate_model` | Admins only. Source `doc_type` **value** (`user_value` from `scope="account"`); optional new title; `upload_sample` (default true) adds the sample. Returns the new `doc_type` and `title`. |
| Create a custom type | `docsumo_agents_hub_create_custom_model(title)` | Admins only. Returns the new `others__...` `doc_type` and the `title` actually created; a taken title is renamed with a number ("Invoice 1"). Without `sections` the type starts with one placeholder section and string field, as in the app; with `sections` it is created with its fields in one call. |
| Title uniqueness | `docsumo_agents_hub_validate_title` | Run before creating: a taken title fails here but is silently renumbered by create. |
| The sample document | `upload_sample` on enable or duplicate | No tool adds a sample to an already-enabled model. Under an API key the sample step often fails while the enable succeeds; the user then adds the sample from the app. |
| LLM list | `docsumo_list_llm_models` | Models and reasoning levels for **workflow** LLM blocks, not the doctype's model choice (that is Configure > Extraction > Select AI Model). |

### Duplicate

Duplicating creates a new doctype in the **same account** from an existing one's definition
(fields and settings); documents are not copied. Uses: re-add an already-enabled pretrained
model under a new name, try configuration changes on a copy before touching the production
doctype, or build a reference copy. Copying to another account is not supported by these tools. After a duplicate,
verify with `docsumo_field_setup_get` on the new doctype before relying on it.

### Older and special document types

- Some older accounts have document types built on **trained models** rather than the AI extractor. Their behaviour
  cannot be reproduced by copying configuration; for changes to them, the user contacts Docsumo support.
- **AI Auto-Classify** is a special doctype (`auto_classify_ai`) that sorts uploads into other
  document types. Setting it up — General vs Custom candidates, the descriptions the AI reads,
  splitting — belongs to
  [doctype setup](../../product-doctype-setup/references/doctype-setup.md#splitting-and-the-ai-auto-classifier).
- Case types are created from the Agents Hub too but belong to Cases ([adjacent areas](other-areas.md)).
