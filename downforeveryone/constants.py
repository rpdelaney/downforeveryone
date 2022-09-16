from types import MappingProxyType

from downforeveryone import useragents

API_URL = "https://downforeveryoneorjustme.com/api/httpcheck/{domain}"

QUERY_HEADERS = MappingProxyType(
    {
        "User-Agent": useragents.random_agent(),
        "Referer": "https://downforeveryoneorjustme.com",
        "Origin": "https://downforeveryoneorjustme.com",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive",
    }
)
