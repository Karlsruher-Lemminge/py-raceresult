"""Event-related models for Raceresult API.

Based on go-model/model.go.
"""

from __future__ import annotations

from decimal import Decimal
from enum import IntEnum

from pydantic import BaseModel, Field

from raceresult.models.types import RRDate, RRDecimal


class CustomFieldType(IntEnum):
    """Type of a custom field.

    Based on go-model/model.go:79-94.
    """

    TEXT = 0
    DROP_DOWN = 1
    YES_NO = 2
    INTEGER = 3
    DECIMAL = 4
    DATE = 5
    CURRENCY = 6
    COUNTRY = 7
    EMAIL = 8
    CELL_PHONE = 9
    TRANSPONDER = 10


class AgeGroup(BaseModel):
    """Age group definition.

    Based on go-model/model.go:15-27.

    Note: Age groups can be based on either birth year or birth date.
    This is determined by the date_start/date_end fields:
    - If they specify full dates (e.g., 1990-01-01 to 1990-12-31), it's by birth date
    - If they specify year boundaries (e.g., 1990-01-01 to 1990-01-01), it's by birth year
    """

    id: int = Field(default=0, alias="ID")
    name: str = Field(default="", alias="Name")
    name_short: str = Field(default="", alias="NameShort")
    date_start: RRDate = Field(default=None, alias="DateStart")
    date_end: RRDate = Field(default=None, alias="DateEnd")
    age_from: int = Field(default=0, alias="AgeFrom")
    age_to: int = Field(default=0, alias="AgeTo")
    contest: int = Field(default=0, alias="Contest")
    ag_set: int = Field(default=0, alias="AGSet")
    order_pos: int = Field(default=0, alias="OrderPos")
    sex: str = Field(default="", alias="Sex")

    model_config = {"populate_by_name": True}


class BibRange(BaseModel):
    """Bib number range definition.

    Based on go-model/model.go:29-40.
    """

    id: int = Field(default=0, alias="ID")
    bib_start: int = Field(default=0, alias="BibStart")
    bib_end: int = Field(default=0, alias="BibEnd")
    contest: int = Field(default=0, alias="Contest")
    time_difference: RRDecimal = Field(default=Decimal(0), alias="TimeDifference")
    finish_time_limit: RRDecimal = Field(default=Decimal(0), alias="FinishTimeLimit")
    comment: str = Field(default="", alias="Comment")
    filter: str = Field(default="", alias="Filter")

    model_config = {"populate_by_name": True}


class Contest(BaseModel):
    """Contest/competition definition.

    Based on go-model/model.go:42-76.
    """

    id: int = Field(default=0, alias="ID")
    name: str = Field(default="", alias="Name")
    name_short: str = Field(default="", alias="NameShort")
    age_start: RRDate = Field(default=None, alias="AgeStart")
    age_end: RRDate = Field(default=None, alias="AgeEnd")
    sex: str = Field(default="", alias="Sex")
    day: int = Field(default=0, alias="Day")
    start_time: RRDecimal = Field(default=Decimal(0), alias="StartTime")
    length: RRDecimal = Field(default=Decimal(0), alias="Length")
    length_unit: str = Field(default="", alias="LengthUnit")
    time_format: str = Field(default="", alias="TimeFormat")
    time_rounding: int = Field(default=0, alias="TimeRounding")
    start_transponder: int = Field(default=0, alias="StartTransponder")
    start_result: int = Field(default=0, alias="StartResult")
    time_difference: RRDecimal = Field(default=Decimal(0), alias="TimeDifference")
    finish_result: int = Field(default=0, alias="FinishResult")
    finish_time_limit: RRDecimal = Field(default=Decimal(0), alias="FinishTimeLimit")
    laps: int = Field(default=0, alias="Laps")
    min_result_id: int = Field(default=0, alias="MinResultID")
    min_lap_time: RRDecimal = Field(default=Decimal(0), alias="MinLapTime")
    timing_mode: int = Field(default=0, alias="TimingMode")
    timing_mode_filter: str = Field(default="", alias="TimingModeFilter")
    attributes: str = Field(default="", alias="Attributes")
    order_pos: float = Field(default=0.0, alias="OrderPos")
    sort1: str = Field(default="", alias="Sort1")
    sort2: str = Field(default="", alias="Sort2")
    sort3: str = Field(default="", alias="Sort3")
    sort4: str = Field(default="", alias="Sort4")
    sort_desc1: bool = Field(default=False, alias="SortDesc1")
    sort_desc2: bool = Field(default=False, alias="SortDesc2")
    sort_desc3: bool = Field(default=False, alias="SortDesc3")
    sort_desc4: bool = Field(default=False, alias="SortDesc4")
    inactive: bool = Field(default=False, alias="Inactive")

    model_config = {"populate_by_name": True}


class CustomField(BaseModel):
    """Custom field definition.

    Based on go-model/model.go:96-112.
    """

    id: int = Field(default=0, alias="ID")
    name: str = Field(default="", alias="Name")
    alt_name: str = Field(default="", alias="AltName")
    group: str = Field(default="", alias="Group")
    field_type: CustomFieldType = Field(default=CustomFieldType.TEXT, alias="Type")
    enabled: bool = Field(default=False, alias="Enabled")
    mandatory: bool = Field(default=False, alias="Mandatory")
    config: str = Field(default="", alias="Config")
    default: str = Field(default="", alias="Default")
    placeholder: str = Field(default="", alias="Placeholder")
    label: str = Field(default="", alias="Label")
    order_pos: int = Field(default=0, alias="OrderPos")
    min_len: int = Field(default=0, alias="MinLen")
    max_len: int = Field(default=0, alias="MaxLen")

    model_config = {"populate_by_name": True}


class EntryFee(BaseModel):
    """Entry fee definition.

    Based on go-model/model.go:176-195.
    """

    id: int = Field(default=0, alias="ID")
    name: str = Field(default="", alias="Name")
    contest: int = Field(default=0, alias="Contest")
    date_start: RRDate = Field(default=None, alias="DateStart")
    date_end: RRDate = Field(default=None, alias="DateEnd")
    reg_start: RRDate = Field(default=None, alias="RegStart")
    reg_end: RRDate = Field(default=None, alias="RegEnd")
    field: str = Field(default="", alias="Field")
    operator: str = Field(default="", alias="Operator")
    value: str = Field(default="", alias="Value")
    fee: RRDecimal = Field(default=Decimal(0), alias="Fee")
    show_as_basic_fee: bool = Field(default=False, alias="ShowAsBasicFee")
    is_multiplicator: bool = Field(default=False, alias="IsMultiplicator")
    multiplication: str = Field(default="", alias="Multiplication")
    category: str = Field(default="", alias="Category")
    tax: RRDecimal = Field(default=Decimal(0), alias="Tax")
    order_pos: int = Field(default=0, alias="OrderPos")

    model_config = {"populate_by_name": True}


class EntryFeeItem(BaseModel):
    """Entry fee item charged to a participant.

    Based on go-model/model.go:651-658.
    """

    id: int = Field(default=0, alias="ID")
    name: str = Field(default="", alias="Name")
    fee: RRDecimal = Field(default=Decimal(0), alias="Fee")
    field: str = Field(default="", alias="Field")
    tax: RRDecimal = Field(default=Decimal(0), alias="Tax")
    multiplication: RRDecimal = Field(default=Decimal(0), alias="Multiplication")

    model_config = {"populate_by_name": True}


class Ranking(BaseModel):
    """Ranking definition.

    Based on go-model/model.go:266-276.
    """

    id: int = Field(default=0, alias="ID")
    name: str = Field(default="", alias="Name")
    group: list[str] = Field(default_factory=list, alias="Group")
    sort: list[str] = Field(default_factory=list, alias="Sort")
    sort_desc: list[bool] = Field(default_factory=list, alias="SortDesc")
    use_ties: bool = Field(default=False, alias="UseTies")
    contest_sort: bool = Field(default=False, alias="ContestSort")
    filter: str = Field(default="", alias="Filter")

    model_config = {"populate_by_name": True}


class Result(BaseModel):
    """Result definition.

    Based on go-model/model.go:357-364.
    """

    id: int = Field(default=0, alias="ID")
    name: str = Field(default="", alias="Name")
    formula: str = Field(default="", alias="Formula")
    time_format: str = Field(default="", alias="TimeFormat")
    location: str = Field(default="", alias="Location")
    time_rounding: int = Field(default=0, alias="TimeRounding")

    model_config = {"populate_by_name": True}


class Split(BaseModel):
    """Split definition.

    Based on go-model/model.go:367-390.
    """

    id: int = Field(default=0, alias="ID")
    contest: int = Field(default=0, alias="Contest")
    name: str = Field(default="", alias="Name")
    timing_point: str = Field(default="", alias="TimingPoint")
    backup: str = Field(default="", alias="Backup")
    backup_offset: RRDecimal = Field(default=Decimal(0), alias="BackupOffset")
    type_of_sport: int = Field(default=0, alias="TypeOfSport")
    distance: RRDecimal = Field(default=Decimal(0), alias="Distance")
    distance_unit: str = Field(default="", alias="DistanceUnit")
    distance_from: int = Field(default=0, alias="DistanceFrom")
    time_min: RRDecimal = Field(default=Decimal(0), alias="TimeMin")
    time_max: RRDecimal = Field(default=Decimal(0), alias="TimeMax")
    color: str = Field(default="", alias="Color")
    order_pos: int = Field(default=0, alias="OrderPos")
    split_type: int = Field(default=0, alias="SplitType")
    sector_from: int = Field(default=0, alias="SectorFrom")
    sector_to: int = Field(default=0, alias="SectorTo")
    speed_or_pace: str = Field(default="", alias="SpeedOrPace")
    time_mode: int = Field(default=0, alias="TimeMode")
    label: str = Field(default="", alias="Label")
    sector_from2: int = Field(default=0, alias="SectorFrom2")
    sector_to2: int = Field(default=0, alias="SectorTo2")

    model_config = {"populate_by_name": True}


# Split type constants
SPLIT_TYPE_SPLIT = 0
SPLIT_TYPE_INTERNAL = 2
SPLIT_TYPE_LEG = 9

# Split time mode constants
SPLIT_TIME_MODE_REF_SPLIT = 1
SPLIT_TIME_MODE_RACE_TIME = 0
SPLIT_TIME_MODE_TOD = -1
SPLIT_TIME_MODE_DELTA = -2
SPLIT_TIME_MODE_MIN_KM = -3
SPLIT_TIME_MODE_MIN_MILE = -4
SPLIT_TIME_MODE_MIN_100M = -5
SPLIT_TIME_MODE_KMH = -6
SPLIT_TIME_MODE_MPH = -7
SPLIT_TIME_MODE_MPS = -8


class UserDefinedField(BaseModel):
    """User-defined field definition.

    Based on go-model/model.go:516-521.
    """

    name: str = Field(default="", alias="Name")
    expression: str = Field(default="", alias="Expression")
    note: str = Field(default="", alias="Note")
    group: str = Field(default="", alias="Group")

    model_config = {"populate_by_name": True}
