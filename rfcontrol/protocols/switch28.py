"""Switch28 protocol: remotes with on, off and both buttons.

Brands: oh!haus & Co.

No mapping to binary fits all codes, so the pulses themselves are read as bits.
"""

import logging
from typing import Any

from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

name = "switch28"
type = RFControlProtocolTypes.SWITCH
brands = ["oh!haus & Co."]
commands = ["on", "off", "both"]
pulse_lengths = [417, 1287, 13042]
pulse_count = 50

_command_codes = {"on": "01011010", "off": "10100101", "both": "01010101"}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01010110010101100101011001100110011001010101101002"``.

    Returns:
        Dict with ``id``, ``unit`` and ``command``; ``command`` is None for an unknown
        command code,
        or None if the pulses don't match the protocol.
    """
    # Now we extract the data from the pulses.
    # | 0101011001010110010101100 | 110011001100101 | 01011010 | 02     |
    # | ID                        | Unit            | Command  | footer |
    command_code = pulses[40:48]
    try:
        decoded = {
            "id": int(pulses[0:25], 2),
            "unit": int(pulses[25:40], 2),
            "command": next(
                (c for c, code in _command_codes.items() if code == command_code), None
            ),
        }
    except ValueError:
        return None
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, command: str) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code.
        command: ``on``, ``off`` or ``both``.

    Returns:
        Pulse sequence string.
    """
    encoded = f"{id:025b}{unit:015b}{_command_codes[command]}02"
    logger.debug(encoded)
    return encoded
