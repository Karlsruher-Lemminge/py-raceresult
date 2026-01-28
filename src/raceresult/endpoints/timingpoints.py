"""Timing points endpoint for Raceresult API.

Based on go-webapi/eventapi_timingpoints.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.timing import TimingPoint

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class TimingPointsEndpoint:
    """Timing Points API endpoint.

    Based on go-webapi/eventapi_timingpoints.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            timing_points = await event.timingpoints.get()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def get(self) -> list[TimingPoint]:
        """Get all timing points.

        Based on go-webapi/eventapi_timingpoints.go:22-33.

        Returns:
            List of all timing points
        """
        result = await self._client.get_json(self._event_id, "timingpoints/get")
        if not result:
            return []
        return [TimingPoint.model_validate(item) for item in result]

    async def get_one(self, name: str) -> TimingPoint:
        """Get a single timing point by name.

        Based on go-webapi/eventapi_timingpoints.go:36-50.

        Args:
            name: Timing point name

        Returns:
            TimingPoint object
        """
        params = {"name": name}
        result = await self._client.get_json(self._event_id, "timingpoints/get", params)
        return TimingPoint.model_validate(result)

    async def delete(self, name: str) -> None:
        """Delete a timing point.

        Based on go-webapi/eventapi_timingpoints.go:53-59.

        Args:
            name: Timing point name
        """
        params = {"name": name}
        await self._client.get(self._event_id, "timingpoints/delete", params)

    async def save(self, item: TimingPoint, old_name: str = "") -> None:
        """Save a timing point.

        Based on go-webapi/eventapi_timingpoints.go:62-68.

        Args:
            item: Timing point to save
            old_name: Old name (for renames)
        """
        params = {"oldName": old_name}
        data = item.model_dump(by_alias=True)
        await self._client.post_json(self._event_id, "timingpoints/save", params, data)
