"""Webhooks endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import WebHook

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class WebHooksEndpoint:
    """Webhooks API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def get(self) -> list[WebHook]:
        """Return all webhooks."""
        result = await self._client.get_json(self._event_id, "webhooks/get")
        return [WebHook.model_validate(x) for x in (result or [])]

    async def delete(self, id: int) -> None:
        """Delete a webhook."""
        await self._client.get(self._event_id, "webhooks/delete", {"id": id})

    async def save(self, items: list[WebHook]) -> list[int]:
        """Save webhooks and return their IDs."""
        data = [item.model_dump(by_alias=True) for item in items]
        result = await self._client.post_json(self._event_id, "webhooks/save", data=data)
        return result if result else []
