"""Times endpoint for Raceresult API.

Based on go-webapi/eventapi_times.go.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any

from raceresult.models.timing import Time, Passing
from raceresult.endpoints.participants import Identifier

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class TimesAddResponseItem:
    """Response item from times/add.

    Based on go-model/model.go:590-598.
    """

    def __init__(
        self,
        status: int = 0,
        time: Decimal = Decimal(0),
        result_id: int = 0,
        result_name: str = "",
        raw_data_id: int = 0,
        timing_point: str = "",
        fields: dict[str, Any] | None = None,
    ):
        self.status = status
        self.time = time
        self.result_id = result_id
        self.result_name = result_name
        self.raw_data_id = raw_data_id
        self.timing_point = timing_point
        self.fields = fields or {}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TimesAddResponseItem:
        """Create from dictionary."""
        return cls(
            status=data.get("Status", 0),
            time=Decimal(str(data.get("Time", 0))),
            result_id=data.get("ResultID", 0),
            result_name=data.get("ResultName", ""),
            raw_data_id=data.get("RawDataID", 0),
            timing_point=data.get("TimingPoint", ""),
            fields=data.get("Fields", {}),
        )


class TimesEndpoint:
    """Times API endpoint.

    Based on go-webapi/eventapi_times.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            times = await event.times.get(Identifier.by_bib(123), result=1)
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
        result: int = 0,
        lang: str = "",
    ) -> bytes:
        """Export times as CSV file.

        Based on go-webapi/eventapi_times.go:23-30.

        Args:
            identifier: Participant identifier
            result: Result ID filter
            lang: Language code

        Returns:
            CSV file as bytes
        """
        params = {
            identifier.name: identifier.value,
            "result": result,
            "lang": lang,
        }
        return await self._client.get(self._event_id, "times/excelexport", params)

    async def delete(
        self,
        identifier: Identifier,
        contest: int = 0,
        result: int = 0,
        filter_expr: str = "",
        filter_info: str = "",
    ) -> None:
        """Delete times matching the given filters.

        Based on go-webapi/eventapi_times.go:33-43.

        Args:
            identifier: Participant identifier
            contest: Contest ID filter
            result: Result ID filter
            filter_expr: Filter expression
            filter_info: Filter info expression
        """
        params = {
            identifier.name: identifier.value,
            "contest": contest,
            "result": result,
            "filter": filter_expr,
            "filterInfo": filter_info,
        }
        await self._client.get(self._event_id, "times/delete", params)

    async def swap(self, identifier1: Identifier, identifier2: Identifier) -> None:
        """Swap times between two participants.

        Based on go-webapi/eventapi_times.go:46-53.

        Args:
            identifier1: First participant identifier
            identifier2: Second participant identifier
        """
        params = {
            f"{identifier1.name}1": identifier1.value,
            f"{identifier2.name}2": identifier2.value,
        }
        await self._client.get(self._event_id, "times/swap", params)

    async def single_start(
        self,
        result: int,
        contest: int = 0,
        first_time: Decimal = Decimal(0),
        interval: Decimal = Decimal(0),
        sort: str = "",
        filter_expr: str = "",
        no_history: bool = False,
    ) -> None:
        """Create single start times.

        Based on go-webapi/eventapi_times.go:56-70.

        Args:
            result: Result ID
            contest: Contest ID
            first_time: First start time
            interval: Interval between starts
            sort: Sort expression
            filter_expr: Filter expression
            no_history: Skip history entry
        """
        params = {
            "result": result,
            "contest": contest,
            "firstTime": float(first_time),
            "interval": float(interval),
            "sort": sort,
            "filter": filter_expr,
            "noHistory": no_history,
        }
        await self._client.get(self._event_id, "times/singlestart", params)

    async def random_times(
        self,
        result: int,
        contest: int = 0,
        min_time: Decimal = Decimal(0),
        max_time: Decimal = Decimal(0),
        offset_result: int = 0,
        filter_expr: str = "",
        no_history: bool = False,
    ) -> None:
        """Create random times.

        Based on go-webapi/eventapi_times.go:73-87.

        Args:
            result: Result ID
            contest: Contest ID
            min_time: Minimum time
            max_time: Maximum time
            offset_result: Offset result ID
            filter_expr: Filter expression
            no_history: Skip history entry
        """
        params = {
            "result": result,
            "contest": contest,
            "minTime": float(min_time),
            "maxTime": float(max_time),
            "offsetResult": offset_result,
            "filter": filter_expr,
            "noHistory": no_history,
        }
        await self._client.get(self._event_id, "times/randomtimes", params)

    async def copy(
        self,
        from_: Identifier,
        to: Identifier,
        overwrite_existing: bool = False,
    ) -> None:
        """Copy times from one participant to another.

        Based on go-webapi/eventapi_times.go:90-98.

        Args:
            from_: Source participant identifier
            to: Target participant identifier
            overwrite_existing: Overwrite existing times
        """
        params = {
            f"{from_.name}From": from_.value,
            f"{from_.name}To": to.value,
            "overwriteExisting": overwrite_existing,
        }
        await self._client.get(self._event_id, "times/copy", params)

    async def interpolate(
        self,
        dest_id: int,
        helper_id: int,
        contest: int = 0,
        helpers: int = 0,
    ) -> None:
        """Interpolate missing times.

        Based on go-webapi/eventapi_times.go:101-110.

        Args:
            dest_id: Destination result ID
            helper_id: Helper result ID
            contest: Contest ID
            helpers: Number of helpers
        """
        params = {
            "destID": dest_id,
            "helperID": helper_id,
            "contest": contest,
            "helpers": helpers,
        }
        await self._client.get(self._event_id, "times/interpolate", params)

    async def get(self, identifier: Identifier, result: int = 0) -> list[Time]:
        """Get times matching the given filters.

        Based on go-webapi/eventapi_times.go:113-128.

        Args:
            identifier: Participant identifier
            result: Result ID filter

        Returns:
            List of time entries
        """
        params = {
            identifier.name: identifier.value,
            "result": result,
        }
        data = await self._client.get_json(self._event_id, "times/get", params)
        if not data:
            return []
        return [Time.model_validate(item) for item in data]

    async def count(
        self,
        identifier: Identifier,
        contest: int = 0,
        result: int = 0,
        filter_expr: str = "",
    ) -> int:
        """Count times matching the given filters.

        Based on go-webapi/eventapi_times.go:131-146.

        Args:
            identifier: Participant identifier
            contest: Contest ID filter
            result: Result ID filter
            filter_expr: Filter expression

        Returns:
            Count of matching times
        """
        params = {
            identifier.name: identifier.value,
            "contest": contest,
            "result": result,
            "filter": filter_expr,
        }
        result_data = await self._client.get_json(self._event_id, "times/count", params)
        return int(result_data) if result_data is not None else 0

    async def add(
        self,
        passings: list[Passing],
        return_fields: list[str] | None = None,
        contest_filter: int = 0,
        ignore_bib_to_bib_assign: bool = False,
    ) -> list[TimesAddResponseItem]:
        """Add times/passings.

        Based on go-webapi/eventapi_times.go:149-167.

        Args:
            passings: List of passing data
            return_fields: Fields to return
            contest_filter: Contest filter
            ignore_bib_to_bib_assign: Ignore bib-to-bib assignment

        Returns:
            List of response items
        """
        params = {
            "contestFilter": contest_filter,
            "ignoreBibToBibAssign": ignore_bib_to_bib_assign,
        }
        if return_fields:
            params["returnFields"] = return_fields
        data = [p.model_dump(by_alias=True) for p in passings]
        result = await self._client.post_json(self._event_id, "times/add", params, data)
        if not result:
            return []
        return [TimesAddResponseItem.from_dict(item) for item in result]
