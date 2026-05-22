"""Labels endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from raceresult.models.label import Label

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class LabelsEndpoint:
    """Labels API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def names(self) -> list[str]:
        """Return names of all labels."""
        result = await self._client.get_json(self._event_id, "labels/names")
        return result if result else []

    async def get(self, name: str) -> Label:
        """Return a label by name."""
        result = await self._client.get_json(
            self._event_id, "labels/get", {"name": name}
        )
        return Label.model_validate(result)

    async def save(self, item: Label) -> None:
        """Save a label."""
        await self._client.post_json(
            self._event_id, "labels/save", data=item.model_dump(by_alias=True)
        )

    async def delete(self, name: str) -> None:
        """Delete a label."""
        await self._client.get(self._event_id, "labels/delete", {"name": name})

    async def copy(self, name: str, new_name: str) -> None:
        """Create a copy of a label."""
        await self._client.get(
            self._event_id, "labels/copy", {"name": name, "newName": new_name}
        )

    async def rename(self, name: str, new_name: str) -> None:
        """Rename a label."""
        await self._client.get(
            self._event_id, "labels/rename", {"name": name, "newName": new_name}
        )

    async def new(self, name: str) -> None:
        """Create a new label."""
        await self._client.get(self._event_id, "labels/new", {"name": name})

    async def create(
        self,
        name: str,
        contests: list[int] | None = None,
        start_x: int = 0,
        start_y: int = 0,
        lang: str = "",
    ) -> bytes:
        """Render labels as PDF."""
        params: dict[str, Any] = {
            "name": name,
            "startX": start_x,
            "startY": start_y,
            "lang": lang,
        }
        if contests:
            params["contest"] = ",".join(str(c) for c in contests)
        return await self._client.get(self._event_id, "labels/create", params)
