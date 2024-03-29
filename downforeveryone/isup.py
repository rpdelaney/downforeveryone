"""Checks if a website is down for everyone or just you, via isup.me.

Usage example when importing this module:

    import downforeveryone.isup as isup

    isup_message, isup_status == isup.isitup("https://a.website")

    if isup_status == 0:
        print("down for everyone")
    elif isup_status == 1:
        print("it's just you")
    elif isup_status == 3:
        print("there was an error")
"""
import sys
import traceback
from http import HTTPStatus
from json.decoder import JSONDecodeError
from typing import Any, Dict, Tuple

import requests
from requests.exceptions import RequestException, Timeout

from downforeveryone import cli
from downforeveryone.constants import API_URL, QUERY_HEADERS


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

    return (
        f"There was a problem with the request. response was:\n{response}"
    ), 3


def isitup(url: str) -> Tuple[str, int]:
    """Check if a URL is up. Returns a status code.

    Args:
        url: URL to the site to be checked

    Returns: A human-readable status message, and a status code
        0       The site is down
        1       The site is up
        3       Error state

    """
    try:
        response = requests.get(
            API_URL.format(domain=url),
            headers=QUERY_HEADERS,
        )
    except Timeout:
        return "Network timeout.", 3
    except RequestException as rexc:
        title = type(rexc).__name__
        message = str(rexc) if str(rexc) else "Unexpected error occurred."
        return (f"{title}: {message}"), 3

    if response.status_code != HTTPStatus.OK.value:
        status_name = HTTPStatus(response.status_code).description
        return (f"{response.status_code} {status_name}"), 3

    try:
        jsondata = response.json()
    except JSONDecodeError as jde:
        title = type(jde).__name__
        message = str(jde)
        return (f"{title}: {message}"), 3

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
