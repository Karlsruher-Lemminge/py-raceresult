"""Synchronization endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class SynchronizationEndpoint:
    """Synchronization API endpoint (online server only)."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def is_checked_out(self) -> bool:
        """Return True if the file currently has checked-out status."""
        result = await self._client.get_json(
            self._event_id, "synchronization/isCheckedOut"
        )
        return bool(result)

    async def set_checked_in(self) -> None:
        """Set the event status to checked-in (use to recover a lost checkout)."""
        await self._client.get(self._event_id, "synchronization/setCheckedIn")
