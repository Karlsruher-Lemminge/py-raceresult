# py-raceresult

Python API client for Raceresult.

## Installation

```bash
pip install raceresult
```

## Usage

```python
from raceresult import RaceResultAPI

async with RaceResultAPI() as api:
    await api.login(api_key="your-api-key")

    # List events
    events = await api.event_list(2024)

    # Access an event
    event = api.event("event123")

    # Query data
    count = await event.data.count()
    settings = await event.settings.get("EventName", "EventDate")

    # Get registration forms
    reg_names = await event.registrations.names()
    reg = await event.registrations.get(reg_names[0])
```

## Requirements

- Python 3.10+
- httpx
- pydantic
