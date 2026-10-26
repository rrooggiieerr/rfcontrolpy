"""Python port of the pimatic rfcontroljs RF pulse decoder and encoder.

The controller logic and all protocols are ported.
"""

import contextlib

with contextlib.suppress(ModuleNotFoundError):
    from ._version import __version__ as __version__

from . import controller as controller, helpers as helpers
