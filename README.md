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
   - **Output Path**: Directory where the converted WebM will be saved
   - **Output Filename**: Name for the output file (without extension)
   - **Scale**: Manual scaling (Original, 75%, 50%) - auto-scaling also applies based on bitrate
   - **Target File Size**: Desired output file size in MB
   - **Override Target Size** (optional): Use a different size for bitrate calculation if overshooting
   - **Audio**: Enable audio with Opus codec or disable for video-only
   - **Codec**: VP9 (default, faster) or AV1 (better compression, slower)
   - **2-Pass Encoding**: Enable for better quality (VP9 only, slower)

4. **Edit Video** (Optional): Click to trim, rotate (0°/90°/180°/270°), or scale before conversion

5. **Convert**: Click "Start Conversion" to begin encoding

The application will:
- Calculate optimal bitrate based on your target file size and video duration
- Auto-scale video if bitrate is very low
- Adjust audio bitrate iteratively to hit the exact target size
- Display real-time encoding progress in the log

### Advanced Features

#### Video Editor (Trim, Rotate, Scale)
Click **"Edit Video"** to open the video editor dialog where you can:
- **Preview** the video with frame-by-frame scrubbing
- **Trim**: Set start time and duration
- **Rotate**: Apply 0°, 90°, 180°, or 270° rotation
- **Scale**: Adjust video scaling (0.2x to 1.0x)

#### Audio Adjustment
The application automatically adjusts audio bitrate to hit your target file size:
- Extracts audio from the original video
- Iteratively re-encodes with different bitrates (up to 25 attempts, 4 kbps steps)
- Converges to within 5KB of your target size
- Uses Opus codec for efficient audio compression

#### Override Target Size for Bitrate
- **Use Case**: If the application overshoots your target, use this field to calculate bitrate from a smaller value
- **Example**: Target 4 MB but getting 4.5 MB? Set override to 3.5 MB
- Leave blank to use the target file size for bitrate calculation

#### Codec Selection
- **AV1**: Selected for bitrates ≥ 800 kbps (better compression, slower encoding)
- **VP9**: Selected for bitrates < 800 kbps (faster encoding, still excellent quality)
- **Manual Override**: Check "Allow AV1 codec" to enable AV1 for all videos

#### Encoding Modes
- **1-Pass** (Default): Faster, good quality for most use cases
- **2-Pass**: Slower but better quality; analyzes video twice for optimal compression

### Quality & Performance

The application uses these bitrate thresholds for adaptive scaling:

| Bitrate Range | Auto-Scale | Codec | Use Case |
|---|---|---|---|
| < 150 kbps | 0.25x | VP9 | Tiny files |
| 150-250 kbps | 0.35x | VP9 | Very low bitrate |
| 250-350 kbps | 0.5x | VP9 | Low bitrate |
| 350-550 kbps | 0.75x | VP9 | Moderate bitrate |
| > 800 kbps | 1.0x | AV1 | High bitrate |

### Configuration

All settings are defined in [constants.py](pyWebmConverter/constants.py):
- Audio codec and bitrate defaults
- Bitrate thresholds for codec selection
- Quality parameters per codec
- Threading and performance tuning

## How It Works

### Encoding Pipeline

1. **Input Analysis**
   - Extracts video duration and frame rate
   - Calculates optimal video bitrate from target file size
   - Reserves bitrate for audio (if enabled)

2. **Codec & Quality Selection**
   - AV1 selected for high bitrates (≥ 800 kbps) for better compression
   - VP9 selected for lower bitrates for faster encoding
   - Quality parameters (cpu-used, tile settings) optimized per codec

3. **Adaptive Scaling**
   - Ultra-low bitrates (< 150 kbps) trigger aggressive 0.25x scaling
   - Very low bitrates scale to 0.35x, 0.5x, etc.
   - Adequate bitrates keep original resolution

4. **Video Encoding**
   - VP9: Optional 2-pass mode (cpu-used=0 for 2-pass, 6 for 1-pass)
   - AV1: 1-pass or 2-pass with adaptive cpu-used levels
   - 10-bit color depth (yuv420p10le) for better quality

5. **Audio Processing**
   - Extracts Opus audio from original video
   - Iteratively adjusts bitrate (0.5 kbps steps, max 25 iterations)
   - Re-muxes with final video to hit target size within 5KB tolerance

### File Size Targeting

The application works backward from your target file size:
- Size = Duration × Total Bitrate
- Bitrate = (Target MB × 8,388,608 bits) ÷ Duration
- Video Bitrate = Total Bitrate - Audio Bitrate (if enabled)

If audio adjustment overshoots, use the "Override Target Size" feature to calculate bitrate from a smaller value.

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

**Latest Version**: 1.1.0 "XenialXuixo"
