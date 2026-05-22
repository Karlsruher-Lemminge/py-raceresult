"""Main API class for Raceresult.

Based on go-webapi/api.go and go-webapi/eventapi.go.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from raceresult.client import RaceResultClient
from raceresult.endpoints.agegroups import AgeGroupsEndpoint
from raceresult.endpoints.archives import ArchivesEndpoint
from raceresult.endpoints.backup import BackupEndpoint
from raceresult.endpoints.bibranges import BibRangesEndpoint
from raceresult.endpoints.certificate_sets import CertificateSetsEndpoint
from raceresult.endpoints.certificates import CertificatesEndpoint
from raceresult.endpoints.chat import ChatEndpoint
from raceresult.endpoints.contests import ContestsEndpoint
from raceresult.endpoints.customfields import CustomFieldsEndpoint
from raceresult.endpoints.data import DataEndpoint
from raceresult.endpoints.dependencies import DependenciesEndpoint
from raceresult.endpoints.email_templates import EmailTemplatesEndpoint
from raceresult.endpoints.entryfees import EntryFeesEndpoint
from raceresult.endpoints.exporters import ExportersEndpoint
from raceresult.endpoints.file import FileEndpoint
from raceresult.endpoints.forwarding import ForwardingEndpoint
from raceresult.endpoints.general import GeneralEndpoint
from raceresult.endpoints.group_times import GroupTimesEndpoint
from raceresult.endpoints.history import HistoryEndpoint
from raceresult.endpoints.information import InformationEndpoint
from raceresult.endpoints.kiosks import KiosksEndpoint
from raceresult.endpoints.labels import LabelsEndpoint
from raceresult.endpoints.lists import ListsEndpoint
from raceresult.endpoints.overwrite_values import OverwriteValuesEndpoint
from raceresult.endpoints.participants import ParticipantsEndpoint
from raceresult.endpoints.pictures import PicturesEndpoint
from raceresult.endpoints.rankings import RankingsEndpoint
from raceresult.endpoints.rawdata import RawDataEndpoint
from raceresult.endpoints.rawdata_rules import RawDataRulesEndpoint
from raceresult.endpoints.registrations import RegistrationsEndpoint
from raceresult.endpoints.results import ResultsEndpoint
from raceresult.endpoints.settings import SettingsEndpoint
from raceresult.endpoints.simple_api import SimpleAPIEndpoint
from raceresult.endpoints.splits import SplitsEndpoint
from raceresult.endpoints.statistics import StatisticsEndpoint
from raceresult.endpoints.synchronization import SynchronizationEndpoint
from raceresult.endpoints.team_scores import TeamScoresEndpoint
from raceresult.endpoints.times import TimesEndpoint
from raceresult.endpoints.timing import ChipFileEndpoint
from raceresult.endpoints.timingpoints import TimingPointsEndpoint
from raceresult.endpoints.timingpointrules import TimingPointRulesEndpoint
from raceresult.endpoints.user_defined_fields import UserDefinedFieldsEndpoint
from raceresult.endpoints.vouchers import VouchersEndpoint
from raceresult.endpoints.webhooks import WebHooksEndpoint
from raceresult.models.public import UserInfo, UserRight, OAuthToken


class EventListItem:
    """Item in the event list."""

    def __init__(
        self,
        id: str,
        user_id: int,
        user_name: str,
        checked_out: bool,
        participants: int,
        not_activated: int,
        event_name: str,
        event_date: datetime | None,
        event_date2: datetime | None,
        event_location: str,
        event_country: int,
    ):
        self.id = id
        self.user_id = user_id
        self.user_name = user_name
        self.checked_out = checked_out
        self.participants = participants
        self.not_activated = not_activated
        self.event_name = event_name
        self.event_date = event_date
        self.event_date2 = event_date2
        self.event_location = event_location
        self.event_country = event_country


class EventAPI:
    """API for a specific event.

    Based on go-webapi/eventapi.go.

    Provides access to all event-specific endpoints.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            count = await event.data.count()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the event API.

        Args:
            client: HTTP client
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

        # Lazy-initialized endpoints
        self._settings: SettingsEndpoint | None = None
        self._registrations: RegistrationsEndpoint | None = None
        self._participants: ParticipantsEndpoint | None = None
        self._vouchers: VouchersEndpoint | None = None
        self._email_templates: EmailTemplatesEndpoint | None = None
        self._data: DataEndpoint | None = None
        self._chipfile: ChipFileEndpoint | None = None
        self._contests: ContestsEndpoint | None = None
        self._agegroups: AgeGroupsEndpoint | None = None
        self._bibranges: BibRangesEndpoint | None = None
        self._customfields: CustomFieldsEndpoint | None = None
        self._entryfees: EntryFeesEndpoint | None = None
        self._results: ResultsEndpoint | None = None
        self._times: TimesEndpoint | None = None
        self._timingpoints: TimingPointsEndpoint | None = None
        self._timingpointrules: TimingPointRulesEndpoint | None = None
        self._rawdata: RawDataEndpoint | None = None
        self._lists: ListsEndpoint | None = None
        self._exporters: ExportersEndpoint | None = None
        self._history: HistoryEndpoint | None = None
        self._kiosks: KiosksEndpoint | None = None
        self._archives: ArchivesEndpoint | None = None
        self._backup: BackupEndpoint | None = None
        self._certificate_sets: CertificateSetsEndpoint | None = None
        self._certificates: CertificatesEndpoint | None = None
        self._chat: ChatEndpoint | None = None
        self._dependencies: DependenciesEndpoint | None = None
        self._file: FileEndpoint | None = None
        self._forwarding: ForwardingEndpoint | None = None
        self._group_times: GroupTimesEndpoint | None = None
        self._information: InformationEndpoint | None = None
        self._labels: LabelsEndpoint | None = None
        self._overwrite_values: OverwriteValuesEndpoint | None = None
        self._pictures: PicturesEndpoint | None = None
        self._rankings: RankingsEndpoint | None = None
        self._rawdata_rules: RawDataRulesEndpoint | None = None
        self._simple_api: SimpleAPIEndpoint | None = None
        self._splits: SplitsEndpoint | None = None
        self._statistics: StatisticsEndpoint | None = None
        self._synchronization: SynchronizationEndpoint | None = None
        self._team_scores: TeamScoresEndpoint | None = None
        self._user_defined_fields: UserDefinedFieldsEndpoint | None = None
        self._webhooks: WebHooksEndpoint | None = None

    @property
    def event_id(self) -> str:
        """Get the event ID."""
        return self._event_id

    @property
    def settings(self) -> SettingsEndpoint:
        """Get the settings endpoint."""
        if self._settings is None:
            self._settings = SettingsEndpoint(self._client, self._event_id)
        return self._settings

    @property
    def registrations(self) -> RegistrationsEndpoint:
        """Get the registrations endpoint."""
        if self._registrations is None:
            self._registrations = RegistrationsEndpoint(self._client, self._event_id)
        return self._registrations

    @property
    def participants(self) -> ParticipantsEndpoint:
        """Get the participants endpoint."""
        if self._participants is None:
            self._participants = ParticipantsEndpoint(self._client, self._event_id)
        return self._participants

    @property
    def vouchers(self) -> VouchersEndpoint:
        """Get the vouchers endpoint."""
        if self._vouchers is None:
            self._vouchers = VouchersEndpoint(self._client, self._event_id)
        return self._vouchers

    @property
    def email_templates(self) -> EmailTemplatesEndpoint:
        """Get the email templates endpoint."""
        if self._email_templates is None:
            self._email_templates = EmailTemplatesEndpoint(self._client, self._event_id)
        return self._email_templates

    @property
    def data(self) -> DataEndpoint:
        """Get the data endpoint."""
        if self._data is None:
            self._data = DataEndpoint(self._client, self._event_id)
        return self._data

    @property
    def chipfile(self) -> ChipFileEndpoint:
        """Get the chip file endpoint."""
        if self._chipfile is None:
            self._chipfile = ChipFileEndpoint(self._client, self._event_id)
        return self._chipfile

    @property
    def contests(self) -> ContestsEndpoint:
        """Get the contests endpoint."""
        if self._contests is None:
            self._contests = ContestsEndpoint(self._client, self._event_id)
        return self._contests

    @property
    def agegroups(self) -> AgeGroupsEndpoint:
        """Get the age groups endpoint."""
        if self._agegroups is None:
            self._agegroups = AgeGroupsEndpoint(self._client, self._event_id)
        return self._agegroups

    @property
    def bibranges(self) -> BibRangesEndpoint:
        """Get the bib ranges endpoint."""
        if self._bibranges is None:
            self._bibranges = BibRangesEndpoint(self._client, self._event_id)
        return self._bibranges

    @property
    def customfields(self) -> CustomFieldsEndpoint:
        """Get the custom fields endpoint."""
        if self._customfields is None:
            self._customfields = CustomFieldsEndpoint(self._client, self._event_id)
        return self._customfields

    @property
    def entryfees(self) -> EntryFeesEndpoint:
        """Get the entry fees endpoint."""
        if self._entryfees is None:
            self._entryfees = EntryFeesEndpoint(self._client, self._event_id)
        return self._entryfees

    @property
    def results(self) -> ResultsEndpoint:
        """Get the results endpoint."""
        if self._results is None:
            self._results = ResultsEndpoint(self._client, self._event_id)
        return self._results

    @property
    def times(self) -> TimesEndpoint:
        """Get the times endpoint."""
        if self._times is None:
            self._times = TimesEndpoint(self._client, self._event_id)
        return self._times

    @property
    def timingpoints(self) -> TimingPointsEndpoint:
        """Get the timing points endpoint."""
        if self._timingpoints is None:
            self._timingpoints = TimingPointsEndpoint(self._client, self._event_id)
        return self._timingpoints

    @property
    def timingpointrules(self) -> TimingPointRulesEndpoint:
        """Get the timing point rules endpoint."""
        if self._timingpointrules is None:
            self._timingpointrules = TimingPointRulesEndpoint(self._client, self._event_id)
        return self._timingpointrules

    @property
    def rawdata(self) -> RawDataEndpoint:
        """Get the raw data endpoint."""
        if self._rawdata is None:
            self._rawdata = RawDataEndpoint(self._client, self._event_id)
        return self._rawdata

    @property
    def lists(self) -> ListsEndpoint:
        """Get the lists endpoint."""
        if self._lists is None:
            self._lists = ListsEndpoint(self._client, self._event_id)
        return self._lists

    @property
    def exporters(self) -> ExportersEndpoint:
        """Get the exporters endpoint."""
        if self._exporters is None:
            self._exporters = ExportersEndpoint(self._client, self._event_id)
        return self._exporters

    @property
    def history(self) -> HistoryEndpoint:
        """Get the history endpoint."""
        if self._history is None:
            self._history = HistoryEndpoint(self._client, self._event_id)
        return self._history

    @property
    def kiosks(self) -> KiosksEndpoint:
        """Get the kiosks endpoint."""
        if self._kiosks is None:
            self._kiosks = KiosksEndpoint(self._client, self._event_id)
        return self._kiosks

    @property
    def archives(self) -> ArchivesEndpoint:
        if self._archives is None:
            self._archives = ArchivesEndpoint(self._client, self._event_id)
        return self._archives

    @property
    def backup(self) -> BackupEndpoint:
        if self._backup is None:
            self._backup = BackupEndpoint(self._client, self._event_id)
        return self._backup

    @property
    def certificate_sets(self) -> CertificateSetsEndpoint:
        if self._certificate_sets is None:
            self._certificate_sets = CertificateSetsEndpoint(self._client, self._event_id)
        return self._certificate_sets

    @property
    def certificates(self) -> CertificatesEndpoint:
        if self._certificates is None:
            self._certificates = CertificatesEndpoint(self._client, self._event_id)
        return self._certificates

    @property
    def chat(self) -> ChatEndpoint:
        if self._chat is None:
            self._chat = ChatEndpoint(self._client, self._event_id)
        return self._chat

    @property
    def dependencies(self) -> DependenciesEndpoint:
        if self._dependencies is None:
            self._dependencies = DependenciesEndpoint(self._client, self._event_id)
        return self._dependencies

    @property
    def file(self) -> FileEndpoint:
        if self._file is None:
            self._file = FileEndpoint(self._client, self._event_id)
        return self._file

    @property
    def forwarding(self) -> ForwardingEndpoint:
        if self._forwarding is None:
            self._forwarding = ForwardingEndpoint(self._client, self._event_id)
        return self._forwarding

    @property
    def group_times(self) -> GroupTimesEndpoint:
        if self._group_times is None:
            self._group_times = GroupTimesEndpoint(self._client, self._event_id)
        return self._group_times

    @property
    def information(self) -> InformationEndpoint:
        if self._information is None:
            self._information = InformationEndpoint(self._client, self._event_id)
        return self._information

    @property
    def labels(self) -> LabelsEndpoint:
        if self._labels is None:
            self._labels = LabelsEndpoint(self._client, self._event_id)
        return self._labels

    @property
    def overwrite_values(self) -> OverwriteValuesEndpoint:
        if self._overwrite_values is None:
            self._overwrite_values = OverwriteValuesEndpoint(self._client, self._event_id)
        return self._overwrite_values

    @property
    def pictures(self) -> PicturesEndpoint:
        if self._pictures is None:
            self._pictures = PicturesEndpoint(self._client, self._event_id)
        return self._pictures

    @property
    def rankings(self) -> RankingsEndpoint:
        if self._rankings is None:
            self._rankings = RankingsEndpoint(self._client, self._event_id)
        return self._rankings

    @property
    def rawdata_rules(self) -> RawDataRulesEndpoint:
        if self._rawdata_rules is None:
            self._rawdata_rules = RawDataRulesEndpoint(self._client, self._event_id)
        return self._rawdata_rules

    @property
    def simple_api(self) -> SimpleAPIEndpoint:
        if self._simple_api is None:
            self._simple_api = SimpleAPIEndpoint(self._client, self._event_id)
        return self._simple_api

    @property
    def splits(self) -> SplitsEndpoint:
        if self._splits is None:
            self._splits = SplitsEndpoint(self._client, self._event_id)
        return self._splits

    @property
    def statistics(self) -> StatisticsEndpoint:
        if self._statistics is None:
            self._statistics = StatisticsEndpoint(self._client, self._event_id)
        return self._statistics

    @property
    def synchronization(self) -> SynchronizationEndpoint:
        if self._synchronization is None:
            self._synchronization = SynchronizationEndpoint(self._client, self._event_id)
        return self._synchronization

    @property
    def team_scores(self) -> TeamScoresEndpoint:
        if self._team_scores is None:
            self._team_scores = TeamScoresEndpoint(self._client, self._event_id)
        return self._team_scores

    @property
    def user_defined_fields(self) -> UserDefinedFieldsEndpoint:
        if self._user_defined_fields is None:
            self._user_defined_fields = UserDefinedFieldsEndpoint(self._client, self._event_id)
        return self._user_defined_fields

    @property
    def webhooks(self) -> WebHooksEndpoint:
        if self._webhooks is None:
            self._webhooks = WebHooksEndpoint(self._client, self._event_id)
        return self._webhooks


class RaceResultAPI:
    """Main Raceresult API client.

    Based on go-webapi/api.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="your-api-key")

            # List events
            events = await api.event_list(2024)

            # Access an event
            event = api.event("event123")
            count = await event.data.count()
            settings = await event.settings.get("EventName", "EventDate")
    """

    def __init__(
        self,
        server: str = RaceResultClient.DEFAULT_SERVER,
        https: bool = True,
        timeout: float = RaceResultClient.DEFAULT_TIMEOUT,
        user_agent: str = RaceResultClient.DEFAULT_USER_AGENT,
    ):
        """Initialize the API.

        Args:
            server: Server hostname (default: events.raceresult.com)
            https: Use HTTPS (default: True)
            timeout: Request timeout in seconds (default: 30)
            user_agent: User-Agent header value
        """
        self._client = RaceResultClient(
            server=server,
            https=https,
            timeout=timeout,
            user_agent=user_agent,
        )

    @property
    def client(self) -> RaceResultClient:
        """Get the underlying HTTP client."""
        return self._client

    @property
    def is_logged_in(self) -> bool:
        """Check if the client is logged in."""
        return self._client.is_logged_in

    @property
    def session_id(self) -> str:
        """Get the current session ID."""
        return self._client.session_id

    async def __aenter__(self) -> RaceResultAPI:
        """Enter async context manager."""
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit async context manager."""
        await self._client.__aexit__(exc_type, exc_val, exc_tb)

    def general(self) -> GeneralEndpoint:
        """Get the general (non-event-specific) API endpoint."""
        return GeneralEndpoint(self._client)

    async def login(
        self,
        api_key: str | None = None,
        user: str | None = None,
        password: str | None = None,
        sign_in_as: str | None = None,
        totp: str | None = None,
        rr_user_token: str | None = None,
    ) -> None:
        """Login to the API.

        Args:
            api_key: API key for authentication
            user: Username for authentication
            password: Password for authentication
            sign_in_as: Sign in as another user
            totp: Time-based OTP for 2FA
            rr_user_token: RR user token
        """
        await self._client.login(
            api_key=api_key,
            user=user,
            password=password,
            sign_in_as=sign_in_as,
            totp=totp,
            rr_user_token=rr_user_token,
        )

    async def logout(self) -> None:
        """Logout from the API."""
        await self._client.logout()

    def event(self, event_id: str) -> EventAPI:
        """Get an EventAPI for a specific event.

        Args:
            event_id: Event ID

        Returns:
            EventAPI instance
        """
        return EventAPI(self._client, event_id)

    async def event_list(
        self, year: int = 0, filter_expr: str = ""
    ) -> list[EventListItem]:
        """Get list of events.

        Based on go-webapi/api_public.go:121-137.

        Args:
            year: Year filter (0 for all)
            filter_expr: Filter expression

        Returns:
            List of events
        """
        params = {
            "year": year,
            "filter": filter_expr,
            "addsettings": "EventName,EventDate,EventDate2,EventLocation,EventCountry",
        }
        result = await self._client.get_json(None, "public/eventlist", params)

        events = []
        for item in result or []:
            event_date = None
            event_date2 = None
            if item.get("EventDate"):
                try:
                    event_date = datetime.fromisoformat(
                        item["EventDate"].replace("Z", "+00:00")
                    )
                except (ValueError, TypeError):
                    pass
            if item.get("EventDate2"):
                try:
                    event_date2 = datetime.fromisoformat(
                        item["EventDate2"].replace("Z", "+00:00")
                    )
                except (ValueError, TypeError):
                    pass

            events.append(
                EventListItem(
                    id=item.get("ID", ""),
                    user_id=item.get("UserID", 0),
                    user_name=item.get("UserName", ""),
                    checked_out=item.get("CheckedOut", False),
                    participants=item.get("Participants", 0),
                    not_activated=item.get("NotActivated", 0),
                    event_name=item.get("EventName", ""),
                    event_date=event_date,
                    event_date2=event_date2,
                    event_location=item.get("EventLocation", ""),
                    event_country=item.get("EventCountry", 0),
                )
            )
        return events

    async def create_event(
        self,
        event_name: str,
        event_date: datetime,
        event_country: int = 0,
        copy_of: int = 0,
        template_id: int = 0,
        mode: int = 0,
        laps: int = 0,
    ) -> EventAPI:
        """Create a new event.

        Based on go-webapi/api_public.go:140-158.

        Args:
            event_name: Event name
            event_date: Event date
            event_country: Country code
            copy_of: Copy from existing event ID
            template_id: Template ID
            mode: Event mode
            laps: Number of laps

        Returns:
            EventAPI for the new event
        """
        params = {
            "name": event_name,
            "date": event_date.isoformat(),
            "country": event_country,
            "copyOf": copy_of,
            "templateID": template_id,
            "mode": mode,
            "laps": laps,
        }
        result = await self._client.get(None, "public/createevent", params)
        event_id = result.decode("utf-8")
        return EventAPI(self._client, event_id)

    async def delete_event(self, event_id: str) -> None:
        """Delete an event.

        Based on go-webapi/api_public.go:161-167.

        Warning: This permanently deletes the event!

        Args:
            event_id: Event ID to delete
        """
        params = {"eventID": event_id}
        await self._client.get(None, "public/deleteevent", params)

    async def user_info(self) -> UserInfo:
        """Get current user info.

        Based on go-webapi/api_public.go:184-195.

        Returns:
            UserInfo object with CustNo, UserName, UserPic
        """
        result = await self._client.get_json(None, "public/userinfo")
        return UserInfo.model_validate(result if result else {})

    async def token_from_session(self) -> OAuthToken:
        """Get an auth token for other RR services.

        Based on go-webapi/api_public.go:170-181.

        Returns:
            OAuthToken object
        """
        result = await self._client.get_json(None, "public/tokenfromsession")
        return OAuthToken.model_validate(result if result else {})

    async def user_rights_get(self, event_id: str) -> list[UserRight]:
        """Get list of users with access rights for an event.

        Based on go-webapi/api_public.go:198-212.

        Args:
            event_id: Event ID

        Returns:
            List of UserRight objects
        """
        params = {"eventID": event_id}
        result = await self._client.get_json(None, "userrights/get", params)
        if not result:
            return []
        return [UserRight.model_validate(item) for item in result]

    async def user_rights_save(
        self,
        event_id: str,
        user: str,
        rights: str,
    ) -> None:
        """Save user rights for an event.

        Based on go-webapi/api_public.go:215-223.

        Args:
            event_id: Event ID
            user: Username or email
            rights: Rights string
        """
        params = {
            "eventID": event_id,
            "user": user,
            "rights": rights,
        }
        await self._client.get(None, "userrights/save", params)

    async def user_rights_delete(self, event_id: str, user_id: int) -> None:
        """Delete user rights for an event.

        Based on go-webapi/api_public.go:226-233.

        Args:
            event_id: Event ID
            user_id: User ID to remove
        """
        params = {
            "eventID": event_id,
            "userID": user_id,
        }
        await self._client.get(None, "userrights/delete", params)
