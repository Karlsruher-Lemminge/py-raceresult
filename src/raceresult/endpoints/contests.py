"""Contests endpoint for Raceresult API.

Based on go-webapi/eventapi_contests.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import Contest

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class ContestsEndpoint:
    """Contests API endpoint.

    Based on go-webapi/eventapi_contests.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            contests = await event.contests.get()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def pdf(self) -> bytes:
        """Get PDF with all contests.

        Based on go-webapi/eventapi_contests.go:22-24.

        Returns:
            PDF file as bytes
        """
        return await self._client.get(self._event_id, "contests/pdf")

    async def get(self) -> list[Contest]:
        """Get all contests.

        Based on go-webapi/eventapi_contests.go:44-55.

        Returns:
            List of all contests
        """
        result = await self._client.get_json(self._event_id, "contests/get")
        if not result:
            return []
        return [Contest.model_validate(item) for item in result]

    async def get_one(self, id: int) -> Contest:
        """Get a single contest by ID.

        Based on go-webapi/eventapi_contests.go:27-41.

        Args:
            id: Contest ID

        Returns:
            Contest object
        """
        params = {"id": id}
        result = await self._client.get_json(self._event_id, "contests/get", params)
        return Contest.model_validate(result)

    async def delete(self, id: int) -> None:
        """Delete a contest.

        Based on go-webapi/eventapi_contests.go:58-64.

        Args:
            id: Contest ID
        """
        params = {"id": id}
        await self._client.get(self._event_id, "contests/delete", params)

    async def save(self, contest: Contest, old_id: int = 0) -> int:
        """Save a contest.

        Based on go-webapi/eventapi_contests.go:67-81.

        Args:
            contest: Contest to save
            old_id: Old contest ID (for updates)

        Returns:
            New contest ID
        """
        params = {"oldID": old_id}
        data = contest.model_dump(by_alias=True)
        result = await self._client.post_json(
            self._event_id, "contests/save", params, data
        )
        return int(result)
