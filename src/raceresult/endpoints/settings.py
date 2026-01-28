"""Settings endpoint for Raceresult API.

Based on go-webapi/eventapi_settings.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class Setting(BaseModel):
    """Setting to save.

    Based on go-webapi/eventapi_settings.go:23-28.
    """

    name: str = Field(alias="Name")
    value: Any = Field(alias="Value")
    result: int = Field(default=0, alias="Result")
    contest: int = Field(default=0, alias="Contest")

    model_config = {"populate_by_name": True}


class SettingsEndpoint:
    """Settings API endpoint.

    Based on go-webapi/eventapi_settings.go.

    Example:
        async with RaceResultClient() as client:
            await client.login(api_key="...")
            settings = SettingsEndpoint(client, "event123")
            event_name = await settings.get_value("EventName")
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def get(self, *names: str) -> dict[str, Any]:
        """Get setting values.

        Based on go-webapi/eventapi_settings.go:31-51.

        Args:
            names: Setting names to retrieve

        Returns:
            Dictionary mapping setting names to values
        """
        if not names:
            return {}

        params: dict[str, Any] = {}
        if len(names) == 1:
            params["name"] = names[0]
        else:
            params["names"] = ",".join(names)

        result = await self._client.get_json(self._event_id, "settings/getsettings", params)
        return result if result else {}

    async def get_value(self, name: str) -> Any:
        """Get a single setting value.

        Based on go-webapi/eventapi_settings.go:54-60.

        Args:
            name: Setting name

        Returns:
            Setting value or None
        """
        values = await self.get(name)
        return values.get(name)

    async def save(self, settings: list[Setting]) -> None:
        """Save setting values.

        Based on go-webapi/eventapi_settings.go:63-66.

        Args:
            settings: List of settings to save
        """
        data = [s.model_dump(by_alias=True) for s in settings]
        await self._client.post_json(self._event_id, "settings/savesettings", data=data)

    async def save_value(self, name: str, value: Any) -> None:
        """Save a single setting value.

        Based on go-webapi/eventapi_settings.go:69-74.

        Args:
            name: Setting name
            value: Setting value
        """
        await self.save([Setting(name=name, value=value)])

    async def delete(self, name: str, contest: int = 0, result: int = 0) -> None:
        """Delete a setting.

        Based on go-webapi/eventapi_settings.go:77-85.

        Args:
            name: Setting name
            contest: Contest ID (optional)
            result: Result ID (optional)
        """
        params = {
            "name": name,
            "contest": contest,
            "result": result,
        }
        await self._client.get(self._event_id, "settings/delete", params)

    async def names_by_prefix(self, prefix: str) -> list[str]:
        """Get setting names matching a prefix.

        Based on go-webapi/eventapi_settings.go:88-97.

        Args:
            prefix: Setting name prefix

        Returns:
            List of matching setting names
        """
        params = {"prefix": prefix}
        result = await self._client.get_json(self._event_id, "settings/settingnamesbyprefix", params)
        return result if result else []
