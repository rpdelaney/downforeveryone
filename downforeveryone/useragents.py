"""Provide a random user agent."""
import json
import os
import pathlib
import random
from typing import cast

root_dir = pathlib.Path(__file__).parent

with open(os.path.join(root_dir, "useragents.json")) as f:
    USER_AGENTS = json.load(f)


def random_agent() -> str:
    """Return a random user agent string."""
    return cast(str, random.choice(USER_AGENTS))
