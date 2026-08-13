# py-raceresult

[![CI](https://github.com/Karlsruher-Lemminge/py-raceresult/actions/workflows/ci.yml/badge.svg)](https://github.com/Karlsruher-Lemminge/py-raceresult/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-blue)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Async Python client for the [Raceresult](https://www.raceresult.com/) event management API. This is unofficial Python implementation of [Raceresult go-webapi](https://github.com/raceresult/go-webapi) Vibe Coded with Claude Code. **Use at your own risk.**

You can receive an Raceresult API Key in your Account.

## Features

- **Async-first design** using httpx for non-blocking I/O
- **Full API coverage** with 44 endpoint modules matching go-webapi
- **Type-safe** with Pydantic v2 models, full type annotations, and a `py.typed` marker
- **Multiple auth methods** including API key, username/password, 2FA, and RR user token
- **Custom type handling** for Raceresult date/time/decimal formats
- **Certificate generation** — create individual or bulk PDF/JPG certificates (Urkunden)
- **Portal settings** — read and write all my.raceresult.com page configuration via the `Portal` prefix

Every endpoint, query parameter and JSON field name in this client is ported
from — and verified against — the official Go reference client, so the wire
format matches what the Raceresult server actually expects.

## Installation

From GitHub:

```bash
pip install git+https://github.com/Karlsruher-Lemminge/py-raceresult.git
```

Or with uv:

```bash
uv add git+https://github.com/Karlsruher-Lemminge/py-raceresult.git
```

For local development:

```bash
git clone https://github.com/Karlsruher-Lemminge/py-raceresult.git
cd py-raceresult
pip install -e .
```

## Quick Start

```python
import asyncio
from raceresult import RaceResultAPI

async def main():
    async with RaceResultAPI() as api:
        # Login with API key
        await api.login(api_key="your-api-key")

        # List events
        events = await api.event_list(year=2024)

        # Access a specific event
        event = api.event("your-event-id")

        # Get event settings
        settings = await event.settings.get("EventName", "EventDate")
        print(f"Event: {settings['EventName']}")

        # Count participants
        count = await event.data.count()
        print(f"Participants: {count}")

asyncio.run(main())
```

## Authentication

The API supports multiple authentication methods:

```python
# API key (recommended)
await api.login(api_key="your-api-key")

# Username and password
await api.login(user="username", password="password")

# With 2FA (TOTP)
await api.login(user="username", password="password", totp="123456")

# Check login status
if api.is_logged_in:
    print(f"Session: {api.session_id}")

# Logout
await api.logout()
```

## Available Endpoints

Non-event endpoints are accessed directly on the API object:

| Endpoint | Description |
|----------|-------------|
| `api.general()` | Server fonts, version, translations |
| `await api.event_list()` | List all events |
| `await api.create_event()` | Create a new event |
| `await api.user_info()` | Current user info |

Event-specific endpoints are accessed via `api.event(event_id)`:

| Category | Endpoints | Description |
|----------|-----------|-------------|
| **Core Data** | `data`, `participants`, `settings` | Query, filter, and manage participant data |
| **Event Config** | `contests`, `agegroups`, `bibranges`, `customfields`, `entryfees`, `user_defined_fields` | Event structure and pricing |
| **Timing** | `times`, `rawdata`, `rawdata_rules`, `timingpoints`, `timingpointrules`, `chipfile`, `group_times`, `overwrite_values`, `splits` | Timing device data and configuration |
| **Results** | `results`, `lists`, `exporters`, `rankings`, `team_scores` | Result definitions and output generation |
| **Output** | `certificates`, `certificate_sets`, `labels`, `statistics` | Printable output generation |
| **Registration** | `registrations`, `vouchers` | Registration forms and discount codes |
| **Communication** | `email_templates`, `chat`, `webhooks`, `simple_api` | Messaging and integrations |
| **Check-In** | `kiosks` | Check-in kiosk configuration |
| **Audit** | `history` | Change tracking |
| **Media** | `pictures` | Picture library |
| **Archives** | `archives` | Cross-event participant history |
| **Infrastructure** | `file`, `backup`, `forwarding`, `synchronization`, `dependencies`, `information` | File management, replication, utilities |

## Usage Examples

### Query Participants

```python
event = api.event("event-id")

# Get participant count with filter
count = await event.data.count(filter_expr="[Status]=1")

# List participants with specific fields
data = await event.data.list(
    fields=["Bib", "Firstname", "Lastname", "Contest"],
    filter_expr="[Contest]=1",
    sort=["Bib"],
    limit_to=100
)
for row in data:
    print(f"Bib {row[0]}: {row[1]} {row[2]}")
```

### Access Timing Data

```python
from raceresult.endpoints.participants import Identifier

event = api.event("event-id")

# Get times for a participant
times = await event.times.get(Identifier.by_bib(123))
for t in times:
    print(f"Result {t.result}: {t.time_text}")

# Get raw timing data
raw_count = await event.rawdata.count(Identifier.by_filter(""))
distinct = await event.rawdata.distinct_values()
print(f"Decoder IDs: {distinct.decoder_id}")
```

### Registration Forms

```python
event = api.event("event-id")

# List registration forms
reg_names = await event.registrations.names()
print(f"Forms: {reg_names}")

# Get form details
reg = await event.registrations.get(reg_names[0])
print(f"Form: {reg.name}")
print(f"Steps: {len(reg.steps)}")
print(f"Enabled: {reg.enabled}")
```

### Export Data

```python
event = api.event("event-id")

# Get all list names
list_names = await event.lists.names()

# Generate PDF
pdf_bytes = await event.lists.create_pdf(
    name=list_names[0],
    contests=[1]
)
with open("results.pdf", "wb") as f:
    f.write(pdf_bytes)

# Export as CSV
csv_bytes = await event.lists.create_csv(
    name=list_names[0],
    contests=[1]
)
```

### Certificates (Urkunden)

```python
event = api.event("event-id")

# List available certificate templates
names = await event.certificates.names()
print(names)  # ['Urkunde', 'UrkundeMitSponsoren', ...]

# Get certificate definition (template, elements, page size)
cert = await event.certificates.get("Urkunde")
print(f"{cert.page_size.value} {cert.page_format.value}, {len(cert.elements)} elements")

# Generate a PDF certificate for one participant (by bib number)
pdf = await event.certificates.create_pdf("Urkunde", page=1, bib=42, lang="de")
with open("urkunde_42.pdf", "wb") as f:
    f.write(pdf)

# Generate a JPG preview
jpg = await event.certificates.create_jpg("Urkunde", page=1, bib=42, dpi=150, lang="de")

# List certificate sets (define who gets which certificate)
set_names = await event.certificate_sets.names()
cs = await event.certificate_sets.get(set_names[0])
print(f"Set '{cs.name}' uses template '{cs.certificate}'")

# Count participants included in a set
n = await event.certificate_sets.count("Urkunde", contests=[1, 2])
print(f"{n} participants will receive a certificate")

# Generate bulk PDF for all participants in a set
bulk_pdf = await event.certificate_sets.create("Urkunde", contests=[1], lang="de")
with open("alle_urkunden.pdf", "wb") as f:
    f.write(bulk_pdf)
```

### my.raceresult.com Portal Settings

The my.raceresult.com pages (Participants, Results, Live) are fully configurable
via the `settings` endpoint using the `Portal` prefix.

```python
event = api.event("event-id")

# Read all portal settings (228+ keys)
names = await event.settings.names_by_prefix("Portal")
vals = await event.settings.get(*names)

# Page visibility windows (pages 1–4: Results, Participants, …, Live)
print(vals["PortalShowFrom1"])   # e.g. "2026-05-17"
print(vals["PortalShowUntil1"])  # e.g. "2100-12-31 23:59:59"
print(vals["PortalShowFrom4"])   # Live page start
print(vals["PortalShowUntil4"])  # Live page end (often just the race day)

# Registration window
print(vals["PortalRegEnabled"])  # True/False
print(vals["PortalRegFrom"])     # "2026-02-01"
print(vals["PortalRegUntil"])    # "2026-05-10 23:59:59"

# Change a value
await event.settings.save_value("PortalShowUntil4", "2026-05-18 23:59:59")
```

Key `Portal` setting groups:

| Prefix | Description |
|--------|-------------|
| `PortalShowFrom/Until1..4` | Visibility window for each portal page |
| `PortalRegEnabled/From/Until` | Online registration window |
| `PortalListsJSON`, `PortalLists2JSON`, … | Lists shown on each page |
| `PortalLinkCertificates1..4` | Whether certificates are linked on each page |
| `PortalCertificateSetsJSON` | Certificate sets and their display modes |
| `PortalConf*` | Confirmation email content and routing |
| `PortalPay*` | Payment provider configuration |
| `PortalOrganizer*` | Organizer contact info shown on the portal |

## Models

All API responses are validated using Pydantic v2 models. Key models:

| Module | Models |
|--------|--------|
| `raceresult.models.event` | `Contest`, `AgeGroup`, `BibRange`, `EntryFee`, `Ranking`, `Split`, `TeamScore`, `WebHook`, `ChatMessage`, `GroupTimes`, `RawDataRule`, `SimpleAPIItem`, `Version`, `ForwardingInfo` |
| `raceresult.models.participant` | `Participant`, `ParticipantNewResponse` |
| `raceresult.models.timing` | `TimingPoint`, `TimingPointRule`, `RawData`, `Time`, `Passing`, `PassingPosition` |
| `raceresult.models.registration` | `Registration`, `Step`, `Element`, `FormField` |
| `raceresult.models.payment` | `Voucher`, `VoucherType` |
| `raceresult.models.email` | `EmailTemplate` |
| `raceresult.models.kiosk` | `Kiosk`, `KioskStep`, `KioskDisplayField`, `KioskEditField` |
| `raceresult.endpoints.certificates` | `Certificate`, `Element`, `Zone`, `PageSize`, `PageFormat` |
| `raceresult.endpoints.certificatesets` | `CertificateSet`, `CertificateSetType` |
| `raceresult.models.label` | `Label`, `LabelDirection`, `LabelBarcodeType` |
| `raceresult.models.statistic` | `Statistics`, `Aggregation` |
| `raceresult.models.archives` | `ArchivesParticipant`, `ParticipationExt`, `ArchivesMatch` |

```python
from raceresult.models import Participant, Contest, AgeGroup
from raceresult.endpoints.certificates import Certificate
from raceresult.models.statistic import Statistics, Aggregation
```

## Behaviour worth knowing

A few places where the Raceresult wire format leaks into the Python API.
These match the Go reference client exactly; deviating from them causes
silent data corruption rather than errors.

### Dates and times are naive unless the server sends a timezone

Raceresult transmits datetimes in three forms, and only one carries a zone:

| Wire value | Python value |
|------------|--------------|
| `"2024-05-01"` | `datetime(2024, 5, 1)` — naive |
| `"2024-05-01 10:00:00"` | `datetime(2024, 5, 1, 10, 0)` — naive |
| `"2024-05-01T10:00:00+02:00"` | timezone-aware |
| `""`, `"1899-12-30"`, `"0001-01-01"` | `None` |

Zoneless values stay **naive** on purpose — they are event-local, and the Go
model tracks this with an explicit `hasZone` flag. Attaching UTC to them would
turn a 10:00 local start time into 12:00 on the next save. To compare a model
value against `datetime.now(timezone.utc)`, normalise it first:

```python
from raceresult.models.types import align_timezone

now = datetime.now(timezone.utc)
if voucher.valid_until and now > align_timezone(voucher.valid_until, now):
    ...
```

Values are also truncated to whole seconds on the way out, because the server
parses datetimes by string length and rejects anything with microseconds.

### Field lists may contain expressions

Field, sort and group parameters are sent as a JSON array, not a comma-joined
string, so expressions containing commas survive intact:

```python
rows = await event.data.list(fields=['Bib', 'IIF([Sex]="m","M","W")'])
```

### `Identifier.by_filter` conflicts with an explicit filter

`by_filter` has no equivalent in go-webapi and maps onto the same `filter`
query parameter that several endpoints expose directly. Passing both raises
`ValueError` instead of silently discarding one of them:

```python
await event.participants.delete(filter_expr="[Contest]=1")            # ok
await event.participants.delete(identifier=Identifier.by_bib(42))     # ok
await event.participants.delete(                                      # ValueError
    filter_expr="[Contest]=1", identifier=Identifier.by_filter("[Bib]=99")
)
```

### Empty collections arrive as `null`

The API returns JSON `null` rather than `[]`/`{}` for empty lists and maps.
Models coerce these to empty collections, so `ranking.sort` is `[]` rather
than raising or being `None`.

## Requirements

- Python 3.9 – 3.13
- httpx >= 0.25.0
- pydantic >= 2.0.0

## Development

The project uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync --extra dev

uv run pytest                  # tests
uv run ruff check .            # lint
uv run mypy src/raceresult     # type-check (strict)
uv build                       # sdist + wheel
```

`tests/manual_*.py` are smoke-test scripts, not part of the suite. They need a
live event and read `API_KEY` from a local `.env`:

```bash
uv run python tests/manual_test_live.py <event-id>
```

CI runs lint, strict type-checking and the test suite on Python 3.9–3.13.

## Releasing

1. Bump `version` in `pyproject.toml` and update `CHANGELOG.md`.
2. Tag the commit: `git tag v0.2.0 && git push origin v0.2.0`.

The release workflow re-runs the full CI gates, verifies the tag matches the
project version, builds the distributions and creates a GitHub release.
Publishing to PyPI additionally requires a `pypi` environment configured as a
[Trusted Publisher](https://docs.pypi.org/trusted-publishers/) and the
repository variable `PUBLISH_TO_PYPI` set to `true`.

