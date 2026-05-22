"""Tests for raceresult models."""

from datetime import date, datetime, timezone
from decimal import Decimal

import pytest

from raceresult.models.types import RRDate, RRDateTime, RRDecimal
from raceresult.models.event import Contest, AgeGroup, CustomField, CustomFieldType
from raceresult.models.participant import Participant
from raceresult.models.registration import Registration, Step, Element, FormField
from raceresult.models.payment import Voucher, VoucherType
from raceresult.models.email import EmailTemplate, TemplateType
from raceresult.models.timing import ChipFileEntry, TimingPoint
from raceresult.models.kiosk import Kiosk, KioskAfterSave, KioskStep, KioskDisplayField, KioskEditField, KioskSearchField


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
