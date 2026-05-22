"""TeamScores endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import TeamScore

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class TeamScoresEndpoint:
    """Team scores API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def get(self) -> list[TeamScore]:
        """Return all team scores."""
        result = await self._client.get_json(self._event_id, "teamscores/get")
        return [TeamScore.model_validate(x) for x in (result or [])]

    async def get_one(self, id: int) -> TeamScore:
        """Return the team score with the given ID."""
        result = await self._client.get_json(self._event_id, "teamscores/get", {"id": id})
        items = [TeamScore.model_validate(x) for x in (result or [])]
        if not items:
            raise ValueError(f"team score {id} not found")
        return items[0]

    async def delete(self, id: int) -> None:
        """Delete a team score."""
        await self._client.get(self._event_id, "teamscores/delete", {"id": id})

    async def save(self, item: TeamScore) -> None:
        """Save a team score."""
        await self._client.post_json(
            self._event_id, "teamscores/save", data=item.model_dump(by_alias=True)
        )
