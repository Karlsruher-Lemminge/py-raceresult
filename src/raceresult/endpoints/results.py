"""Results endpoint for Raceresult API.

Based on go-webapi/eventapi_results.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import Result

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class ResultsEndpoint:
    """Results API endpoint.

    Based on go-webapi/eventapi_results.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            results = await event.results.get()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def get(
        self,
        name: str = "",
        only_formulas: bool = False,
        only_no_formulas: bool = False,
    ) -> list[Result]:
        """Get results matching the given filters.

        Based on go-webapi/eventapi_results.go:22-38.

        Args:
            name: Name filter
            only_formulas: Only return results with formulas
            only_no_formulas: Only return results without formulas

        Returns:
            List of matching results
        """
        params = {
            "name": name,
            "onlyFormulas": only_formulas,
            "onlyNoFormulas": only_no_formulas,
        }
        result = await self._client.get_json(self._event_id, "results/get", params)
        if not result:
            return []
        return [Result.model_validate(item) for item in result]

    async def get_one(self, id: int) -> Result:
        """Get a single result by ID.

        Based on go-webapi/eventapi_results.go:41-55.

        Args:
            id: Result ID

        Returns:
            Result object
        """
        params = {"id": id}
        result = await self._client.get_json(self._event_id, "results/get", params)
        return Result.model_validate(result)

    async def delete(self, id: int) -> None:
        """Delete a result.

        Based on go-webapi/eventapi_results.go:58-64.

        Args:
            id: Result ID
        """
        params = {"id": id}
        await self._client.get(self._event_id, "results/delete", params)

    async def save(self, items: list[Result]) -> None:
        """Save results.

        Based on go-webapi/eventapi_results.go:67-70.

        Args:
            items: Results to save
        """
        data = [item.model_dump(by_alias=True) for item in items]
        await self._client.post_json(self._event_id, "results/save", data=data)
