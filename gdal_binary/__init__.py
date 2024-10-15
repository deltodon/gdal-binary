from __future__ import annotations

from ._core import __doc__, add, subtract
from .version import VERSION as __version__

__all__ = ["__doc__", "__version__", "add", "subtract"]

# The version is now managed by Meson and imported from version.py
# This ensures consistency between Meson, pyproject.toml, and Python code
