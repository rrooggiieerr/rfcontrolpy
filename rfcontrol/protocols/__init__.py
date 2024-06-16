"""
RF Protocols implement (part of) the protocols of the original CoffeeScript/nodejs implementation
https://github.com/pimatic/rfcontroljs/tree/master/src/protocols
"""

import glob
from enum import StrEnum
from os.path import basename, dirname, isfile, join

__all__ = [
    basename(f)[:-3]
    for f in glob.glob(join(dirname(__file__), "*.py"))
    if isfile(f) and not basename(f).startswith("_")
]


class RFControlProtocolTypes(StrEnum):
    """
    The type of protocols.
    """

    ALARM = "alarm"
    AWNING = "awning"
    CONTACT = "contact"
    DIMMER = "dimmer"
    DOORBELL = "doorbell"
    GENERIC = "generic"
    LED = "led"
    PIR = "pir"
    ROLLING = "rolling"
    SHUTTER = "shutter"
    SWITCH = "switch"
    WEATHER = "weather"
