"""Switch32 protocol: switches with system code and program code positions.

Brands: Rising Sun RSL366, Conrad RSL366, PROmax.

The system code and program code are a position from 1 to 4, 0 means none.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0110", "0"],  # Binary 0
    ["0101", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "0110", "1": "0101"}

name = "switch32"
type = RFControlProtocolTypes.SWITCH
brands = ["Rising Sun RSL366", "Conrad RSL366", "PROmax"]
pulse_lengths = [440, 1300, 13488]
pulse_count = 50


def _bits_to_position(bits: str) -> int:
    """Return the position (1-4) of the only set bit, LSB first, or 0."""
    number = int(bits[::-1], 2)
    if number > 0 and number & (number - 1) == 0:
        return number.bit_length()
    return 0


def _position_to_bits(position: int, length: int) -> str:
    """Return length bits, LSB first, with only the bit at position set."""
    if position < 1 or position > length:
        return "0" * length
    return "0" * (position - 1) + "1" + "0" * (length - position)


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01010110011001100101011001100110011001100110011002"``.

    Returns:
        Dict with ``id`` (system code), ``unit`` (program code) and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 12:
        return None

    # Binary is now something like:
    # 100010000000

    # Now we extract the data from that string.
    # | 1000        | 1000         | 000 | 0              |
    # | System code | Program code | -   | inverted state |
    decoded = {
        "id": _bits_to_position(binary[0:4]),
        "unit": _bits_to_position(binary[4:8]),
        "state": binary[11] != "1",
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: System code, 1-4.
        unit: Program code, 1-4.
        state: True for on, False for off.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """
    encoded = binary2pulses(_position_to_bits(id, 4), binary2pulses_mapping)
    encoded += binary2pulses(_position_to_bits(unit, 4), binary2pulses_mapping)
    encoded += "011001100110"
    encoded += binary2pulses_mapping["0"] if state else binary2pulses_mapping["1"]
    encoded += "02"
    logger.debug(encoded)
    return encoded
