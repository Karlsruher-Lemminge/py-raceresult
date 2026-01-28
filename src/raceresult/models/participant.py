"""Participant model for Raceresult API.

Based on go-model/model.go:115-168.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field

from raceresult.models.types import RRDate, RRDateTime, RRDecimal


class Participant(BaseModel):
    """Participant data model.

    Based on go-model/model.go:115-168.
    """

    id: int = Field(default=0, alias="ID")
    bib: int = Field(default=0, alias="Bib")
    transponder1: str = Field(default="", alias="Transponder1")
    transponder2: str = Field(default="", alias="Transponder2")
    reg_no: str = Field(default="", alias="RegNo")
    title: str = Field(default="", alias="Title")
    lastname: str = Field(default="", alias="Lastname")
    firstname: str = Field(default="", alias="Firstname")
    sex: str = Field(default="", alias="Sex")
    date_of_birth: RRDate = Field(default=None, alias="DateOfBirth")
    street: str = Field(default="", alias="Street")
    zip: str = Field(default="", alias="ZIP")
    city: str = Field(default="", alias="City")
    state2: str = Field(default="", alias="State2")
    country: str = Field(default="", alias="Country")
    nation: str = Field(default="", alias="Nation")
    age_group1: int = Field(default=0, alias="AgeGroup1")
    age_group2: int = Field(default=0, alias="AgeGroup2")
    age_group3: int = Field(default=0, alias="AgeGroup3")
    club: str = Field(default="", alias="Club")
    contest: int = Field(default=0, alias="Contest")
    status: int = Field(default=0, alias="Status")
    booleans: int = Field(default=0, alias="Booleans")
    paid_entry_fee: RRDecimal = Field(default=Decimal(0), alias="PaidEntryFee")
    phone: str = Field(default="", alias="Phone")
    cell_phone: str = Field(default="", alias="CellPhone")
    send_sms: int = Field(default=0, alias="SendSMS")
    email: str = Field(default="", alias="Email")
    account_no: str = Field(default="", alias="AccountNo")
    branch_no: str = Field(default="", alias="BranchNo")
    bankname: str = Field(default="", alias="Bankname")
    account_owner: str = Field(default="", alias="AccountOwner")
    iban: str = Field(default="", alias="IBAN")
    bic: str = Field(default="", alias="BIC")
    sepa_mandate: str = Field(default="", alias="SEPAMandate")
    comment: str = Field(default="", alias="Comment")
    created: RRDateTime = Field(default=None, alias="Created")
    modified: RRDateTime = Field(default=None, alias="Modified")
    uploaded: RRDateTime = Field(default=None, alias="Uploaded")
    created_by: str = Field(default="", alias="CreatedBy")
    foreign_id: int = Field(default=0, alias="ForeignID")
    record_pay_guid: str = Field(default="", alias="RecordPayGUID")
    activation_event_id: str = Field(default="", alias="ActivationEventID")
    op_json: str = Field(default="", alias="OPJSON")
    op_id: int = Field(default=0, alias="OPID")
    license: str = Field(default="", alias="License")
    show_underscores: bool = Field(default=False, alias="ShowUnderscores")
    group_reg_pos: int = Field(default=0, alias="GroupRegPos")
    group_id: int = Field(default=0, alias="GroupID")
    password: str = Field(default="", alias="Password")
    voucher: str = Field(default="", alias="Voucher")
    language: str = Field(default="", alias="Language")

    model_config = {"populate_by_name": True}

    @property
    def full_name(self) -> str:
        """Get the full name of the participant."""
        parts = []
        if self.firstname:
            parts.append(self.firstname)
        if self.lastname:
            parts.append(self.lastname)
        return " ".join(parts)

    @property
    def full_address(self) -> str:
        """Get the full address of the participant."""
        parts = []
        if self.street:
            parts.append(self.street)
        if self.zip or self.city:
            city_part = " ".join(filter(None, [self.zip, self.city]))
            parts.append(city_part)
        if self.country:
            parts.append(self.country)
        return ", ".join(parts)


class ParticipantNewResponse(BaseModel):
    """Response from creating a new participant.

    Based on go-model/model.go:171-174.
    """

    id: int = Field(default=0, alias="ID")
    bib: int = Field(default=0, alias="Bib")

    model_config = {"populate_by_name": True}


class ImportResult(BaseModel):
    """Result of an import operation.

    Based on go-model/model.go:660-664.
    """

    added: int = Field(default=0, alias="Added")
    updated: int = Field(default=0, alias="Updated")
    pids: list[int] = Field(default_factory=list, alias="PIDs")

    model_config = {"populate_by_name": True}


class SaveValueArrayItem(BaseModel):
    """Item for saving multiple values at once.

    Based on go-model/model.go:643-648.
    """

    bib: int = Field(default=0, alias="Bib")
    pid: int = Field(default=0, alias="PID")
    field_name: str = Field(default="", alias="FieldName")
    value: str | int | float | bool | None = Field(default=None, alias="Value")

    model_config = {"populate_by_name": True}
