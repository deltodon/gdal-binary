from __future__ import annotations

from ._core import __doc__, __version__, add, subtract

__all__ = ["__doc__", "__version__", "add", "subtract"]


# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
#   X.Y.0     # For first release after an increment in Y
#   X.Y.Z     # For bugfix releases
#
# Admissible pre-release markers:
#   X.Y.ZaN   # Alpha release
#   X.Y.ZbN   # Beta release
#   X.Y.ZrcN  # Release Candidate
#   X.Y.Z     # Final release
#
# Admissible development markers:
#   X.Y.Z.devN  # Developmental release
#
__version__ = "0.2.0.dev1"
