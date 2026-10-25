"""RF protocols, a partial port of the CoffeeScript/Node.js rfcontroljs implementation.

Not all protocols of the original implementation have been ported yet.

https://github.com/pimatic/rfcontroljs/tree/master/src/protocols
"""

from enum import StrEnum
from pathlib import Path

__all__ = [
    f.stem
    for f in Path(__file__).parent.glob("*.py")
    if f.is_file() and not f.name.startswith("_")
]


class RFControlProtocolTypes(StrEnum):
    """The type of protocols."""

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
