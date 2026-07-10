def banner(title):
    width = max(50, len(title) + 6)
    print(f"\n{'═' * width}")
    print(f"  {title}")
    print(f"{'═' * width}")


def step(number, title):
    print(f"\n── Step {number}: {title} {'─' * max(0, 40 - len(title))}")


def substep(title):
    print(f"\n  ▸ {title}")


def kv(key, value, indent=2):
    print(f"{' ' * indent}{key:<18} {value}")


def ok(message, indent=2):
    print(f"{' ' * indent}✓ {message}")


def warn(message, indent=2):
    print(f"{' ' * indent}⚠ {message}")


def fail(message, indent=2):
    print(f"{' ' * indent}✗ {message}")


def info(message, indent=2):
    print(f"{' ' * indent}· {message}")


def progress(current, total, detail, indent=2):
    print(f"{' ' * indent}[{current}/{total}] {detail}")


def summary(title, rows):
    print(f"\n── {title} {'─' * max(0, 36 - len(title))}")
    for key, value in rows:
        kv(key, value)


def short_token(token_id, tail=10):
    text = str(token_id)
    return text if len(text) <= tail + 1 else f"…{text[-tail:]}"
