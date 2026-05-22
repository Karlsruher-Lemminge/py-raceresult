# py-raceresult

Async Python client for the [Raceresult](https://www.raceresult.com/) event management API. This is unofficial Python implementation of [Raceresult go-webapi](https://github.com/raceresult/go-webapi) Vibe Coded with Claude Code. **Use at your own risk.**

You can receive an Raceresult API Key in your Account.

## Features

- **Async-first design** using httpx for non-blocking I/O
- **Full API coverage** with 44 endpoint modules matching go-webapi
- **Type-safe** with Pydantic v2 models and full type annotations
- **Multiple auth methods** including API key, username/password, 2FA, and RR user token
- **Custom type handling** for Raceresult date/time/decimal formats

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
    sort_by="Bib",
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
    contest=1
)
with open("results.pdf", "wb") as f:
    f.write(pdf_bytes)

# Export as CSV
csv_bytes = await event.lists.create_csv(
    name=list_names[0],
    contest=1
)
```

## Models

All API responses are validated using Pydantic v2 models. Key models:

| Module | Models |
|--------|--------|
| `raceresult.models.event` | `Contest`, `AgeGroup`, `BibRange`, `EntryFee`, `Ranking`, `Split`, `TeamScore`, `WebHook`, `ChatMessage`, `GroupTimes`, `RawDataRule`, `SimpleAPIItem`, `Version`, `ForwardingInfo` |
| `raceresult.models.participant` | `Participant`, `ParticipantNewResponse` |
| `raceresult.models.timing` | `TimingPoint`, `TimingPointRule`, `RawData`, `Time`, `Passing` |
| `raceresult.models.registration` | `Registration`, `Step`, `Element`, `FormField` |
| `raceresult.models.payment` | `Voucher`, `VoucherType` |
| `raceresult.models.email` | `EmailTemplate` |
| `raceresult.models.kiosk` | `Kiosk`, `KioskStep`, `KioskDisplayField`, `KioskEditField` |
| `raceresult.models.certificate` | `Certificate`, `CertificateElement`, `CertificateZone` |
| `raceresult.models.certificate_set` | `CertificateSet`, `CertificateSetType` |
| `raceresult.models.label` | `Label`, `LabelDirection`, `LabelBarcodeType` |
| `raceresult.models.statistic` | `Statistics`, `Aggregation` |
| `raceresult.models.archives` | `ArchivesParticipant`, `ParticipationExt`, `ArchivesMatch` |

```python
from raceresult.models import Participant, Contest, AgeGroup
from raceresult.models.certificate import Certificate
from raceresult.models.statistic import Statistics, Aggregation
```

## Requirements

- Python 3.9+
- httpx >= 0.25.0
- pydantic >= 2.0.0

