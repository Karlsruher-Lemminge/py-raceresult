"""CertificateSet model for Raceresult API."""

from __future__ import annotations

from enum import IntEnum

from pydantic import BaseModel, Field


class CertificateSetType(IntEnum):
    """Type of certificate set."""

    SINGLE = 0
    TEAM = 1
    TEAM_MULTI = 2


class CertificateSet(BaseModel):
    """Certificate set definition."""

    name: str = Field(default="", alias="Name")
    certificate: str = Field(default="", alias="CertificateName")
    certificate_set_type: CertificateSetType = Field(
        default=CertificateSetType.SINGLE, alias="CertificateSetType"
    )
    team_score: int = Field(default=0, alias="TeamScore")
    filter_rank_id: int = Field(default=0, alias="FilterRankID")
    filter_rank_operator: str = Field(default="", alias="FilterRankOperator")
    filter_rank_compare: int = Field(default=0, alias="FilterRankCompare")
    filter_ayn: int = Field(default=0, alias="FilterAYN")
    filter_only_finishers: bool = Field(default=False, alias="FilterOnlyFinishers")
    filter_general: str = Field(default="", alias="FilterGeneral")
    only_unshown_certificates: bool = Field(default=False, alias="OnlyUnshownCertificates")
    sort1: str = Field(default="", alias="Sort1")
    sort2: str = Field(default="", alias="Sort2")
    sort3: str = Field(default="", alias="Sort3")
    sort4: str = Field(default="", alias="Sort4")
    sort_desc1: bool = Field(default=False, alias="SortDesc1")
    sort_desc2: bool = Field(default=False, alias="SortDesc2")
    sort_desc3: bool = Field(default=False, alias="SortDesc3")
    sort_desc4: bool = Field(default=False, alias="SortDesc4")

    model_config = {"populate_by_name": True}
