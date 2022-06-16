"""Module imported functionality required for correct localization."""

import gettext
import os

translation = gettext.translation("bot", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "localization"), fallback=True)
_, ngettext = translation.gettext, translation.ngettext
