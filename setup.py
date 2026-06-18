#!/usr/bin/env python3
"""Setup configuration for pyWebmConverter."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = (
    readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""
)

setup(
    name="pyWebmConverter",
    version="1.1.0",
    author="pyWebmConverter Contributors",
    description="A Python GUI application for converting video files to WebM format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pyWebmConverter",
    license="Unlicense",
    packages=find_packages(exclude=["test", "tests"]),
    python_requires=">=3.8",
    install_requires=[
        "PyQt5>=5.15.0",
        "opencv-python>=4.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12",
            "pytest-github-actions-annotate-failures>=0.1",
            "pylint>=2.0",
        ],
    },
    entry_points={
        "gui_scripts": [
            "pywebmconverter=pyWebmConverter.ffmpeg_gui:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Video :: Conversion",
    ],
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pyWebmConverter/issues",
        "Source": "https://github.com/yourusername/pyWebmConverter",
    },
)
