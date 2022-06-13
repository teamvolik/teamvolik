"""Init module file"""
import os
import sys

sys.path.append(os.path.join(os.getcwd(), "src"))

from . import _version

__version__ = _version.get_versions()["version"]
