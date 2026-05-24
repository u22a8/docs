# Contributing

Before writing anything, read [`CLAUDE.md`](./CLAUDE.md). It carries the product vocabulary, the public-surface inventory, the content boundaries, and the writing and IA rules (distilled from DR 018 and DR 019). The points below are the short version.

## Non-negotiables

- **Public surfaces only.** Document observable behavior, inputs, outputs, guarantees, and failure modes. Never internal modules, infrastructure, secrets, provider names, or anything unshipped. When in doubt, document the contract, not the mechanism.
- **Ground every page in shipped behavior.** Verify against the live API, the console, or the OpenAPI snapshot before describing it. Do not document intent as if it shipped.
- **Fixed terminology.** Use the canonical terms (model, trait, sample, score card, tier, break, headroom, confidence, composite). Never "profile", "resonance profile", "micro model", or "dimension".

## Writing

- Declare what a thing **is** before what it isn't.
- Neutral third person; use "you" only in procedural steps.
- Authority over metaphor; delete decoration.
- Concept pages follow the structure of `concepts/score-card.mdx`: Definition → Mechanism → Interpretation → Edge cases → Related.
- Reference pages follow `api-reference/introduction.mdx`: plain headings, and every endpoint gets purpose, request, response, failure modes, a `curl` example, a client example, and a rate-limit note.
- Every page ends with a **Next** block of at most two forward links.
- Tables and figures carry the load; prose connects them.

## Before opening a PR

```bash
mint broken-links   # internal links resolve
mint validate       # strict build check + OpenAPI snapshot validity
```

CI runs these two checks and blocks the merge on either failure. **Leaks are caught separately**: the monorepo's `/police` sweep scans this repo for internal leaks (its rule set names internals, so it isn't kept here). That's a backstop, not your gate — re-read the content-boundary list in `CLAUDE.md` and do a deliberate no-leak pass before every PR. When in doubt, document the contract, not the mechanism.

Found an awkward API or naming while documenting? File it in the Linear **Public Docs** project — don't work around it in prose, and don't fix the product from here.
