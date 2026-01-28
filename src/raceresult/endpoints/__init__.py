"""Raceresult API endpoints."""

from raceresult.endpoints.agegroups import AgeGroupsEndpoint
from raceresult.endpoints.bibranges import BibRangesEndpoint
from raceresult.endpoints.contests import ContestsEndpoint
from raceresult.endpoints.customfields import CustomFieldsEndpoint
from raceresult.endpoints.data import DataEndpoint
from raceresult.endpoints.email_templates import EmailTemplatesEndpoint
from raceresult.endpoints.entryfees import EntryFeesEndpoint
from raceresult.endpoints.exporters import ExportersEndpoint
from raceresult.endpoints.history import HistoryEndpoint
from raceresult.endpoints.lists import ListsEndpoint
from raceresult.endpoints.participants import ParticipantsEndpoint, Identifier
from raceresult.endpoints.rawdata import RawDataEndpoint
from raceresult.endpoints.registrations import RegistrationsEndpoint
from raceresult.endpoints.results import ResultsEndpoint
from raceresult.endpoints.settings import SettingsEndpoint
from raceresult.endpoints.times import TimesEndpoint
from raceresult.endpoints.timing import ChipFileEndpoint
from raceresult.endpoints.timingpoints import TimingPointsEndpoint
from raceresult.endpoints.timingpointrules import TimingPointRulesEndpoint
from raceresult.endpoints.vouchers import VouchersEndpoint

__all__ = [
    # Core
    "DataEndpoint",
    "SettingsEndpoint",
    "ParticipantsEndpoint",
    "Identifier",
    "RegistrationsEndpoint",
    # Event config
    "ContestsEndpoint",
    "AgeGroupsEndpoint",
    "BibRangesEndpoint",
    "CustomFieldsEndpoint",
    "EntryFeesEndpoint",
    # Timing
    "TimesEndpoint",
    "TimingPointsEndpoint",
    "TimingPointRulesEndpoint",
    "RawDataEndpoint",
    "ChipFileEndpoint",
    # Results & output
    "ResultsEndpoint",
    "ListsEndpoint",
    "ExportersEndpoint",
    "HistoryEndpoint",
    # Communication
    "EmailTemplatesEndpoint",
    "VouchersEndpoint",
]
