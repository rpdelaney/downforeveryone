"""Checks if a website is down for everyone or just you, via isup.me.

A typical usage example when importing this module:

    import downforeveryone.isup as isup

    isup_status == isup.isitup("https://a.website")

    if isup_status == 0:
        print("down for everyone")
    elif isup_status == 1:
        print("it's just you")
    elif isup_status == 3:
        print("there was an error")
"""
import sys
import traceback
import urllib.parse as parse
from typing import Any, Dict

import requests

from . import cli, useragents

__API_URL__ = {"netloc": "https://api.downfor.cloud", "path": "httpcheck/"}
__QUERY_HEADERS__ = {
    "User-Agent": useragents.random_agent(),
    "Referer": "https://api.downfor.cloud/",
    "Origin": "https://downforeveryoneorjustme.com",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "DNT": "1",
    "Connection": "keep-alive",
}


def query_url(url: str) -> str:
    """Return a URL with isup.me API endpoint and our target.

    If the scheme is unspecified or is unsecured http, it will be coerced to
    https. Any query and fragment properties of a url will be stripped.

    Args:
        url: URL to the site to be checked

    Returns:
        The composed API endpoint URL.
    """
    o = parse.urlsplit(url)
    scheme = "https" if (not o.scheme or o.scheme == "http") else o.scheme
    query_url = parse.SplitResult(
        scheme=scheme,
        netloc=o.netloc if o.netloc else o.path,
        path="",
        query="",
        fragment="",
    )
    return (
        __API_URL__["netloc"]
        + "/"
        + f"{__API_URL__['path']}"
        + parse.urlunsplit(query_url)
    )


def handle_response(response: Dict[str, Any]) -> int:
    """Handle isup.me API response.

    Args:
        response: A dict representation of the received json response

    Returns: A status code
        0       The site is down
        1       The site is up
        3       Error state

    """
    if response.get("statusCode") == "200":
        isdown = response.get("isDown")
    else:
        isdown = None

    if isdown is True:
        print("down for everyone.")
        return 0
    elif isdown is False:
        print("just you.")
        return 1
    else:
        print(
            "There was a problem with the request. response was:\n"
            "{}".format(response),
            file=sys.stderr,
        )
        return 3


def isitup(url: str) -> int:
    """Check if a URL is up. Returns a status code.

    Args:
        url: URL to the site to be checked

    Returns: A status code
        0       The site is down
        1       The site is up
        3       Error state

    """
    r = requests.get(query_url(url), headers=__QUERY_HEADERS__,)

    return handle_response(r.json())


def main() -> None:
    """Provide the console entrypoint."""
    args = cli.parse_args()

    try:
        exit_code = isitup(args.url)
    except Exception:
        exit_code = 3
        traceback.print_exc()
    sys.exit(exit_code)
