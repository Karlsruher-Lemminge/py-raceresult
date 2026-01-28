"""History endpoint for Raceresult API.

Based on go-webapi/eventapi_history.go.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from raceresult.models.types import RRDateTime
from raceresult.endpoints.participants import Identifier

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class HistoryEntry(BaseModel):
    """History entry.

    Based on go-model/model.go:225-236.
    """

    id: int = Field(default=0, alias="ID")
    bib: int = Field(default=0, alias="Bib")
    part_id: int = Field(default=0, alias="PartID")
    date_time: RRDateTime = Field(default=None, alias="DateTime")
    field_name: str = Field(default="", alias="FieldName")
    old_value: Any = Field(default=None, alias="OldValue")
    new_value: Any = Field(default=None, alias="NewValue")
    user: str = Field(default="", alias="User")
    application: str = Field(default="", alias="Application")

    model_config = {"populate_by_name": True}


class HistoryEndpoint:
    """History API endpoint.

    Based on go-webapi/eventapi_history.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            history = await event.history.get(Identifier.by_bib(123))
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def get(self, identifier: Identifier) -> list[HistoryEntry]:
        """Get history entries matching the given filters.

        Based on go-webapi/eventapi_history.go:23-37.

        Args:
            identifier: Participant identifier

        Returns:
            List of history entries
        """
        params = {identifier.name: identifier.value}
        result = await self._client.get_json(self._event_id, "history/get", params)
        if not result:
            return []
        return [HistoryEntry.model_validate(item) for item in result]

    async def excel_export(
        self,
        identifier: Identifier,
        lang: str = "",
    ) -> bytes:
        """Export history as CSV file.

        Based on go-webapi/eventapi_history.go:40-46.

        Args:
            identifier: Participant identifier
            lang: Language code

        Returns:
            CSV file as bytes
        """
        params = {
            identifier.name: identifier.value,
            "lang": lang,
        }
        return await self._client.get(self._event_id, "history/excelexport", params)

    async def delete(
        self,
        identifier: Identifier,
        contest: int = 0,
        field: str = "",
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        filter_expr: str = "",
    ) -> None:
        """Delete history entries matching the given filters.

        Based on go-webapi/eventapi_history.go:49-60.

        Args:
            identifier: Participant identifier
            contest: Contest ID filter
            field: Field name filter
            date_from: Date from filter
            date_to: Date to filter
            filter_expr: Filter expression
        """
        params: dict[str, Any] = {
            identifier.name: identifier.value,
            "contest": contest,
            "field": field,
            "filter": filter_expr,
        }
        if date_from is not None:
            params["dateFrom"] = date_from.isoformat()
        if date_to is not None:
            params["dateTo"] = date_to.isoformat()
        await self._client.get(self._event_id, "history/delete", params)

    async def count(
        self,
        identifier: Identifier,
        contest: int = 0,
        field: str = "",
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        filter_expr: str = "",
    ) -> int:
        """Count history entries matching the given filters.

        Based on go-webapi/eventapi_history.go:63-80.

        Args:
            identifier: Participant identifier
            contest: Contest ID filter
            field: Field name filter
            date_from: Date from filter
            date_to: Date to filter
            filter_expr: Filter expression

        Returns:
            Count of matching entries
        """
        params: dict[str, Any] = {
            identifier.name: identifier.value,
            "contest": contest,
            "field": field,
            "filter": filter_expr,
        }
        if date_from is not None:
            params["dateFrom"] = date_from.isoformat()
        if date_to is not None:
            params["dateTo"] = date_to.isoformat()
        result = await self._client.get_json(self._event_id, "history/count", params)
        return int(result) if result is not None else 0
