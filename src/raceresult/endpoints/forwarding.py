"""Forwarding endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import ForwardingInfo

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class ForwardingEndpoint:
    """Online forwarding API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def active(self) -> bool:
        """Return True if forwarding is currently running."""
        result = await self._client.get_json(self._event_id, "forwarding/active")
        return bool(result)

    async def start(self, hostname: str, eventid: str, auth_token: str) -> None:
        """Start forwarding to a remote server."""
        params = {"hostname": hostname, "eventid": eventid, "authToken": auth_token}
        await self._client.get(self._event_id, "forwarding/start", params)

    async def restart(self) -> None:
        """Restart forwarding with the previous settings."""
        await self._client.get(self._event_id, "forwarding/restart")

    async def stop(self) -> None:
        """Stop the forwarding process."""
        await self._client.get(self._event_id, "forwarding/stop")

    async def info(self) -> ForwardingInfo:
        """Return statistics about the forwarding connection."""
        result = await self._client.get_json(self._event_id, "forwarding/info")
        return ForwardingInfo.model_validate(result if result else {})
