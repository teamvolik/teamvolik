"""Init module file."""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from . import _version

__version__ = _version.get_versions()["version"]
