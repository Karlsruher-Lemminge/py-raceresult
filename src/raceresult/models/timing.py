"""Timing models for Raceresult API.

Based on go-model/model.go.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field

from raceresult.models.types import RRDecimal


class TimingPoint(BaseModel):
    """Timing point definition.

    Based on go-model/model.go:501-514.
    """

    name: str = Field(default="", alias="Name")
    type: int = Field(default=0, alias="Type")
    ddt: int = Field(default=0, alias="DDT")
    ignore_if_time_in: int = Field(default=0, alias="IgnoreIfTimeIn")
    ignore_before: RRDecimal = Field(default=Decimal(0), alias="IgnoreBefore")
    ignore_after: RRDecimal = Field(default=Decimal(0), alias="IgnoreAfter")
    subtract_t0: int = Field(default=0, alias="SubtractT0")
    ignore_ps: int = Field(default=0, alias="IgnorePS")
    position: str = Field(default="", alias="Position")
    order_pos: int = Field(default=0, alias="OrderPos")
    color: str = Field(default="", alias="Color")

    model_config = {"populate_by_name": True}


class TimingPointRule(BaseModel):
    """Timing point rule for raw data processing.

    Based on go-model/model.go:487-499.
    """

    id: int = Field(default=0, alias="ID")
    decoder_id: str = Field(default="", alias="DecoderID")
    decoder_name: str = Field(default="", alias="DecoderName")
    loop_id: int = Field(default=0, alias="LoopID")
    channel_id: int = Field(default=0, alias="ChannelID")
    order_id: int = Field(default=0, alias="OrderID")
    min_time: RRDecimal = Field(default=Decimal(0), alias="MinTime")
    max_time: RRDecimal = Field(default=Decimal(0), alias="MaxTime")
    order_pos: int = Field(default=0, alias="OrderPos")
    timing_point: str = Field(default="", alias="TimingPoint")

    model_config = {"populate_by_name": True}


class ChipFileEntry(BaseModel):
    """Chip file entry mapping transponder to identification.

    Based on go-model/model.go:621-624.
    """

    transponder: str = Field(default="", alias="Transponder")
    identification: str = Field(default="", alias="Identification")

    model_config = {"populate_by_name": True}


class RawData(BaseModel):
    """Raw timing data entry.

    Based on go-model/model.go:278-287.
    """

    id: int = Field(default=0, alias="ID")
    pid: int = Field(default=0, alias="PID")
    timing_point: str = Field(default="", alias="TimingPoint")
    result: int = Field(default=0, alias="Result")
    time: RRDecimal = Field(default=Decimal(0), alias="Time")
    invalid: bool = Field(default=False, alias="Invalid")

    model_config = {"populate_by_name": True}


class RawDataReduced(BaseModel):
    """Reduced raw timing data.

    Based on go-model/model.go:289-299.
    """

    timing_point: str = Field(default="", alias="TimingPoint")
    pid: int = Field(default=0, alias="PID")
    time: RRDecimal = Field(default=Decimal(0), alias="Time")
    invalid: bool = Field(default=False, alias="Invalid")
    order_id: int = Field(default=0, alias="OrderID")
    result: int = Field(default=0, alias="Result")
    is_marker: bool = Field(default=False, alias="IsMarker")
    rssi: int = Field(default=0, alias="RSSI")

    model_config = {"populate_by_name": True}


class Time(BaseModel):
    """Time entry for a participant.

    Based on go-model/model.go:478-485.
    """

    pid: int = Field(default=0, alias="PID")
    result: int = Field(default=0, alias="Result")
    decimal_time: RRDecimal = Field(default=Decimal(0), alias="DecimalTime")
    time_text: str = Field(default="", alias="TimeText")
    info_text: str = Field(default="", alias="InfoText")

    model_config = {"populate_by_name": True}


class Passing(BaseModel):
    """Passing data from timing hardware.

    Based on go-model/model.go:559-581.
    """

    transponder: str = Field(default="", alias="Transponder")
    hits: int = Field(default=0, alias="Hits")
    rssi: int = Field(default=0, alias="RSSI")
    battery: RRDecimal = Field(default=Decimal(0), alias="Battery")
    temperature: int = Field(default=0, alias="Temperature")
    wakeup_counter: int = Field(default=0, alias="WUC")
    loop_id: int = Field(default=0, alias="LoopID")
    channel: int = Field(default=0, alias="Channel")
    internal_data: str = Field(default="", alias="InternalData")
    status_flags: int = Field(default=0, alias="StatusFlags")
    device_id: str = Field(default="", alias="DeviceID")
    device_name: str = Field(default="", alias="DeviceName")
    order_id: int = Field(default=0, alias="OrderID")
    port: int = Field(default=0, alias="Port")
    is_marker: bool = Field(default=False, alias="IsMarker")
    file_no: int = Field(default=0, alias="FileNo")
    passing_no: int = Field(default=0, alias="PassingNo")
    customer: int = Field(default=0, alias="Customer")

    model_config = {"populate_by_name": True}


class PassingToProcess(BaseModel):
    """Passing to be processed.

    Based on go-model/model.go:549-556.
    """

    bib: int = Field(default=0, alias="Bib")
    timing_point: str = Field(default="", alias="TimingPoint")
    result_id: int = Field(default=0, alias="ResultID")
    time: RRDecimal = Field(default=Decimal(0), alias="Time")
    info_text: str = Field(default="", alias="InfoText")
    passing: Passing | None = Field(default=None, alias="Passing")

    model_config = {"populate_by_name": True}
