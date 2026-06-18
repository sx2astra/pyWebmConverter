# Running pyWebmConverter

## Quick Start

### Windows
**Easiest:**
```powershell
# Double-click run.bat
# OR from PowerShell:
.\run.bat
```

### Linux/macOS
```bash
# Make executable
chmod +x run.sh

# Run
./run.sh
```

### Command Line (All Platforms)
```bash
python -m pyWebmConverter
```

---

## Installation & Running

### Option 1: Installed Package (Recommended)

After installing from PyPI or locally:

```bash
# Install
pip install pyWebmConverter

# Run
pywebmconverter
```

This is the simplest method after installation.

### Option 2: Development Installation

If you want to work on the source code:

```bash
# Clone/enter repository
cd pyWebmConverter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run via command
pywebmconverter

# Or via module
python -m pyWebmConverter
```

### Option 3: Direct Module Execution

Without installing, if you have the source:

```bash
cd pyWebmConverter
python -m pyWebmConverter.ffmpeg_gui
```

**Note:** Relative imports require module execution, not direct script execution.

---

## Common Issues

### ❌ `ImportError: attempted relative import with no known parent package`

**Problem:** Running directly with `python pyWebmConverter/ffmpeg_gui.py`

**Solution:** Use module execution instead:
```bash
python -m pyWebmConverter
# or
python -m pyWebmConverter.ffmpeg_gui
```

### ❌ `ModuleNotFoundError: No module named 'pyWebmConverter'`

**Problem:** Trying to run before installing or from wrong directory

**Solution:** 
```bash
# First, install the package
pip install -e .

# Then run
pywebmconverter
```

Or navigate to the parent directory of `pyWebmConverter/`:
```bash
cd /path/to/pyWebmConverter
python -m pyWebmConverter
```

### ❌ `ffmpeg: command not found`

**Problem:** FFmpeg is not installed or not in PATH

**Solution:** Install FFmpeg for your platform:

**Windows:**
```powershell
# Using Chocolatey
choco install ffmpeg

# Or using Scoop
scoop install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install ffmpeg
```

---

## Running Headless (No GUI)

For batch processing or automation, you can import the package:

```python
from pyWebmConverter.command_builder import build_encoding_commands
from pyWebmConverter.audio_processor import adjust_audio_bitrate

# Use the functions programmatically
```

---

## Development & Testing

### Run Tests
```bash
python -m pytest test/ -v
```

### Code Quality Checks
```bash
pylint pyWebmConverter/
```

### Build Distribution
```bash
# Wheel distribution
python -m build

# PyInstaller executable
pyinstaller pywebmconverter.spec
```

---

## Entry Points

The package provides multiple entry points:

| Method | Command | Requirements |
|--------|---------|--------------|
| GUI command | `pywebmconverter` | `pip install -e .` (dev) or `pip install pyWebmConverter` (release) |
| Module execution | `python -m pyWebmConverter` | Package in PYTHONPATH or `pip install -e .` |
| Module execution | `python -m pyWebmConverter.ffmpeg_gui` | Package in PYTHONPATH or `pip install -e .` |
| Run script (Windows) | `run.bat` | Python in PATH, package installed |
| Run script (Unix) | `./run.sh` | Python in PATH, package installed |
| Direct import | Python code | Package in PYTHONPATH |

---

## Troubleshooting

### GUI won't start

1. Check Python version: `python --version` (needs 3.8+)
2. Check FFmpeg: `ffmpeg -version`
3. Reinstall package: `pip install --force-reinstall -e .`
4. Check for GUI library: `python -c "from PyQt5 import QtWidgets"`

### Slow startup

- GUI takes a moment to load - this is normal with PyQt5
- Video preview may be slow depending on video codec

### Memory usage

- Large video files may use significant memory during preview
- Audio adjustment process iterates multiple times - this is expected

---

For more help, see [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue on GitHub.
