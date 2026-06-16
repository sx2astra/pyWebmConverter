# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-XX-XX

### Added
- Initial public release
- FFmpeg-based WebM video converter with PyQt5 GUI
- Support for VP9 and AV1 video codecs
- Audio processing with Opus support
- Video scaling and quality settings
- Preview window for video editing
- Configuration-based codec settings
- Comprehensive test suite

### Fixed
- Cleaned up project structure for production release
- Removed obsolete dependencies

### Changed
- Migrated to modern Python packaging (setup.py, pyproject.toml)
- Updated documentation for GitHub release

## Development Guidelines

When updating this changelog:
- Add new changes under an `[Unreleased]` section at the top
- Follow the existing format
- Categorize changes: Added, Changed, Deprecated, Removed, Fixed, Security
- Link to comparative view: `[1.0.0]: https://github.com/yourusername/pyWebmConverter/releases/tag/v1.0.0`
