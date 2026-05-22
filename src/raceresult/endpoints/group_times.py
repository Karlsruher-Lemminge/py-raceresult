"""GroupTimes endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import GroupTimes

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class GroupTimesEndpoint:
    """Group/wave start times API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def get(self, ttype: str) -> GroupTimes:
        """Return group times of the given type."""
        result = await self._client.get_json(
            self._event_id, "grouptimes/get", {"type": ttype}
        )
        return GroupTimes.model_validate(result if result else {})

    async def save(self, ttype: str, item: GroupTimes) -> None:
        """Save group times."""
        params = {"type": ttype}
        await self._client.post_json(
            self._event_id, "grouptimes/save", params, item.model_dump(by_alias=True)
        )
