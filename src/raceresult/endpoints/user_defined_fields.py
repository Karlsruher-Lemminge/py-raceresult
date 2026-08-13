"""UserDefinedFields endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import UserDefinedField

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class UserDefinedFieldsEndpoint:
    """User-defined fields API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def get(self) -> list[UserDefinedField]:
        """Return all user-defined fields."""
        result = await self._client.get_json(self._event_id, "userdefinedfields/get")
        return [UserDefinedField.model_validate(x) for x in (result or [])]

    async def set(self, items: list[UserDefinedField]) -> None:
        """Overwrite all user-defined fields."""
        data = [item.model_dump(by_alias=True) for item in items]
        await self._client.post_json(self._event_id, "userdefinedfields/set", data=data)
