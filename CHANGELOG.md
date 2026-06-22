# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] "WhimsicalWispa" - 2026-06-22

### Added
- Resolution-based scaling options (480p, 720p, 1080p) in addition to percentage-based scaling
- Frame-by-frame navigation in video editor (← Frame / Frame → buttons)
- Set Start / Set End buttons in video editor to mark trim points at the current frame
- Output filename auto-populated from input filename when a file is selected
- Post-conversion summary showing final file size vs target with a colour indicator
- "Open Output Folder" button appears after a successful conversion
- Output filename written to WebM container metadata as the title tag

### Changed

- Audio bitrate adjustment replaced linear ±4 kbps search with binary search (8–128 kbps range), converging in ~7 iterations instead of up to 80
- Audio bitrate ceiling lowered from 320 kbps to 128 kbps (Opus at 128 kbps is perceptually transparent, higher rates wasted video budget)
- VBV buffer size increased to 2× maxrate for correct VP9 rate control behaviour
- Safety margins applied to the bit budget (2–6% depending on file size) to prevent container overhead overshoot
- `AUDIO_DEFAULT_BITRATE` aligned to 96 kbps to match the audio binary search starting point, eliminating a systematic overshoot
- Output filename now trimmed of whitespace and auto-suffixed with `.webm` if no extension is provided

### Removed

- Redundant Scale control from the video editor dialog (scale is controlled from the main UI)

### Fixed

- "Could not determine video dimensions" error after resolution scaling was introduced — switched from fragile `ffmpeg -i` + regex parsing to `ffprobe` with structured CSV output
- Git folder casing corrected from `pyWebMConverter` to `pyWebmConverter`


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
