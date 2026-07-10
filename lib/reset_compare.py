import json
import os

from lib.paths import CRAWL_OUTPUT_DIR, CRAWL_PROGRESS_FILE, CRAWL_REPORT_FILE

PROGRESS_FILE = CRAWL_PROGRESS_FILE
REPORT_FILE = CRAWL_REPORT_FILE


def reset_compare_files():
    os.makedirs(CRAWL_OUTPUT_DIR, exist_ok=True)
    with open(CRAWL_PROGRESS_FILE, "w") as file:
        json.dump({}, file, indent=2)
    with open(CRAWL_REPORT_FILE, "w") as file:
        json.dump({"outOfSync": [], "errors": []}, file, indent=2)
    return CRAWL_PROGRESS_FILE, CRAWL_REPORT_FILE
