"""Archives models for Raceresult API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from raceresult.models.types import RRDate


class ArchivesMatch(BaseModel):
    """Match returned by archives search."""

    id: int = Field(default=0, alias="ID")
    first_name: str = Field(default="", alias="FirstName")
    last_name: str = Field(default="", alias="LastName")
    year: int = Field(default=0, alias="Year")

    model_config = {"populate_by_name": True}


class ArchivesParticipation(BaseModel):
    """Participation record within an archived participant."""

    event: str = Field(default="", alias="Event")
    contest: int = Field(default=0, alias="Contest")
    time: str = Field(default="", alias="Time")
    tot_rank: int = Field(default=0, alias="TotRank")
    mf_rank: int = Field(default=0, alias="MFRank")
    ag_rank: int = Field(default=0, alias="AGRank")
    bib: int = Field(default=0, alias="Bib")

    model_config = {"populate_by_name": True}


class ArchivesParticipant(BaseModel):
    """Participant record from the archives."""

    id: int = Field(default=0, alias="ID")
    transponder1: str = Field(default="", alias="Transponder1")
    transponder2: str = Field(default="", alias="Transponder2")
    reg_no: str = Field(default="", alias="RegNo")
    title: str = Field(default="", alias="Title")
    language: str = Field(default="", alias="Language")
    lastname: str = Field(default="", alias="Lastname")
    firstname: str = Field(default="", alias="Firstname")
    sex: str = Field(default="", alias="Sex")
    date_of_birth: RRDate = Field(default=None, alias="DateOfBirth")
    street: str = Field(default="", alias="Street")
    zip: str = Field(default="", alias="ZIP")
    state: str = Field(default="", alias="State")
    city: str = Field(default="", alias="City")
    country: int = Field(default=0, alias="Country")
    nation: int = Field(default=0, alias="Nation")
    club: str = Field(default="", alias="Club")
    license: str = Field(default="", alias="License")
    phone: str = Field(default="", alias="Phone")
    cell_phone: str = Field(default="", alias="CellPhone")
    email: str = Field(default="", alias="Email")
    add_fields: dict[str, Any] = Field(default_factory=dict, alias="AddFields")
    participations: list[ArchivesParticipation] = Field(default_factory=list, alias="Participations")

    model_config = {"populate_by_name": True}


class ParticipationExt(BaseModel):
    """Extended participation record (cross-event history)."""

    event_date: RRDate = Field(default=None, alias="EventDate")
    event_name: str = Field(default="", alias="EventName")
    contest_name: str = Field(default="", alias="ContestName")
    final_time: str = Field(default="", alias="FinalTime")
    tot_rank: int = Field(default=0, alias="TotRank")
    mf_rank: int = Field(default=0, alias="MFRank")
    ag_rank: int = Field(default=0, alias="AGRank")
    bib: int = Field(default=0, alias="Bib")

    model_config = {"populate_by_name": True}
