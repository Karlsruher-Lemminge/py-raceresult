"""Lists endpoint for Raceresult API.

Based on go-webapi/eventapi_lists.go.
"""

from __future__ import annotations

from decimal import Decimal
from enum import IntEnum
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from raceresult.models.types import RRDecimal, RRDateTime

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class ShowAt(IntEnum):
    """Show at position constants.

    Based on go-model/list/list.go:144-151.
    """

    NEVER = 0
    FIRST_PAGE = 1
    EVERY_PAGE = 2
    LAST_PAGE = 3


class PageBreak(IntEnum):
    """Page break constants.

    Based on go-model/list/list.go:153-160.
    """

    NO_PAGE_BREAK = 0
    NEW_PAGE = 1
    KEEP_TOGETHER = 2
    NEW_COLUMN = 3
    REPEAT = 4


class ListOrder(BaseModel):
    """Order/Grouping of a list.

    Based on go-model/list/list.go:91-107.
    """

    expression: str = Field(default="", alias="Exp")
    descending: bool = Field(default=False, alias="D")
    grouping: int = Field(default=0, alias="Grouping")
    group_filter_default: int = Field(default=0, alias="GroupFilterDefault")
    group_filter_label: str = Field(default="", alias="GroupFilterLabel")
    page_break: PageBreak = Field(default=PageBreak.NO_PAGE_BREAK, alias="P")
    font_name: str = Field(default="", alias="F")
    font_size: int = Field(default=0, alias="S")
    font_bold: bool = Field(default=False, alias="B")
    font_italic: bool = Field(default=False, alias="I")
    font_underlined: bool = Field(default=False, alias="U")
    color: str = Field(default="", alias="C")
    background_color: str = Field(default="", alias="BC")
    spacing: int = Field(default=0, alias="SP")

    model_config = {"populate_by_name": True}


class ListFilter(BaseModel):
    """Filter of a list.

    Based on go-model/list/list.go:110-115.
    """

    or_conjunction: bool = Field(default=False, alias="Or")
    expression1: str = Field(default="", alias="Exp1")
    operator: str = Field(default="", alias="Op")
    expression2: str = Field(default="", alias="Exp2")

    model_config = {"populate_by_name": True}


class ListField(BaseModel):
    """Field of a list.

    Based on go-model/list/list.go:118-135.
    """

    expression: str = Field(default="", alias="Exp")
    label: str = Field(default="", alias="La")
    label2: str = Field(default="", alias="La2")
    alignment: int = Field(default=0, alias="A")
    font_bold: bool = Field(default=False, alias="B")
    font_italic: bool = Field(default=False, alias="I")
    font_underlined: bool = Field(default=False, alias="U")
    line: int = Field(default=0, alias="Li")
    color: str = Field(default="", alias="C")
    link: str = Field(default="", alias="Link")
    col_span: int = Field(default=0, alias="ColSpan")
    col_offset: int = Field(default=0, alias="CO")
    position: RRDecimal = Field(default=Decimal(0), alias="P")
    dynamic_format: str = Field(default="", alias="DF")
    preview_only: bool = Field(default=False, alias="PO")
    responsive_hide: int = Field(default=0, alias="RH")

    model_config = {"populate_by_name": True}


class SelectorResult(BaseModel):
    """Selector result of a list.

    Based on go-model/list/list.go:138-142.
    """

    result_id: int = Field(default=0, alias="ResultID")
    result_id2: int = Field(default=0, alias="ResultID2")
    show_as: str = Field(default="", alias="ShowAs")

    model_config = {"populate_by_name": True}


class List(BaseModel):
    """List definition.

    Based on go-model/list/list.go:10-88.
    """

    name: str = Field(default="", alias="ListName")
    bottom_picture: str = Field(default="", alias="BottomPicture")
    bottom_picture_show: ShowAt = Field(default=ShowAt.NEVER, alias="BottomPictureShow")
    column_heads_font_name: str = Field(default="", alias="ColumnHeadsFontName")
    column_heads_font_size: int = Field(default=0, alias="ColumnHeadsFontSize")
    column_heads_font_bold: bool = Field(default=False, alias="ColumnHeadsFontBold")
    column_heads_font_italic: bool = Field(default=False, alias="ColumnHeadsFontItalic")
    column_heads_font_underlined: bool = Field(default=False, alias="ColumnHeadsFontUnderlined")
    column_heads_color: str = Field(default="", alias="ColumnHeadsColor")
    column_heads_show: ShowAt = Field(default=ShowAt.NEVER, alias="ColumnHeadsShow")
    columns: int = Field(default=0, alias="Columns")
    column_spacing: RRDecimal = Field(default=Decimal(0), alias="ColumnSpacing")
    cover_sheet: str = Field(default="", alias="CoverSheet")
    back_sheet: str = Field(default="", alias="BackSheet")
    design: str = Field(default="", alias="Design")
    design_show: ShowAt = Field(default=ShowAt.NEVER, alias="DesignShow")
    every_other_line_gray: bool = Field(default=False, alias="EveryOtherLineGray")
    font_name: str = Field(default="", alias="FontName")
    font_size: int = Field(default=0, alias="FontSize")
    footer_font_name: str = Field(default="", alias="FooterFontName")
    footer_font_size: int = Field(default=0, alias="FooterFontSize")
    footer_font_bold: bool = Field(default=False, alias="FooterFontBold")
    footer_font_italic: bool = Field(default=False, alias="FooterFontItalic")
    footer_font_underlined: bool = Field(default=False, alias="FooterFontUnderlined")
    footer_color: str = Field(default="", alias="FooterColor")
    gray_line: bool = Field(default=False, alias="GrayLine")
    head_line1: str = Field(default="", alias="HeadLine1")
    head_line1_font_name: str = Field(default="", alias="HeadLine1FontName")
    head_line1_font_size: int = Field(default=0, alias="HeadLine1FontSize")
    head_line1_font_bold: bool = Field(default=False, alias="HeadLine1FontBold")
    head_line1_font_italic: bool = Field(default=False, alias="HeadLine1FontItalic")
    head_line1_font_underlined: bool = Field(default=False, alias="HeadLine1FontUnderlined")
    head_line2: str = Field(default="", alias="HeadLine2")
    head_line1_color: str = Field(default="", alias="HeadLine1Color")
    head_line1_show: ShowAt = Field(default=ShowAt.NEVER, alias="HeadLine1Show")
    head_line2_font_name: str = Field(default="", alias="HeadLine2FontName")
    head_line2_font_size: int = Field(default=0, alias="HeadLine2FontSize")
    head_line2_font_bold: bool = Field(default=False, alias="HeadLine2FontBold")
    head_line2_font_italic: bool = Field(default=False, alias="HeadLine2FontItalic")
    head_line2_font_underlined: bool = Field(default=False, alias="HeadLine2FontUnderlined")
    head_line2_color: str = Field(default="", alias="HeadLine2Color")
    head_line2_show: ShowAt = Field(default=ShowAt.NEVER, alias="HeadLine2Show")
    height_bottom_picture: RRDecimal = Field(default=Decimal(0), alias="HeightBottomPicture")
    line_color: str = Field(default="", alias="LineColor")
    line_back_color: str = Field(default="", alias="LineBackColor")
    line_dynamic_format: str = Field(default="", alias="LineDynamicFormat")
    line_spacing: RRDecimal = Field(default=Decimal(0), alias="LineSpacing")
    max_records: int = Field(default=0, alias="MaxRecords")
    multiplier_field: str = Field(default="", alias="MultiplierField")
    page_format: int = Field(default=0, alias="PageFormat")
    page_margin_bottom: RRDecimal = Field(default=Decimal(0), alias="PageMarginBottom")
    page_margin_left: RRDecimal = Field(default=Decimal(0), alias="PageMarginLeft")
    page_margin_right: RRDecimal = Field(default=Decimal(0), alias="PageMarginRight")
    page_margin_top: RRDecimal = Field(default=Decimal(0), alias="PageMarginTop")
    page_size: int = Field(default=0, alias="PageSize")
    page_height: RRDecimal = Field(default=Decimal(0), alias="PageHeight")
    page_width: RRDecimal = Field(default=Decimal(0), alias="PageWidth")
    sep_line: bool = Field(default=False, alias="SepLine")
    top_right_picture: str = Field(default="", alias="TopRightPicture")
    top_right_picture_show: ShowAt = Field(default=ShowAt.NEVER, alias="TopRightPictureShow")
    list_header_text: str = Field(default="", alias="ListHeaderText")
    list_footer_text: str = Field(default="", alias="ListFooterText")
    list_header_footer_font_name: str = Field(default="", alias="ListHeaderFooterFontName")
    list_header_footer_font_size: int = Field(default=0, alias="ListHeaderFooterFontSize")
    list_header_footer_font_bold: bool = Field(default=False, alias="ListHeaderFooterFontBold")
    list_header_footer_font_italic: bool = Field(default=False, alias="ListHeaderFooterFontItalic")
    list_header_footer_font_underlined: bool = Field(default=False, alias="ListHeaderFooterFontUnderlined")
    list_header_footer_alignment: int = Field(default=0, alias="ListHeaderFooterAlignment")
    remarks: str = Field(default="", alias="Remarks")
    last_change: RRDateTime = Field(default=None, alias="LastChange")
    footer_text1: str = Field(default="", alias="FooterText1")
    footer_text2: str = Field(default="", alias="FooterText2")
    footer_text3: str = Field(default="", alias="FooterText3")
    orders: list[ListOrder] = Field(default_factory=list, alias="Orders")
    filters: list[ListFilter] = Field(default_factory=list, alias="Filters")
    fields: list[ListField] = Field(default_factory=list, alias="Fields")
    selector_results: list[SelectorResult] = Field(default_factory=list, alias="SelectorResults")

    model_config = {"populate_by_name": True}


class ListsEndpoint:
    """Lists API endpoint.

    Based on go-webapi/eventapi_lists.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            names = await event.lists.names()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def names(self) -> list[str]:
        """Get names of all lists.

        Based on go-webapi/eventapi_lists.go:22-28.

        Returns:
            List of list names
        """
        result = await self._client.get_json(self._event_id, "lists/names")
        return result if result else []

    async def delete(self, name: str) -> None:
        """Delete a list.

        Based on go-webapi/eventapi_lists.go:31-37.

        Args:
            name: List name
        """
        params = {"name": name}
        await self._client.get(self._event_id, "lists/delete", params)

    async def copy(self, name: str, new_name: str) -> None:
        """Create a copy of a list.

        Based on go-webapi/eventapi_lists.go:40-47.

        Args:
            name: Source list name
            new_name: Target list name
        """
        params = {
            "name": name,
            "newName": new_name,
        }
        await self._client.get(self._event_id, "lists/copy", params)

    async def rename(self, name: str, new_name: str) -> None:
        """Rename a list.

        Based on go-webapi/eventapi_lists.go:50-57.

        Args:
            name: Current list name
            new_name: New list name
        """
        params = {
            "name": name,
            "newName": new_name,
        }
        await self._client.get(self._event_id, "lists/rename", params)

    async def new(self, name: str) -> None:
        """Create a new list.

        Based on go-webapi/eventapi_lists.go:60-66.

        Args:
            name: List name
        """
        params = {"name": name}
        await self._client.get(self._event_id, "lists/new", params)

    async def get(
        self,
        name: str,
        no_translate: bool = False,
        lang: str = "",
    ) -> List:
        """Get the settings of a list.

        Based on go-webapi/eventapi_lists.go:69-84.

        Args:
            name: List name
            no_translate: Skip translation
            lang: Language code

        Returns:
            List object
        """
        params = {
            "name": name,
            "noTranslate": no_translate,
            "lang": lang,
        }
        result = await self._client.get_json(self._event_id, "lists/get", params)
        return List.model_validate(result if result else {})

    async def save(self, item: List) -> None:
        """Save a list.

        Based on go-webapi/eventapi_lists.go:87-90.

        Args:
            item: List to save
        """
        data = item.model_dump(by_alias=True)
        await self._client.post_json(self._event_id, "lists/save", data=data)

    def _int_list_to_string(self, values: list[int]) -> str:
        """Convert int list to comma-separated string."""
        return ",".join(str(v) for v in values)

    async def create_pdf(
        self,
        name: str,
        contests: list[int] | None = None,
        filter_expr: str = "",
        selector_result: str = "",
        lang: str = "",
    ) -> bytes:
        """Create a list in PDF format.

        Based on go-webapi/eventapi_lists.go:93-103.

        Args:
            name: List name
            contests: Contest IDs
            filter_expr: Filter expression
            selector_result: Selector result
            lang: Language code

        Returns:
            PDF file as bytes
        """
        params: dict[str, Any] = {
            "name": name,
            "format": "pdf",
            "filter": filter_expr,
            "selectorResult": selector_result,
            "lang": lang,
        }
        if contests:
            params["contest"] = self._int_list_to_string(contests)
        return await self._client.get(self._event_id, "lists/create", params)

    async def create_html(
        self,
        name: str,
        contests: list[int] | None = None,
        filter_expr: str = "",
        selector_result: str = "",
        lang: str = "",
    ) -> bytes:
        """Create a list in HTML format.

        Based on go-webapi/eventapi_lists.go:106-116.

        Args:
            name: List name
            contests: Contest IDs
            filter_expr: Filter expression
            selector_result: Selector result
            lang: Language code

        Returns:
            HTML file as bytes
        """
        params: dict[str, Any] = {
            "name": name,
            "format": "html",
            "filter": filter_expr,
            "selectorResult": selector_result,
            "lang": lang,
        }
        if contests:
            params["contest"] = self._int_list_to_string(contests)
        return await self._client.get(self._event_id, "lists/create", params)

    async def create_xml(
        self,
        name: str,
        charset: str = "",
        contests: list[int] | None = None,
        filter_expr: str = "",
        selector_result: str = "",
        lang: str = "",
    ) -> bytes:
        """Create a list in XML format.

        Based on go-webapi/eventapi_lists.go:119-130.

        Args:
            name: List name
            charset: Character set
            contests: Contest IDs
            filter_expr: Filter expression
            selector_result: Selector result
            lang: Language code

        Returns:
            XML file as bytes
        """
        params: dict[str, Any] = {
            "name": name,
            "format": "xml",
            "charset": charset,
            "filter": filter_expr,
            "selectorResult": selector_result,
            "lang": lang,
        }
        if contests:
            params["contest"] = self._int_list_to_string(contests)
        return await self._client.get(self._event_id, "lists/create", params)

    async def create_json(
        self,
        name: str,
        contests: list[int] | None = None,
        filter_expr: str = "",
        selector_result: str = "",
        lang: str = "",
    ) -> bytes:
        """Create a list in JSON format.

        Based on go-webapi/eventapi_lists.go:133-143.

        Args:
            name: List name
            contests: Contest IDs
            filter_expr: Filter expression
            selector_result: Selector result
            lang: Language code

        Returns:
            JSON file as bytes
        """
        params: dict[str, Any] = {
            "name": name,
            "format": "JSON",
            "filter": filter_expr,
            "selectorResult": selector_result,
            "lang": lang,
        }
        if contests:
            params["contest"] = self._int_list_to_string(contests)
        return await self._client.get(self._event_id, "lists/create", params)

    async def create_csv(
        self,
        name: str,
        charset: str = "",
        separator: str = "",
        contests: list[int] | None = None,
        filter_expr: str = "",
        selector_result: str = "",
        lang: str = "",
    ) -> bytes:
        """Create a list in CSV format.

        Based on go-webapi/eventapi_lists.go:159-171.

        Args:
            name: List name
            charset: Character set
            separator: Field separator
            contests: Contest IDs
            filter_expr: Filter expression
            selector_result: Selector result
            lang: Language code

        Returns:
            CSV file as bytes
        """
        params: dict[str, Any] = {
            "name": name,
            "format": "csv",
            "charset": charset,
            "separator": separator,
            "filter": filter_expr,
            "selectorResult": selector_result,
            "lang": lang,
        }
        if contests:
            params["contest"] = self._int_list_to_string(contests)
        return await self._client.get(self._event_id, "lists/create", params)

    async def create_xlsx(
        self,
        name: str,
        contests: list[int] | None = None,
        filter_expr: str = "",
        selector_result: str = "",
        lang: str = "",
    ) -> bytes:
        """Create a list in XLSX format.

        Based on go-webapi/eventapi_lists.go:189-199.

        Args:
            name: List name
            contests: Contest IDs
            filter_expr: Filter expression
            selector_result: Selector result
            lang: Language code

        Returns:
            XLSX file as bytes
        """
        params: dict[str, Any] = {
            "name": name,
            "format": "xlsx",
            "filter": filter_expr,
            "selectorResult": selector_result,
            "lang": lang,
        }
        if contests:
            params["contest"] = self._int_list_to_string(contests)
        return await self._client.get(self._event_id, "lists/create", params)

    async def participants_not_activated(
        self,
        name: str,
        contests: list[int] | None = None,
        only_with_underscores: bool = False,
    ) -> int:
        """Get count of participants in list that are not activated.

        Based on go-webapi/eventapi_lists.go:202-218.

        Args:
            name: List name
            contests: Contest IDs
            only_with_underscores: Only count those with underscores

        Returns:
            Count of non-activated participants
        """
        params: dict[str, Any] = {
            "name": name,
            "onlyWithUnderscores": only_with_underscores,
        }
        if contests:
            params["contest"] = self._int_list_to_string(contests)
        result = await self._client.get_json(
            self._event_id, "lists/participantsnotactivated", params
        )
        return int(result) if result is not None else 0
