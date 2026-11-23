---
name: product-workflows
description: Explain, build and operate Docsumo workflows and cases in product terms, covering case versus independent workflows, triggers, supported operations, designing for input size, testing, publishing, runs and results, schedules, and case stages, sharing and artifacts, through the supported MCP tools. A case type's email Inbox has its own skill. Uploading to a case, retrying its documents, and workflow runs or tests that extract documents spend Docsumo credits: always ask the user first.
---

# Workflows and linked cases

Use for workflow setup, trigger/run/publish questions and case workflow failures. This is the Docsumo product
workflow. Before working in an account, confirm which account is connected ([connection setup](../connection-setup/SKILL.md)).

- Identify the workflow type and trigger before choosing a test: [workflow operations](references/workflows.md).
- Large files or many output rows: [design for the input size](references/workflows.md#design-for-the-input-size) before wiring.
- Case stages, documents, sharing and artifacts: [linked cases](references/cases.md).
- Emails sent to a case type, its Inbox, matching emails to cases and the Inbox settings:
  [case type Inbox](../product-inbox/SKILL.md).
- How blocks pass data, Python code blocks, limits and reruns: [block behavior](references/block-behavior.md).
- Table Lookup/Write and linked records: [tables](../product-tables/SKILL.md).

Read the saved draft, current block catalog, published version and relevant execution separately. Apply requested
changes through the current tool schema; read back an uncertain save before retrying. Testing or publishing must stay
within what the user asked for and may execute downstream actions. Verify block outputs and actual effects before
claiming success. If a trigger operation is unavailable, say exactly what is missing instead of using an upload test as
a substitute. Explain UI labels and concrete next steps; keep raw graph IDs and payloads out of the answer.

**Credits:** uploading to a case, retrying or reprocessing a case's documents, and runs or tests that extract
documents spend Docsumo credits. That includes `docsumo_run_independent_workflow`, `docsumo_run_workflow_test`, and
arming `docsumo_run_workflow_trigger` for the next file. Before each, ask the user to proceed, saying it spends
Docsumo credits, and wait for a yes, even when their request already names the action. Give the credits only if you
already know them; don't make an extra call to find out.

Links of the form `../<skill-name>/...` open another installed skill; if one does not resolve, load the skill of that name and read the same file.
