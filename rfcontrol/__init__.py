"""Python port of the pimatic rfcontroljs RF pulse decoder and encoder.

The controller logic is fully ported, only part of the protocols are.
"""

import contextlib

with contextlib.suppress(ModuleNotFoundError):
    from ._version import __version__ as __version__

from . import controller as controller, helpers as helpers
