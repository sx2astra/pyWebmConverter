"""
Entry point for running pyWebmConverter as a module.
Allows: python -m pyWebmConverter
"""

from .ffmpeg_gui import main

if __name__ == "__main__":
    main()
