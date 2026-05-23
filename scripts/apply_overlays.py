#!/usr/bin/env python3
"""Apply curated per-endpoint overlays to the /v1 OpenAPI snapshot.

The snapshot at ``api-reference/openapi.json`` is a clean copy of the live
``https://u22a8.ai/v1/openapi.json`` (see CLAUDE.md § Keeping docs true).
Mintlify auto-generates the endpoint pages from it, but the auto-generated
pages carry no copy-pasteable examples. This script layers two OpenAPI
extensions onto each operation, keyed by ``operationId``:

* ``x-codeSamples`` — a curated ``curl`` and Python example, shown in the
  request examples panel (DR 018 §7: every endpoint gets >=1 curl and >=1
  client example).
* ``x-mint.content`` — endpoint-specific prose (async polling, content
  negotiation, draft-only rules) prepended to the page body, only where it
  earns its place. Failure modes are already rendered from the spec's
  ``ErrorEnvelope`` responses, so overlays do not re-document error shapes.

Run it after refreshing the snapshot:

    # in the docs repo
    curl -s https://u22a8.ai/v1/openapi.json > api-reference/openapi.json  # verbatim
    python scripts/apply_overlays.py                                       # re-apply
    git diff api-reference/openapi.json                                    # review

Idempotent: re-running overwrites the overlays it owns and leaves the rest
of the spec untouched. Operations absent from the snapshot are skipped.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SPEC = Path(__file__).resolve().parent.parent / "api-reference" / "openapi.json"

_DRAFT_ONLY = (
    "<Note>Draft-only — trait and sample edits apply only while the model is "
    "in the `draft` state. A trained (`ready`) model returns `409`; the "
    "samples and traits are frozen into its versions.</Note>"
)


def _samples(curl: str, python: str, *extra: tuple[str, str, str]) -> list[dict]:
    """Build an x-codeSamples list: a cURL entry, a Python entry, then extras."""
    out = [
        {"lang": "bash", "label": "cURL", "source": curl},
        {"lang": "python", "label": "Python", "source": python},
    ]
    out.extend({"lang": lang, "label": label, "source": src} for lang, label, src in extra)
    return out


# operationId -> {"code": [...x-codeSamples...], "content": "...MDX..."}
OVERLAYS: dict[str, dict] = {
    # ----- System -------------------------------------------------------
    "health_health_get": {
        "code": _samples(
            "curl https://u22a8.ai/v1/health",
            'import requests\n\n'
            'requests.get("https://u22a8.ai/v1/health").json()  # {"status": "ok"}',
        ),
    },
    # ----- Models -------------------------------------------------------
    "list_models_models_get": {
        "code": _samples(
            'curl "https://u22a8.ai/v1/models?limit=20" \\\n'
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            'r = requests.get(\n'
            '    "https://u22a8.ai/v1/models",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            '    params={"limit": 20},\n'
            ")\n"
            'for m in r.json()["items"]:\n'
            '    print(m["handle"], m["traits"])',
        ),
        "content": (
            "Without a `namespace` query parameter the listing covers the "
            "public `u22a8` catalog. Pass `namespace=<name>` to list a "
            "namespace your key owns. Results are cursor-paginated: follow "
            "`next_cursor` until it is `null`."
        ),
    },
    "create_model_models_post": {
        "code": _samples(
            "curl -X POST https://u22a8.ai/v1/models \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            "  -d '{\"handle\": \"acme.support-tone\", \"description\": "
            "\"Warmth and clarity of support replies\"}'",
            "import os, requests\n\n"
            "r = requests.post(\n"
            '    "https://u22a8.ai/v1/models",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            '    json={\n'
            '        "handle": "acme.support-tone",\n'
            '        "description": "Warmth and clarity of support replies",\n'
            "    },\n"
            ")\n"
            'print(r.json()["handle"], r.json()["state"])  # acme.support-tone draft',
        ),
        "content": (
            "Creates a model in the `draft` state. The `handle` must be in a "
            "namespace your key owns. Next: add traits and samples, then "
            "train."
        ),
    },
    "get_model_detail_models__handle__get": {
        "code": _samples(
            "curl https://u22a8.ai/v1/models/u22a8.commit-message \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            "r = requests.get(\n"
            '    "https://u22a8.ai/v1/models/u22a8.commit-message",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            ")\n"
            'print(r.json()["traits"])',
            (
                "bash",
                "cURL (model card)",
                "curl https://u22a8.ai/v1/models/u22a8.commit-message \\\n"
                '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
                '  -H "Accept: text/markdown"',
            ),
        ),
        "content": (
            "Returns JSON by default. Set `Accept: text/markdown` to fetch the "
            "**model card** — a human-readable summary of the model, its "
            "traits, and any additional terms. It is the same markdown the "
            "MCP server serves as the model's resource."
        ),
    },
    "update_model_models__handle__patch": {
        "code": _samples(
            "curl -X PATCH https://u22a8.ai/v1/models/acme.support-tone \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            "  -d '{\"description\": \"Tone and clarity of customer replies\"}'",
            "import os, requests\n\n"
            "r = requests.patch(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            '    json={"description": "Tone and clarity of customer replies"},\n'
            ")",
        ),
        "content": (
            "Patches model metadata; omitted fields are left unchanged. "
            "Lifecycle state is not patchable — use `POST …/train` to move a "
            "draft to `ready` and `DELETE` to archive."
        ),
    },
    "delete_model_models__handle__delete": {
        "code": _samples(
            "curl -X DELETE https://u22a8.ai/v1/models/acme.support-tone \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            "requests.delete(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            ")",
        ),
    },
    "list_traits_models__handle__traits_get": {
        "code": _samples(
            "curl https://u22a8.ai/v1/models/u22a8.commit-message/traits \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            "r = requests.get(\n"
            '    "https://u22a8.ai/v1/models/u22a8.commit-message/traits",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            ")\n"
            'for t in r.json()["traits"]:\n'
            '    print(t["key"], t["sample_count"])',
        ),
    },
    "add_traits_models__handle__traits_post": {
        "code": _samples(
            "curl -X POST https://u22a8.ai/v1/models/acme.support-tone/traits \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            "  -d '{\"traits\": [{\"name\": \"Warmth\", "
            "\"positive_label\": \"warm\", \"negative_label\": \"cold\"}]}'",
            "import os, requests\n\n"
            "r = requests.post(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/traits",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            '    json={"traits": [\n'
            '        {"name": "Warmth", "positive_label": "warm", "negative_label": "cold"},\n'
            "    ]},\n"
            ")",
        ),
        "content": _DRAFT_ONLY,
    },
    "discover_traits_models__handle__traits_discover_post": {
        "code": _samples(
            "curl -X POST https://u22a8.ai/v1/models/acme.support-tone/traits/discover \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            "  -d '{\"effort\": \"medium\"}'",
            "import os, time, requests\n\n"
            "base = \"https://u22a8.ai/v1/models/acme.support-tone\"\n"
            "headers = {\"Authorization\": f\"Bearer {os.environ['U22A8_API_KEY']}\"}\n\n"
            "requests.post(f\"{base}/traits/discover\", headers=headers,\n"
            '              json={"effort": "medium"})\n'
            "# Discovery runs asynchronously; poll the model until it leaves `busy`.\n"
            'while requests.get(base, headers=headers).json()["state"] == "busy":\n'
            "    time.sleep(5)",
        ),
        "content": (
            "Derives intrinsic traits from the model's samples and attaches "
            "them. Draft-only and asynchronous: it returns `202` with a run "
            "id, the model enters `busy`, and the new traits appear on "
            "`GET …/traits` once it returns to `draft`. Poll `GET …/models/"
            "{handle}` for the state — there is no run resource to fetch."
        ),
    },
    "get_trait_models__handle__traits__key__get": {
        "code": _samples(
            "curl https://u22a8.ai/v1/models/acme.support-tone/traits/warmth \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            "r = requests.get(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/traits/warmth",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            ")",
        ),
    },
    "update_trait_models__handle__traits__key__patch": {
        "code": _samples(
            "curl -X PATCH https://u22a8.ai/v1/models/acme.support-tone/traits/warmth \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            "  -d '{\"description\": \"How warm and personable the reply reads\"}'",
            "import os, requests\n\n"
            "requests.patch(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/traits/warmth",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            '    json={"description": "How warm and personable the reply reads"},\n'
            ")",
        ),
        "content": _DRAFT_ONLY,
    },
    "delete_trait_models__handle__traits__key__delete": {
        "code": _samples(
            "curl -X DELETE https://u22a8.ai/v1/models/acme.support-tone/traits/warmth \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            "requests.delete(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/traits/warmth",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            ")",
        ),
        "content": _DRAFT_ONLY,
    },
    "add_samples_models__handle__samples_post": {
        "code": _samples(
            "curl -X POST https://u22a8.ai/v1/models/acme.support-tone/samples \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            "  -d '{\"samples\": ["
            "{\"trait\": \"warmth\", \"text\": \"Happy to help — let us sort this out together.\", \"quality\": 1.0}, "
            "{\"trait\": \"warmth\", \"text\": \"Request denied. Refer to the policy.\", \"quality\": 0.0}"
            "]}'",
            "import os, requests\n\n"
            "r = requests.post(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/samples",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            '    json={"samples": [\n'
            '        {"trait": "warmth", "text": "Happy to help \\u2014 let us sort this out together.", "quality": 1.0},\n'
            '        {"trait": "warmth", "text": "Request denied. Refer to the policy.", "quality": 0.0},\n'
            "    ]},\n"
            ")\n"
            'print(r.json()["ids"])',
        ),
        "content": (
            "Each sample labels one trait: `quality` `1.0` is the positive "
            "pole, `0.0` the negative. Up to 500 samples per request.\n\n"
            + _DRAFT_ONLY
        ),
    },
    "list_samples_models__handle__samples_get": {
        "code": _samples(
            'curl "https://u22a8.ai/v1/models/acme.support-tone/samples?trait=warmth&limit=100" \\\n'
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            "r = requests.get(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/samples",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            '    params={"trait": "warmth", "limit": 100},\n'
            ")",
        ),
    },
    "delete_sample_models__handle__samples__sample_id__delete": {
        "code": _samples(
            "curl -X DELETE https://u22a8.ai/v1/models/acme.support-tone/samples/4217 \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            "requests.delete(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/samples/4217",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            ")",
        ),
        "content": _DRAFT_ONLY,
    },
    "train_model_models__handle__train_post": {
        "code": _samples(
            "curl -X POST https://u22a8.ai/v1/models/acme.support-tone/train \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            "  -d '{\"effort\": \"medium\"}'",
            "import os, time, requests\n\n"
            "base = \"https://u22a8.ai/v1/models/acme.support-tone\"\n"
            "headers = {\"Authorization\": f\"Bearer {os.environ['U22A8_API_KEY']}\"}\n\n"
            "requests.post(f\"{base}/train\", headers=headers, json={\"effort\": \"medium\"})\n"
            "# Training runs asynchronously; poll until the model is ready.\n"
            'while requests.get(base, headers=headers).json()["state"] == "busy":\n'
            "    time.sleep(10)",
        ),
        "content": (
            "Asynchronous: a first train from `draft` returns `202` with a "
            "run id and moves the model through `busy` to `ready`. Poll "
            "`GET …/models/{handle}` for the state. From a `ready` model, "
            "pass `reoptimize_params: true` to force a fresh parameter "
            "search; otherwise routine retraining on new samples happens "
            "automatically."
        ),
    },
    # ----- Scoring ------------------------------------------------------
    "score_models__handle__score_post": {
        "code": _samples(
            "curl https://u22a8.ai/v1/models/u22a8.commit-message/score \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
            '  -H "Content-Type: text/plain" \\\n'
            "  --data-binary 'Fix race condition in worker dispatch by draining "
            "the in-flight queue before shutdown'",
            "import os, requests\n\n"
            "r = requests.post(\n"
            '    "https://u22a8.ai/v1/models/u22a8.commit-message/score",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            '    json={"content": "Fix race condition in worker dispatch by '
            'draining the in-flight queue before shutdown"},\n'
            ")\n"
            'card = r.json()\n'
            'print(card["composite"], card["scores"])',
            (
                "bash",
                "cURL (text view)",
                "curl https://u22a8.ai/v1/models/u22a8.commit-message/score \\\n"
                '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
                '  -H "Accept: text/plain" \\\n'
                '  -H "Content-Type: text/plain" \\\n'
                "  --data-binary 'Fix race condition in worker dispatch'",
            ),
        ),
        "content": (
            "Send `content` as JSON, or the raw text with "
            "`Content-Type: text/plain`. A URL in `content` is fetched and "
            "its extracted text is scored. Set `Accept: text/plain` for a "
            "bar-chart rendering instead of JSON. An optional `feedback` map "
            "captures labels as new samples for continuous learning. The full "
            "response shape is documented in [the score card]"
            "(/concepts/score-card)."
        ),
    },
    "compare_models__handle__compare_post": {
        "code": _samples(
            "curl https://u22a8.ai/v1/models/u22a8.commit-message/compare \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            "  -d '{\"a\": \"fix bug\", \"b\": \"Fix race condition in worker "
            "dispatch by draining the in-flight queue before shutdown\"}'",
            "import os, requests\n\n"
            "r = requests.post(\n"
            '    "https://u22a8.ai/v1/models/u22a8.commit-message/compare",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            '    json={\n'
            '        "a": "fix bug",\n'
            '        "b": "Fix race condition in worker dispatch by draining '
            'the in-flight queue before shutdown",\n'
            "    },\n"
            ")\n"
            'print(r.json()["improvement"], r.json()["per_trait"])',
        ),
        "content": (
            "Scores a baseline `a` against a candidate `b` and returns the "
            "per-trait delta plus the overall improvement (`b.composite − "
            "a.composite`). URLs in `a` and `b` are auto-fetched. Set "
            "`Accept: text/plain` for a side-by-side rendering."
        ),
    },
    # ----- Extract ------------------------------------------------------
    "extract_extract_post": {
        "code": _samples(
            "curl -X POST https://u22a8.ai/v1/extract \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            "  -d '{\"url\": \"https://example.com/article\"}'",
            "import os, requests\n\n"
            "r = requests.post(\n"
            '    "https://u22a8.ai/v1/extract",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            '    json={"url": "https://example.com/article"},\n'
            ")\n"
            'print(r.json()["content_sha256"])',
        ),
        "content": (
            "Returns the same readable text the score endpoint extracts from "
            "a URL, plus a content hash for deduplication. Useful to preview "
            "what will be scored."
        ),
    },
    # ----- Versions -----------------------------------------------------
    "list_versions_models__handle__versions_get": {
        "code": _samples(
            "curl https://u22a8.ai/v1/models/acme.support-tone/versions \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            "r = requests.get(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/versions",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            ")\n"
            'for v in r.json()["items"]:\n'
            '    print(v["version_no"], v["tags"])',
        ),
    },
    "get_version_models__handle__versions__v__get": {
        "code": _samples(
            "curl https://u22a8.ai/v1/models/acme.support-tone/versions/v3 \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            "r = requests.get(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/versions/v3",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            ")",
        ),
        "content": (
            "Accepts a `vN` number or a tag name. The response includes the "
            "full `snapshot` of trained parameters, which is large; for "
            "metadata only, use the list endpoint."
        ),
    },
    "tag_version_models__handle__versions__name__post": {
        "code": _samples(
            "curl -X POST https://u22a8.ai/v1/models/acme.support-tone/versions/prod \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            "requests.post(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/versions/prod",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            ")",
        ),
        "content": (
            "Pins the tag `{name}` to the model's current active version. "
            "Re-using a tag moves the pointer. Tag names of the form `vN` are "
            "rejected so the version-number space stays unambiguous."
        ),
    },
    "untag_version_models__handle__versions__name__delete": {
        "code": _samples(
            "curl -X DELETE https://u22a8.ai/v1/models/acme.support-tone/versions/prod \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY"',
            "import os, requests\n\n"
            "requests.delete(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/versions/prod",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            ")",
        ),
    },
    "activate_version_models__handle__versions_active_put": {
        "code": _samples(
            "curl -X PUT https://u22a8.ai/v1/models/acme.support-tone/versions/active \\\n"
            '  -H "Authorization: Bearer $U22A8_API_KEY" \\\n'
            '  -H "Content-Type: application/json" \\\n'
            "  -d '{\"version\": \"v3\"}'",
            "import os, requests\n\n"
            "requests.put(\n"
            '    "https://u22a8.ai/v1/models/acme.support-tone/versions/active",\n'
            '    headers={"Authorization": f"Bearer {os.environ[\'U22A8_API_KEY\']}"},\n'
            '    json={"version": "v3"},  # or {"tag": "prod"}\n'
            ")",
        ),
        "content": (
            "Points the model at the chosen version so it serves scores — use "
            "it to roll back or pin. Send **exactly one** of `version` (a "
            "`vN` number) or `tag`. Non-destructive: new samples keep "
            "accumulating and automatic retraining keeps minting versions "
            "regardless of which one is active."
        ),
    },
}


def main() -> int:
    spec = json.loads(SPEC.read_text())
    by_id = {
        op["operationId"]: op
        for path in spec["paths"].values()
        for method, op in path.items()
        if method in ("get", "post", "put", "patch", "delete") and "operationId" in op
    }

    applied, missing = 0, []
    for op_id, overlay in OVERLAYS.items():
        op = by_id.get(op_id)
        if op is None:
            missing.append(op_id)
            continue
        if "code" in overlay:
            op["x-codeSamples"] = overlay["code"]
        if "content" in overlay:
            op["x-mint"] = {"content": overlay["content"]}
        applied += 1

    uncovered = sorted(set(by_id) - set(OVERLAYS))
    SPEC.write_text(json.dumps(spec, indent=2, ensure_ascii=False))

    print(f"Applied overlays to {applied}/{len(by_id)} operations.")
    if missing:
        print("  Not in snapshot (skipped):", ", ".join(missing))
    if uncovered:
        print("  No overlay defined:", ", ".join(uncovered))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
