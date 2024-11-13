# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Removed
- Drop support for GeoIP and `guess_timezone_by_ip()`.

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
