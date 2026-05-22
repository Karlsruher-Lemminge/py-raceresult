"""Kiosk models for Raceresult API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from raceresult.models.types import RRDateTime


class KioskAfterSave(BaseModel):
    """Action performed after a kiosk step is saved.

    Common types:
    - "SaveValue": set a participant field to a fixed value
      (use destination=field name, value=value to set)
    - "SendTemplate": send an email/SMS template
      (use value=template name)
    """

    type: str = Field(default="", alias="Type")
    value: str = Field(default="", alias="Value")
    destination: str = Field(default="", alias="Destination")
    filter: str = Field(default="", alias="Filter")
    printer: str = Field(default="", alias="Printer")
    flags: list[str] = Field(default_factory=list, alias="Flags")

    model_config = {"populate_by_name": True}


class KioskSearchField(BaseModel):
    """A field used for searching participants in the kiosk."""

    field: str = Field(default="", alias="Field")
    hide: bool = Field(default=False, alias="Hide")
    function: str = Field(default="", alias="Function")

    model_config = {"populate_by_name": True}


class KioskDisplayField(BaseModel):
    """A field displayed to the operator in the kiosk."""

    type: str = Field(default="", alias="Type")
    value: str = Field(default="", alias="Value")
    label: str = Field(default="", alias="Label")

    model_config = {"populate_by_name": True}


class KioskEditField(BaseModel):
    """An editable field in the kiosk."""

    label: str = Field(default="", alias="Label")
    field: str = Field(default="", alias="Field")
    special: str = Field(default="", alias="Special")
    mandatory: bool = Field(default=False, alias="Mandatory")
    validation_rule: str = Field(default="", alias="ValidationRule")
    validation_msg: str = Field(default="", alias="ValidationMsg")
    event_tools: str = Field(default="", alias="EventTools")

    model_config = {"populate_by_name": True}


class KioskStep(BaseModel):
    """A step in the kiosk workflow.

    Steps control the flow of the check-in process. Common types:
    - "search": participant lookup screen
    - "edit": display and edit participant data
    """

    type: str = Field(default="", alias="Type")
    label: str = Field(default="", alias="Label")
    title: str = Field(default="", alias="Title")
    text: str = Field(default="", alias="Text")
    only_show_if: str = Field(default="", alias="OnlyShowIf")
    search_fields: list[KioskSearchField] | None = Field(default=None, alias="SearchFields")
    display_fields: list[KioskDisplayField] | None = Field(default=None, alias="DisplayFields")
    edit_fields: list[KioskEditField] | None = Field(default=None, alias="EditFields")
    settings: dict[str, Any] | None = Field(default=None, alias="Settings")
    # Note: Settings for search steps contains keys: AutoSel1 (bool), Placeholder (str), Filter (str)

    model_config = {"populate_by_name": True}


class Kiosk(BaseModel):
    """Check-In Kiosk configuration."""

    name: str = Field(default="", alias="Name")
    key: str = Field(default="", alias="Key")
    enabled: bool = Field(default=False, alias="Enabled")
    enabled_from: RRDateTime = Field(default=None, alias="EnabledFrom")
    enabled_to: RRDateTime = Field(default=None, alias="EnabledTo")
    transponder_mode: int = Field(default=0, alias="TransponderMode")
    accepted_transponders: int = Field(default=0, alias="AcceptedTransponders")
    ignore_bib_ranges: bool = Field(default=False, alias="IgnoreBibRanges")
    auto_finish: bool = Field(default=False, alias="AutoFinish")
    css: str = Field(default="", alias="CSS")
    title: str = Field(default="", alias="Title")
    steps: list[KioskStep] = Field(default_factory=list, alias="Steps")
    after_save: list[KioskAfterSave] | None = Field(default=None, alias="AfterSave")

    model_config = {"populate_by_name": True}
