"""Checks if a website is down for everyone or just you, via isup.me.

Usage example when importing this module:

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
import urllib.parse
from http import HTTPStatus
from json.decoder import JSONDecodeError
from typing import Any, Dict, Tuple

import requests
from requests.exceptions import RequestException

from . import cli, useragents

__API_URL__ = {
    "netloc": "https://api-prod.downfor.cloud",
    "path": "httpcheck/",
}
__QUERY_HEADERS__ = {
    "User-Agent": useragents.random_agent(),
    "Referer": "https://api.downfor.cloud/",
    "Origin": "https://downforeveryoneorjustme.com",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "DNT": "1",
    "Connection": "keep-alive",
}


def _query_url(url: str) -> str:
    """Return a URL with isup.me API endpoint and our target.

    Args:
        url: URL to the site to be checked

    Returns:
        The composed API endpoint URL.

    Raises:
        TypeError: If the url argument cannot be concatenated with a string.

    """
    return urllib.parse.urljoin(
        __API_URL__["netloc"], f"{__API_URL__['path']}" + url
    )


def _handle_response(response: Dict[str, Any]) -> Tuple[str, int]:
    """Handle isup.me API response.

    Args:
        response: A dict representation of the received json response

    Returns: A status code
        0       The site is down
        1       The site is up
        3       Error state

    """
    isdown = response.get("isDown")

    if isdown is True:
        return "down for everyone.", 0
    elif isdown is False:
        return "just you.", 1
    else:
        return (
            "There was a problem with the request. response was:\n"
            f"{response}"
        ), 3


def isitup(url: str) -> Tuple[str, int]:
    """Check if a URL is up. Returns a status code.

    Args:
        url: URL to the site to be checked

    Returns: A status code
        0       The site is down
        1       The site is up
        3       Error state

    """
    try:
        r = requests.get(
            _query_url(url),
            headers=__QUERY_HEADERS__,
        )
    except RequestException as rexc:
        title = type(rexc).__name__
        message = str(rexc)
        return (f"{title}: {message}"), 3

    if r.status_code != HTTPStatus.OK.value:
        status_name = [
            status.description
            for status in list(HTTPStatus)
            if status.value == r.status_code
        ]
        return (
            f"HTTP request failure. Status: {r.status_code} "
            f"Description: {status_name}"
        ), 3

    try:
        jsondata = r.json()
    except JSONDecodeError as jde:
        title = type(jde).__name__
        message = str(jde)
        return (f"{title}: {message}"), 3
    else:
        return _handle_response(jsondata)


def main() -> None:
    """Provide the console entrypoint."""
    args = cli.parse_args()

    try:
        message, exit_code = isitup(args.url)
    except Exception:
        exit_code = 3
        traceback.print_exc()
    else:
        output_device = sys.stderr if exit_code == 3 else sys.stdout
        print(message, file=output_device)

    sys.exit(exit_code)
