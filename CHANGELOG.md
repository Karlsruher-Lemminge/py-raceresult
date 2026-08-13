# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-13

First release. The client covers the full go-webapi surface, and every
endpoint path, query parameter and JSON field name has been verified against
the Go reference implementation.

### Added

- Full go-webapi endpoint coverage: 22 further endpoint modules (archives,
  backup, chat, dependencies, file, forwarding, general, group_times,
  information, kiosks, labels, overwrite_values, pictures, rankings,
  rawdata_rules, simple_api, splits, statistics, synchronization, team_scores,
  user_defined_fields, webhooks), bringing the total to 44.
- `PassingPosition` model and `Passing.position` / `.received` / `.utc_time`,
  so GPS and device timestamps can be read and submitted.
- `RawData.passing` — the embedded hardware payload (transponder, decoder,
  RSSI, hits, battery, …) that was previously discarded on every read.
- `RawDataFilter.battery` for filtering raw data by battery voltage.
- `align_timezone()` helper for comparing naive and aware Raceresult datetimes
  the way the Go client does.
- `py.typed` marker so downstream type checkers see the annotations.
- CI (lint, strict mypy, tests on Python 3.9–3.13) and a release workflow.
- Test suite grown from 61 to 125 tests, now covering the HTTP client, auth,
  error handling and the JSON wire format.

### Fixed

- **String list query parameters** (`fields`, `sort`, `groups`, `rowFields`,
  `addFields`, `returnFields`) are JSON-encoded instead of comma-joined,
  matching `go-webapi/urlvalues.go`. Field expressions containing a comma were
  previously split by the server into bogus columns, silently misaligning
  returned rows.
- **Datetimes with sub-second precision** are truncated to whole seconds.
  The server parses datetimes by string length, so anything built from
  `datetime.now()` was rejected outright with "date time format not supported".
- **Zoneless datetimes stay naive** rather than being stamped as UTC. A
  read-modify-write of an event-local time previously shifted it by the
  event's UTC offset.
- **VB zero dates** (`1899-12-30`) parse to `None` for datetimes as they
  already did for dates, so `Voucher.is_valid()` no longer reports every
  never-expiring voucher as invalid.
- **`null` collections** no longer raise `ValidationError` in `Ranking`,
  `EmailTemplate`, `Preview`, `ImportResult` and `UserRight`. A single ranking
  without grouping made `rankings.get()` fail for an entire event.
- **`participants.import_ses()`** sends the parameters the endpoint actually
  takes (`contestFrom`, `contestTo`, `timesFrom`, `timesTo`, `importRawData`);
  raw data and times were silently dropped on every SES import.
- **`team_scores.get_one()`** parses the array response this endpoint returns.
  It is the one `get_one` in the API that does not return a bare object.
- **Binary and text uploads** are no longer labelled `Content-Type:
  application/json`; the reference client sends no Content-Type at all.
- **`Identifier.by_filter`** no longer silently overwrites an explicit
  `filter_expr`, which could delete a different set of participants than
  intended. Conflicts now raise `ValueError`.
- **`history.delete()` / `.count()`** send the `dateForm` parameter spelled the
  way the server expects, so the lower date bound is no longer ignored.
- **Certificate `PageSize` / `PageFormat`** parse leniently and case
  insensitively, falling back to `UserDefined` / `Portrait` like the Go
  parsers, instead of raising on an unknown or empty value.
- Null-tolerant responses for `get_one`/`get` across `customfields`,
  `timingpoints`, `timingpointrules`, `splits`, `rankings`, `contests`,
  `results`, `exporters`, `registrations`, `email_templates` and the
  count-style endpoints in `file`, `archives` and `overwrite_values`.
- `agegroups.generate()` formats its `date` parameter as the endpoint expects
  rather than as RFC3339.
- Removed `KioskAfterSave.flags`, which has no counterpart in the Go model.
- `SaveValueArrayItem.value` accepts any variant type, including dates.

### Changed

- `pytest` and `dotenv` moved out of the runtime dependencies — installing the
  library no longer pulls a test framework into production. The dev extra uses
  the correct `python-dotenv` distribution.
- Project metadata: added `LICENSE`, removed the duplicate license classifier
  that blocks PyPI uploads, and corrected the repository URLs.
- README documents the datetime, field-list and identifier semantics above.

[Unreleased]: https://github.com/Karlsruher-Lemminge/py-raceresult/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Karlsruher-Lemminge/py-raceresult/releases/tag/v0.1.0
