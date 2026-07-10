import os

from lib.paths import PROJECT_ROOT

ENV_FILE = os.path.join(PROJECT_ROOT, ".env")


def load_dotenv(path=None):
    """Load KEY=VALUE pairs from .env into os.environ (does not override existing)."""
    env_path = path or ENV_FILE
    if not os.path.exists(env_path):
        return
    with open(env_path, "r") as file:
        for raw in file:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                value = value[1:-1]
            if key and key not in os.environ:
                os.environ[key] = value
