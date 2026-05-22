"""Statistics endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from raceresult.models.statistic import Aggregation, Statistics

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class StatisticsEndpoint:
    """Statistics API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def names(self) -> list[str]:
        """Return names of all statistics."""
        result = await self._client.get_json(self._event_id, "statistics/names")
        return result if result else []

    async def get(self, name: str) -> Statistics:
        """Return a statistics definition by name."""
        result = await self._client.get_json(
            self._event_id, "statistics/get", {"name": name}
        )
        return Statistics.model_validate(result)

    async def save(self, item: Statistics) -> None:
        """Save a statistics definition."""
        await self._client.post_json(
            self._event_id, "statistics/save", data=item.model_dump(by_alias=True)
        )

    async def delete(self, name: str) -> None:
        """Delete a statistics definition."""
        await self._client.get(self._event_id, "statistics/delete", {"name": name})

    async def copy(self, name: str, new_name: str) -> None:
        """Create a copy of a statistics definition."""
        await self._client.get(
            self._event_id, "statistics/copy", {"name": name, "newName": new_name}
        )

    async def rename(self, name: str, new_name: str) -> None:
        """Rename a statistics definition."""
        await self._client.get(
            self._event_id, "statistics/rename", {"name": name, "newName": new_name}
        )

    async def new(self, name: str) -> None:
        """Create a new statistics definition."""
        await self._client.get(self._event_id, "statistics/new", {"name": name})

    async def create(
        self,
        name: str,
        format: str = "pdf",
        contests: list[int] | None = None,
    ) -> bytes:
        """Render a statistics output in the given format."""
        params: dict[str, Any] = {"name": name, "format": format}
        if contests:
            params["contest"] = ",".join(str(c) for c in contests)
        return await self._client.get(self._event_id, "statistics/create", params)

    async def query(
        self,
        row: str,
        col: str,
        filter_expr: str = "",
        field: str = "",
        aggregation: Aggregation = Aggregation.COUNT,
    ) -> list[list[Any]]:
        """Execute an ad-hoc statistics query and return a 2D result table."""
        params = {
            "row": row,
            "col": col,
            "filter": filter_expr,
            "field": field,
            "aggregation": int(aggregation),
        }
        result = await self._client.get_json(self._event_id, "statistics/statistics", params)
        return result if result else []
