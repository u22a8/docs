#!/usr/bin/env python3
"""OpenAPI freshness check: docs snapshot vs the live /v1 spec (U22-152).

The docs snapshot ``api-reference/openapi.json`` is review-gated, not a live
pointer — a new endpoint must not appear unreviewed and leak. This script
detects when the snapshot has drifted from the live contract so a human (or the
``/police`` sweep) can refresh it deliberately.

It compares **structure only** — the set of operations (method + path), their
parameters, request/response schema shapes, and ``components.schemas`` property
sets. Prose (``description``/``summary``/``title``), examples, and the docs-only
``x-mint`` overlays are stripped before comparison, because the snapshot is
intentionally sanitized and example-decorated relative to live (see
``scripts/apply_overlays.py``). Only a real contract change counts as drift.

Usage:
    python3 scripts/openapi_freshness.py                  # fetch live, diff vs snapshot
    python3 scripts/openapi_freshness.py --live-file f    # diff vs a local spec (no network)
    python3 scripts/openapi_freshness.py --json           # machine-readable summary

Exit codes:
    0  snapshot is structurally in sync with live
    1  drift found (operations or schemas added/removed/changed)
    2  could not obtain the live spec (network/parse error) — check skipped

Stdlib only; no third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SNAPSHOT = REPO_ROOT / "api-reference" / "openapi.json"
DEFAULT_LIVE_URL = "https://u22a8.ai/v1/openapi.json"

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
# Cosmetic / docs-only keys stripped before structural comparison.
COSMETIC_KEYS = {"description", "summary", "title", "example", "examples", "externalDocs"}


def strip_cosmetic(node: Any) -> Any:
    """Recursively drop prose, examples, and ``x-*`` extensions (incl. x-mint)."""
    if isinstance(node, dict):
        return {
            k: strip_cosmetic(v)
            for k, v in node.items()
            if k not in COSMETIC_KEYS and not k.startswith("x-")
        }
    if isinstance(node, list):
        return [strip_cosmetic(v) for v in node]
    return node


def load_snapshot(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_live(url: str, timeout: float = 20.0) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "u22a8-docs-freshness/1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (trusted host)
        return json.loads(resp.read().decode("utf-8"))


def operations(spec: dict[str, Any]) -> dict[str, Any]:
    """Map ``"METHOD /path"`` -> stripped operation object."""
    ops: dict[str, Any] = {}
    for path, item in spec.get("paths", {}).items():
        if not isinstance(item, dict):
            continue
        for method, op in item.items():
            if method.lower() in HTTP_METHODS:
                ops[f"{method.upper()} {path}"] = strip_cosmetic(op)
    return ops


def schemas(spec: dict[str, Any]) -> dict[str, Any]:
    raw = spec.get("components", {}).get("schemas", {})
    return {name: strip_cosmetic(body) for name, body in raw.items()}


def _canon(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True)


def _op_change_reason(live_op: dict[str, Any], snap_op: dict[str, Any]) -> str:
    reasons: list[str] = []
    live_params = {(p.get("in"), p.get("name")) for p in live_op.get("parameters", [])}
    snap_params = {(p.get("in"), p.get("name")) for p in snap_op.get("parameters", [])}
    if live_params != snap_params:
        added = sorted(f"{i}:{n}" for i, n in live_params - snap_params)
        removed = sorted(f"{i}:{n}" for i, n in snap_params - live_params)
        reasons.append(f"params +{added} -{removed}")
    live_resp = set((live_op.get("responses") or {}).keys())
    snap_resp = set((snap_op.get("responses") or {}).keys())
    if live_resp != snap_resp:
        reasons.append(f"responses +{sorted(live_resp - snap_resp)} -{sorted(snap_resp - live_resp)}")
    elif _canon(live_op.get("responses")) != _canon(snap_op.get("responses")):
        # Same status codes, but a response body schema changed — report it
        # regardless of whether params/requestBody also changed.
        reasons.append("response shape")
    if _canon(live_op.get("requestBody")) != _canon(snap_op.get("requestBody")):
        reasons.append("requestBody")
    return "; ".join(reasons) or "structural change"


def _schema_change_reason(live_s: dict[str, Any], snap_s: dict[str, Any]) -> str:
    live_props = set((live_s.get("properties") or {}).keys())
    snap_props = set((snap_s.get("properties") or {}).keys())
    reasons: list[str] = []
    if live_props != snap_props:
        reasons.append(f"properties +{sorted(live_props - snap_props)} -{sorted(snap_props - live_props)}")
    live_req = set(live_s.get("required") or [])
    snap_req = set(snap_s.get("required") or [])
    if live_req != snap_req:
        reasons.append(f"required +{sorted(live_req - snap_req)} -{sorted(snap_req - live_req)}")
    return "; ".join(reasons) or "structural change"


def diff(live: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    live_ops, snap_ops = operations(live), operations(snapshot)
    live_sch, snap_sch = schemas(live), schemas(snapshot)

    ops_changed = [
        {"op": k, "reason": _op_change_reason(live_ops[k], snap_ops[k])}
        for k in sorted(live_ops.keys() & snap_ops.keys())
        if _canon(live_ops[k]) != _canon(snap_ops[k])
    ]
    sch_changed = [
        {"schema": k, "reason": _schema_change_reason(live_sch[k], snap_sch[k])}
        for k in sorted(live_sch.keys() & snap_sch.keys())
        if _canon(live_sch[k]) != _canon(snap_sch[k])
    ]
    return {
        "operations_added": sorted(live_ops.keys() - snap_ops.keys()),
        "operations_removed": sorted(snap_ops.keys() - live_ops.keys()),
        "operations_changed": ops_changed,
        "schemas_added": sorted(live_sch.keys() - snap_sch.keys()),
        "schemas_removed": sorted(snap_sch.keys() - live_sch.keys()),
        "schemas_changed": sch_changed,
    }


def has_drift(report: dict[str, Any]) -> bool:
    return any(report[k] for k in report)


def print_report(report: dict[str, Any]) -> None:
    labels = {
        "operations_added": "Operations present in live but missing from the snapshot",
        "operations_removed": "Operations in the snapshot but gone from live",
        "operations_changed": "Operations whose shape changed",
        "schemas_added": "Schemas added in live",
        "schemas_removed": "Schemas removed from live",
        "schemas_changed": "Schemas whose shape changed",
    }
    for key, label in labels.items():
        items = report[key]
        if not items:
            continue
        print(f"\n{label}:")
        for item in items:
            if isinstance(item, dict):
                k = item.get("op") or item.get("schema")
                print(f"  - {k}  ({item['reason']})")
            else:
                print(f"  - {item}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Diff the docs OpenAPI snapshot against the live spec.")
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--live-url", default=DEFAULT_LIVE_URL)
    parser.add_argument("--live-file", type=Path, help="Compare against a local spec instead of fetching.")
    parser.add_argument("--json", action="store_true", help="Emit the diff as JSON.")
    args = parser.parse_args(argv)

    try:
        snapshot = load_snapshot(args.snapshot)
    except (OSError, json.JSONDecodeError) as e:
        print(f"freshness: cannot read snapshot {args.snapshot}: {e}", file=sys.stderr)
        return 2

    try:
        if args.live_file:
            live = load_snapshot(args.live_file)
            source = str(args.live_file)
        else:
            live = fetch_live(args.live_url)
            source = args.live_url
    except urllib.error.HTTPError as e:
        # A 4xx/5xx means the URL itself is wrong/broken — distinct from a
        # network outage. Still exit 2 (skip), but say so loudly.
        print(f"freshness: live spec {args.live_url} returned HTTP {e.code}; "
              f"the URL may have moved. Check skipped.", file=sys.stderr)
        return 2
    except (urllib.error.URLError, OSError, json.JSONDecodeError, TimeoutError) as e:
        print(f"freshness: could not obtain live spec ({e}); check skipped.", file=sys.stderr)
        return 2

    report = diff(live, snapshot)

    if args.json:
        print(json.dumps(report, indent=2))
    if has_drift(report):
        if not args.json:
            print(f"freshness: snapshot has drifted from {source}.")
            print_report(report)
            print("\nRefresh deliberately: re-fetch the live spec into the snapshot, "
                  "re-apply overlays, review the diff, and re-run the leak scan before publishing.")
        return 1

    if not args.json:
        print(f"freshness: snapshot is structurally in sync with {source}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
