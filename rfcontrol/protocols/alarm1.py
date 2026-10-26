"""Alarm1 protocol: smoke alarms.

Brands: FA20RF.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["30", ""],  # Header
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["04", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "02"}

name = "alarm1"
type = RFControlProtocolTypes.ALARM
brands = ["FA20RF"]
pulse_lengths = [800, 1423, 2760, 8040, 13000]
pulse_count = 52


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"3002020101010102020201010101020101010102020202010204"``.

    Returns:
        Dict with ``id`` and ``state``; ``state`` is always True,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Binary is now something like:
    # 110000111000010000111101

    # Now we extract the data from that string.
    # | 110000111000010000111101 |
    # | ID                       |
    decoded = {
        "id": int(binary[0:24], 2),
        "state": True,
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, state: bool = True) -> str:
    """Encode a message into a pulse sequence.

    The message is sent three times.

    Args:
        id: Device ID.
        state: True to trigger the alarm. For False the original
            implementation sends ``"0"``, which is kept for compatibility.

    Returns:
        Pulse sequence string.
    """
    if state is False:
        return "0"
    unit = binary2pulses(f"{id:024b}", binary2pulses_mapping)
    encoded = f"30{unit}04" * 3
    logger.debug(encoded)
    return encoded
