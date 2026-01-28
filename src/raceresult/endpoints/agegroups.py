"""Age groups endpoint for Raceresult API.

Based on go-webapi/eventapi_agegroups.go.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from raceresult.models.event import AgeGroup
from raceresult.endpoints.participants import Identifier

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class AgeGroupsEndpoint:
    """Age Groups API endpoint.

    Based on go-webapi/eventapi_agegroups.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            agegroups = await event.agegroups.get()
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
        """Get PDF with all age groups.

        Based on go-webapi/eventapi_agegroups.go:22-24.

        Returns:
            PDF file as bytes
        """
        return await self._client.get(self._event_id, "agegroups/pdf")

    async def get(
        self,
        contest: int = 0,
        set: int = 0,
        name: str = "",
    ) -> list[AgeGroup]:
        """Get age groups matching the given filters.

        Based on go-webapi/eventapi_agegroups.go:27-43.

        Args:
            contest: Contest ID filter (0 for all)
            set: Age group set filter (0 for all)
            name: Name filter

        Returns:
            List of matching age groups
        """
        params = {
            "contest": contest,
            "set": set,
            "name": name,
        }
        result = await self._client.get_json(self._event_id, "agegroups/get", params)
        if not result:
            return []
        return [AgeGroup.model_validate(item) for item in result]

    async def delete(
        self,
        id: int = 0,
        contest: int = 0,
        set: int = 0,
    ) -> None:
        """Delete age groups.

        Based on go-webapi/eventapi_agegroups.go:46-54.

        Args:
            id: Age group ID (0 to use contest/set filters)
            contest: Contest ID filter
            set: Age group set filter
        """
        params = {
            "id": id,
            "contest": contest,
            "set": set,
        }
        await self._client.get(self._event_id, "agegroups/delete", params)

    async def save(self, items: list[AgeGroup]) -> list[int]:
        """Save age groups.

        Based on go-webapi/eventapi_agegroups.go:57-63.

        Args:
            items: Age groups to save

        Returns:
            List of saved age group IDs
        """
        data = [item.model_dump(by_alias=True) for item in items]
        result = await self._client.post_json(self._event_id, "agegroups/save", data=data)
        return result if result else []

    async def generate(
        self,
        mode: str,
        contest: int = 0,
        set: int = 0,
        age_base: bool = False,
        date: datetime | None = None,
        lang: str = "",
    ) -> list[AgeGroup]:
        """Generate new age groups from templates.

        Based on go-webapi/eventapi_agegroups.go:66-87.

        Args:
            mode: Generation mode (e.g., "standard", "custom")
            contest: Contest ID
            set: Age group set
            age_base: Use age-based calculation
            date: Reference date
            lang: Language code

        Returns:
            Generated age groups
        """
        params = {
            "mode": mode,
            "contest": contest,
            "set": set,
            "ageBase": age_base,
            "lang": lang,
        }
        if date is not None:
            params["date"] = date.isoformat()
        result = await self._client.get_json(self._event_id, "agegroups/generate", params)
        if not result:
            return []
        return [AgeGroup.model_validate(item) for item in result]

    async def reassign(
        self,
        contest: int,
        identifier: Identifier,
        set: int = 0,
        add_only: bool = False,
    ) -> None:
        """Reassign age groups to participants.

        Based on go-webapi/eventapi_agegroups.go:90-99.

        Args:
            contest: Contest ID
            identifier: Participant identifier
            set: Age group set
            add_only: Only add, don't remove existing
        """
        params = {
            "contest": contest,
            identifier.name: identifier.value,
            "set": set,
            "addOnly": add_only,
        }
        await self._client.get(self._event_id, "agegroups/reassign", params)
