"""Tests for raceresult models."""

from datetime import date, datetime, timezone
from decimal import Decimal

import pytest

from raceresult.models.types import RRDate, RRDateTime, RRDecimal
from raceresult.models.event import (
    Contest, AgeGroup, CustomField, CustomFieldType,
    ChatMessage, ForwardingInfo, GroupTimes, GroupTime,
    RawDataRule, SimpleAPIItem, TeamScore, WebHook, WebHookType, Version,
)
from raceresult.models.participant import Participant
from raceresult.models.registration import Registration, Step, Element, FormField
from raceresult.models.payment import Voucher, VoucherType
from raceresult.models.email import EmailTemplate, TemplateType
from raceresult.models.timing import ChipFileEntry, TimingPoint
from raceresult.models.kiosk import Kiosk, KioskAfterSave, KioskStep, KioskDisplayField, KioskEditField, KioskSearchField
from raceresult.models.archives import ArchivesMatch, ArchivesParticipant, ParticipationExt
from raceresult.models.certificate import Certificate, CertificateElement, CertificateZone, ElementType
from raceresult.models.certificate_set import CertificateSet, CertificateSetType
from raceresult.models.statistic import Statistics, Aggregation
from raceresult.models.label import Label, LabelDirection, LabelBarcodeType


class TestRRDate:
    """Tests for RRDate type."""

    def test_parse_iso_format(self):
        """Test parsing ISO format dates."""
        from raceresult.models.types import _parse_rr_date

        result = _parse_rr_date("2024-06-15")
        assert result == date(2024, 6, 15)

    def test_parse_european_format(self):
        """Test parsing European format dates."""
        from raceresult.models.types import _parse_rr_date

        result = _parse_rr_date("15.06.2024")
        assert result == date(2024, 6, 15)

    def test_parse_empty(self):
        """Test parsing empty string returns None."""
        from raceresult.models.types import _parse_rr_date

        result = _parse_rr_date("")
        assert result is None

    def test_parse_vb_zero_date(self):
        """Test VB zero date returns None."""
        from raceresult.models.types import _parse_rr_date

        result = _parse_rr_date("1899-12-30")
        assert result is None


class TestRRDateTime:
    """Tests for RRDateTime type."""

    def test_parse_rfc3339(self):
        """Test parsing RFC3339 format."""
        from raceresult.models.types import _parse_rr_datetime

        result = _parse_rr_datetime("2024-06-15T10:30:00Z")
        assert result is not None
        assert result.year == 2024
        assert result.month == 6
        assert result.day == 15
        assert result.hour == 10
        assert result.minute == 30

    def test_parse_datetime_format(self):
        """Test parsing datetime format."""
        from raceresult.models.types import _parse_rr_datetime

        result = _parse_rr_datetime("2024-06-15 10:30:00")
        assert result is not None
        assert result.year == 2024
        assert result.hour == 10


class TestRRDecimal:
    """Tests for RRDecimal type."""

    def test_parse_string(self):
        """Test parsing decimal string."""
        from raceresult.models.types import _parse_rr_decimal

        result = _parse_rr_decimal("123.4567")
        assert result == Decimal("123.4567")

    def test_parse_comma_decimal(self):
        """Test parsing decimal with comma."""
        from raceresult.models.types import _parse_rr_decimal

        result = _parse_rr_decimal("123,45")
        assert result == Decimal("123.45")

    def test_parse_int(self):
        """Test parsing integer."""
        from raceresult.models.types import _parse_rr_decimal

        result = _parse_rr_decimal(100)
        assert result == Decimal("100")


class TestContest:
    """Tests for Contest model."""

    def test_from_dict(self):
        """Test creating Contest from dict."""
        data = {
            "ID": 1,
            "Name": "5K Run",
            "NameShort": "5K",
            "Day": 1,
            "StartTime": 36000.0,  # 10:00:00
        }
        contest = Contest.model_validate(data)
        assert contest.id == 1
        assert contest.name == "5K Run"
        assert contest.name_short == "5K"

    def test_to_dict(self):
        """Test serializing Contest to dict."""
        contest = Contest(id=1, name="5K Run", name_short="5K")
        data = contest.model_dump(by_alias=True)
        assert data["ID"] == 1
        assert data["Name"] == "5K Run"


class TestParticipant:
    """Tests for Participant model."""

    def test_full_name(self):
        """Test full_name property."""
        p = Participant(firstname="John", lastname="Doe")
        assert p.full_name == "John Doe"

    def test_full_address(self):
        """Test full_address property."""
        p = Participant(street="123 Main St", zip="12345", city="Springfield")
        assert p.full_address == "123 Main St, 12345 Springfield"


class TestRegistration:
    """Tests for Registration model."""

    def test_is_active_enabled(self):
        """Test is_active when enabled."""
        now = datetime.now(timezone.utc)
        reg = Registration(
            name="Test",
            enabled=True,
            enabled_from=datetime(2020, 1, 1, tzinfo=timezone.utc),
            enabled_to=datetime(2030, 12, 31, tzinfo=timezone.utc),
        )
        assert reg.is_active() is True

    def test_is_active_disabled(self):
        """Test is_active when disabled."""
        reg = Registration(name="Test", enabled=False)
        assert reg.is_active() is False


class TestVoucher:
    """Tests for Voucher model."""

    def test_is_valid(self):
        """Test is_valid method."""
        voucher = Voucher(
            code="TEST123",
            type=VoucherType.AMOUNT,
            amount=Decimal("10.00"),
            valid_from=datetime(2020, 1, 1, tzinfo=timezone.utc),
            valid_until=datetime(2030, 12, 31, tzinfo=timezone.utc),
            reusable=0,  # Unlimited
        )
        assert voucher.is_valid() is True

    def test_is_valid_expired(self):
        """Test is_valid when expired."""
        voucher = Voucher(
            code="TEST123",
            valid_until=datetime(2020, 1, 1, tzinfo=timezone.utc),
        )
        assert voucher.is_valid() is False


class TestEmailTemplate:
    """Tests for EmailTemplate model."""

    def test_from_dict(self):
        """Test creating EmailTemplate from dict."""
        data = {
            "Name": "Confirmation",
            "Type": 0,
            "Subject": "Registration Confirmed",
            "Text": "Hello {Firstname}!",
            "HTML": True,
        }
        template = EmailTemplate.model_validate(data)
        assert template.name == "Confirmation"
        assert template.type == TemplateType.SINGLE
        assert template.html is True


class TestChipFileEntry:
    """Tests for ChipFileEntry model."""

    def test_create(self):
        """Test creating ChipFileEntry."""
        entry = ChipFileEntry(transponder="ABC123", identification="42")
        assert entry.transponder == "ABC123"
        assert entry.identification == "42"


class TestKiosk:
    """Tests for Kiosk models."""

    def test_kiosk_from_dict(self):
        """Test parsing a full kiosk config from API response."""
        data = {
            "Name": "CheckIn",
            "Key": "abc123",
            "Enabled": True,
            "EnabledFrom": None,
            "EnabledTo": None,
            "TransponderMode": 0,
            "AcceptedTransponders": 0,
            "IgnoreBibRanges": False,
            "AutoFinish": False,
            "CSS": "",
            "Title": "My Kiosk",
            "Steps": [
                {
                    "Type": "search",
                    "Label": "Search",
                    "Title": "",
                    "Text": "",
                    "OnlyShowIf": "",
                    "SearchFields": [{"Field": "Bib", "Hide": False, "Function": ""}],
                    "DisplayFields": [{"Type": "setting", "Value": "EventName", "Label": ""}],
                    "EditFields": None,
                    "Settings": {"AutoSel1": True, "Placeholder": "Enter bib"},
                },
                {
                    "Type": "edit",
                    "Label": "Check-In",
                    "Title": "",
                    "Text": "",
                    "OnlyShowIf": "",
                    "SearchFields": None,
                    "DisplayFields": [{"Type": "field", "Value": "FLName", "Label": ""}],
                    "EditFields": [
                        {
                            "Label": "Bib",
                            "Field": "bib",
                            "Special": "",
                            "Mandatory": True,
                            "ValidationRule": "",
                            "ValidationMsg": "",
                            "EventTools": "",
                        }
                    ],
                    "Settings": None,
                },
            ],
            "AfterSave": None,
        }
        kiosk = Kiosk.model_validate(data)
        assert kiosk.name == "CheckIn"
        assert kiosk.enabled is True
        assert kiosk.title == "My Kiosk"
        assert len(kiosk.steps) == 2

        search_step = kiosk.steps[0]
        assert search_step.type == "search"
        assert search_step.search_fields is not None
        assert len(search_step.search_fields) == 1
        assert search_step.search_fields[0].field == "Bib"
        assert search_step.settings == {"AutoSel1": True, "Placeholder": "Enter bib"}

        edit_step = kiosk.steps[1]
        assert edit_step.type == "edit"
        assert edit_step.edit_fields is not None
        assert edit_step.edit_fields[0].mandatory is True

    def test_kiosk_roundtrip(self):
        """Test that model_dump produces valid data for model_validate."""
        kiosk = Kiosk(
            name="Test",
            enabled=False,
            title="Test Kiosk",
            steps=[
                KioskStep(
                    type="edit",
                    label="Youth Info",
                    only_show_if="AgeOnDate(2026;06;13)<18",
                    display_fields=[
                        KioskDisplayField(type="field", value="EBZustimmung", label="EB Consent"),
                        KioskDisplayField(type="field", value="EBName", label="EB Name"),
                    ],
                )
            ],
        )
        data = kiosk.model_dump(by_alias=True)
        kiosk2 = Kiosk.model_validate(data)
        assert kiosk2.name == "Test"
        assert len(kiosk2.steps) == 1
        assert kiosk2.steps[0].only_show_if == "AgeOnDate(2026;06;13)<18"
        assert kiosk2.steps[0].display_fields is not None
        assert kiosk2.steps[0].display_fields[0].value == "EBZustimmung"

    def test_kiosk_step_only_show_if(self):
        """Test that OnlyShowIf is correctly serialized."""
        step = KioskStep(type="edit", label="Youth", only_show_if="AgeOnDate(2026;6;13)<18")
        data = step.model_dump(by_alias=True)
        assert data["OnlyShowIf"] == "AgeOnDate(2026;6;13)<18"

    def test_kiosk_edit_field_mandatory(self):
        """Test KioskEditField mandatory flag."""
        field = KioskEditField(label="Bib", field="bib", mandatory=True)
        assert field.mandatory is True
        data = field.model_dump(by_alias=True)
        assert data["Mandatory"] is True

    def test_kiosk_after_save_SaveValue(self):
        """Test KioskAfterSave SaveValue configuration."""
        action = KioskAfterSave(type="SaveValue", destination="CheckIn", value="1")
        data = action.model_dump(by_alias=True)
        assert data["Type"] == "SaveValue"
        assert data["Destination"] == "CheckIn"
        assert data["Value"] == "1"

    def test_kiosk_after_save_roundtrip(self):
        """Test Kiosk with AfterSave survives model round-trip."""
        kiosk = Kiosk(
            name="Test",
            after_save=[KioskAfterSave(type="SaveValue", destination="CheckIn", value="1")],
        )
        data = kiosk.model_dump(by_alias=True)
        kiosk2 = Kiosk.model_validate(data)
        assert kiosk2.after_save is not None
        assert len(kiosk2.after_save) == 1
        assert kiosk2.after_save[0].destination == "CheckIn"

    def test_kiosk_after_save_from_api_response(self):
        """Test parsing AfterSave from real API response format."""
        data = {
            "Name": "Check-In", "Key": "x", "Enabled": False,
            "Steps": [], "AfterSave": [
                {"Type": "SaveValue", "Value": "1", "Destination": "CheckIn",
                 "Filter": "", "Printer": "", "Flags": []}
            ],
        }
        kiosk = Kiosk.model_validate(data)
        assert kiosk.after_save is not None
        assert kiosk.after_save[0].type == "SaveValue"
        assert kiosk.after_save[0].destination == "CheckIn"


class TestChatMessage:
    """Tests for ChatMessage — uses single-character JSON aliases."""

    def test_parse_from_api(self):
        data = {"i": 7, "u": "alice", "d": "2024-06-01 10:00", "m": "Hello!"}
        msg = ChatMessage.model_validate(data)
        assert msg.id == 7
        assert msg.username == "alice"
        assert msg.date == "2024-06-01 10:00"
        assert msg.message == "Hello!"

    def test_roundtrip(self):
        msg = ChatMessage(id=1, username="bob", date="now", message="hi")
        data = msg.model_dump(by_alias=True)
        assert data["i"] == 1
        assert data["u"] == "bob"
        assert data["d"] == "now"
        assert data["m"] == "hi"
        assert ChatMessage.model_validate(data).message == "hi"


class TestVersion:
    """Tests for Version — uses lowercase JSON aliases."""

    def test_parse_from_api(self):
        data = {"major": 12, "minor": 3, "revision": 45, "tag": "release", "hash": "abc123"}
        v = Version.model_validate(data)
        assert v.major == 12
        assert v.minor == 3
        assert v.revision == 45
        assert v.tag == "release"

    def test_roundtrip(self):
        v = Version(major=1, minor=2, revision=3, tag="", hash="")
        data = v.model_dump(by_alias=True)
        assert data["major"] == 1
        assert data["minor"] == 2
        assert "revision" in data


class TestForwardingInfo:
    def test_parse(self):
        data = {"BytesSent": 1024, "BytesReceived": 512}
        info = ForwardingInfo.model_validate(data)
        assert info.bytes_sent == 1024
        assert info.bytes_received == 512

    def test_roundtrip(self):
        info = ForwardingInfo(bytes_sent=100, bytes_received=200)
        data = info.model_dump(by_alias=True)
        assert data["BytesSent"] == 100
        assert ForwardingInfo.model_validate(data).bytes_received == 200


class TestGroupTimes:
    def test_parse(self):
        data = {
            "Mode": "wave",
            "WaveField": "WaveNo",
            "Items": [
                {"ID": 1, "Time": "3600", "Count": 50},
                {"ID": "A", "Time": "0", "Item": "special", "Count": 10},
            ],
        }
        gt = GroupTimes.model_validate(data)
        assert gt.mode == "wave"
        assert len(gt.items) == 2
        assert gt.items[0].count == 50
        assert gt.items[1].id == "A"
        assert gt.items[1].item == "special"

    def test_roundtrip(self):
        gt = GroupTimes(mode="wave", wave_field="WaveNo", items=[GroupTime(id=1, count=5)])
        data = gt.model_dump(by_alias=True)
        assert data["Mode"] == "wave"
        assert data["Items"][0]["ID"] == 1


class TestRawDataRule:
    def test_parse(self):
        data = {"ID": 3, "ResultID": 1, "ContestID": 2, "Mode": 0, "N": 1,
                "Min": 0, "MinOffset": "0", "Max": 0, "MaxOffset": "0",
                "Ref": 0, "RefOffset": "0"}
        rule = RawDataRule.model_validate(data)
        assert rule.id == 3
        assert rule.result_id == 1
        assert rule.contest_id == 2

    def test_roundtrip(self):
        rule = RawDataRule(id=1, result_id=2, contest_id=3)
        data = rule.model_dump(by_alias=True)
        assert data["ID"] == 1
        assert data["ResultID"] == 2
        assert RawDataRule.model_validate(data).contest_id == 3


class TestSimpleAPIItem:
    def test_parse(self):
        data = {"Disabled": False, "Key": "results", "URL": "https://example.com", "Label": "Results"}
        item = SimpleAPIItem.model_validate(data)
        assert item.key == "results"
        assert item.url == "https://example.com"
        assert item.disabled is False

    def test_roundtrip(self):
        item = SimpleAPIItem(key="k", url="u", label="l")
        data = item.model_dump(by_alias=True)
        assert data["Key"] == "k"
        assert SimpleAPIItem.model_validate(data).label == "l"


class TestWebHook:
    def test_parse(self):
        data = {
            "ID": 5, "Disabled": False, "Name": "My Hook",
            "Type": 0, "URL": "https://hook.example.com",
            "Fields": ["Bib", "Firstname"], "Filter": "", "OrderPos": 1,
        }
        hook = WebHook.model_validate(data)
        assert hook.id == 5
        assert hook.type == WebHookType.PARTICIPANT_NEW
        assert hook.fields == ["Bib", "Firstname"]

    def test_roundtrip(self):
        hook = WebHook(name="test", type=WebHookType.MOD_JOB_ID, url="https://x.com")
        data = hook.model_dump(by_alias=True)
        assert data["Type"] == WebHookType.MOD_JOB_ID
        assert WebHook.model_validate(data).url == "https://x.com"


class TestTeamScore:
    def test_parse(self):
        data = {"ID": 1, "Name": "Mixed Relay", "Filter": "[Sex]='M'", "MaxTeams": 3}
        ts = TeamScore.model_validate(data)
        assert ts.id == 1
        assert ts.name == "Mixed Relay"
        assert ts.max_teams == 3

    def test_roundtrip(self):
        ts = TeamScore(id=2, name="Open", filter="")
        data = ts.model_dump(by_alias=True)
        assert data["ID"] == 2
        assert data["Name"] == "Open"
        assert TeamScore.model_validate(data).id == 2


class TestArchivesModels:
    def test_match_parse(self):
        data = {"ID": 42, "FirstName": "Anna", "LastName": "Müller", "Year": 1985}
        m = ArchivesMatch.model_validate(data)
        assert m.id == 42
        assert m.first_name == "Anna"
        assert m.year == 1985

    def test_participant_parse(self):
        data = {
            "ID": 1, "Lastname": "Müller", "Firstname": "Anna", "Sex": "F",
            "Participations": [
                {"Event": "evt1", "Contest": 2, "Bib": 99, "Time": "1:23:45",
                 "TotRank": 5, "MFRank": 3, "AGRank": 1}
            ],
        }
        p = ArchivesParticipant.model_validate(data)
        assert p.lastname == "Müller"
        assert len(p.participations) == 1
        assert p.participations[0].bib == 99

    def test_participation_ext_parse(self):
        data = {
            "EventName": "Berlin Marathon 2023", "ContestName": "Full",
            "FinalTime": "3:45:00", "TotRank": 120, "MFRank": 80, "AGRank": 10, "Bib": 42,
        }
        pe = ParticipationExt.model_validate(data)
        assert pe.event_name == "Berlin Marathon 2023"
        assert pe.bib == 42

    def test_participant_roundtrip(self):
        p = ArchivesParticipant(id=1, lastname="Smith", firstname="John")
        data = p.model_dump(by_alias=True)
        assert data["Lastname"] == "Smith"
        assert ArchivesParticipant.model_validate(data).firstname == "John"


class TestCertificate:
    def test_element_parse(self):
        data = {
            "Type": 1, "Data": "Hello", "Left": "10", "Top": "20",
            "Width": "100", "Height": "50", "FontName": "Arial",
            "FontSize": 12, "Page": 1, "DF": "[Firstname]",
        }
        el = CertificateElement.model_validate(data)
        assert el.type == ElementType.TEXT
        assert el.data == "Hello"
        assert el.dynamic_format == "[Firstname]"

    def test_zone_parse(self):
        data = {"Top": "148", "Page": 1, "Type": "fold"}
        z = CertificateZone.model_validate(data)
        assert z.type == "fold"
        assert z.page == 1

    def test_certificate_parse(self):
        data = {
            "CertificateName": "BibNumber",
            "PageSize": "A4", "PageFormat": "Portrait",
            "Copies": 1,
            "Fields": [{"Type": 1, "Data": "Hello", "Left": "0", "Top": "0",
                         "Width": "50", "Height": "20", "Page": 1}],
            "Zones": [],
        }
        cert = Certificate.model_validate(data)
        assert cert.name == "BibNumber"
        assert cert.page_size == "A4"
        assert len(cert.elements) == 1
        assert cert.elements[0].type == ElementType.TEXT

    def test_certificate_roundtrip(self):
        cert = Certificate(name="Test", page_size="A4", page_format="Portrait")
        data = cert.model_dump(by_alias=True)
        assert data["CertificateName"] == "Test"
        assert data["PageSize"] == "A4"
        assert Certificate.model_validate(data).page_format == "Portrait"


class TestCertificateSet:
    def test_parse(self):
        data = {
            "Name": "Age Group Awards", "CertificateName": "AwardCert",
            "CertificateSetType": 0, "FilterRankOperator": "<=",
            "FilterRankCompare": 3,
        }
        cs = CertificateSet.model_validate(data)
        assert cs.name == "Age Group Awards"
        assert cs.certificate == "AwardCert"
        assert cs.certificate_set_type == CertificateSetType.SINGLE
        assert cs.filter_rank_compare == 3

    def test_roundtrip(self):
        cs = CertificateSet(name="Top3", certificate="Cert1",
                            certificate_set_type=CertificateSetType.TEAM)
        data = cs.model_dump(by_alias=True)
        assert data["Name"] == "Top3"
        assert data["CertificateSetType"] == CertificateSetType.TEAM
        assert CertificateSet.model_validate(data).certificate == "Cert1"


class TestStatistics:
    def test_parse(self):
        data = {
            "StatisticName": "By Country", "Type": "table",
            "Row": "[Country]", "Col": "", "Aggregation": 1,
        }
        s = Statistics.model_validate(data)
        assert s.name == "By Country"
        assert s.aggregation == Aggregation.COUNT

    def test_roundtrip(self):
        s = Statistics(name="Test", aggregation=Aggregation.SUM, row="[Contest]")
        data = s.model_dump(by_alias=True)
        assert data["StatisticName"] == "Test"
        assert data["Aggregation"] == Aggregation.SUM
        assert Statistics.model_validate(data).row == "[Contest]"


class TestLabel:
    def test_parse(self):
        data = {
            "LabelName": "Sticker", "PageSize": 3, "PageFormat": 0,
            "Width": "70", "Height": "36",
            "Direction": 0, "BarcodeType": 0, "Alignment": 1,
        }
        label = Label.model_validate(data)
        assert label.name == "Sticker"
        assert label.direction == LabelDirection.DOWN_THEN_RIGHT
        assert label.barcode_type == LabelBarcodeType.NO_BARCODE

    def test_roundtrip(self):
        label = Label(name="MyLabel", direction=LabelDirection.RIGHT_THEN_DOWN,
                      barcode_type=LabelBarcodeType.CODE128)
        data = label.model_dump(by_alias=True)
        assert data["LabelName"] == "MyLabel"
        assert data["Direction"] == LabelDirection.RIGHT_THEN_DOWN
        assert Label.model_validate(data).barcode_type == LabelBarcodeType.CODE128
