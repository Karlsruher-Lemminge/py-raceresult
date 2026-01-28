"""Email templates endpoint for Raceresult API.

Based on go-webapi/eventapi_emailtemplates.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.email import EmailTemplate, Preview

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class EmailTemplatesEndpoint:
    """Email templates API endpoint.

    Based on go-webapi/eventapi_emailtemplates.go.

    Example:
        async with RaceResultClient() as client:
            await client.login(api_key="...")
            emails = EmailTemplatesEndpoint(client, "event123")
            names = await emails.names()
            template = await emails.get(names[0])
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
        """Get names of all email templates.

        Based on go-webapi/eventapi_emailtemplates.go:23-29.

        Returns:
            List of template names
        """
        result = await self._client.get_json(self._event_id, "emailtemplates/names")
        return result if result else []

    async def get(self, name: str) -> EmailTemplate:
        """Get an email template.

        Based on go-webapi/eventapi_emailtemplates.go:32-45.

        Args:
            name: Template name

        Returns:
            Email template
        """
        params = {"name": name}
        result = await self._client.get_json(self._event_id, "emailtemplates/get", params)
        return EmailTemplate.model_validate(result)

    async def save(self, template: EmailTemplate) -> None:
        """Save an email template.

        Based on go-webapi/eventapi_emailtemplates.go:48-51.

        Args:
            template: Email template to save
        """
        data = template.model_dump(by_alias=True)
        await self._client.post_json(self._event_id, "emailtemplates/save", data=data)

    async def delete(self, name: str) -> None:
        """Delete an email template.

        Based on go-webapi/eventapi_emailtemplates.go:54-60.

        Args:
            name: Template name
        """
        params = {"name": name}
        await self._client.get(self._event_id, "emailtemplates/delete", params)

    async def copy(self, name: str, new_name: str) -> None:
        """Copy an email template.

        Based on go-webapi/eventapi_emailtemplates.go:63-70.

        Args:
            name: Source template name
            new_name: New template name
        """
        params = {"name": name, "newName": new_name}
        await self._client.get(self._event_id, "emailtemplates/copy", params)

    async def rename(self, name: str, new_name: str) -> None:
        """Rename an email template.

        Based on go-webapi/eventapi_emailtemplates.go:73-80.

        Args:
            name: Current template name
            new_name: New template name
        """
        params = {"name": name, "newName": new_name}
        await self._client.get(self._event_id, "emailtemplates/rename", params)

    async def new(self, name: str) -> None:
        """Create a new email template.

        Based on go-webapi/eventapi_emailtemplates.go:83-89.

        Args:
            name: Template name
        """
        params = {"name": name}
        await self._client.get(self._event_id, "emailtemplates/new", params)

    async def preview(
        self, name: str, filter_expr: str = "", lang: str = ""
    ) -> list[Preview]:
        """Generate email previews.

        Based on go-webapi/eventapi_emailtemplates.go:92-107.

        Args:
            name: Template name
            filter_expr: Filter expression
            lang: Language code

        Returns:
            List of previews
        """
        params = {
            "name": name,
            "filter": filter_expr,
            "lang": lang,
        }
        result = await self._client.get_json(self._event_id, "emailtemplates/preview", params)
        return [Preview.model_validate(item) for item in (result or [])]

    async def send_preview(self, name: str, lang: str, preview: Preview) -> None:
        """Send a preview email.

        Based on go-webapi/eventapi_emailtemplates.go:110-117.

        Args:
            name: Template name
            lang: Language code
            preview: Preview to send
        """
        params = {"name": name, "lang": lang}
        data = preview.model_dump(by_alias=True)
        await self._client.post_json(self._event_id, "emailtemplates/sendpreview", params, data)

    async def send(self, name: str, filter_expr: str = "", lang: str = "") -> None:
        """Generate and send emails.

        Based on go-webapi/eventapi_emailtemplates.go:120-128.

        Args:
            name: Template name
            filter_expr: Filter expression
            lang: Language code
        """
        params = {
            "name": name,
            "filter": filter_expr,
            "lang": lang,
        }
        await self._client.get(self._event_id, "emailtemplates/send", params)
