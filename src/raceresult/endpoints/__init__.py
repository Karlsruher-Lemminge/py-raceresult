"""Raceresult API endpoints."""

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
from raceresult.endpoints.participants import ParticipantsEndpoint, Identifier
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

__all__ = [
    # Core
    "DataEndpoint",
    "FileEndpoint",
    "SettingsEndpoint",
    "ParticipantsEndpoint",
    "Identifier",
    "RegistrationsEndpoint",
    "SynchronizationEndpoint",
    # Event config
    "ContestsEndpoint",
    "AgeGroupsEndpoint",
    "BibRangesEndpoint",
    "CustomFieldsEndpoint",
    "EntryFeesEndpoint",
    "UserDefinedFieldsEndpoint",
    # Timing
    "TimesEndpoint",
    "TimingPointsEndpoint",
    "TimingPointRulesEndpoint",
    "RawDataEndpoint",
    "RawDataRulesEndpoint",
    "ChipFileEndpoint",
    "GroupTimesEndpoint",
    "OverwriteValuesEndpoint",
    "SplitsEndpoint",
    # Results & output
    "ResultsEndpoint",
    "ListsEndpoint",
    "ExportersEndpoint",
    "HistoryEndpoint",
    "RankingsEndpoint",
    "TeamScoresEndpoint",
    "CertificatesEndpoint",
    "CertificateSetsEndpoint",
    "LabelsEndpoint",
    "StatisticsEndpoint",
    # Communication
    "EmailTemplatesEndpoint",
    "VouchersEndpoint",
    "ChatEndpoint",
    "WebHooksEndpoint",
    "SimpleAPIEndpoint",
    # Check-In
    "KiosksEndpoint",
    # Media
    "PicturesEndpoint",
    # Archives
    "ArchivesEndpoint",
    # Infrastructure
    "BackupEndpoint",
    "ForwardingEndpoint",
    "DependenciesEndpoint",
    "InformationEndpoint",
    "GeneralEndpoint",
]
