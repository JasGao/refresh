import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCOUNTS_DIR = os.path.join(PROJECT_ROOT, "accounts")
ACCOUNTS_FILE = os.path.join(ACCOUNTS_DIR, "accounts.json")
ACCOUNT_STATE_FILE = os.path.join(ACCOUNTS_DIR, "state.json")

CRAWL_DIR = os.path.join(PROJECT_ROOT, "crawl")
TOKEN_IDS_FILE = os.path.join(PROJECT_ROOT, "tokens.csv")
CRAWL_OUTPUT_DIR = os.path.join(CRAWL_DIR, "output")
CRAWL_PROGRESS_FILE = os.path.join(CRAWL_OUTPUT_DIR, "progress.json")
CRAWL_REPORT_FILE = os.path.join(CRAWL_OUTPUT_DIR, "report.json")

REFRESH_METADATA_DIR = os.path.join(PROJECT_ROOT, "refresh-metadata")
REFRESH_SCRIPT = os.path.join(REFRESH_METADATA_DIR, "refresh.py")

# Legacy filenames (for one-time migration)
LEGACY_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "refresh-metadata-output")
LEGACY_STATE_FILE = os.path.join(LEGACY_OUTPUT_DIR, "bscscan-account-state.json")
LEGACY_PROGRESS_FILE = os.path.join(LEGACY_OUTPUT_DIR, "bscscan-compare-progress.json")
LEGACY_REPORT_FILE = os.path.join(LEGACY_OUTPUT_DIR, "bscscan-compare-report.json")
LEGACY_ACCOUNTS_FILE = os.path.join(ACCOUNTS_DIR, "bscscan-accounts.json")
LEGACY_TOKEN_IDS_FILE = os.path.join(CRAWL_DIR, "tokenids-check-diff.csv")
LEGACY_TOKENS_CSV = os.path.join(CRAWL_DIR, "tokens.csv")


def migrate_legacy_paths():
    """Move files from the old layout if the new paths do not exist yet."""
    os.makedirs(CRAWL_OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(ACCOUNTS_FILE) and os.path.exists(LEGACY_ACCOUNTS_FILE):
        os.replace(LEGACY_ACCOUNTS_FILE, ACCOUNTS_FILE)

    if not os.path.exists(ACCOUNT_STATE_FILE) and os.path.exists(LEGACY_STATE_FILE):
        os.replace(LEGACY_STATE_FILE, ACCOUNT_STATE_FILE)

    if not os.path.exists(TOKEN_IDS_FILE) and os.path.exists(LEGACY_TOKENS_CSV):
        os.replace(LEGACY_TOKENS_CSV, TOKEN_IDS_FILE)

    if not os.path.exists(TOKEN_IDS_FILE) and os.path.exists(LEGACY_TOKEN_IDS_FILE):
        os.replace(LEGACY_TOKEN_IDS_FILE, TOKEN_IDS_FILE)

    if not os.path.exists(CRAWL_PROGRESS_FILE) and os.path.exists(LEGACY_PROGRESS_FILE):
        os.replace(LEGACY_PROGRESS_FILE, CRAWL_PROGRESS_FILE)

    if not os.path.exists(CRAWL_REPORT_FILE) and os.path.exists(LEGACY_REPORT_FILE):
        os.replace(LEGACY_REPORT_FILE, CRAWL_REPORT_FILE)
