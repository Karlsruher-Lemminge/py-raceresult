"""Participants endpoint for Raceresult API.

Based on go-webapi/eventapi_participants.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from raceresult.models.participant import (
    ImportResult,
    ParticipantNewResponse,
    SaveValueArrayItem,
)
from raceresult.models.event import EntryFeeItem

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class Identifier:
    """Participant identifier for API calls."""

    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value

    @classmethod
    def by_bib(cls, bib: int) -> Identifier:
        """Identify by bib number."""
        return cls("bib", bib)

    @classmethod
    def by_pid(cls, pid: int) -> Identifier:
        """Identify by participant ID."""
        return cls("pid", pid)

    @classmethod
    def by_filter(cls, filter_expr: str) -> Identifier:
        """Identify by filter expression."""
        return cls("filter", filter_expr)


class ParticipantsEndpoint:
    """Participants API endpoint.

    Based on go-webapi/eventapi_participants.go.

    Example:
        async with RaceResultClient() as client:
            await client.login(api_key="...")
            parts = ParticipantsEndpoint(client, "event123")
            fields = await parts.get_fields(Identifier.by_bib(123), ["Firstname", "Lastname"])
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def get_fields(
        self, identifier: Identifier, fields: list[str]
    ) -> dict[str, Any]:
        """Get fields of one participant.

        Based on go-webapi/eventapi_participants.go:23-37.

        Args:
            identifier: Participant identifier
            fields: Field names to retrieve

        Returns:
            Dictionary of field names to values
        """
        params = {
            identifier.name: identifier.value,
            "fields": ",".join(fields),
        }
        result = await self._client.get_json(self._event_id, "part/getfields", params)
        return result if result else {}

    async def get_fields_with_changes(
        self,
        identifier: Identifier,
        fields: list[str],
        changes: dict[str, Any],
    ) -> dict[str, Any]:
        """Get fields as if changes were applied.

        Based on go-webapi/eventapi_participants.go:40-54.

        Args:
            identifier: Participant identifier
            fields: Field names to retrieve
            changes: Hypothetical changes to apply

        Returns:
            Dictionary of field names to values
        """
        params = {
            identifier.name: identifier.value,
            "fields": ",".join(fields),
        }
        result = await self._client.post_json(
            self._event_id, "part/getfieldswithchanges", params, changes
        )
        return result if result else {}

    async def save_expression(
        self,
        identifier: Identifier,
        field: str,
        expression: str,
        no_history: bool = False,
    ) -> None:
        """Calculate expression and save to field.

        Based on go-webapi/eventapi_participants.go:57-66.

        Args:
            identifier: Participant identifier
            field: Target field name
            expression: Expression to calculate
            no_history: Skip history entry
        """
        params = {
            identifier.name: identifier.value,
            "field": field,
            "expression": expression,
            "noHistory": no_history,
        }
        await self._client.get(self._event_id, "part/saveexpression", params)

    async def save_value_array(
        self, values: list[SaveValueArrayItem], no_history: bool = False
    ) -> None:
        """Save multiple values for multiple participants.

        Based on go-webapi/eventapi_participants.go:69-75.

        Args:
            values: List of values to save
            no_history: Skip history entries
        """
        params = {"noHistory": no_history}
        data = [v.model_dump(by_alias=True) for v in values]
        await self._client.post_json(self._event_id, "part/savevaluearray", params, data)

    async def save_fields(
        self,
        identifier: Identifier,
        values: dict[str, Any],
        no_history: bool = False,
    ) -> None:
        """Save multiple fields for one participant.

        Based on go-webapi/eventapi_participants.go:78-85.

        Args:
            identifier: Participant identifier
            values: Field values to save
            no_history: Skip history entry
        """
        params = {
            identifier.name: identifier.value,
            "noHistory": no_history,
        }
        await self._client.post_json(self._event_id, "part/savefields", params, values)

    async def save(
        self, values: list[dict[str, Any]], no_history: bool = False
    ) -> None:
        """Add or update one or more participants.

        Based on go-webapi/eventapi_participants.go:88-94.

        Args:
            values: List of participant field dictionaries
            no_history: Skip history entries
        """
        params = {"noHistory": no_history}
        await self._client.post_json(self._event_id, "part/savefields", params, values)

    async def delete(
        self,
        filter_expr: str = "",
        identifier: Identifier | None = None,
        contest: int = 0,
    ) -> None:
        """Delete participants.

        Based on go-webapi/eventapi_participants.go:97-105.

        Args:
            filter_expr: Filter expression
            identifier: Participant identifier
            contest: Contest ID
        """
        params: dict[str, Any] = {
            "filter": filter_expr,
            "contest": contest,
        }
        if identifier:
            params[identifier.name] = identifier.value
        await self._client.get(self._event_id, "part/delete", params)

    async def new(
        self,
        bib: int = 0,
        contest: int = 0,
        firstfree: bool = False,
    ) -> ParticipantNewResponse:
        """Create new participant.

        Based on go-webapi/eventapi_participants.go:108-124.

        Args:
            bib: Bib number (0 for auto)
            contest: Contest ID
            firstfree: Use first free bib

        Returns:
            New participant ID and bib
        """
        params = {
            "bib": bib,
            "contest": contest,
            "firstfree": firstfree,
            "v2": True,
        }
        result = await self._client.get_json(self._event_id, "part/new", params)
        return ParticipantNewResponse.model_validate(result)

    async def entry_fee(self, bibs: list[int]) -> list[EntryFeeItem]:
        """Get entry fees for participants.

        Based on go-webapi/eventapi_participants.go:127-140.

        Args:
            bibs: Bib numbers

        Returns:
            List of entry fee items
        """
        params = {"bibs": ",".join(str(b) for b in bibs)}
        result = await self._client.get_json(self._event_id, "part/entryfee", params)
        return [EntryFeeItem.model_validate(item) for item in (result or [])]

    async def create_blanks(
        self,
        from_bib: int,
        to_bib: int,
        contest: int = 0,
        skip_excluded: bool = False,
    ) -> None:
        """Create blank participants.

        Based on go-webapi/eventapi_participants.go:143-152.

        Args:
            from_bib: Starting bib number
            to_bib: Ending bib number
            contest: Contest ID
            skip_excluded: Skip excluded bib ranges
        """
        params = {
            "from": from_bib,
            "to": to_bib,
            "contest": contest,
            "skipExcluded": skip_excluded,
        }
        await self._client.get(self._event_id, "part/createblanks", params)

    async def swap_bibs(self, bib1: int, bib2: int) -> None:
        """Swap bibs of two participants.

        Based on go-webapi/eventapi_participants.go:155-162.

        Args:
            bib1: First bib number
            bib2: Second bib number
        """
        params = {"bib1": bib1, "bib2": bib2}
        await self._client.get(self._event_id, "part/swapbibs", params)

    async def reset_bibs(
        self,
        sort: str,
        first_bib: int = 1,
        ranges: bool = False,
        filter_expr: str = "",
        no_history: bool = False,
    ) -> None:
        """Reset/reassign bibs.

        Based on go-webapi/eventapi_participants.go:165-175.

        Args:
            sort: Sort expression
            first_bib: First bib number
            ranges: Use bib ranges
            filter_expr: Filter expression
            no_history: Skip history entries
        """
        params = {
            "sort": sort,
            "firstBib": first_bib,
            "ranges": ranges,
            "filter": filter_expr,
            "noHistory": no_history,
        }
        await self._client.get(self._event_id, "part/resetbibs", params)

    async def data_manipulation(
        self,
        values: dict[str, str],
        filter_expr: str = "",
        no_history: bool = False,
    ) -> None:
        """Change multiple participants at once.

        Based on go-webapi/eventapi_participants.go:178-185.

        Args:
            values: Field assignments
            filter_expr: Filter expression
            no_history: Skip history entries
        """
        params = {
            "filter": filter_expr,
            "noHistory": no_history,
        }
        await self._client.post_json(self._event_id, "part/datamanipulation", params, values)

    async def clear_bank_information(
        self,
        identifier: Identifier | None = None,
        contest: int = 0,
        filter_expr: str = "",
    ) -> None:
        """Clear bank information.

        Based on go-webapi/eventapi_participants.go:188-196.

        Args:
            identifier: Participant identifier
            contest: Contest ID
            filter_expr: Filter expression
        """
        params: dict[str, Any] = {
            "contest": contest,
            "filter": filter_expr,
        }
        if identifier:
            params[identifier.name] = identifier.value
        await self._client.get(self._event_id, "part/clearbankinformation", params)

    async def free_bib(
        self,
        max_bib_plus1: bool = False,
        contest: int = 0,
        preferred: int = 0,
    ) -> int:
        """Get an unused bib number.

        Based on go-webapi/eventapi_participants.go:245-260.

        Args:
            max_bib_plus1: Use max bib + 1
            contest: Contest ID
            preferred: Preferred bib

        Returns:
            Available bib number
        """
        params = {
            "maxBibPlus1": max_bib_plus1,
            "contest": contest,
            "preferred": preferred,
        }
        result = await self._client.get_json(self._event_id, "part/freebib", params)
        return int(result)

    async def frequent_clubs(self, wildcard: str, max_number: int = 10) -> list[str]:
        """Get frequent club names.

        Based on go-webapi/eventapi_participants.go:263-273.

        Args:
            wildcard: Search pattern
            max_number: Maximum results

        Returns:
            List of club names
        """
        params = {
            "wildcard": wildcard,
            "maxNumber": max_number,
        }
        result = await self._client.get_json(self._event_id, "part/frequentclubs", params)
        return result if result else []

    async def import_file(
        self,
        file_data: bytes,
        add_participants: bool = True,
        update_participants: bool = True,
        col_handling: int = 0,
        identity_columns: int = 0,
        lang: str = "",
    ) -> ImportResult:
        """Import participants from file.

        Based on go-webapi/eventapi_participants.go:224-242.

        Args:
            file_data: File content (CSV/XLS/XLSX)
            add_participants: Add new participants
            update_participants: Update existing participants
            col_handling: Column handling mode
            identity_columns: Identity column mode
            lang: Language code

        Returns:
            Import result
        """
        params = {
            "addParticipants": add_participants,
            "updateParticipants": update_participants,
            "colHandling": col_handling,
            "identityColumns": identity_columns,
            "lang": lang,
        }
        result = await self._client.post_json(
            self._event_id,
            "part/import",
            params,
            file_data,
        )
        return ImportResult.model_validate(result)
