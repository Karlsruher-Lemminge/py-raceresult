"""Certificate sets endpoint for Raceresult API.

Based on go-webapi/eventapi_certificatesets.go and go-model/certificateset/.
"""

from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class CertificateSetType(IntEnum):
    """Certificate set type.

    Based on go-model/certificateset/certificateset.go.
    """

    SINGLE = 0
    TEAM = 1
    TEAM_MULTI = 2


class CertificateSet(BaseModel):
    """A certificate set groups a certificate template with filter/sort rules.

    Based on go-model/certificateset/certificateset.go.
    Note: certificate name maps to "CertificateName" in JSON.
    """

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
    only_unshown_certificates: bool = Field(
        default=False, alias="OnlyUnshownCertificates"
    )
    sort1: str = Field(default="", alias="Sort1")
    sort2: str = Field(default="", alias="Sort2")
    sort3: str = Field(default="", alias="Sort3")
    sort4: str = Field(default="", alias="Sort4")
    sort_desc1: bool = Field(default=False, alias="SortDesc1")
    sort_desc2: bool = Field(default=False, alias="SortDesc2")
    sort_desc3: bool = Field(default=False, alias="SortDesc3")
    sort_desc4: bool = Field(default=False, alias="SortDesc4")

    model_config = {"populate_by_name": True}


class CertificateSetsEndpoint:
    """Certificate sets API endpoint.

    Based on go-webapi/eventapi_certificatesets.go.

    Certificate sets define which participants receive which certificate,
    and can generate a bulk PDF for mass printing.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            sets = await event.certificate_sets.names()
            n = await event.certificate_sets.count(sets[0], contests=[1])
            pdf = await event.certificate_sets.create(sets[0], contests=[1], filter="", lang="de")
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def names(self) -> list[str]:
        """Return names of all certificate sets.

        Based on go-webapi/eventapi_certificatesets.go:22-28.
        """
        result = await self._client.get_json(self._event_id, "certificatesets/names")
        if not result:
            return []
        return list(result)

    async def get(self, name: str) -> CertificateSet:
        """Return a certificate set by name.

        Based on go-webapi/eventapi_certificatesets.go:31-44.
        """
        result = await self._client.get_json(
            self._event_id, "certificatesets/get", {"name": name}
        )
        return CertificateSet.model_validate(result if result else {})

    async def save(self, item: CertificateSet) -> None:
        """Save a certificate set.

        Based on go-webapi/eventapi_certificatesets.go:47-50.
        """
        await self._client.post_json(
            self._event_id,
            "certificatesets/save",
            data=item.model_dump(mode="json", by_alias=True),
        )

    async def delete(self, name: str) -> None:
        """Delete a certificate set.

        Based on go-webapi/eventapi_certificatesets.go:53-59.
        """
        await self._client.get(
            self._event_id, "certificatesets/delete", {"name": name}
        )

    async def copy(self, name: str, new_name: str) -> None:
        """Copy a certificate set.

        Based on go-webapi/eventapi_certificatesets.go:62-69.
        """
        await self._client.get(
            self._event_id,
            "certificatesets/copy",
            {"name": name, "newName": new_name},
        )

    async def rename(self, name: str, new_name: str) -> None:
        """Rename a certificate set.

        Based on go-webapi/eventapi_certificatesets.go:72-79.
        """
        await self._client.get(
            self._event_id,
            "certificatesets/rename",
            {"name": name, "newName": new_name},
        )

    async def new(self, name: str) -> None:
        """Create a new empty certificate set.

        Based on go-webapi/eventapi_certificatesets.go:82-88.
        """
        await self._client.get(self._event_id, "certificatesets/new", {"name": name})

    async def create(
        self,
        name: str,
        contests: list[int],
        filter: str = "",
        lang: str = "",
    ) -> bytes:
        """Generate a bulk PDF for all participants in the certificate set.

        Based on go-webapi/eventapi_certificatesets.go:91-99.

        Args:
            name: Certificate set name
            contests: Contest IDs to include (empty = all)
            filter: Additional filter expression
            lang: Language code (e.g. "de", "en")

        Returns:
            PDF bytes
        """
        contest_str = ",".join(str(c) for c in contests)
        return await self._client.get(
            self._event_id,
            "certificatesets/create",
            {"name": name, "contest": contest_str, "filter": filter, "lang": lang},
        )

    async def count(self, name: str, contests: list[int]) -> int:
        """Return the number of participants included in the certificate set.

        Based on go-webapi/eventapi_certificatesets.go:102-117.
        """
        contest_str = ",".join(str(c) for c in contests)
        result = await self._client.get_json(
            self._event_id,
            "certificatesets/count",
            {"name": name, "contest": contest_str},
        )
        return int(result) if result is not None else 0
