"""Raw data endpoint for Raceresult API.

Based on go-webapi/eventapi_rawdata.go.
"""

from __future__ import annotations

import json
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field, field_validator

from raceresult.models.timing import RawData
from raceresult.models.types import RRDecimal
from raceresult.endpoints.participants import Identifier

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class RawDataFilter(BaseModel):
    """Filter for raw data queries.

    Based on go-model/model.go:301-324.
    """

    id: list[int] | None = Field(default=None, alias="ID")
    min_id: int = Field(default=0, alias="MinID")
    max_id: int = Field(default=0, alias="MaxID")
    timing_point: list[str] | None = Field(default=None, alias="TimingPoint")
    min_time: RRDecimal | None = Field(default=None, alias="MinTime")
    max_time: RRDecimal | None = Field(default=None, alias="MaxTime")
    result: list[int] | None = Field(default=None, alias="Result")
    device_id: list[str] | None = Field(default=None, alias="DeviceID")
    device_name: list[str] | None = Field(default=None, alias="DeviceName")
    transponder: list[str] | None = Field(default=None, alias="Transponder")
    order_id: list[int] | None = Field(default=None, alias="OrderID")
    hits: list[int] | None = Field(default=None, alias="Hits")
    rssi: list[int] | None = Field(default=None, alias="RSSI")
    loop_id: list[int] | None = Field(default=None, alias="LoopID")
    channel: list[int] | None = Field(default=None, alias="Channel")
    port: list[int] | None = Field(default=None, alias="Port")
    status_flags: list[int] | None = Field(default=None, alias="StatusFlags")
    file_no: list[int] | None = Field(default=None, alias="FileNo")
    passing_no: list[int] | None = Field(default=None, alias="PassingNo")
    is_marker: list[bool] | None = Field(default=None, alias="IsMarker")

    model_config = {"populate_by_name": True}


class RawDataWithAdditionalFields(RawData):
    """Raw data with additional participant fields.

    Based on go-model/model.go:326-331.
    """

    bib: int = Field(default=0, alias="Bib")
    fields: dict[str, Any] = Field(default_factory=dict, alias="Fields")

    model_config = {"populate_by_name": True}


class RawDataDistinctValues(BaseModel):
    """Distinct values in raw data.

    Based on go-model/model.go:348-354.
    """

    decoder_id: list[str] = Field(default_factory=list, alias="DecoderID")
    order_id: list[int] = Field(default_factory=list, alias="OrderID")
    battery_voltage: list[Decimal] = Field(default_factory=list, alias="BatteryVoltage")
    hits: list[int] = Field(default_factory=list, alias="Hits")
    rssi: list[int] = Field(default_factory=list, alias="RSSI")

    model_config = {"populate_by_name": True}

    @field_validator("decoder_id", "order_id", "battery_voltage", "hits", "rssi", mode="before")
    @classmethod
    def none_to_empty_list(cls, v):
        """Convert None to empty list."""
        return v if v is not None else []


class RawDataEndpoint:
    """Raw Data API endpoint.

    Based on go-webapi/eventapi_rawdata.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            count = await event.rawdata.count(Identifier.by_bib(123))
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def excel_export(
        self,
        identifier: Identifier,
        lang: str = "",
    ) -> bytes:
        """Export raw data as CSV file.

        Based on go-webapi/eventapi_rawdata.go:23-29.

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
        return await self._client.get(self._event_id, "rawdata/excelexport", params)

    async def set_invalid(self, id: int, invalid: bool) -> None:
        """Set a raw data entry to valid or invalid.

        Based on go-webapi/eventapi_rawdata.go:32-39.

        Args:
            id: Raw data entry ID
            invalid: Mark as invalid
        """
        params = {
            "id": id,
            "invalid": invalid,
        }
        await self._client.get(self._event_id, "rawdata/setinvalid", params)

    async def set_invalid_batch(
        self,
        filter_expr: str,
        rd_filter: RawDataFilter,
        invalid: bool,
    ) -> None:
        """Set multiple raw data entries to valid or invalid.

        Based on go-webapi/eventapi_rawdata.go:42-51.

        Args:
            filter_expr: Filter expression
            rd_filter: Raw data filter
            invalid: Mark as invalid
        """
        rd_filter_json = rd_filter.model_dump(by_alias=True, exclude_none=True)
        params = {
            "filter": filter_expr,
            "rdFilter": json.dumps(rd_filter_json),
            "invalid": invalid,
        }
        await self._client.get(self._event_id, "rawdata/setinvalidbatch", params)

    async def delete_id(self, id: int) -> None:
        """Delete raw data entry by ID.

        Based on go-webapi/eventapi_rawdata.go:54-60.

        Args:
            id: Raw data entry ID
        """
        params = {"id": id}
        await self._client.get(self._event_id, "rawdata/deleteid", params)

    async def delete(
        self,
        identifier: Identifier,
        filter_expr: str = "",
        rd_filter: RawDataFilter | None = None,
    ) -> None:
        """Delete raw data entries matching the given filters.

        Based on go-webapi/eventapi_rawdata.go:63-72.

        Args:
            identifier: Participant identifier
            filter_expr: Filter expression
            rd_filter: Raw data filter
        """
        params: dict[str, Any] = {
            identifier.name: identifier.value,
            "filter": filter_expr,
        }
        if rd_filter:
            rd_filter_json = rd_filter.model_dump(by_alias=True, exclude_none=True)
            params["rdFilter"] = json.dumps(rd_filter_json)
        await self._client.get(self._event_id, "rawdata/delete", params)

    async def get(
        self,
        identifier: Identifier,
        filter_expr: str = "",
        rd_filter: RawDataFilter | None = None,
        add_fields: list[str] | None = None,
        first_row: int = 0,
        max_rows: int = 0,
        sort_by: str = "",
    ) -> list[RawDataWithAdditionalFields]:
        """Get raw data entries.

        Based on go-webapi/eventapi_rawdata.go:75-97.

        Args:
            identifier: Participant identifier
            filter_expr: Filter expression
            rd_filter: Raw data filter
            add_fields: Additional fields to include
            first_row: First row to return
            max_rows: Maximum rows to return
            sort_by: Sort expression

        Returns:
            List of raw data entries with additional fields
        """
        params: dict[str, Any] = {
            identifier.name: identifier.value,
            "filter": filter_expr,
            "firstRow": first_row,
            "maxRows": max_rows,
            "sortBy": sort_by,
        }
        if rd_filter:
            rd_filter_json = rd_filter.model_dump(by_alias=True, exclude_none=True)
            params["rdFilter"] = json.dumps(rd_filter_json)
        if add_fields:
            params["addFields"] = add_fields
        result = await self._client.get_json(self._event_id, "rawdata/get", params)
        if not result:
            return []
        return [RawDataWithAdditionalFields.model_validate(item) for item in result]

    async def export(
        self,
        identifier: Identifier,
        filter_expr: str = "",
        rd_filter: RawDataFilter | None = None,
        fields: list[str] | None = None,
        first_row: int = 0,
        max_rows: int = 0,
        sort_by: str = "",
    ) -> list[list[Any]]:
        """Export raw data entries.

        Based on go-webapi/eventapi_rawdata.go:100-122.

        Args:
            identifier: Participant identifier
            filter_expr: Filter expression
            rd_filter: Raw data filter
            fields: Fields to include
            first_row: First row to return
            max_rows: Maximum rows to return
            sort_by: Sort expression

        Returns:
            List of rows with field values
        """
        params: dict[str, Any] = {
            identifier.name: identifier.value,
            "filter": filter_expr,
            "firstRow": first_row,
            "maxRows": max_rows,
            "sortBy": sort_by,
        }
        if rd_filter:
            rd_filter_json = rd_filter.model_dump(by_alias=True, exclude_none=True)
            params["rdFilter"] = json.dumps(rd_filter_json)
        if fields:
            params["fields"] = fields
        result = await self._client.get_json(self._event_id, "rawdata/export", params)
        return result if result else []

    async def count(
        self,
        identifier: Identifier,
        filter_expr: str = "",
        rd_filter: RawDataFilter | None = None,
    ) -> int:
        """Count raw data entries matching the given filters.

        Based on go-webapi/eventapi_rawdata.go:125-140.

        Args:
            identifier: Participant identifier
            filter_expr: Filter expression
            rd_filter: Raw data filter

        Returns:
            Count of matching entries
        """
        params: dict[str, Any] = {
            identifier.name: identifier.value,
            "filter": filter_expr,
        }
        if rd_filter:
            rd_filter_json = rd_filter.model_dump(by_alias=True, exclude_none=True)
            params["rdFilter"] = json.dumps(rd_filter_json)
        result = await self._client.get_json(self._event_id, "rawdata/count", params)
        return int(result) if result is not None else 0

    async def distinct_values(self) -> RawDataDistinctValues:
        """Get distinct values in raw data.

        Based on go-webapi/eventapi_rawdata.go:143-152.

        Returns:
            Distinct values object
        """
        result = await self._client.get_json(self._event_id, "rawdata/distinctvalues")
        return RawDataDistinctValues.model_validate(result if result else {})

    async def add_manual(
        self,
        timing_point: str,
        identifier: Identifier,
        time: Decimal,
        add_t0: bool = False,
    ) -> None:
        """Add a raw data entry manually.

        Based on go-webapi/eventapi_rawdata.go:155-164.

        Args:
            timing_point: Timing point name
            identifier: Participant identifier
            time: Time value
            add_t0: Add T0 time
        """
        params = {
            "timingPoint": timing_point,
            identifier.name: identifier.value,
            "time": float(time),
            "addT0": add_t0,
        }
        await self._client.get(self._event_id, "rawdata/addmanual", params)

    async def copy(self, from_: Identifier, to: Identifier) -> None:
        """Copy raw data from one participant to another.

        Based on go-webapi/eventapi_rawdata.go:167-174.

        Args:
            from_: Source participant identifier
            to: Target participant identifier
        """
        params = {
            f"{from_.name}From": from_.value,
            f"{from_.name}To": to.value,
        }
        await self._client.get(self._event_id, "rawdata/copy", params)

    async def swap(self, identifier1: Identifier, identifier2: Identifier) -> None:
        """Swap raw data between two participants.

        Based on go-webapi/eventapi_rawdata.go:177-184.

        Args:
            identifier1: First participant identifier
            identifier2: Second participant identifier
        """
        params = {
            f"{identifier1.name}1": identifier1.value,
            f"{identifier2.name}2": identifier2.value,
        }
        await self._client.get(self._event_id, "rawdata/swap", params)
