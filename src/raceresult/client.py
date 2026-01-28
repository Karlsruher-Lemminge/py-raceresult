"""HTTP client for Raceresult API.

Based on go-webapi/api.go and go-webapi/api_public.go.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import httpx


class RaceResultError(Exception):
    """Base exception for Raceresult API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class RaceResultClient:
    """Low-level HTTP client for Raceresult API.

    Based on go-webapi/api.go.

    Example:
        async with RaceResultClient() as client:
            await client.login(api_key="your-api-key")
            result = await client.get("event123", "data/count", {"filter": ""})
    """

    DEFAULT_SERVER = "events.raceresult.com"
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_USER_AGENT = "py-raceresult/0.1.0"

    def __init__(
        self,
        server: str = DEFAULT_SERVER,
        https: bool = True,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
    ):
        """Initialize the client.

        Args:
            server: Server hostname (default: events.raceresult.com)
            https: Use HTTPS (default: True)
            timeout: Request timeout in seconds (default: 30)
            user_agent: User-Agent header value
        """
        self.server = server
        self.https = https
        self.timeout = timeout
        self.user_agent = user_agent
        self._session_id: str = "0"
        self._client: httpx.AsyncClient | None = None

    @property
    def base_url(self) -> str:
        """Get the base URL for API requests."""
        scheme = "https" if self.https else "http"
        return f"{scheme}://{self.server}"

    @property
    def session_id(self) -> str:
        """Get the current session ID."""
        return self._session_id

    @property
    def is_logged_in(self) -> bool:
        """Check if the client is logged in."""
        return self._session_id != "0" and self._session_id != ""

    async def __aenter__(self) -> RaceResultClient:
        """Enter async context manager."""
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit async context manager."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    def _build_url(
        self, event_id: str | None, cmd: str, params: dict[str, Any] | None = None
    ) -> str:
        """Build URL for API request.

        Based on go-webapi/api.go:153-173.
        """
        url_parts = [self.base_url]
        if event_id:
            url_parts.append(f"/_{event_id}")
        url_parts.append(f"/api/{cmd}")

        url = "".join(url_parts)
        if params:
            # Filter out None values and convert to strings
            filtered_params = {
                k: self._serialize_param(v) for k, v in params.items() if v is not None
            }
            if filtered_params:
                url += "?" + urlencode(filtered_params)
        return url

    def _serialize_param(self, value: Any) -> str:
        """Serialize a parameter value to string."""
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (list, tuple)):
            return ",".join(str(v) for v in value)
        return str(value)

    def _get_headers(self) -> dict[str, str]:
        """Get headers for API request."""
        return {
            "Authorization": f"Bearer {self._session_id}",
            "User-Agent": self.user_agent,
        }

    async def _handle_response(self, response: httpx.Response) -> bytes:
        """Handle API response, raising errors if needed.

        Based on go-webapi/api.go:116-151.
        """
        if response.status_code == 200:
            return response.content

        # Try to parse error message from JSON
        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "Error" in error_data:
                error_msg = error_data["Error"]
            else:
                error_msg = response.text
        except Exception:
            error_msg = response.text

        raise RaceResultError(error_msg, response.status_code)

    async def login(
        self,
        api_key: str | None = None,
        user: str | None = None,
        password: str | None = None,
        sign_in_as: str | None = None,
        totp: str | None = None,
        rr_user_token: str | None = None,
    ) -> None:
        """Login to the Raceresult API.

        Based on go-webapi/api_public.go:66-95.

        Args:
            api_key: API key for authentication
            user: Username for authentication
            password: Password for authentication
            sign_in_as: Sign in as another user
            totp: Time-based OTP for 2FA
            rr_user_token: RR user token

        Raises:
            RaceResultError: If login fails
        """
        data: dict[str, str] = {}
        if api_key:
            data["apikey"] = api_key
        if user:
            data["user"] = user
            data["pw"] = password or ""
        if sign_in_as:
            data["signinas"] = sign_in_as
        if totp:
            data["totp"] = totp
        if rr_user_token:
            data["rruser_token"] = rr_user_token

        client = self._get_client()
        url = self._build_url(None, "public/login")
        response = await client.post(
            url,
            data=data,
            headers={"User-Agent": self.user_agent},
        )
        content = await self._handle_response(response)
        self._session_id = content.decode("utf-8")

    async def logout(self) -> None:
        """Logout from the Raceresult API.

        Based on go-webapi/api_public.go:98-104.
        """
        if not self.is_logged_in:
            raise RaceResultError("not logged in")
        await self.get(None, "public/logout")
        self._session_id = "0"

    async def get(
        self, event_id: str | None, cmd: str, params: dict[str, Any] | None = None
    ) -> bytes:
        """Make a GET request to the API.

        Based on go-webapi/api.go:76-82.

        Args:
            event_id: Event ID (None for public endpoints)
            cmd: API command/endpoint
            params: Query parameters

        Returns:
            Response body as bytes

        Raises:
            RaceResultError: If request fails
        """
        client = self._get_client()
        url = self._build_url(event_id, cmd, params)
        response = await client.get(url, headers=self._get_headers())
        return await self._handle_response(response)

    async def post(
        self,
        event_id: str | None,
        cmd: str,
        params: dict[str, Any] | None = None,
        data: Any = None,
        content_type: str = "application/json",
    ) -> bytes:
        """Make a POST request to the API.

        Based on go-webapi/api.go:85-113.

        Args:
            event_id: Event ID (None for public endpoints)
            cmd: API command/endpoint
            params: Query parameters
            data: Request body data
            content_type: Content-Type header

        Returns:
            Response body as bytes

        Raises:
            RaceResultError: If request fails
        """
        client = self._get_client()
        url = self._build_url(event_id, cmd, params)
        headers = self._get_headers()

        if data is not None:
            if isinstance(data, (dict, list)):
                import json

                body = json.dumps(data).encode("utf-8")
                headers["Content-Type"] = "application/json"
            elif isinstance(data, str):
                body = data.encode("utf-8")
                headers["Content-Type"] = content_type
            elif isinstance(data, bytes):
                body = data
                headers["Content-Type"] = content_type
            else:
                import json

                body = json.dumps(data).encode("utf-8")
                headers["Content-Type"] = "application/json"
        else:
            body = None

        response = await client.post(url, content=body, headers=headers)
        return await self._handle_response(response)

    async def get_json(
        self, event_id: str | None, cmd: str, params: dict[str, Any] | None = None
    ) -> Any:
        """Make a GET request and parse JSON response."""
        import json

        content = await self.get(event_id, cmd, params)
        return json.loads(content)

    async def post_json(
        self,
        event_id: str | None,
        cmd: str,
        params: dict[str, Any] | None = None,
        data: Any = None,
    ) -> Any:
        """Make a POST request and parse JSON response."""
        import json

        content = await self.post(event_id, cmd, params, data)
        if content:
            return json.loads(content)
        return None
