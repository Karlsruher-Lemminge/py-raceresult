"""Label model for Raceresult API."""

from __future__ import annotations

from decimal import Decimal
from enum import IntEnum

from pydantic import BaseModel, Field

from raceresult.models.types import RRDecimal


class LabelDirection(IntEnum):
    """Label printing direction."""

    DOWN_THEN_RIGHT = 0
    RIGHT_THEN_DOWN = 1


class LabelBarcodeType(IntEnum):
    """Barcode type for labels."""

    NO_BARCODE = 0
    CODE39 = 1
    EAN13 = 2
    CODE128 = 3


class LabelAlignment(IntEnum):
    """Text alignment for labels."""

    LEFT = 1
    CENTER = 2
    RIGHT = 3


class Label(BaseModel):
    """Label/sticker design.

    page_format and page_size are plain ints (page.Format / page.Size from go-model).
    """

    name: str = Field(default="", alias="LabelName")
    page_format: int = Field(default=0, alias="PageFormat")
    page_size: int = Field(default=0, alias="PageSize")
    page_height: RRDecimal = Field(default=Decimal(0), alias="PageHeight")
    page_width: RRDecimal = Field(default=Decimal(0), alias="PageWidth")
    page_margin_top: RRDecimal = Field(default=Decimal(0), alias="PageMarginTop")
    page_margin_left: RRDecimal = Field(default=Decimal(0), alias="PageMarginLeft")
    page_margin_bottom: RRDecimal = Field(default=Decimal(0), alias="PageMarginBottom")
    page_margin_right: RRDecimal = Field(default=Decimal(0), alias="PageMarginRight")
    width: RRDecimal = Field(default=Decimal(0), alias="Width")
    height: RRDecimal = Field(default=Decimal(0), alias="Height")
    spacing_vertical: RRDecimal = Field(default=Decimal(0), alias="SpacingVertical")
    spacing_horizontal: RRDecimal = Field(default=Decimal(0), alias="SpacingHorizontal")
    direction: LabelDirection = Field(default=LabelDirection.DOWN_THEN_RIGHT, alias="Direction")
    expression: str = Field(default="", alias="Expression")
    font_name: str = Field(default="", alias="FontName")
    font_size: int = Field(default=0, alias="FontSize")
    font_bold: bool = Field(default=False, alias="FontBold")
    font_italic: bool = Field(default=False, alias="FontItalic")
    font_underline: bool = Field(default=False, alias="FontUnderline")
    design: str = Field(default="", alias="Design")
    barcode_type: LabelBarcodeType = Field(default=LabelBarcodeType.NO_BARCODE, alias="BarcodeType")
    alignment: LabelAlignment = Field(default=LabelAlignment.LEFT, alias="Alignment")
    filter: str = Field(default="", alias="Filter")
    sort1: str = Field(default="", alias="Sort1")
    sort2: str = Field(default="", alias="Sort2")
    sort3: str = Field(default="", alias="Sort3")
    sort_desc1: bool = Field(default=False, alias="SortDesc1")
    sort_desc2: bool = Field(default=False, alias="SortDesc2")
    sort_desc3: bool = Field(default=False, alias="SortDesc3")

    model_config = {"populate_by_name": True}
