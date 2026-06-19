# py-raceresult

Async Python client for the [Raceresult](https://www.raceresult.com/) event management API. This is unofficial Python implementation of [Raceresult go-webapi](https://github.com/raceresult/go-webapi) Vibe Coded with Claude Code. **Use at your own risk.**

You can receive an Raceresult API Key in your Account.

## Features

- **Async-first design** using httpx for non-blocking I/O
- **Full API coverage** with 23 endpoint modules and 100+ methods
- **Type-safe** with Pydantic v2 models and full type annotations
- **Multiple auth methods** including API key, username/password, and 2FA
- **Custom type handling** for Raceresult date/time/decimal formats
- **Certificate generation** — create individual or bulk PDF/JPG certificates (Urkunden)
- **Portal settings** — read and write all my.raceresult.com page configuration via the `Portal` prefix

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
| **Certificates** | `certificates`, `certificate_sets` | Certificate (Urkunden) templates and bulk PDF generation |
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

All API responses are validated using Pydantic models. Key models include:

- `Participant` - Participant data with all standard fields
- `Contest`, `AgeGroup`, `BibRange` - Event configuration
- `TimingPoint`, `TimingPointRule`, `RawData` - Timing system
- `Registration`, `Step`, `Element`, `FormField` - Registration forms
- `Voucher`, `EntryFee` - Payment and pricing
- `EmailTemplate` - Communication templates
- `Certificate`, `Element`, `Zone` - Certificate templates with layout elements
- `CertificateSet` - Certificate set rules (filter, sort, bulk generation)

Import models from `raceresult.models`:

```python
from raceresult.models import Participant, Contest, AgeGroup
```

## Requirements

- Python 3.9+
- httpx >= 0.25.0
- pydantic >= 2.0.0

