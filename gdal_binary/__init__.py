from __future__ import annotations

from ._gdal import *
from .version import VERSION as __version__

# The version is managed by Meson and imported from version.py
# This ensures consistency between Meson, pyproject.toml, and Python code

# You might want to explicitly import and expose specific GDAL functions here
# For example:
# from ._gdal import gdal_version, Dataset, Driver

__all__ = ['__version__']  # Add other explicitly imported names to this list if needed

# Optionally, you can add a convenience function to get the GDAL version
def get_gdal_version():
    return gdal_version()  # Make sure this function exists in the GDAL Python bindings
