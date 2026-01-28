"""Data endpoint for Raceresult API.

Based on go-webapi/eventapi_data.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class DataEndpoint:
    """Data API endpoint for querying participant data.

    Based on go-webapi/eventapi_data.go.

    Example:
        async with RaceResultClient() as client:
            await client.login(api_key="...")
            data = DataEndpoint(client, "event123")
            count = await data.count()
            results = await data.list(["Bib", "Firstname", "Lastname"])
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def count(self, filter_expr: str = "") -> int:
        """Get count of records matching filter.

        Based on go-webapi/eventapi_data.go:22-35.

        Args:
            filter_expr: Filter expression

        Returns:
            Number of matching records
        """
        params = {"filter": filter_expr}
        result = await self._client.get_json(self._event_id, "data/count", params)
        return int(result) if result is not None else 0

    async def list(
        self,
        fields: list[str],
        filter_expr: str = "",
        sort: list[str] | None = None,
        limit_from: int = 0,
        limit_to: int = 0,
        groups: list[str] | None = None,
        multiplier_field: str = "",
        selector_result: str = "",
    ) -> list[list[Any]]:
        """Get arbitrary records.

        Based on go-webapi/eventapi_data.go:38-73.

        Args:
            fields: Field expressions to retrieve
            filter_expr: Filter expression
            sort: Sort expressions
            limit_from: Starting row (0-based)
            limit_to: Ending row (exclusive, 0 for no limit)
            groups: Group by expressions
            multiplier_field: Field for row multiplication
            selector_result: Result selector

        Returns:
            List of rows, each row is a list of field values
        """
        params: dict[str, Any] = {
            "fields": ",".join(fields),
            "filter": filter_expr,
            "limitFrom": limit_from,
            "limitTo": limit_to,
            "multiplierField": multiplier_field,
            "selectorResult": selector_result,
            "listFormat": "JSON",
        }
        if sort:
            params["sort"] = ",".join(sort)
        if groups:
            params["groups"] = ",".join(groups)

        result = await self._client.get_json(self._event_id, "data/list", params)
        return result if result else []

    async def transformation(
        self,
        col_field: str,
        row_fields: list[str],
        filter_expr: str = "",
        field: str = "",
        mode: int = 0,
        sort_by_value: bool = False,
    ) -> list[list[Any]]:
        """Create min/max/sum/count/avg statistics.

        Based on go-webapi/eventapi_data.go:76-108.

        Args:
            col_field: Column field expression
            row_fields: Row field expressions
            filter_expr: Filter expression
            field: Field for aggregation
            mode: Aggregation mode (0=count, 1=sum, 2=avg, 3=min, 4=max)
            sort_by_value: Sort by aggregated value

        Returns:
            Transformation result matrix
        """
        params: dict[str, Any] = {
            "colField": col_field,
            "rowFields": ",".join(row_fields),
            "filter": filter_expr,
            "field": field,
            "mode": mode,
            "sortByValue": sort_by_value,
        }
        result = await self._client.get_json(self._event_id, "data/transformation", params)
        return result if result else []
