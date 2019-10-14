"""
A command-line tool to call the down for everyone API

Exit status:

    0       The site is down
    1       The site is up
    3       There was a problem with the API request, or an unhandled
                exception
"""
import sys
import traceback
import urllib.parse

import requests

from . import cli
from . import useragents


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
    return urllib.parse.urljoin(
        __API_URL__["netloc"], f"{__API_URL__['path']}" + url
    )


def handle_response(response: dict) -> int:
    isdown = response.get("isDown")

    if isdown is True:
        print("down for everyone.")
        return 0
    elif isdown is False:
        print("just you.")
        return 1
    else:
        print(
            "There was a problem with the request. response was:\n"
            "{}".format(response)
        )
        return 3


def isitup(url: str) -> int:
    """
    Checks if a URL is up. Returns a status code.

    0       The site is down
    1       The site is up
    3       Error state
    """
    r = requests.get(query_url(url), headers=__QUERY_HEADERS__,)

    return handle_response(r.json())


def main() -> None:
    args = cli.parse_args()

    try:
        exit_code = isitup(args.url)
    except Exception:
        exit_code = 3
        traceback.print_exc()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
