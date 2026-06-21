# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased [1.2.0] "WhisicalWispa" - 2026-XX-XX

### Added
- Resolution-based scaling options (480p, 720p, 1080p) in addition to percentage-based scaling
- Auto-detection of video dimensions for accurate resolution scaling


## [1.1.0] "XenialXuixo" - 2026-06-17

### Added
- Full PyQt5 graphical user interface
- Video editor dialog for preview, trimming, rotation, and scaling
- FFmpeg command builder with codec and quality optimization
- Audio bitrate adjustment with iterative refinement
- Support for both VP9 and AV1 video codecs
- Adaptive video scaling based on bitrate constraints
- Two-pass encoding option for VP9
- Configuration constants for centralized parameter management

### Changed
- Replaced conf.ini configuration with constants-based settings
- Refactored encoding pipeline into modular components
- Enhanced documentation with encoding logic and feature descriptions

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
