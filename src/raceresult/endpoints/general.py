"""General API endpoint for Raceresult."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class GeneralEndpoint:
    """General (non-event-specific) API endpoint.

    Based on go-webapi/api_general.go.
    """

    def __init__(self, client: RaceResultClient):
        self._client = client

    async def fonts(self) -> list[str]:
        """Return the list of fonts supported by the server."""
        result = await self._client.get_json(None, "fonts")
        return result if result else []

    async def app_version(self) -> str:
        """Return the web server version string."""
        result = await self._client.get(None, "appversion")
        return result.decode("utf-8")

    async def translate(
        self, items: list[str], from_english: bool = True, lang: str = ""
    ) -> list[str]:
        """Translate field names or expressions between English and the target language."""
        params = {"fromEnglish": from_english, "lang": lang}
        result = await self._client.post_json(None, "translate2", params, items)
        return result if result else []

    async def get_lang_item(self, name: str, lang: str = "") -> str:
        """Return a single translation text item."""
        params = {"name": name, "lang": lang}
        result = await self._client.get(None, "getlangitem", params)
        return result.decode("utf-8")
