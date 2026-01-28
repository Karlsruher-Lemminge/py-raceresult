"""Vouchers endpoint for Raceresult API.

Based on go-webapi/eventapi_vouchers.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.payment import Voucher

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class VouchersEndpoint:
    """Vouchers API endpoint.

    Based on go-webapi/eventapi_vouchers.go.

    Example:
        async with RaceResultClient() as client:
            await client.login(api_key="...")
            vouchers = VouchersEndpoint(client, "event123")
            all_vouchers = await vouchers.get()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def get(self, code: str = "") -> list[Voucher]:
        """Get vouchers.

        Based on go-webapi/eventapi_vouchers.go:24-38.

        Args:
            code: Voucher code (empty for all)

        Returns:
            List of vouchers
        """
        params = {"code": code} if code else {}
        result = await self._client.get_json(self._event_id, "vouchers/get", params)
        return [Voucher.model_validate(item) for item in (result or [])]

    async def delete(self, ids: list[int]) -> None:
        """Delete vouchers.

        Based on go-webapi/eventapi_vouchers.go:41-48.

        Args:
            ids: Voucher IDs to delete
        """
        data = ";".join(str(id) for id in ids)
        await self._client.post(
            self._event_id,
            "vouchers/delete",
            data=data,
            content_type="text/plain",
        )

    async def save(self, vouchers: list[Voucher]) -> list[int]:
        """Save vouchers.

        Based on go-webapi/eventapi_vouchers.go:51-57.

        Args:
            vouchers: Vouchers to save

        Returns:
            List of voucher IDs
        """
        data = [v.model_dump(by_alias=True) for v in vouchers]
        result = await self._client.post_json(self._event_id, "vouchers/save", data=data)
        return result if result else []
