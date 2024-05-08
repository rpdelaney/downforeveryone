"""Provide a random user agent."""

import json
import random
from pathlib import Path
from typing import cast


root_dir = Path(__file__).parent

with Path.open(root_dir, "useragents.json") as f:
    USER_AGENTS = json.load(f)


def random_agent() -> str:
    """Return a random user agent string."""
    return cast(str, random.choice(USER_AGENTS))  # noqa: S311
