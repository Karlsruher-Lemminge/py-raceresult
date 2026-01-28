"""Timing point rules endpoint for Raceresult API.

Based on go-webapi/eventapi_timingpointrules.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.timing import TimingPointRule

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class TimingPointRulesEndpoint:
    """Timing Point Rules API endpoint.

    Based on go-webapi/eventapi_timingpointrules.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            rules = await event.timingpointrules.get()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def get(self) -> list[TimingPointRule]:
        """Get all timing point rules.

        Based on go-webapi/eventapi_timingpointrules.go:22-33.

        Returns:
            List of all timing point rules
        """
        result = await self._client.get_json(self._event_id, "timingpointrules/get")
        if not result:
            return []
        return [TimingPointRule.model_validate(item) for item in result]

    async def get_one(self, id: int) -> TimingPointRule:
        """Get a single timing point rule by ID.

        Based on go-webapi/eventapi_timingpointrules.go:36-50.

        Args:
            id: Timing point rule ID

        Returns:
            TimingPointRule object
        """
        params = {"id": id}
        result = await self._client.get_json(self._event_id, "timingpointrules/get", params)
        return TimingPointRule.model_validate(result)

    async def delete(self, id: int) -> None:
        """Delete a timing point rule.

        Based on go-webapi/eventapi_timingpointrules.go:53-59.

        Args:
            id: Timing point rule ID
        """
        params = {"id": id}
        await self._client.get(self._event_id, "timingpointrules/delete", params)

    async def save(self, items: list[TimingPointRule]) -> list[int]:
        """Save timing point rules.

        Based on go-webapi/eventapi_timingpointrules.go:62-68.

        Args:
            items: Timing point rules to save

        Returns:
            List of saved timing point rule IDs
        """
        data = [item.model_dump(by_alias=True) for item in items]
        result = await self._client.post_json(
            self._event_id, "timingpointrules/save", data=data
        )
        return result if result else []
