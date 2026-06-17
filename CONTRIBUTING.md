# Contributing to pyWebmConverter

Thank you for your interest in contributing to pyWebmConverter! Here are some guidelines to help you get started.

## Project Structure

Understanding the codebase will help you contribute effectively:

```
pyWebmConverter/
├── __init__.py           # Package metadata (version, exports)
├── __main__.py           # CLI entry point
├── ffmpeg_gui.py         # Main PyQt5 GUI application
├── video_editor.py       # Video trimming, rotation, scaling dialog
├── ffmpeg_worker.py      # Worker thread for non-blocking encoding
├── command_builder.py    # FFmpeg command construction and optimization
├── audio_processor.py    # Audio bitrate adjustment to hit target file size
└── constants.py          # Configuration constants and thresholds
```

### Key Components

- **ffmpeg_gui.py**: Main GUI window with input fields, encoding controls, and logging
- **video_editor.py**: OpenCV-based dialog for video preview and frame-by-frame editing
- **command_builder.py**: Codec selection, adaptive scaling, FFmpeg parameter building
- **audio_processor.py**: Iterative audio bitrate adjustment to hit exact target size
- **constants.py**: Centralized configuration (thresholds, quality parameters)

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/pyWebmConverter.git
   cd pyWebmConverter
   ```

3. **Create a development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## Development Setup

Install the package in editable mode with development dependencies:
```bash
pip install -e ".[dev]"
```

## Running Tests

Run the test suite:
```bash
pytest
pytest --cov=pyWebmConverter  # With coverage report
```

## Code Quality

We use pylint for code quality checks:
```bash
pylint pyWebmConverter/
```

## Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with clear commit messages
3. Push to your fork and create a **Pull Request**

### Guidelines for Changes

- **Constants**: Update [constants.py](pyWebmConverter/constants.py) for magic numbers and thresholds
- **Commands**: Modify [command_builder.py](pyWebmConverter/command_builder.py) for FFmpeg parameters
- **Audio**: Edit [audio_processor.py](pyWebmConverter/audio_processor.py) for audio adjustment logic
- **UI**: Update [ffmpeg_gui.py](pyWebmConverter/ffmpeg_gui.py) for GUI changes
- **Tests**: Add tests in [test/](test/) directory for new functionality

## Pull Request Process

- Ensure all tests pass: `pytest`
- Ensure code passes linting: `pylint pyWebmConverter/`
- Update documentation if needed:
  - Update [README.md](README.md) for user-facing changes
  - Update [CHANGELOG.md](CHANGELOG.md) with "Unreleased" section
  - Update [RUNNING.md](RUNNING.md) if installation/execution changes
- Add a clear description of your changes in the PR

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep lines under 100 characters
- Use type hints in function signatures

## Reporting Issues

If you find a bug:
1. Check if it's already reported in **Issues**
2. Provide a clear title and description
3. Include steps to reproduce the issue
4. Mention your Python version, OS, and FFmpeg version
5. Include relevant log output or screenshots

## Questions?

Feel free to open an issue with the `question` label if you have any questions.

## Performance Considerations

When contributing changes that affect encoding:
- Test with various file sizes and bitrates
- Verify audio adjustment converges properly
- Ensure quality parameters are optimized per codec
- Document any threshold or constant changes

Thank you for contributing!
