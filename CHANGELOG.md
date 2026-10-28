# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [4.0.0] - 2026-10-28
### Added
- Add `America/Vancouver`, since British Columbia stays on UTC-7 all year from November 2026.
- Add `America/Edmonton` and `America/Winnipeg`, since Alberta and Manitoba stay on UTC-6 and UTC-5 all year from November 2026.

### Changed
- "Central America" uses `America/Guatemala` instead of `Canada/Central`, which follows Manitoba's rules.

### Removed
- Drop the `Canada/Central` entry labeled "Central Time (US & Canada)". `US/Central` covers the US, and `America/Winnipeg` covers Manitoba.

## [3.0.0] - 2024-11-15
### Changed
- Add support for Python 3.11, 3.12 and 3.13.
- Add notice about the package being in maintenance mode only.

### Removed
- Drop support for GeoIP and `guess_timezone_by_ip()`.
- Drop support for Python 3.9 and 3.10.

## [2.2.0] - 2023-03-06
### Added
- Add type hints to all public functions.

### Changed
- Use `zoneinfo` (in the standard library since Python 3.9) instead of `pytz`.
- Improved UTC offsets, to ensure they're always up-to-date (according to `zoneinfo`) and never include DST.

## Removed
- Drop support for Python 3.8.

## [2.1.0] - 2022-07-20
### Added
- Introduce this changelog 🎉

### Changed
- Rename Europe/Kiev to Europe/Kyiv.
- Switch to Poetry for packaging.
- Dependencies: `future` is no longer required, and `geoip2` is now optional.
- Improve CI and dev tooling.

### Removed
- Python 2 is no longer supported.
