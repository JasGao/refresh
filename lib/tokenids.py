import math

from lib.paths import TOKEN_IDS_FILE

# Planning estimate for crawl login budget (ceil(tokens/N)).
TOKENS_PER_COOKIE = 80
# Refresh daily limit per cookie (~100); used for rotation + login budget.
REFRESH_TOKENS_PER_COOKIE = 100


def load_token_ids(path=None):
    path = path or TOKEN_IDS_FILE
    with open(path, "r") as file:
        return [
            line.strip()
            for line in file
            if line.strip() and line.strip() != "tokenId"
        ]


def count_token_ids(path=None):
    return len(load_token_ids(path))


def cookies_needed(token_count, per_cookie=TOKENS_PER_COOKIE):
    if token_count <= 0:
        return 0
    return math.ceil(token_count / per_cookie)


def refresh_cookies_needed(token_count):
    return cookies_needed(token_count, per_cookie=REFRESH_TOKENS_PER_COOKIE)
