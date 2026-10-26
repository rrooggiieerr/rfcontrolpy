"""Switch7 protocol: 3-bit unit / 3-bit ID switches.

Brands: eHome.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0110", "0"],  # Binary 0
    ["1010", "0"],  # State  0
    ["0101", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {
    "0": "0110",
    "1": "0101",
}

name = "switch7"
type = RFControlProtocolTypes.SWITCH
brands = ["eHome"]
pulse_lengths = [307, 944, 9712]
pulse_count = 50


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01010101010101100110011001100110011001100110011002"``.

    Returns:
        Dict with ``id``, ``unit`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 7:
        return None

    # Binary is now something like:
    # 111000000000

    # Now we extract the data from that string.
    # |     1 |  110 |  000 | 00000 |
    # | State | Unit |   ID | fixed |
    # Unit and ID are LSB first.
    decoded = {
        "id": int(binary[4:7][::-1], 2),
        "unit": int(binary[1:4][::-1], 2),
        "state": binary[0] == "1",
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code.
        state: True for on, False for off.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """
    encoded = "0101" if state else "1010"
    encoded += binary2pulses(f"{unit:03b}"[::-1], binary2pulses_mapping)
    encoded += binary2pulses(f"{id:03b}"[::-1], binary2pulses_mapping)
    encoded += "0110011001100110011002"
    logger.debug(encoded)
    return encoded
