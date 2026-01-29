# py-raceresult

Async Python client for the [Raceresult](https://www.raceresult.com/) event management API. This is unofficial Python implementation of [Raceresult go-webapi](https://github.com/raceresult/go-webapi) Vibe Coded with Claude Code. **Use at your own risk.**

You can receive an Raceresult API Key in your Account.

## Features

- **Async-first design** using httpx for non-blocking I/O
- **Full API coverage** with 21 endpoint modules and 100+ methods
- **Type-safe** with Pydantic v2 models and full type annotations
- **Multiple auth methods** including API key, username/password, and 2FA
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

Once logged in, access event-specific endpoints via `api.event(event_id)`:

| Category | Endpoints | Description |
|----------|-----------|-------------|
| **Core Data** | `data`, `participants`, `settings` | Query, filter, and manage participant data |
| **Event Config** | `contests`, `agegroups`, `bibranges`, `customfields`, `entryfees` | Event structure and pricing |
| **Timing** | `times`, `rawdata`, `timingpoints`, `timingpointrules`, `chipfile` | Timing device data and configuration |
| **Results** | `results`, `lists`, `exporters` | Result definitions and output generation |
| **Registration** | `registrations`, `vouchers` | Registration forms and discount codes |
| **Communication** | `email_templates` | Email and SMS templates |
| **Audit** | `history` | Change tracking |

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

All API responses are validated using Pydantic models. Key models include:

- `Participant` - Participant data with all standard fields
- `Contest`, `AgeGroup`, `BibRange` - Event configuration
- `TimingPoint`, `TimingPointRule`, `RawData` - Timing system
- `Registration`, `Step`, `Element`, `FormField` - Registration forms
- `Voucher`, `EntryFee` - Payment and pricing
- `EmailTemplate` - Communication templates

Import models from `raceresult.models`:

```python
from raceresult.models import Participant, Contest, AgeGroup
```

## Requirements

- Python 3.9+
- httpx >= 0.25.0
- pydantic >= 2.0.0

