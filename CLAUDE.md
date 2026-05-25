# U+22A8 — Public Documentation

This repo is the **public documentation site** for u22a8.ai (U+22A8), built on [Mintlify](https://mintlify.com) and deployed to **docs.u22a8.ai**. It is a standalone repo: everything you need to write accurate docs is in this file. The product monorepo and Outline are *optional* verification sources, not dependencies.

> `AGENTS.md` is a symlink to this file. We use Claude, so `CLAUDE.md` is canonical; the symlink keeps Mintlify's tooling and other agents working.

## What we are documenting

U+22A8 hosts **trait-scoring models**: you define a standard of judgment from labelled examples, train a model, and score content against it. Scoring is **deterministic** — same text + same model = same score — and runs **no LLM at score time**. That determinism (and the absence of an LLM judge in the hot path) is the core differentiator; lead with it, don't bury it.

The audience is **anyone integrating or evaluating the platform** — developers calling the API, agents driving the MCP server, people authoring models. Not internal engineers. If a sentence only makes sense to someone who has read our source code, it does not belong here.

### The mental model (canonical vocabulary — use these terms exactly)

- **Model** — a learned geometry in embedding space that applies a standard of judgment to content. Learned from examples, **not** rules, prompts, or fine-tuned weights. Four types by geometry (DR 022):
  - **scoring** — a learned axis; "how much of X?"
  - **classification** — per-class pools; "which bucket?"
  - **conformance** — one normal pool; "is this in-distribution?"
  - **retrieval** — an indexed corpus; "what's most like this?"
  - *moderation* is packaged classification (a configuration, not a fifth type).
- **Trait** — an axis of judgment a model measures. A model has one or more. Simple traits are **typed** (DR 028), each a triple of *(geometry, score range, native metric)*:
  - **topic** — "is this about X?"
  - **spectrum** — a pole-pair axis (e.g. formal ↔ casual)
  - **claim** — relevance × agreement
  - **outlier** — distance to a cohort (Mahalanobis)
- **Sample** — a labelled example: content plus a polarity/quality label per trait.
- **Score card** — the result of scoring: a per-trait **score** (an integer **0–100** on the wire; conceptually a universal value in [0,1]), a **composite**, plus context. Two score channels (DR 029): the universal score (for display + cross-trait composition) and a typed **native score** (`polarity`, `topicality`, `relevance`/`agreement`, `cohort_similarity`/`anomaly_z`) for ranking and diagnostics. **Never compare scores across trait types.** Per-trait `detail` carries the tier `label`, `confidence`, `band`, `headroom`, calibrated `breaks` (`developing`/`solid`/`strong` thresholds), and `native`.
- **Tiers** (DR 013) — label bands: **Strong / Solid / Developing / Weak**.
- **Breaks** — trained thresholds that define tier boundaries.
- **Headroom** — score distance to the next break above.
- **Confidence** — reliability signal (high / moderate / low) derived from training-distribution geometry.
- **Composite** — harmonic mean of per-trait scores.
- **Lifecycle** (DR 032 — *the model is the API contract*) — `draft → training → ready` (plus `failed`, `archived`). One pattern for everything: **create a model → add samples → train → score** (with optional `feedback` for online learning). Versions are snapshots with named tags and rollback. Trait and sample mutations are **draft-only** (DR 035); discovery is a draft-only transition.

Retired terms — **never use**: "resonance profile", "profile" (→ *model*), "micro model", "dimension" (→ *trait*), the tuning-fork metaphor.

### Score-card field semantics (pin these — easy to get subtly wrong)

The score response shape is canonical in `api-reference/openapi.json`; `concepts/score-card.mdx` is the worked example and the Scoring concept pages (`traits`, `score-types`, `tiers` — one page covering tiers, breaks, and headroom — `confidence`, `composite`) each elaborate part of it. Exact rules, grounded in the live engine — write to these, don't re-derive:

- **Universal score** is 0–100 on the wire (an integer; conceptually $[0,1]$). **Native scores keep their own ranges, never rescaled to 0–100**: `polarity`/`topicality` ∈ [-1, 1], `relevance`/`agreement` ∈ [0, 1], `cohort_similarity` ∈ [-1, 1], `anomaly_z` ∈ ℝ.
- **Trait types** (DR 028) are `topic` / `spectrum` / `claim` / `outlier` — a triple of *(geometry, score range, native metric)*. These are **trait** types; do not conflate with the four **model** geometries (scoring/classification/conformance/retrieval, DR 022). The IA page that covers them is titled "Score types".
- **Breaks** (DR 013) come from training-cluster quartiles: `developing = neg_p75`, `solid = max(pos_p25, developing)`, `strong = max(pos_p75, solid)` — the nested `max(…)` keeps them monotonic when clusters overlap.
- **Tier** from breaks: `≥ strong → Strong`, `≥ solid → Solid`, `≥ developing → Developing`, else `Weak`.
- **Confidence**: `high` inside a cluster (a tail, or a well-separated cluster's body), `moderate` in the gap between separated clusters, `low` in the overlap. Low confidence ⇒ `label = null` **and** `headroom = null` (the model withholds the grade). For well-separated traits the pairing is deterministic: Strong/Solid/Weak → high, Developing → moderate, overlap → low/null. Confidence is a per-score heuristic, not a calibrated probability, and never implies the score is non-deterministic.
- **Headroom** is the distance to the *next* break above (`Weak→developing`, `Developing→solid`, `Solid→strong`). **At Strong, headroom is `0`, not `null`** — `null` is reserved for low confidence. (An earlier `score-card.mdx` draft stated headroom is null at the top tier; that was wrong — don't reintroduce it.)
- **Composite** = harmonic mean of trait scores; a trait scoring exactly `0` is *excluded* from the mean rather than zeroing it. Composite `confidence` = weakest per-trait; composite `headroom` = largest per-trait (the bottleneck). **The composite carries no tier label** — no distribution to grade against (DR 013).
- Scores are comparable **within** a trait, never **across** trait types (DR 028/029).
- The trait wire shape (`list_traits` / OpenAPI `TraitDetail`) exposes `kind` (`extrinsic`/`intrinsic`), `key`, `name`, `description`, the two poles, and sample counts — **not** a `type`/geometry field. A trait's DR 028 type (geometry) is conveyed by the *shape* of its `native` score, not as a standalone returned field; don't document a returned `type` field. (Product gap: DR 029 intends `type` as the native discriminator but it isn't surfaced — capture in Linear, don't paper over.)

## Public surfaces (what gets documented, and where truth lives)

The **public programmatic surface is HTTP**: the REST API and the product MCP server. Document these first.

| Surface | What it is | Canonical truth |
|---|---|---|
| **REST API** | `https://u22a8.ai/v1` — resource-shaped, key-authenticated. 16 resource paths under `/v1/models/{handle}/…` (`score`, `compare`, `samples`, `traits`, `train`, `versions`) plus `/v1/extract`. | `api-reference/openapi.json` (snapshot of the live spec) |
| **Product MCP** | `https://u22a8.ai/mcp` — OAuth (WorkOS) MCP server exposing reading / scoring / authoring / lifecycle tools, and models as readable resources (model-card markdown). | The live server + the tool list below |
| **Console** | `https://u22a8.ai/console` — WorkOS magic-link sign-in, **API-key management** (scoped at issuance), per-key usage. Where developers get a key. | The live console |
| **Authoring schemas** | `model.yaml` + JSONL samples — the published training-input contract (DR 009), at `u22a8.ai/schemas`. | The published JSON Schemas |
| **TypeScript SDK** | Hand-written HTTP client for `/v1` — **in progress (U22-57)**, not shipped. Document when it lands. | — |

**MCP tools** (group them this way in docs): *reading* — `list_models`, `get_model`, `list_traits`, `list_samples`\*, `list_versions`\*, `get_version`\* (\*owner-only); *scoring* — `score`, `compare`, `extract`; *authoring* (draft-only) — `create_model`, `update_model`, `delete_model`, `add_traits`, `update_trait`, `delete_trait`, `add_samples`, `delete_sample`; *lifecycle* — `train`, `discover_traits`, `synthesize_samples`, `tag_version`, `untag_version`, `activate_version`.

**Authentication.** Developers issue an API key in the console and send `Authorization: Bearer <key>`. Keys carry a scope — **`scoring`** (read + score/compare) or **`authoring`** (full). A key authors only in namespaces it owns, and reads its own plus the public namespaces (`u22a8`, `live`, `bench`). MCP uses OAuth via WorkOS rather than a static key.

> **The `oa` Python package is NOT the public client.** It is the in-process service layer behind REST/MCP, connecting directly to the datastore (and doubles as a self-host/local-authoring tool). Never present `oa.connect(...)` as "how to use the hosted platform." Public integration is HTTP: REST, MCP, and the forthcoming TypeScript SDK. The `python -m oa` CLI and the local modeler plugin are *local authoring* (advanced/self-host audience) — keep them out of the primary integration path.

> **Two different "MCP" servers — keep them distinct.** Mintlify auto-hosts a **docs MCP** at this site's domain that answers questions *about the docs* (search + page read). That is **not** our product MCP at `u22a8.ai/mcp`, which scores content. When a page says "MCP," be explicit about which one.

## Content boundaries — never leak internals (DR 018 §4)

Public docs document **observable behavior, inputs, outputs, guarantees, and failure modes** — not how it's built. A published page must never name *how the product is built*, in any of these categories:

- Internal module or package paths.
- Production infrastructure and hosting: hosts/addresses, the CDN, container/orchestration, database schema and migrations, backups, cron.
- Unpublished repos and private benchmark internals.
- Secrets and operator environment variables. The only env var a *reader* ever sees is `U22A8_API_KEY`.
- Embedding/model-provider names and model IDs; cost and optimization internals.
- Retired or unadvertised surfaces and namespaces (only `u22a8.ai/v1`, `/mcp`, `/console`, and the published schemas are public).

When in doubt, document the contract, not the mechanism. If an internal detail genuinely changes a reader's decision, state the *effect*, not the implementation.

> The *specific* forbidden tokens — exact module paths, provider and infra names, env-var names, retired terms — are deliberately **not** enumerated here: this is a public repo, and the list itself is internal signal (it names the very things it forbids). They live in the `/police` sweep's leak scanner in the private monorepo, which scans this repo as a backstop. Don't reconstruct the list in this file.

## How pages must read (DR 018 — writing rubric, distilled)

DR 018 is the enforceable rubric. Model voice on the **NASA Systems Engineering Handbook**: clarity without warmth (warm voice is for marketing surfaces, not here).

1. **Declare, don't negate.** Open by stating what the concept *is*. Test: strip "not / isn't / doesn't / actually / just" from the first paragraph — if it still reads, the original was hedging.
2. **Neutral third person.** Use "you" only for concrete procedural steps, never conceptual exposition. Prefer "the/a" over "your" except for things the reader literally owns.
3. **Authority over metaphor.** Delete any metaphor a same-length direct statement could replace.
4. **Describe the system, not the mechanics.** (See content boundaries above.)
5. **Ship docs for shipped features only.** No unreleased capabilities on concept/reference pages. Roadmap lives in a dedicated meta page or a `proposed` DR.
6. **Terminology is fixed** — use the canonical vocabulary above; one term per concept, no synonyms.
7. **Reference describes, doesn't sell.** Every endpoint/tool gets: a one-sentence purpose, request shape, response shape, failure modes, **≥1 copy-pasteable `curl`**, **≥1 copy-pasteable example in a client language**, and a rate-limit note where applicable (the `/v1` API is not currently rate-limited; the legacy `/m` surface is). Reference headings are plain ("Authentication", "Endpoints"), not numbered.
8. **Examples match the domain** — real evaluation/judgment use cases, not toys.
9. **Concept pages are structured, not narrated.** Fixed sections: **Definition** (one sentence + formal expression) → **Mechanism** (diagram/table) → **Interpretation** (what decision it changes) → **Edge cases** (optional) → **Related** (optional).
10. **Every page ends with a "Next" block** — **at most two** forward links. More than two means the page should be a hub.
11. **Tables and figures are load-bearing**, with declarative-sentence captions; prose is connective tissue.
12. **Link a term on first use; never define inline in parentheses.** A glossary page is the link target.

DR 018 and DR 019 are **accepted** and are this site's foundation. DR 018 §6 predates DR 022 and still says "profile" — DR 022 supersedes it, so always use "model".

## How pages are organized (DR 019 — information architecture, distilled)

- **Content type is the primary axis** (Diátaxis): *Explanation* (understand), *Reference* (retrieve), *How-to* (complete a task), *Tutorial* (guided from nothing). Surface only the types that have pages.
- **Domain is the secondary axis, only inside Explanation.** Add a domain heading (e.g. "Scoring", "Models") only at **≥4 concept pages**; below that, fold in.
- **Surface labels prioritize reader clarity over framework vocabulary.** The sidebar shows "Scoring", not "Explanation".
- **Flat URLs** (`/concept-slug`, addressed by concept, not type) and a **flat sidebar** (sibling groups, not nested). If a second level seems needed, supersede DR 019 rather than nest.
- **Cross-cutting meta** (roadmap, changelog) is its own top-level section, never nested in a domain.
- **Cross-link by content-type pair**: Reference→Explanation on first use of a term; Explanation→Reference only when an integration detail clarifies a concept; never link to Meta from body text (sidebar-discoverable only).

**Target IA** (build toward this; `docs.json` only lists pages that exist):

- **Guides** tab — *Get started* (overview, quickstart, authentication), *How-to* guides, and *Concepts* grouped by domain (Scoring: score card, traits, tiers, breaks, headroom, confidence, composite, score types; Models & training: models, training, supervision, samples, briefs, discovery, calibration, versions/evolution).
- **API reference** tab — REST API (auto-generated from the OpenAPI snapshot + curated overlays), MCP server, SDK (when shipped), authoring schemas.

The legacy web `/docs` (18 pages on the main site) is the *inspiration* set, not a migration source. Rebuild from first principles per DR 018/019.

## Mintlify mechanics

- **`docs.json`** is the single config (theme, colors, fonts, navigation, `api`, `contextual`). Navigation must reference **only pages that exist**, or the build breaks.
- **Pages** are `.mdx` with YAML frontmatter: `title`, `description`, `icon`, optional `sidebarTitle`. Use sentence case in body headings; bold for UI elements; code formatting for paths/commands/identifiers.
- **Components**: `Card`/`Columns`, `Steps`, `Tabs`, `Accordion`, `CodeGroup`, `ParamField`/`ResponseField`/`Expandable`, callouts (`Note`/`Tip`/`Warning`/`Info`/`Check`/`Danger`), `Frame`, `Mermaid` (fenced ` ```mermaid `), `Visibility`, `Prompt`.
- **Illustrations: inline SVG, never screenshots.** Concept figures are hand-authored SVG components in `/snippets/figures/*.jsx` (named export, e.g. `export const ScoreAxis = () => (...)`), imported per page and wrapped in `<Frame caption="…">` with a declarative-sentence caption (DR 018 §11). **Never screenshot the live UI** — the brand rule is "isolated illustrations, no screenshots" (DR 021), and screenshots rot; construct the figure from the same data the page already shows (the `score-card.mdx` figure mirrors its JSON). On-brand without Pro CSS (SVG carries its own styling, sidestepping the Pro-tier `style.css` blocker): use `fill`/`stroke="currentColor"` for ink and structure so figures adapt to light/dark. For data and markers use **cobalt `#1e3a8a`** — DR 021: cobalt is brand/data/status, and the composite marker is cobalt. For tier visuals use the **tier palette**: Strong `#1e3a8a` cobalt · Solid `#2e6b42` moss · Developing `#c17338` amber · Weak `#8a7f68` warm-dim. **Never use vermillion `#e2462c` in a figure** — it is the *action* color (links, buttons, CTAs) only; using it for data violates DR 021's action-vs-status discipline and floods the warm-cream page with more warm, killing contrast. Write **JSX-valid** SVG: camelCase attributes (`viewBox`, `strokeWidth`, `fillOpacity`, `textAnchor`, `strokeDasharray`), `style={{…}}` objects, and `style={{ width: "100%", height: "auto" }}` + `viewBox` for responsiveness. The Scoring set is the reference: `ScoreCardFigure`, `TraitsFigure`, the merged `tiers` page's trio (`ScoreAxis` = tier bands, `BreaksDistribution`, `HeadroomGap` — one targeted figure per section), `ConfidenceClusters`, `ScoreTypeGlyphs`, `CompositePull`. Reach for `Mermaid` only when the subject is a flow/relationship, not a figure.
- **Agent-ready features are on by default** — every page has a `.md` mirror, `llms.txt`/`llms-full.txt` auto-generate, and Mintlify hosts a docs MCP. Use `<Visibility for="agents">` to give agents direct API calls where humans get UI steps; embed a `<Prompt>` with `npx skills add https://docs.u22a8.ai` on the getting-started page.
- **API reference**: auto-generated from `api-reference/openapi.json` (a snapshot of `https://u22a8.ai/v1/openapi.json`). Customize per-endpoint with the `x-mint` OpenAPI extension (curated prose, the required `curl`/client example) rather than dropping to hand-written MDX. Refresh the snapshot deliberately (see drift below).
- **Local dev**: `mint dev` (preview at :3000), `mint broken-links`, `mint validate` (strict build + OpenAPI validity; replaces the deprecated `openapi-check`). Deploy is automatic via the Mintlify GitHub app on push to the default branch; PRs get preview deployments.
- Install Mintlify's own authoring skill once per environment: `npx skills add https://mintlify.com/docs`.

## Keeping docs true (drift & police)

- **OpenAPI snapshot** is review-gated, not a live pointer — so a new endpoint can't silently appear and leak. It is now a **clean verbatim copy** of the live spec (no local patching): U22-149 hardened the upstream `/v1` spec so it declares the absolute `servers` URL, a bearer `securitySchemes` + global `security`, the `score`/`compare` request bodies, and the `ErrorEnvelope` shape on every non-2xx response (so endpoint pages show real failure codes, not FastAPI's default validation error). Refresh by re-fetching `https://u22a8.ai/v1/openapi.json`, diffing, and reviewing — overwrite the file directly, don't hand-edit.
- **Before publishing**, run `mint broken-links` and re-read the content-boundary list above — a deliberate no-leak pass is mandatory. There is no leak-scanner in this repo to lean on: its rule set is a manifest of internals, so it can't live in a public repo. The monorepo's `/police` sweep runs the scan against this checkout as a backstop — your manual pass is still the first line.
- **Drift is caught on two repos.** This repo's CI (`.github/workflows/ci.yml`) is the publish gate for what *can* live here: `mint broken-links` and `mint validate` (strict build + OpenAPI validity) block merge. Two checks run out of band in the monorepo's scheduled `/police` sweep, cross-repo, when this repo is checked out: (1) an **internal-leak scan** — the scanner is a private police asset, not committed here; (2) **OpenAPI freshness** (snapshot vs the live `/v1` spec) — the snapshot is review-gated and the live host is unreliable from CI. On either, police *fixes* drift — bringing pages in line with `/v1` / MCP-tool / schema changes and refreshing the snapshot (`scripts/openapi_freshness.py` → re-fetch → `scripts/apply_overlays.py`) — and lands it in a docs-repo PR for review (it does not auto-merge), filing a *Public Docs* Linear issue only for a net-new page or an unclear treatment. The PR review *is* the snapshot's review gate.

## Working agreements

- **The user manages git.** Never `git commit`, `git push`, `git checkout -b`, or `git branch`. Make edits in place; ask before destructive ops. (Exception: the monorepo's `/police` sweep, when it has this repo checked out, creates its own branch + PR to land docs-sync fixes — per its skill spec; it never auto-merges.)
- **Ground every page in shipped behavior.** Verify against the live API/console or the OpenAPI snapshot before describing it. Don't document intent as if it shipped.
- **Capture, don't fix, product rough edges.** When documenting surfaces this honest, you'll find awkward APIs and naming. File them (Linear, *Public Docs* project) — don't fix product from the docs repo.
- **Reference DRs by code** (e.g. "DR 032"); fetch bodies from Outline (`outline` MCP) when available. The distilled essentials above are enough to write without fetching.
- Work is tracked in Linear under the **Public Docs** project; the planning doc lives in Outline (*Product Planning Active*).
