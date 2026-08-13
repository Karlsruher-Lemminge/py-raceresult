"""Tests for the HTTP client layer.

These pin the exact wire format the Go reference client produces, since
that is the contract the Raceresult server actually implements. Every
assertion here is traceable to a line in go-webapi/.
"""

import json
from datetime import date, datetime, timezone
from decimal import Decimal

import httpx
import pytest

from raceresult.client import RaceResultClient, RaceResultError


def make_client(handler):
    """Build a client whose transport is backed by ``handler``."""
    client = RaceResultClient(server="example.test")
    client._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return client


class TestBuildURL:
    """go-webapi/api.go:153-173 (buildURL)."""

    def test_event_url_has_underscore_prefix(self):
        c = RaceResultClient(server="example.test")
        assert (
            c._build_url("evt1", "data/count")
            == "https://example.test/_evt1/api/data/count"
        )

    def test_public_url_has_no_event_segment(self):
        c = RaceResultClient(server="example.test")
        assert c._build_url(None, "public/login") == "https://example.test/api/public/login"

    def test_http_scheme_when_https_disabled(self):
        c = RaceResultClient(server="example.test", https=False)
        assert c._build_url(None, "x").startswith("http://example.test")

    def test_none_params_are_dropped_but_empty_strings_kept(self):
        # Go's url.Values.Set writes empty strings; only absent keys vanish.
        c = RaceResultClient(server="example.test")
        url = c._build_url(None, "x", {"a": "", "b": None, "c": 1})
        assert "a=" in url and "b=" not in url and "c=1" in url


class TestSerializeParam:
    """go-webapi/urlvalues.go:19-49."""

    def setup_method(self):
        self.c = RaceResultClient()

    def test_bool_is_lowercase(self):
        # urlvalues.go:30-34 -- Python's str(True) == "True" would be wrong.
        assert self.c._serialize_param(True) == "true"
        assert self.c._serialize_param(False) == "false"

    def test_string_list_is_json_encoded(self):
        # urlvalues.go:42-44 json.Marshal, compact separators.
        assert self.c._serialize_param(["Bib", "Firstname"]) == '["Bib","Firstname"]'

    def test_string_list_survives_embedded_commas(self):
        # The whole point: a comma-join would split this into 3 bogus fields.
        expr = 'IIF([Sex]="m","M","W")'
        out = self.c._serialize_param([expr, "Bib"])
        assert json.loads(out) == [expr, "Bib"]

    def test_int_list_is_comma_joined(self):
        # Go pre-joins int slices via helpers.go:25-34 intSliceToString.
        assert self.c._serialize_param([1, 2, 3]) == "1,2,3"

    def test_datetime_is_rfc3339_without_microseconds(self):
        # urlvalues.go:27-28 t.Format(time.RFC3339) has no fractional part.
        v = datetime(2024, 5, 1, 10, 0, 0, 123456, tzinfo=timezone.utc)
        assert self.c._serialize_param(v) == "2024-05-01T10:00:00+00:00"

    def test_date_is_iso(self):
        assert self.c._serialize_param(date(2024, 5, 1)) == "2024-05-01"

    def test_decimal_never_uses_exponent_notation(self):
        # go-model/decimal/string.go always emits plain fixed-point.
        assert self.c._serialize_param(Decimal("1E+2")) == "100"


class TestAuth:
    """go-webapi/api_public.go:66-104."""

    @pytest.mark.asyncio
    async def test_login_posts_credentials_as_form_body(self):
        seen = {}

        def handler(request):
            seen["url"] = str(request.url)
            seen["body"] = request.content.decode()
            seen["ct"] = request.headers.get("content-type")
            return httpx.Response(200, content=b"session-abc")

        c = make_client(handler)
        await c.login(api_key="secret-key")

        assert seen["url"].endswith("/api/public/login")
        assert "apikey=secret-key" in seen["body"]
        assert "application/x-www-form-urlencoded" in seen["ct"]
        # The key must never leak into the query string (it would be logged).
        assert "secret-key" not in seen["url"]
        assert c.session_id == "session-abc"
        assert c.is_logged_in

    @pytest.mark.asyncio
    async def test_password_only_sent_alongside_user(self):
        seen = {}

        def handler(request):
            seen["body"] = request.content.decode()
            return httpx.Response(200, content=b"s")

        c = make_client(handler)
        await c.login(user="bob", password="pw", totp="123456")
        assert "user=bob" in seen["body"]
        assert "pw=pw" in seen["body"]
        assert "totp=123456" in seen["body"]

    @pytest.mark.asyncio
    async def test_requests_carry_bearer_session(self):
        seen = {}

        def handler(request):
            seen["auth"] = request.headers.get("authorization")
            return httpx.Response(200, content=b"1")

        c = make_client(handler)
        c._session_id = "tok123"
        await c.get("evt", "data/count")
        assert seen["auth"] == "Bearer tok123"

    @pytest.mark.asyncio
    async def test_logout_without_session_raises(self):
        c = make_client(lambda r: httpx.Response(200, content=b""))
        with pytest.raises(RaceResultError):
            await c.logout()


class TestErrorHandling:
    """go-webapi/api.go:116-151."""

    @pytest.mark.asyncio
    async def test_json_error_key_is_extracted(self):
        c = make_client(
            lambda r: httpx.Response(400, json={"Error": "event not found"})
        )
        with pytest.raises(RaceResultError) as ei:
            await c.get("evt", "data/count")
        assert str(ei.value) == "event not found"
        assert ei.value.status_code == 400

    @pytest.mark.asyncio
    async def test_non_json_body_falls_back_to_text(self):
        c = make_client(lambda r: httpx.Response(500, content=b"boom"))
        with pytest.raises(RaceResultError) as ei:
            await c.get("evt", "data/count")
        assert "boom" in str(ei.value)
        assert ei.value.status_code == 500

    @pytest.mark.asyncio
    async def test_non_200_success_codes_still_raise(self):
        # Go treats only 200 as success (api.go:133).
        c = make_client(lambda r: httpx.Response(204, content=b""))
        with pytest.raises(RaceResultError):
            await c.get("evt", "x")


class TestPostBodies:
    """go-webapi/eventapi.go:268-270 and api.go:105-112."""

    @pytest.mark.asyncio
    async def test_dict_body_is_json_with_header(self):
        seen = {}

        def handler(request):
            seen["ct"] = request.headers.get("content-type")
            seen["body"] = request.content
            return httpx.Response(200, content=b"{}")

        c = make_client(handler)
        await c.post("evt", "x", data={"A": 1})
        assert seen["ct"] == "application/json"
        assert seen["body"] == b'{"A": 1}'

    @pytest.mark.asyncio
    async def test_binary_body_has_no_content_type(self):
        # Go passes contentType "" and api.go:110 skips the header entirely;
        # labelling an upload as JSON can make a strict server reject it.
        seen = {}

        def handler(request):
            seen["ct"] = request.headers.get("content-type")
            seen["body"] = request.content
            return httpx.Response(200, content=b"{}")

        c = make_client(handler)
        await c.post("evt", "archives/import", data=b"\x00\x01BINARY")
        assert seen["ct"] is None
        assert seen["body"] == b"\x00\x01BINARY"

    @pytest.mark.asyncio
    async def test_explicit_content_type_is_honoured(self):
        seen = {}

        def handler(request):
            seen["ct"] = request.headers.get("content-type")
            return httpx.Response(200, content=b"{}")

        c = make_client(handler)
        await c.post("evt", "x", data="a;b", content_type="text/plain")
        assert seen["ct"] == "text/plain"

    @pytest.mark.asyncio
    async def test_post_json_tolerates_empty_body(self):
        c = make_client(lambda r: httpx.Response(200, content=b""))
        assert await c.post_json("evt", "x", data={}) is None
