# pylint: disable=missing-module-docstring

try:
    from ._version import __version__
except ModuleNotFoundError:
    pass

from rfcontrol import controller, helpers
