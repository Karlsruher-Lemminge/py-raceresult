"""Backup endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import ForwardingInfo

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class BackupEndpoint:
    """Backup API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def active(self) -> bool:
        """Return True if backup is currently running."""
        result = await self._client.get_json(self._event_id, "backup/active")
        return bool(result)

    async def start(self, hostname: str, filename: str) -> None:
        """Start the backup process."""
        params = {"hostname": hostname, "filename": filename}
        await self._client.get(self._event_id, "backup/start", params)

    async def restart(self) -> None:
        """Restart the backup process with previous settings."""
        await self._client.get(self._event_id, "backup/restart")

    async def stop(self) -> None:
        """Stop the backup process."""
        await self._client.get(self._event_id, "backup/stop")

    async def info(self) -> ForwardingInfo:
        """Return statistics about the backup process."""
        result = await self._client.get_json(self._event_id, "backup/info")
        return ForwardingInfo.model_validate(result if result else {})
