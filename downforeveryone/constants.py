from types import MappingProxyType

from downforeveryone import useragents

API_URL = MappingProxyType(
    {
        "netloc": "https://api-prod.downfor.cloud",
        "path": "httpcheck/",
    }
)

QUERY_HEADERS = MappingProxyType(
    {
        "User-Agent": useragents.random_agent(),
        "Referer": "https://api.downfor.cloud/",
        "Origin": "https://downforeveryoneorjustme.com",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive",
    }
)
