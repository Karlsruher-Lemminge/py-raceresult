"""Entry fees endpoint for Raceresult API.

Based on go-webapi/eventapi_entryfees.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import EntryFee

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class EntryFeesEndpoint:
    """Entry Fees API endpoint.

    Based on go-webapi/eventapi_entryfees.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            fees = await event.entryfees.get()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def pdf(self) -> bytes:
        """Get PDF with all entry fees.

        Based on go-webapi/eventapi_entryfees.go:22-24.

        Returns:
            PDF file as bytes
        """
        return await self._client.get(self._event_id, "entryfees/pdf")

    async def get(self, contest: int = 0, id: int = 0) -> list[EntryFee]:
        """Get entry fees matching the given filters.

        Based on go-webapi/eventapi_entryfees.go:27-42.

        Args:
            contest: Contest ID filter (0 for all)
            id: Entry fee ID filter (0 for all)

        Returns:
            List of matching entry fees
        """
        params = {
            "contest": contest,
            "id": id,
        }
        result = await self._client.get_json(self._event_id, "entryfees/get", params)
        if not result:
            return []
        return [EntryFee.model_validate(item) for item in result]

    async def delete(self, id: int) -> None:
        """Delete an entry fee.

        Based on go-webapi/eventapi_entryfees.go:45-51.

        Args:
            id: Entry fee ID
        """
        params = {"id": id}
        await self._client.get(self._event_id, "entryfees/delete", params)

    async def save(self, items: list[EntryFee]) -> list[int]:
        """Save entry fees.

        Based on go-webapi/eventapi_entryfees.go:54-60.

        Args:
            items: Entry fees to save

        Returns:
            List of saved entry fee IDs
        """
        data = [item.model_dump(by_alias=True) for item in items]
        result = await self._client.post_json(self._event_id, "entryfees/save", data=data)
        return result if result else []
