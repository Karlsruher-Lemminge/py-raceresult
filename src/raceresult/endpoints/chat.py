"""Chat endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import ChatMessage

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class ChatEndpoint:
    """Chat API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def get_messages(self, min_id: int = 0) -> list[ChatMessage]:
        """Return chat messages starting at the given ID."""
        result = await self._client.get_json(
            self._event_id, "chat/getmessages", {"minID": min_id}
        )
        return [ChatMessage.model_validate(x) for x in (result or [])]

    async def get_users(self, username: str) -> list[str]:
        """Register a user and return a list of all active users."""
        result = await self._client.get_json(
            self._event_id, "chat/getusers", {"username": username}
        )
        return result if result else []

    async def post_message(self, username: str, msg: str) -> None:
        """Post a new chat message."""
        params = {"username": username}
        await self._client.post(
            self._event_id, "chat/postmessage", params, data=msg.encode()
        )
