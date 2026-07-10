"""Shared page-state detection for Cloudflare challenges and rate limits.

Used by crawl (HTML strings), refresh, and login (Selenium page source).
"""

import re

CLOUDFLARE_RE = re.compile(
    r"Just a moment|cf-mitigated|Attention Required|challenge-platform", re.I
)

RATE_LIMIT_PHRASES = (
    "surpassed the daily limit",
    "too many requests",
    "rate limit",
)


def is_cloudflare_html(html):
    """True if the page HTML looks like a Cloudflare interstitial."""
    return bool(CLOUDFLARE_RE.search(html))


def is_rate_limited_text(text):
    """True if the page text signals a BscScan daily/rate limit."""
    lowered = text.lower()
    return any(phrase in lowered for phrase in RATE_LIMIT_PHRASES)
