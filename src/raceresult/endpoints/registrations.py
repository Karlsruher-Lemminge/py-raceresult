"""Registrations endpoint for Raceresult API.

Based on go-webapi/eventapi_registrations.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.registration import Registration

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class RegistrationsEndpoint:
    """Registrations API endpoint.

    Based on go-webapi/eventapi_registrations.go.

    Example:
        async with RaceResultClient() as client:
            await client.login(api_key="...")
            regs = RegistrationsEndpoint(client, "event123")
            names = await regs.names()
            reg = await regs.get(names[0])
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def names(self) -> list[str]:
        """Get names of all registration forms.

        Based on go-webapi/eventapi_registrations.go:22-28.

        Returns:
            List of registration form names
        """
        result = await self._client.get_json(self._event_id, "registrations/names")
        return result if result else []

    async def get(self, name: str) -> Registration:
        """Get a registration form.

        Based on go-webapi/eventapi_registrations.go:31-44.

        Args:
            name: Registration form name

        Returns:
            Registration form definition
        """
        params = {"name": name}
        result = await self._client.get_json(self._event_id, "registrations/get", params)
        return Registration.model_validate(result)

    async def save(self, registration: Registration) -> None:
        """Save a registration form.

        Based on go-webapi/eventapi_registrations.go:47-50.

        Args:
            registration: Registration form to save
        """
        data = registration.model_dump(by_alias=True)
        await self._client.post_json(self._event_id, "registrations/save", data=data)

    async def delete(self, name: str) -> None:
        """Delete a registration form.

        Based on go-webapi/eventapi_registrations.go:53-59.

        Args:
            name: Registration form name
        """
        params = {"name": name}
        await self._client.get(self._event_id, "registrations/delete", params)

    async def copy(self, name: str, new_name: str) -> None:
        """Copy a registration form.

        Based on go-webapi/eventapi_registrations.go:62-69.

        Args:
            name: Source registration form name
            new_name: New registration form name
        """
        params = {"name": name, "newName": new_name}
        await self._client.get(self._event_id, "registrations/copy", params)

    async def rename(self, name: str, new_name: str) -> None:
        """Rename a registration form.

        Based on go-webapi/eventapi_registrations.go:72-79.

        Args:
            name: Current registration form name
            new_name: New registration form name
        """
        params = {"name": name, "newName": new_name}
        await self._client.get(self._event_id, "registrations/rename", params)

    async def new(self, name: str, group: bool = False) -> None:
        """Create a new registration form.

        Based on go-webapi/eventapi_registrations.go:82-89.

        Args:
            name: Registration form name
            group: Whether this is a group registration form
        """
        params = {"name": name, "group": group}
        await self._client.get(self._event_id, "registrations/new", params)
