"""Certificates endpoint for Raceresult API.

Based on go-webapi/eventapi_certificates.go and go-model/certificate/.
"""

from __future__ import annotations

from decimal import Decimal
from enum import Enum, IntEnum
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from raceresult.models.types import RRDecimal

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class PageSize(str, Enum):
    """Certificate page size.

    Based on go-model/certificate/pagesize.go.
    Serialized as string in JSON ("A4", "Portrait", etc.).
    """

    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"
    A6 = "A6"
    LETTER = "Letter"
    LEGAL = "Legal"
    USER_DEFINED = "UserDefined"


class PageFormat(str, Enum):
    """Certificate page orientation.

    Based on go-model/certificate/pageformat.go.
    Serialized as string in JSON.
    """

    PORTRAIT = "Portrait"
    LANDSCAPE = "Landscape"


class ElementType(IntEnum):
    """Certificate element type.

    Based on go-model/certificate/element.go.
    """

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
    """Barcode type for certificate elements.

    Based on go-model/certificate/element.go.
    """

    NO_BARCODE = 0
    CODE39 = 1
    EAN13 = 2
    CODE128 = 3


class ElementPictureStretchMode(IntEnum):
    """Picture stretch mode for certificate elements.

    Based on go-model/certificate/element.go.
    """

    STRETCH = 0
    NO_STRETCH = 1


class Element(BaseModel):
    """One element within a certificate.

    Based on go-model/certificate/element.go.
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


class Zone(BaseModel):
    """A zone within a certificate.

    Based on go-model/certificate/zones.go.
    """

    top: RRDecimal = Field(default=Decimal(0), alias="Top")
    page: int = Field(default=1, alias="Page")
    type: str = Field(default="", alias="Type")

    model_config = {"populate_by_name": True}


class Certificate(BaseModel):
    """Certificate (Urkunde) definition.

    Based on go-model/certificate/certificate.go.
    Note: name maps to "CertificateName" in JSON; elements map to "Fields".
    """

    name: str = Field(default="", alias="CertificateName")
    page_size: PageSize = Field(default=PageSize.A4, alias="PageSize")
    page_format: PageFormat = Field(default=PageFormat.PORTRAIT, alias="PageFormat")
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
    machine: int = Field(default=0, alias="Machine")
    block_size: int = Field(default=0, alias="BlockSize")
    version: int = Field(default=0, alias="Version")
    elements: list[Element] = Field(default_factory=list, alias="Fields")
    zones: list[Zone] = Field(default_factory=list, alias="Zones")

    model_config = {"populate_by_name": True}


class CertificatesEndpoint:
    """Certificates (Urkunden) API endpoint.

    Based on go-webapi/eventapi_certificates.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            names = await event.certificates.names()
            pdf = await event.certificates.create_pdf(names[0], page=1, bib=100, lang="de")
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def names(self) -> list[str]:
        """Return names of all certificates.

        Based on go-webapi/eventapi_certificates.go:22-28.
        """
        result = await self._client.get_json(self._event_id, "certificates/names")
        if not result:
            return []
        return list(result)

    async def get(self, name: str) -> Certificate:
        """Return a certificate by name.

        Based on go-webapi/eventapi_certificates.go:31-44.
        """
        result = await self._client.get_json(
            self._event_id, "certificates/get", {"name": name}
        )
        return Certificate.model_validate(result if result else {})

    async def save(self, item: Certificate) -> None:
        """Save a certificate.

        Based on go-webapi/eventapi_certificates.go:47-50.
        """
        await self._client.post_json(
            self._event_id,
            "certificates/save",
            data=item.model_dump(mode="json", by_alias=True),
        )

    async def delete(self, name: str) -> None:
        """Delete a certificate.

        Based on go-webapi/eventapi_certificates.go:53-59.
        """
        await self._client.get(self._event_id, "certificates/delete", {"name": name})

    async def copy(self, name: str, new_name: str) -> None:
        """Copy a certificate.

        Based on go-webapi/eventapi_certificates.go:62-69.
        """
        await self._client.get(
            self._event_id, "certificates/copy", {"name": name, "newName": new_name}
        )

    async def rename(self, name: str, new_name: str) -> None:
        """Rename a certificate.

        Based on go-webapi/eventapi_certificates.go:72-79.
        """
        await self._client.get(
            self._event_id, "certificates/rename", {"name": name, "newName": new_name}
        )

    async def new(self, name: str) -> None:
        """Create a new empty certificate.

        Based on go-webapi/eventapi_certificates.go:82-88.
        """
        await self._client.get(self._event_id, "certificates/new", {"name": name})

    async def thumbnail(self, name: str, max_width: int, max_height: int) -> bytes:
        """Return a thumbnail of a certificate as JPEG bytes.

        Based on go-webapi/eventapi_certificates.go:91-98.
        """
        return await self._client.get(
            self._event_id,
            "certificates/thumbnail",
            {"name": name, "maxWidth": max_width, "maxHeight": max_height},
        )

    async def preview_jpg(
        self, name: str, page: int, dpi: int, lang: str
    ) -> bytes:
        """Return a preview of a certificate page as JPEG bytes.

        Based on go-webapi/eventapi_certificates.go:101-109.
        """
        return await self._client.get(
            self._event_id,
            "certificates/previewJPG",
            {"name": name, "page": page, "dpi": dpi, "lang": lang},
        )

    async def create_pdf(
        self, name: str, page: int, bib: int, lang: str
    ) -> bytes:
        """Generate a certificate PDF for one participant.

        Based on go-webapi/eventapi_certificates.go:112-121.
        """
        return await self._client.get(
            self._event_id,
            "certificates/create",
            {"name": name, "page": page, "bib": bib, "lang": lang, "format": "pdf"},
        )

    async def create_jpg(
        self, name: str, page: int, bib: int, dpi: int, lang: str
    ) -> bytes:
        """Generate a certificate JPG for one participant.

        Based on go-webapi/eventapi_certificates.go:124-134.
        """
        return await self._client.get(
            self._event_id,
            "certificates/create",
            {
                "name": name,
                "page": page,
                "bib": bib,
                "dpi": dpi,
                "lang": lang,
                "format": "jpg",
            },
        )
