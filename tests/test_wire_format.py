"""Wire-format and null-tolerance regression tests.

The Raceresult API returns JSON ``null`` where Go unmarshals a nil slice or
map, and it parses datetimes with a strict length switch. Both have already
caused shipped bugs, so they are pinned here rather than left to review.
"""

import json
from datetime import datetime, timezone

import pytest

from raceresult.endpoints.certificates import Certificate, PageFormat, PageSize
from raceresult.endpoints.lists import ListField, ListFilter, ListOrder
from raceresult.endpoints.participants import Identifier, apply_identifier
from raceresult.models.email import EmailTemplate, Preview
from raceresult.models.event import GroupTimes, Ranking, WebHook
from raceresult.models.participant import ImportResult
from raceresult.models.public import UserRight
from raceresult.models.timing import Passing, RawData
from raceresult.models.types import (
    _parse_rr_datetime,
    _serialize_rr_datetime,
    align_timezone,
)


class TestNullCollections:
    """Go marshals a nil slice/map as null, not [] or {}."""

    @pytest.mark.parametrize(
        "model,payload,field",
        [
            (Ranking, {"ID": 1, "Group": None, "Sort": None, "SortDesc": None}, "group"),
            (Ranking, {"ID": 1, "Group": None, "Sort": None, "SortDesc": None}, "sort"),
            (WebHook, {"Name": "h", "Fields": None}, "fields"),
            (GroupTimes, {"Mode": "w", "Items": None}, "items"),
            (EmailTemplate, {"Name": "t", "Attachments": None}, "attachments"),
            (EmailTemplate, {"Name": "t", "HTTPHeaders": None}, "http_headers"),
            (Preview, {"Type": 0, "Bibs": None}, "bibs"),
            (Preview, {"Type": 0, "PIDs": None}, "pids"),
            (ImportResult, {"Added": 0, "PIDs": None}, "pids"),
        ],
    )
    def test_null_list_becomes_empty(self, model, payload, field):
        assert getattr(model.model_validate(payload), field) == []

    def test_null_rights_map_becomes_empty_dict(self):
        assert UserRight.model_validate({"UserID": 1, "Rights": None}).rights == {}

    def test_null_certificate_collections(self):
        cert = Certificate.model_validate(
            {"CertificateName": "X", "Fields": None, "Zones": None}
        )
        assert cert.elements == [] and cert.zones == []


class TestRawDataPassing:
    """go-model/model.go:279-287 -- RawData embeds the full Passing payload."""

    def test_passing_is_parsed_not_discarded(self):
        rd = RawData.model_validate(
            {
                "ID": 1,
                "PID": 7,
                "Passing": {
                    "Transponder": "ABC123",
                    "RSSI": -55,
                    "DeviceName": "Decoder1",
                    "Hits": 3,
                    "Position": {"Latitude": 48.1, "Longitude": 11.5},
                },
            }
        )
        assert rd.passing.transponder == "ABC123"
        assert rd.passing.rssi == -55
        assert rd.passing.device_name == "Decoder1"
        assert rd.passing.position.latitude == 48.1

    def test_null_passing_yields_empty_passing(self):
        assert RawData.model_validate({"ID": 1, "Passing": None}).passing.transponder == ""

    def test_passing_carries_received_and_utc_time(self):
        p = Passing.model_validate(
            {"Transponder": "X", "Received": "2024-05-01 10:00:00", "UTCTime": ""}
        )
        assert p.received == datetime(2024, 5, 1, 10, 0, 0)
        assert p.utc_time is None


class TestDateTimeWireFormat:
    """go-model/datetime/datetime.go:104-131 accepts only these lengths."""

    ACCEPTED_QUOTED_LENGTHS = {0, 2, 12, 21, 22, 27}

    @pytest.mark.parametrize(
        "wire",
        ["2024-05-01", "2024-05-01 10:00:00", "2024-05-01T10:00:00+02:00"],
    )
    def test_round_trip_is_byte_identical(self, wire):
        assert _serialize_rr_datetime(_parse_rr_datetime(wire)) == wire

    @pytest.mark.parametrize(
        "value",
        [
            datetime.now(timezone.utc),
            datetime.now(),
            datetime(2024, 5, 1, 10, 0, 0, 999999),
            datetime(2024, 5, 1, 10, 0, 0, 999999, tzinfo=timezone.utc),
        ],
    )
    def test_serialized_length_is_always_parseable_by_go(self, value):
        # datetime.now() carries microseconds; Go rejects the 34-char result
        # with "date time format not supported".
        out = json.dumps(_serialize_rr_datetime(value))
        assert len(out) in self.ACCEPTED_QUOTED_LENGTHS

    def test_zoneless_values_stay_naive(self):
        # Go tracks this as hasZone=false; stamping UTC would shift an
        # event-local time on the next save.
        assert _parse_rr_datetime("2024-05-01 10:00:00").tzinfo is None
        assert _parse_rr_datetime("2024-05-01T10:00:00+02:00").tzinfo is not None

    @pytest.mark.parametrize("zero", ["1899-12-30", "0001-01-01", ""])
    def test_zero_dates_become_none(self, zero):
        assert _parse_rr_datetime(zero) is None

    def test_align_timezone_matches_go_before_semantics(self):
        aware = datetime(2024, 5, 1, tzinfo=timezone.utc)
        naive = datetime(2024, 5, 1)
        # Neither comparison may raise.
        assert align_timezone(naive, aware) >= aware
        assert align_timezone(aware, naive) >= naive


class TestListModelAliases:
    """Site of the alias bug fixed in a4e8082, previously untested.

    Keys are checked against the Go struct tags in go-model/list/list.go:91-130.
    """

    def test_order_keys_match_go(self):
        d = ListOrder(expression="[Bib]", descending=True).model_dump(by_alias=True)
        assert d["Expression"] == "[Bib]"
        assert d["Descending"] is True
        # Grouping2 carries an explicit json:"Grouping" tag (list.go:94).
        assert "Grouping" in d and "Grouping2" not in d
        # Ignore is json:"-" (list.go:106) and must never be sent.
        assert "Ignore" not in d

    def test_filter_keys_match_go(self):
        d = ListFilter(expression1="[Sex]", operator="=", expression2="m").model_dump(
            by_alias=True
        )
        assert d["Expression1"] == "[Sex]"
        assert d["Operator"] == "="
        assert d["Expression2"] == "m"
        assert d["OrConjunction"] is False

    def test_field_keys_match_go(self):
        d = ListField(expression="[Bib]", label="Nr").model_dump(by_alias=True)
        assert d["Expression"] == "[Bib]"
        assert d["Label"] == "Nr"

    def test_dumps_are_json_serialisable(self):
        # Every save() path hands these straight to json.dumps.
        for m in (ListOrder(expression="[Bib]"), ListFilter(), ListField(label="X")):
            json.dumps(m.model_dump(by_alias=True))


class TestLenientCertificateEnums:
    """go-model/certificate/{pagesize,pageformat}.go never fail to parse."""

    @pytest.mark.parametrize(
        "raw,expected",
        [("A4", PageSize.A4), ("a4", PageSize.A4), ("LETTER", PageSize.LETTER)],
    )
    def test_page_size_is_case_insensitive(self, raw, expected):
        assert PageSize(raw) is expected

    @pytest.mark.parametrize("raw", ["", "Weird", "A9"])
    def test_unknown_page_size_falls_back_to_user_defined(self, raw):
        assert PageSize(raw) is PageSize.USER_DEFINED

    @pytest.mark.parametrize("raw", ["", "junk"])
    def test_unknown_page_format_falls_back_to_portrait(self, raw):
        assert PageFormat(raw) is PageFormat.PORTRAIT

    def test_certificate_with_blank_page_format_parses(self):
        cert = Certificate.model_validate({"CertificateName": "X", "PageFormat": ""})
        assert cert.page_format is PageFormat.PORTRAIT


class TestIdentifierConflict:
    """by_filter used to silently overwrite the caller's own filter."""

    def test_bib_identifier_leaves_filter_intact(self):
        params = apply_identifier(
            {"filter": "[Contest]=1"}, Identifier.by_bib(5)
        )
        assert params == {"filter": "[Contest]=1", "bib": 5}

    def test_conflicting_filter_identifier_raises(self):
        with pytest.raises(ValueError, match="conflicts"):
            apply_identifier(
                {"filter": "[Contest]=1"}, Identifier.by_filter("[Bib]=99")
            )

    def test_filter_identifier_ok_when_no_filter_given(self):
        params = apply_identifier({"filter": ""}, Identifier.by_filter("[Bib]=99"))
        assert params["filter"] == "[Bib]=99"
