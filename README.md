# pyWebmConverter

A Python GUI application for converting video files to WebM format using FFmpeg and VP9/AV1 codecs.

## Features

- 🎬 **Multiple Codec Support** - VP9 and AV1 video codecs
- 🔊 **Audio Processing** - Opus audio codec with customizable bitrate
- 🎨 **Video Editing** - Built-in video preview and scaling tools
- ⚙️ **Quality Settings** - Low, Mid, and High quality presets
- 📊 **Bitrate Control** - Manual and automatic bitrate calculation
- 🖥️ **User-Friendly GUI** - Intuitive PyQt5 interface
- 🚀 **Two-Pass Encoding** - Optional VP9 two-pass mode for better quality

## System Requirements

- **Python**: 3.8+
- **FFmpeg**: Must be installed and available in system PATH
- **OS**: Windows, macOS, or Linux

### Installing FFmpeg

**Windows**:
```bash
choco install ffmpeg
# or
scoop install ffmpeg
```

**macOS**:
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install ffmpeg
```

**Linux (Fedora/RHEL)**:
```bash
sudo dnf install ffmpeg
```

## Installation

### Using pip

```bash
pip install pyWebmConverter
```

Then run the application:
```bash
pywebmconverter
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pyWebmConverter.git
cd pyWebmConverter
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

### Running the Application

**Option 1: Via installed command (Recommended after `pip install`)**
```bash
pywebmconverter
```

**Option 2: Via Python module**
```bash
python -m pyWebmConverter
```

**Option 3: Via run script**
- **Windows**: Double-click `run.bat` or `run.bat` from PowerShell
- **Linux/macOS**: `./run.sh`

**Option 4: Direct module import (for development)**
```bash
python -m pyWebmConverter.ffmpeg_gui
```

## Usage

### GUI Application

1. Launch using one of the methods above

2. **Select Input Video**: Click "Browse" to choose your video file

3. **Configure Settings**:
   - **Output Path**: Where to save the converted WebM file
   - **Quality**: Choose Low, Mid, or High quality
   - **Codec**: Select VP9 or AV1
   - **Audio**: Enable/disable audio, choose bitrate
   - **Scale**: Adjust video scaling (original, 50%, 75%)
   - **Target File Size**: Optional - set desired output file size

4. **Advanced Options**:
   - **Two-Pass Encoding**: Enable for VP9 two-pass mode (slower, better quality)
   - **Video Editor**: Click to preview and edit video before conversion

5. **Convert**: Click "Convert" to start the conversion process

### Configuration

Settings are stored in `conf.ini` in the application directory:

```ini
[audio]
on = -c:a libopus
off = -an

[quality]
low = -crf 20 -qmin 50 -qmax 100
mid = -crf 15 -qmin 25 -qmax 75
high = -crf 10 -qmin 0 -qmax 50
```

## Development

### Setting Up Development Environment

```bash
git clone https://github.com/yourusername/pyWebmConverter.git
cd pyWebmConverter
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
pytest --cov=pyWebmConverter  # With coverage
```

### Code Quality

```bash
pylint pyWebmConverter/
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is released into the public domain under the Unlicense. See [LICENSE](LICENSE) for details.

## Support

For issues, feature requests, or questions:
- Open an [Issue](https://github.com/yourusername/pyWebmConverter/issues)
- Check [Discussions](https://github.com/yourusername/pyWebmConverter/discussions)

## Acknowledgments

- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- Uses [FFmpeg](https://ffmpeg.org/) for video conversion
- Uses [OpenCV](https://opencv.org/) for video processing

## Roadmap

- [ ] Command-line interface (CLI)
- [ ] Batch processing
- [ ] Subtitle support
- [ ] Custom FFmpeg parameters
- [ ] Hardware acceleration support
- [ ] AppImage/DMG distribution

---

**Latest Version**: 1.0.0
