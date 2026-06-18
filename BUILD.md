# Build & Distribution Guide for pyWebmConverter

## Building the Package

### Option 1: Create a Wheel Distribution

```bash
# Install build tools
pip install build

# Build wheel and source distribution
python -m build

# Output will be in dist/
```

### Option 2: Create a Standalone Executable (Windows/Mac/Linux)

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable using the spec file
pyinstaller pywebmconverter.spec

# Output will be in dist/pyWebmConverter/
```

### Option 3: Install Locally for Development

```bash
pip install -e ".[dev]"
```

## Distribution Checklist

Before releasing, ensure:

- [ ] Version updated in `setup.py` and `__init__.py`
- [ ] `CHANGELOG.md` updated with new version entry
- [ ] All tests pass: `pytest --cov=pyWebmConverter`
- [ ] Code quality checks pass: `pylint pyWebmConverter/`
- [ ] Built and tested the executable
- [ ] Updated README if needed

## Release Process

1. **Update Version**:
   - Edit `setup.py` (version field)
   - Edit `pyWebmConverter/__init__.py` (__version__ field)
   - Update `CHANGELOG.md`

2. **Run Tests**:
   ```bash
   pytest --cov=pyWebmConverter
   pylint pyWebmConverter/
   ```

3. **Build**:
   ```bash
   python -m build  # For wheel
   pyinstaller pywebmconverter.spec  # For executable
   ```

4. **Tag Release**:
   ```bash
   git tag -a v1.0.0 -m "Version 1.0.0"
   git push origin v1.0.0
   ```

5. **Upload to PyPI** (optional):
   ```bash
   pip install twine
   twine upload dist/pyWebmConverter-1.0.0-py3-none-any.whl
   ```

6. **Create GitHub Release**:
   - Go to GitHub Releases
   - Create new release from the tag
   - Upload built files (wheel, executable)
   - Write release notes based on CHANGELOG.md

## Platform-Specific Considerations

### Windows
- Executable built with PyInstaller works on Windows 7+
- FFmpeg must be installed separately or bundled

### macOS
- Use `--onedir` or `--onefile` with PyInstaller
- Consider code signing with `-s` option

### Linux
- Test on multiple distributions
- Consider AppImage or snap packaging
- Use `--hidden-import=cv2` if needed

## Troubleshooting

**PyInstaller issues**:
```bash
# Rebuild with verbose output
pyinstaller pywebmconverter.spec --debug all

# Clean build
pyinstaller --clean pywebmconverter.spec
```

**Module not found**:
- Add to `hiddenimports` in the spec file
- Check `PyInstaller.utils.hooks` for hooks

**FFmpeg not found**:
- Ensure FFmpeg is in PATH
- Consider bundling FFmpeg binary with executable

---

For more information, see:
- PyInstaller docs: https://pyinstaller.org/
- setuptools docs: https://setuptools.pypa.io/
- PyPI: https://pypi.org/project/pyWebmConverter/
