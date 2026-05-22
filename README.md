# U+22A8 docs

Public documentation for [u22a8.ai](https://u22a8.ai), built on [Mintlify](https://mintlify.com) and deployed to **docs.u22a8.ai**.

This site documents **public surfaces only** — the REST API, the MCP server, authoring schemas, and the concepts behind trait scoring. It never describes internal architecture, infrastructure, or anything that isn't shipped. The full writing and content rules live in [`CLAUDE.md`](./CLAUDE.md) (symlinked as `AGENTS.md`); read it before contributing.

## Local development

```bash
npm i -g mint        # one-time: install the Mintlify CLI
mint dev             # preview at http://localhost:3000
mint broken-links    # validate internal links
mint openapi-check api-reference/openapi.json   # validate the API spec
```

## Structure

```
docs.json                  # site config: theme, navigation, API, agent features
index.mdx                  # overview
quickstart.mdx             # get a key → first score
authentication.mdx         # keys, scopes, namespaces
concepts/                  # Explanation pages (score-card.mdx is the template)
api-reference/
  introduction.mdx         # REST overview + curated examples
  openapi.json             # review-gated snapshot of https://u22a8.ai/v1/openapi.json
logo/ , favicon.svg        # brand assets (the ⊨ mark)
CLAUDE.md  (← AGENTS.md)   # standalone context + writing/IA rules
```

## Publishing

Changes merged to the default branch deploy automatically via the Mintlify GitHub app. Pull requests get preview deployments. The user manages git — agents make edits in place and do not commit, push, or branch.

## AI-assisted authoring

```bash
npx skills add https://mintlify.com/docs   # install Mintlify's authoring skill
```

The API reference auto-generates from `api-reference/openapi.json`. Refresh it deliberately by re-fetching `https://u22a8.ai/v1/openapi.json`, diffing, and reviewing — never point at the live spec, so a new endpoint can't appear unreviewed.
