"""Exporters endpoint for Raceresult API.

Based on go-webapi/eventapi_exporters.go.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from raceresult.models.types import RRDecimal

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class Exporter(BaseModel):
    """Exporter definition.

    Based on go-model/model.go:197-217.
    """

    id: int = Field(default=0, alias="ID")
    name: str = Field(default="", alias="Name")
    filter: str = Field(default="", alias="Filter")
    trigger_timing_point: str = Field(default="", alias="TriggerTimingPoint")
    trigger_split: str = Field(default="", alias="TriggerSplit")
    trigger_result_id: int = Field(default=0, alias="TriggerResultID")
    destination_type: str = Field(default="", alias="DestinationType")
    destination: str = Field(default="", alias="Destination")
    data: str = Field(default="", alias="Data")
    mtb: int = Field(default=0, alias="MTB")
    mql: int = Field(default=0, alias="MQL")
    line_ending: str = Field(default="", alias="LineEnding")
    start_paused: bool = Field(default=False, alias="StartPaused")
    ignore_before: RRDecimal = Field(default=Decimal(0), alias="IgnoreBefore")
    ignore_after: RRDecimal = Field(default=Decimal(0), alias="IgnoreAfter")
    encoding: str = Field(default="", alias="Encoding")
    connect_msg: str = Field(default="", alias="ConnectMsg")
    order_pos: int = Field(default=0, alias="OrderPos")

    model_config = {"populate_by_name": True}


class ExportersEndpoint:
    """Exporters API endpoint.

    Based on go-webapi/eventapi_exporters.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            exporters = await event.exporters.get()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def get(self) -> list[Exporter]:
        """Get all exporters.

        Based on go-webapi/eventapi_exporters.go:23-34.

        Returns:
            List of all exporters
        """
        result = await self._client.get_json(self._event_id, "exporters/get")
        if not result:
            return []
        return [Exporter.model_validate(item) for item in result]

    async def get_one(self, id: int) -> Exporter:
        """Get a single exporter by ID.

        Based on go-webapi/eventapi_exporters.go:37-54.

        Args:
            id: Exporter ID

        Returns:
            Exporter object

        Raises:
            ValueError: If exporter not found
        """
        params = {"id": id}
        result = await self._client.get_json(self._event_id, "exporters/get", params)
        if not result:
            raise ValueError(f"Exporter with ID {id} not found")
        if isinstance(result, list):
            if len(result) == 0:
                raise ValueError(f"Exporter with ID {id} not found")
            return Exporter.model_validate(result[0])
        return Exporter.model_validate(result)

    async def delete(self, id: int) -> None:
        """Delete an exporter.

        Based on go-webapi/eventapi_exporters.go:57-63.

        Args:
            id: Exporter ID
        """
        params = {"id": id}
        await self._client.get(self._event_id, "exporters/delete", params)

    async def save(self, item: Exporter) -> int:
        """Save an exporter.

        Based on go-webapi/eventapi_exporters.go:66-77.

        Args:
            item: Exporter to save

        Returns:
            Exporter ID
        """
        data = item.model_dump(by_alias=True)
        result = await self._client.post_json(self._event_id, "exporters/save", data=data)
        return int(result) if result is not None else 0
