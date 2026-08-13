"""Statistics models for Raceresult API."""

from __future__ import annotations

from decimal import Decimal
from enum import IntEnum

from pydantic import BaseModel, Field

from raceresult.models.types import RRDecimal


class Aggregation(IntEnum):
    """Aggregation mode for statistics."""

    COUNT = 1
    MINIMUM = 2
    MAXIMUM = 3
    MEAN = 4
    SUM = 5


class Statistics(BaseModel):
    """Statistics definition.

    page_format and page_size are plain ints (page.Format / page.Size from go-model).
    """

    name: str = Field(default="", alias="StatisticName")
    type: str = Field(default="", alias="Type")
    row: str = Field(default="", alias="Row")
    col: str = Field(default="", alias="Col")
    filter: str = Field(default="", alias="Filter")
    only_finishers: bool = Field(default=False, alias="OnlyFinishers")
    field: str = Field(default="", alias="Field")
    aggregation: Aggregation = Field(default=Aggregation.COUNT, alias="Aggregation")
    sort_by_value: bool = Field(default=False, alias="SortByValue")
    sort_desc: bool = Field(default=False, alias="SortDesc")
    headline1: str = Field(default="", alias="Headline1")
    headline2: str = Field(default="", alias="Headline2")
    line_spacing: RRDecimal = Field(default=Decimal(0), alias="LineSpacing")
    font_name: str = Field(default="", alias="FontName")
    font_size: int = Field(default=0, alias="FontSize")
    page_format: int = Field(default=0, alias="PageFormat")
    page_margin_bottom: RRDecimal = Field(default=Decimal(0), alias="PageMarginBottom")
    page_margin_left: RRDecimal = Field(default=Decimal(0), alias="PageMarginLeft")
    page_margin_right: RRDecimal = Field(default=Decimal(0), alias="PageMarginRight")
    page_margin_top: RRDecimal = Field(default=Decimal(0), alias="PageMarginTop")
    page_size: int = Field(default=0, alias="PageSize")
    page_height: RRDecimal = Field(default=Decimal(0), alias="PageHeight")
    page_width: RRDecimal = Field(default=Decimal(0), alias="PageWidth")
    top_left_header: str = Field(default="", alias="TopLeftHeader")

    model_config = {"populate_by_name": True}
