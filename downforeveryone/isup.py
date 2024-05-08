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
from typing import Any

import requests
from requests.exceptions import RequestException, Timeout

from downforeveryone import cli
from downforeveryone.constants import API_URL, QUERY_HEADERS, ExitCodes


def _handle_response(response: dict[str, Any]) -> tuple[str, int]:
    """Handle isup.me API response.

    Args:
    ----
        response: A dict representation of the received json response

    Returns: A status code
        0       The site is down
        1       The site is up
        3       Error state

    """
    isdown = response.get("isDown")

    if isdown is True:
        return "down for everyone.", ExitCodes.EVERYONE
    if isdown is False:
        return "just you.", ExitCodes.YOU

    return (
        f"There was a problem with the request. response was:\n{response}"
    ), ExitCodes.FAIL


def isitup(url: str) -> tuple[str, int]:  # noqa: C901
    """Check if a URL is up. Returns a status code.

    Args:
    ----
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
            timeout=5,
        )
    except Timeout:
        return "Network timeout.", ExitCodes.FAIL
    except RequestException as rexc:
        title = type(rexc).__name__
        message = str(rexc) if str(rexc) else "Unexpected error occurred."
        return (f"{title}: {message}"), ExitCodes.FAIL

    if response.status_code != HTTPStatus.OK.value:
        status_name = HTTPStatus(response.status_code).description
        return (f"{response.status_code} {status_name}"), ExitCodes.FAIL

    try:
        jsondata = response.json()
    except JSONDecodeError as jde:
        title = type(jde).__name__
        message = str(jde)
        return (f"{title}: {message}"), ExitCodes.FAIL

    return _handle_response(jsondata)


def main() -> None:
    """Provide the console entrypoint."""
    args = cli.parse_args()

    try:
        message, exit_code = isitup(args.url)
    except Exception:  # noqa: BLE001
        message, exit_code = (
            "An unhandled exception occurred.",
            ExitCodes.FAIL,
        )
        traceback.print_exc()

    device = sys.stderr if exit_code == ExitCodes.FAIL else sys.stdout

    print(message, file=device)

    sys.exit(exit_code)
