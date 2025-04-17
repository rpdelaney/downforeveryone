"""Provide a random user agent."""

import json
import random
from pathlib import Path
from typing import cast


_ROOT_DIR = Path(__file__).parent

with Path.open(Path(_ROOT_DIR, "useragents.json")) as f:
    USER_AGENTS = json.load(f)


def random_agent() -> str:
    """Return a random user agent string."""
    return cast("str", random.choice(USER_AGENTS))  # noqa: S311
