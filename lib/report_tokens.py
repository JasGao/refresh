import json
import os

from lib.paths import CRAWL_REPORT_FILE


def _token_ids(entries):
    return [entry["tokenId"] for entry in entries if entry.get("tokenId")]


def load_report(report_path=CRAWL_REPORT_FILE):
    if not os.path.exists(report_path):
        return {"outOfSync": [], "errors": []}
    with open(report_path, "r") as file:
        return json.load(file)


def refresh_targets_from_report(report):
    """Out-of-sync tokens plus crawl errors (deduped; out-of-sync first)."""
    seen = set()
    tokens = []
    for token_id in _token_ids(report.get("outOfSync", [])) + _token_ids(report.get("errors", [])):
        if token_id not in seen:
            seen.add(token_id)
            tokens.append(token_id)
    return tokens


def refresh_target_counts(report_path=CRAWL_REPORT_FILE):
    report = load_report(report_path)
    tokens = refresh_targets_from_report(report)
    out_of_sync_ids = set(_token_ids(report.get("outOfSync", [])))
    return {
        "out_of_sync": len([token_id for token_id in tokens if token_id in out_of_sync_ids]),
        "errors": len([token_id for token_id in tokens if token_id not in out_of_sync_ids]),
        "total": len(tokens),
    }


def load_refresh_token_ids(report_path=CRAWL_REPORT_FILE):
    return refresh_targets_from_report(load_report(report_path))
