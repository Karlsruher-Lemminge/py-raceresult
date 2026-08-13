"""Raceresult data models."""

from raceresult.models.email import EmailTemplate, HTTPHeader, Preview, TemplateType
from raceresult.models.event import (
    AgeGroup,
    BibRange,
    Contest,
    CustomField,
    CustomFieldType,
    EntryFee,
    EntryFeeItem,
    Ranking,
    Result,
    Split,
    UserDefinedField,
)
from raceresult.models.kiosk import (
    Kiosk,
    KioskAfterSave,
    KioskDisplayField,
    KioskEditField,
    KioskSearchField,
    KioskStep,
)
from raceresult.models.participant import Participant, ParticipantNewResponse
from raceresult.models.payment import (
    MethodOption,
    PaymentConstants,
    Voucher,
    VoucherType,
)
from raceresult.models.public import OAuthToken, UserInfo, UserRight
from raceresult.models.registration import (
    AdditionalValue,
    AfterSave,
    Confirmation,
    Element,
    ErrorMessages,
    FormField,
    Registration,
    Step,
    Style,
    ValidationRule,
    Value,
)
from raceresult.models.registration import (
    PaymentMethod as RegPaymentMethod,
)
from raceresult.models.timing import (
    ChipFileEntry,
    Passing,
    PassingPosition,
    PassingToProcess,
    RawData,
    RawDataReduced,
    Time,
    TimingPoint,
    TimingPointRule,
)
from raceresult.models.types import RRDate, RRDateTime, RRDecimal

__all__ = [
    # Types
    "RRDate",
    "RRDateTime",
    "RRDecimal",
    # Event
    "AgeGroup",
    "BibRange",
    "Contest",
    "CustomField",
    "CustomFieldType",
    "EntryFee",
    "EntryFeeItem",
    "Ranking",
    "Result",
    "Split",
    "UserDefinedField",
    # Participant
    "Participant",
    "ParticipantNewResponse",
    # Registration
    "Registration",
    "Step",
    "Element",
    "FormField",
    "Style",
    "Value",
    "AdditionalValue",
    "Confirmation",
    "AfterSave",
    "RegPaymentMethod",
    "ValidationRule",
    "ErrorMessages",
    # Payment
    "Voucher",
    "VoucherType",
    "MethodOption",
    "PaymentConstants",
    # Email
    "EmailTemplate",
    "TemplateType",
    "HTTPHeader",
    "Preview",
    # Timing
    "TimingPoint",
    "TimingPointRule",
    "ChipFileEntry",
    "RawData",
    "RawDataReduced",
    "Time",
    "Passing",
    "PassingPosition",
    "PassingToProcess",
    # Kiosk
    "Kiosk",
    "KioskAfterSave",
    "KioskStep",
    "KioskDisplayField",
    "KioskEditField",
    "KioskSearchField",
    # Public
    "UserInfo",
    "UserRight",
    "OAuthToken",
]
