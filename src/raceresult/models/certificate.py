"""Certificate models for Raceresult API."""

from __future__ import annotations

from decimal import Decimal
from enum import IntEnum

from pydantic import BaseModel, Field

from raceresult.models.types import RRDecimal


class ElementType(IntEnum):
    """Type of a certificate element."""

    FIELD = 0
    TEXT = 1
    PICTURE = 2
    PICTURE_NAME = 3
    BARCODE = 4
    PICTURE_EXPRESSION = 5
    RECT = 6
    LINE = 7
    CIRCLE = 8
    CHUNK_BOX = 9
    CHIP_BARCODE = 11
    BIB_POSITION = 12


class ElementBarcodeType(IntEnum):
    """Barcode format for a certificate element."""

    NO_BARCODE = 0
    CODE39 = 1
    EAN13 = 2
    CODE128 = 3


class ElementPictureStretchMode(IntEnum):
    """Picture stretch mode for a certificate element."""

    STRETCH = 0
    NO_STRETCH = 1


class CertificateElement(BaseModel):
    """One design element inside a certificate.

    JSON field names as serialized by Go (no json tags → PascalCase),
    except DF (DynamicFormat), vAlignment, Stretch, Barcode.
    """

    type: ElementType = Field(default=ElementType.FIELD, alias="Type")
    data: str = Field(default="", alias="Data")
    left: RRDecimal = Field(default=Decimal(0), alias="Left")
    top: RRDecimal = Field(default=Decimal(0), alias="Top")
    width: RRDecimal = Field(default=Decimal(0), alias="Width")
    height: RRDecimal = Field(default=Decimal(0), alias="Height")
    font_name: str = Field(default="", alias="FontName")
    font_size: int = Field(default=0, alias="FontSize")
    font_bold: bool = Field(default=False, alias="FontBold")
    font_italic: bool = Field(default=False, alias="FontItalic")
    font_underlined: bool = Field(default=False, alias="FontUnderlined")
    font_color: int = Field(default=0, alias="FontColor")
    font_color_cmyk: str = Field(default="", alias="FontColorCMYK")
    alignment: int = Field(default=0, alias="Alignment")
    v_alignment: int = Field(default=0, alias="vAlignment")
    page: int = Field(default=1, alias="Page")
    rotation: int = Field(default=0, alias="Rotation")
    dynamic_format: str = Field(default="", alias="DF")
    picture_stretch: ElementPictureStretchMode = Field(
        default=ElementPictureStretchMode.STRETCH, alias="Stretch"
    )
    barcode_type: ElementBarcodeType = Field(
        default=ElementBarcodeType.NO_BARCODE, alias="Barcode"
    )
    locked: bool = Field(default=False, alias="Locked")
    text_scaling: RRDecimal = Field(default=Decimal(0), alias="TextScaling")
    text_char_spacing: RRDecimal = Field(default=Decimal(0), alias="TextCharSpacing")
    outline_width: RRDecimal = Field(default=Decimal(0), alias="OutlineWidth")
    outline_color: str = Field(default="", alias="OutlineColor")
    transparency: RRDecimal = Field(default=Decimal(0), alias="Transparency")

    model_config = {"populate_by_name": True}


class CertificateZone(BaseModel):
    """Zone divider inside a certificate."""

    top: RRDecimal = Field(default=Decimal(0), alias="Top")
    page: int = Field(default=0, alias="Page")
    type: str = Field(default="", alias="Type")

    model_config = {"populate_by_name": True}


class Certificate(BaseModel):
    """Certificate/bib-number design.

    PageSize and PageFormat are serialized as strings by Go
    (e.g. "A4", "Portrait") via custom MarshalJSON.
    """

    name: str = Field(default="", alias="CertificateName")
    page_size: str = Field(default="A4", alias="PageSize")
    page_format: str = Field(default="Portrait", alias="PageFormat")
    page_height: int = Field(default=0, alias="PageHeight")
    page_width: int = Field(default=0, alias="PageWidth")
    sheet_height: int = Field(default=0, alias="SheetHeight")
    sheet_width: int = Field(default=0, alias="SheetWidth")
    margin_top: int = Field(default=0, alias="MarginTop")
    margin_left: int = Field(default=0, alias="MarginLeft")
    margin_right: int = Field(default=0, alias="MarginRight")
    margin_bottom: int = Field(default=0, alias="MarginBottom")
    cut_left: int = Field(default=0, alias="CutLeft")
    cut_top: int = Field(default=0, alias="CutTop")
    cut_bottom: int = Field(default=0, alias="CutBottom")
    cut_right: int = Field(default=0, alias="CutRight")
    distance_vertical: int = Field(default=0, alias="DistanceVertical")
    distance_horizontal: int = Field(default=0, alias="DistanceHorizontal")
    holes: int = Field(default=0, alias="Holes")
    special_holes: str = Field(default="", alias="SpecialHoles")
    substrate: str = Field(default="", alias="Substrate")
    rgb_black_to_cmyk: bool = Field(default=False, alias="RGBBlackToCMYK")
    cmyk_black_value: str = Field(default="", alias="CMYKBlackValue")
    print_notes: str = Field(default="", alias="PrintNotes")
    copies: int = Field(default=1, alias="Copies")
    print_mode: str = Field(default="", alias="PrintMode")
    reverse: bool = Field(default=False, alias="Reverse")
    rounded_corners: bool = Field(default=False, alias="RoundedCorners")
    plotter_marks: bool = Field(default=False, alias="PlotterMarks")
    chip_type: int = Field(default=0, alias="ChipType")
    machine: int = Field(default=0, alias="Machine")
    block_size: int = Field(default=0, alias="BlockSize")
    version: int = Field(default=0, alias="Version")
    elements: list[CertificateElement] = Field(default_factory=list, alias="Fields")
    zones: list[CertificateZone] = Field(default_factory=list, alias="Zones")

    model_config = {"populate_by_name": True}
