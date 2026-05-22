"""Archives endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.endpoints.participants import Identifier
from raceresult.models.archives import ArchivesMatch, ArchivesParticipant, ParticipationExt

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class ArchivesEndpoint:
    """Archives API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def create_new_reg_no(self) -> int:
        """Create a new registration number."""
        result = await self._client.get_json(self._event_id, "archives/createnewregno")
        return int(result)

    async def get_matches(self, prefix: str, max_number: int = 10) -> list[ArchivesMatch]:
        """Return matching archive entries for the given name prefix."""
        params = {"prefix": prefix, "maxNumber": max_number}
        result = await self._client.get_json(self._event_id, "archives/getmatches", params)
        return [ArchivesMatch.model_validate(x) for x in (result or [])]

    async def get_entry(self, id: int = 0, reg_no: str = "") -> ArchivesParticipant:
        """Return a single archived participant by ID or registration number."""
        params = {"id": id, "regNo": reg_no}
        result = await self._client.get_json(self._event_id, "archives/getentry", params)
        return ArchivesParticipant.model_validate(result)

    async def get_participations(self, identifier: Identifier) -> list[ParticipationExt]:
        """Return cross-event participation history for a participant."""
        params = {identifier.name: identifier.value}
        result = await self._client.get_json(
            self._event_id, "archives/getparticipations", params
        )
        return [ParticipationExt.model_validate(x) for x in (result or [])]

    async def download(self) -> bytes:
        """Download the entire archives file."""
        return await self._client.get(self._event_id, "archives/download")

    async def remove(self) -> None:
        """Delete the entire archive from the event."""
        await self._client.get(self._event_id, "archives/remove")

    async def create(self) -> None:
        """Create a new archives file."""
        await self._client.get(self._event_id, "archives/create")

    async def write(self) -> None:
        """Write current event data into the archive."""
        await self._client.get(self._event_id, "archives/write")

    async def import_file(self, data: bytes) -> None:
        """Import an archive file into the event."""
        await self._client.post(self._event_id, "archives/import", data=data)
