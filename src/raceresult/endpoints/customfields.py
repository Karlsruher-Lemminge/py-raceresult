"""Custom fields endpoint for Raceresult API.

Based on go-webapi/eventapi_customfields.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import CustomField

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class CustomFieldsEndpoint:
    """Custom Fields API endpoint.

    Based on go-webapi/eventapi_customfields.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            fields = await event.customfields.get()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def get(self) -> list[CustomField]:
        """Get all custom fields.

        Based on go-webapi/eventapi_customfields.go:22-33.

        Returns:
            List of all custom fields
        """
        result = await self._client.get_json(self._event_id, "fields/get")
        if not result:
            return []
        return [CustomField.model_validate(item) for item in result]

    async def get_one(self, id: int) -> CustomField:
        """Get a single custom field by ID.

        Based on go-webapi/eventapi_customfields.go:36-50.

        Args:
            id: Custom field ID

        Returns:
            CustomField object
        """
        params = {"id": id}
        result = await self._client.get_json(self._event_id, "fields/get", params)
        return CustomField.model_validate(result)

    async def delete(self, id: int) -> None:
        """Delete a custom field.

        Based on go-webapi/eventapi_customfields.go:53-59.

        Args:
            id: Custom field ID
        """
        params = {"id": id}
        await self._client.get(self._event_id, "fields/delete", params)

    async def save(self, items: list[CustomField]) -> list[int]:
        """Save custom fields.

        Based on go-webapi/eventapi_customfields.go:62-68.

        Args:
            items: Custom fields to save

        Returns:
            List of saved custom field IDs
        """
        data = [item.model_dump(by_alias=True) for item in items]
        result = await self._client.post_json(self._event_id, "fields/save", data=data)
        return result if result else []
