# Public documentation lookup (support.docsumo.com)

Docsumo's official documentation (Guides and API Reference) lives at **support.docsumo.com**.
Use it to answer *how a feature works*, *what is supported*, limits, integration setup, API
endpoints and parameters, error meanings. Do not use it for the user's own data or
configuration; that comes from the MCP tools. A request that is both ("STP does not work for
my invoices") means: read the docs for the rules, then check the account's settings with the tools.

Use the host's web search or fetch tool to open Docsumo support pages. If browsing is unavailable, say that the
documentation could not be checked; the Docsumo MCP has no documentation tool.

## Procedure

1. **Start at the index.** Open `https://support.docsumo.com/llms.txt` with the host browser/fetch tool. It is
   the only documentation URL you may type from memory. It lists every page with a title and
   often a one-line description, in two parts: Guides (`/docs/...`) and API Reference
   (`/reference/...`).
2. **Pick 1-3 pages.**
   - Scan both parts. API questions (auth, rate limits, endpoints, parameters, errors) are
     usually answered by an API Reference entry, not a Guide.
   - Many entries have no description; match on the **title** too. An exact-title entry
     ("Rate Limits") beats a wordier but adjacent Guide.
   - Prefer the most specific page. Match on meaning, not the user's words ("sorting
     documents automatically" is "Auto Classify").
   - Before deciding something is undocumented, re-scan the index for a more specific entry.
3. **Fetch only URLs you saw**: an index entry or a link inside a page you already fetched.
   Never build a URL from a title, menu label or intuition; slugs do not follow titles.
4. **Cap what you read.** Two or three targeted pages is the norm. Read the section that
   answers the question; do not walk the whole site. If the first pages do not answer it, it is
   probably not documented.
5. **Answer with a quote and the URL.** Lead with the takeaway in a few sentences or steps,
   quote the decisive sentence(s) from the page, and cite the human-readable URL with any
   `.md` suffix removed. Never cite `llms.txt` itself; it is a map, not a source. List every
   page that contributed.

Example: "Docsumo auto-approves a document when every field meets the confidence threshold
and no mandatory field is empty (see 'Straight Through Processing' at
https://support.docsumo.com/docs/<page>). Your Invoice doctype has the threshold at 95%, which
explains why most documents wait in Review."

## Failure handling

| Result | Meaning | Do |
|---|---|---|
| Page does not exist | Dead end for that URL | Go back to the index or the page you came from and take another **listed** URL. Do not retry variants. |
| Temporarily unavailable | Docs host is busy | Retry the same URL once. If it still fails, report that the documentation could not be reached; do not cite a page you never opened. |
| Empty or login-gated body | Shell page | Treat as not loaded; try the next candidate. |
| Marketing or unrelated content | Not documentation | Treat as not documented. |

**"Not documented" and "could not read the docs" are different answers.** Say which one applies.
Never fill a gap from memory about the product: a confident wrong answer is worse than an honest
gap. Where useful, point to Docsumo support or the changelog (`changelog.docsumo.com`) as a
place to check, without presenting it as documentation.

## Scope notes

- Stay on support.docsumo.com. The marketing site (`docsumo.com`) and the changelog are not
  part of the documentation.
- API Reference pages describe the public REST API (upload, document data, review, webhooks).
  The MCP tools are a different interface; do not assume a public API parameter exists on a tool or vice versa.
- For a vague question ("how does Docsumo work?"), summarise the most relevant high-level
  pages and offer to go deeper rather than fetching many pages.
- When a feature the user wants does not exist in the docs or the product, say so plainly, suggest the closest
  documented alternative, and mention that they can request it from Docsumo.
