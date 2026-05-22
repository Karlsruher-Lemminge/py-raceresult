"""Event-related models for Raceresult API.

Based on go-model/model.go.
"""

from __future__ import annotations

from decimal import Decimal
from enum import IntEnum
from typing import Any

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


class TeamScore(BaseModel):
    """Team score definition.

    Based on go-model/model.go:TeamScore.
    """

    id: int = Field(default=0, alias="ID")
    result_id1: int = Field(default=0, alias="ResultID1")
    result_id2: int = Field(default=0, alias="ResultID2")
    result_id3: int = Field(default=0, alias="ResultID3")
    result_id4: int = Field(default=0, alias="ResultID4")
    result_mode1: int = Field(default=0, alias="ResultMode1")
    result_mode2: int = Field(default=0, alias="ResultMode2")
    result_mode3: int = Field(default=0, alias="ResultMode3")
    result_mode4: int = Field(default=0, alias="ResultMode4")
    sort_desc1: bool = Field(default=False, alias="SortDesc1")
    sort_desc2: bool = Field(default=False, alias="SortDesc2")
    sort_desc3: bool = Field(default=False, alias="SortDesc3")
    real_time: bool = Field(default=False, alias="RealTime")
    min_total: int = Field(default=0, alias="MinTotal")
    max_total: int = Field(default=0, alias="MaxTotal")
    min_female: int = Field(default=0, alias="MinFemale")
    max_female: int = Field(default=0, alias="MaxFemale")
    max_teams: int = Field(default=0, alias="MaxTeams")
    filter: str = Field(default="", alias="Filter")
    time_format: str = Field(default="", alias="TimeFormat")
    lap_times: int = Field(default=0, alias="LapTimes")
    lap_times_lemans: bool = Field(default=False, alias="LapTimesLemans")
    lap_times_zero_start: bool = Field(default=False, alias="LapTimesZeroStart")
    name: str = Field(default="", alias="Name")
    lap_mode_location: str = Field(default="", alias="LapModeLocation")
    team_sort: str = Field(default="", alias="TeamSort")
    assigning1: str = Field(default="", alias="Assigning1")
    grouping1: str = Field(default="", alias="Grouping1")
    assigning2: str = Field(default="", alias="Assigning2")
    grouping2: str = Field(default="", alias="Grouping2")
    assigning3: str = Field(default="", alias="Assigning3")
    grouping3: str = Field(default="", alias="Grouping3")
    assigning4: str = Field(default="", alias="Assigning4")
    grouping4: str = Field(default="", alias="Grouping4")
    use_ties: bool = Field(default=False, alias="UseTies")
    lap_times_subtract_t0: bool = Field(default=False, alias="LapTimesSubtractT0")
    lap_times_count_lemans_as_lap: bool = Field(default=False, alias="LapTimesCountLemansAsLap")
    lap_times_penalty_time_result: int = Field(default=0, alias="LapTimesPenaltyTimeResult")
    lap_times_penalty_laps_result: int = Field(default=0, alias="LapTimesPenaltyLapsResult")
    lap_times_min_lap_time: RRDecimal = Field(default=Decimal(0), alias="LapTimesMinLapTime")
    lap_times_ignore_before: RRDecimal = Field(default=Decimal(0), alias="LapTimesIgnoreBefore")
    lap_times_ignore_after: RRDecimal = Field(default=Decimal(0), alias="LapTimesIgnoreAfter")

    model_config = {"populate_by_name": True}


class RawDataRule(BaseModel):
    """Raw data processing rule.

    Based on go-model/model.go:RawDataRule.
    """

    id: int = Field(default=0, alias="ID")
    result_id: int = Field(default=0, alias="ResultID")
    contest_id: int = Field(default=0, alias="ContestID")
    mode: int = Field(default=0, alias="Mode")
    n: int = Field(default=0, alias="N")
    min: int = Field(default=0, alias="Min")
    min_offset: RRDecimal = Field(default=Decimal(0), alias="MinOffset")
    max: int = Field(default=0, alias="Max")
    max_offset: RRDecimal = Field(default=Decimal(0), alias="MaxOffset")
    ref: int = Field(default=0, alias="Ref")
    ref_offset: RRDecimal = Field(default=Decimal(0), alias="RefOffset")

    model_config = {"populate_by_name": True}


class SimpleAPIItem(BaseModel):
    """SimpleAPI entry.

    Based on go-model/model.go:SimpleAPIItem.
    """

    disabled: bool = Field(default=False, alias="Disabled")
    key: str = Field(default="", alias="Key")
    url: str = Field(default="", alias="URL")
    label: str = Field(default="", alias="Label")

    model_config = {"populate_by_name": True}


class WebHookType(IntEnum):
    """Trigger type for a webhook.

    Based on go-model/model.go:WebHookType.
    """

    PARTICIPANT_NEW = 0
    PARTICIPANT_UPDATED = 1
    RAW_DATA_NEW = 2
    MOD_JOB_ID = 3
    MOD_JOB_ID_SETTINGS = 4


class WebHook(BaseModel):
    """Webhook definition.

    Based on go-model/model.go:WebHook.
    """

    id: int = Field(default=0, alias="ID")
    disabled: bool = Field(default=False, alias="Disabled")
    name: str = Field(default="", alias="Name")
    type: WebHookType = Field(default=WebHookType.PARTICIPANT_NEW, alias="Type")
    url: str = Field(default="", alias="URL")
    fields: list[str] = Field(default_factory=list, alias="Fields")
    filter: str = Field(default="", alias="Filter")
    order_pos: int = Field(default=0, alias="OrderPos")

    model_config = {"populate_by_name": True}


class ForwardingInfo(BaseModel):
    """Statistics about the backup/forwarding connection.

    Based on go-model/model.go:ForwardingInfo.
    """

    bytes_sent: int = Field(default=0, alias="BytesSent")
    bytes_received: int = Field(default=0, alias="BytesReceived")

    model_config = {"populate_by_name": True}


class ChatMessage(BaseModel):
    """Chat message.

    Based on go-model/model.go:ChatMessage.
    Uses single-character JSON keys: i, u, d, m.
    """

    id: int = Field(default=0, alias="i")
    username: str = Field(default="", alias="u")
    date: str = Field(default="", alias="d")
    message: str = Field(default="", alias="m")

    model_config = {"populate_by_name": True}


class Version(BaseModel):
    """Software version.

    Based on go-model/model.go:Version.
    Uses lowercase JSON keys.
    """

    major: int = Field(default=0, alias="major")
    minor: int = Field(default=0, alias="minor")
    revision: int = Field(default=0, alias="revision")
    tag: str = Field(default="", alias="tag")
    hash: str = Field(default="", alias="hash")

    model_config = {"populate_by_name": True}


class GroupTime(BaseModel):
    """Single group start time entry.

    Based on go-model/model.go:GroupTime.
    ID and Item are interface{} in Go.
    """

    id: Any = Field(default=None, alias="ID")
    time: RRDecimal = Field(default=Decimal(0), alias="Time")
    item: Any = Field(default=None, alias="Item")
    count: int = Field(default=0, alias="Count")

    model_config = {"populate_by_name": True}


class GroupTimes(BaseModel):
    """Group/wave start times collection.

    Based on go-model/model.go:GroupTimes.
    """

    mode: str = Field(default="", alias="Mode")
    wave_field: str = Field(default="", alias="WaveField")
    items: list[GroupTime] = Field(default_factory=list, alias="Items")

    model_config = {"populate_by_name": True}


class UserDefinedField(BaseModel):
    """User-defined field definition.

    Based on go-model/model.go:516-521.
    """

    name: str = Field(default="", alias="Name")
    expression: str = Field(default="", alias="Expression")
    note: str = Field(default="", alias="Note")
    group: str = Field(default="", alias="Group")

    model_config = {"populate_by_name": True}
