"""File endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import Version

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class FileEndpoint:
    """Event file API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def activate(
        self, bib: int = 0, filter_expr: str = "", max_activations: int = 0
    ) -> int:
        """Activate participants and return the number of records activated."""
        params = {"bib": bib, "filter": filter_expr, "maxActivations": max_activations}
        result = await self._client.get_json(self._event_id, "file/activate", params)
        return int(result)

    async def not_activated(self, filter_expr: str = "") -> int:
        """Return the number of participants not yet activated."""
        result = await self._client.get_json(
            self._event_id, "file/notactivated", {"filter": filter_expr}
        )
        return int(result)

    async def ses_version(self) -> Version:
        """Return the Sports Event Server version."""
        result = await self._client.get_json(self._event_id, "file/sesversion")
        return Version.model_validate(result)

    async def check_expression(self, expressions: str, return_tree: bool = False) -> str:
        """Parse and validate an expression, optionally returning the parse tree."""
        params = {"expressions": expressions, "returnTree": return_tree}
        result = await self._client.get(self._event_id, "file/checkexpression", params)
        return result.decode("utf-8")

    async def get_file(self) -> bytes:
        """Download a copy of the entire event file."""
        return await self._client.get(self._event_id, "file/getfile")

    async def mod_job_id(self) -> int:
        """Return the current modification job ID of the event file."""
        result = await self._client.get_json(self._event_id, "file/modjobid")
        return int(result)

    async def mod_job_ids(self) -> tuple[int, int]:
        """Return both the data and settings modification job IDs."""
        raw = await self._client.get(self._event_id, "file/modjobids")
        parts = raw.decode("utf-8").split(";")
        if len(parts) != 2:
            raise ValueError(f"unexpected modjobids response: {raw!r}")
        return int(parts[0]), int(parts[1])

    async def filename(self) -> str:
        """Return the filename of the event file."""
        result = await self._client.get(self._event_id, "file/filename")
        return result.decode("utf-8")

    async def owner(self) -> int:
        """Return the user ID of the event owner (online server only)."""
        result = await self._client.get_json(self._event_id, "file/owner")
        return int(result)

    async def is_owner(self) -> bool:
        """Return True if the current user owns the event (online server only)."""
        result = await self._client.get_json(self._event_id, "file/isowner")
        return bool(result)

    async def rights(self) -> str:
        """Return the current user's rights code for this event (online server only)."""
        result = await self._client.get(self._event_id, "file/rights")
        return result.decode("utf-8")
