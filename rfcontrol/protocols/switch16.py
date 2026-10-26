"""Switch16 protocol: tri-state switches with letter IDs.

Brands: Everflourish.
"""

import logging
from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0101", "0"],  # Binary 0
    ["1010", "1"],  # Binary 1
    ["0110", "2"],  # Binary tri-state
    ["02", ""],  # Footer
]

name = "switch16"
type = RFControlProtocolTypes.SWITCH
brands = ["Everflourish"]
pulse_lengths = [330, 1000, 10500]
pulse_count = 50


def _count_until_zero(binary: str, start: int, end: int) -> int:
    """Return 1 plus the number of non-zero symbols from start, up to end."""
    count = 1
    i = start
    while i < end:
        if binary[i] == "0":
            break
        i += 1
        count += 1
    return count


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01100101011001100110011001010110011001100110010102"``.

    Returns:
        Dict with ``id`` (a letter), ``unit`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 12:
        return None

    # Binary is now something like:
    # 202222022220

    # Now we extract the data from that string.
    # | 2022 | 220  | 2222       | 0     |
    # | ID   | Unit | don't care | State |
    # The position of the 0 in the ID gives the letter (A is first);
    # the unit is counted the same way.
    decoded = {
        "id": chr(64 + _count_until_zero(binary, 0, 3)),
        "unit": _count_until_zero(binary, 4, 6),
        "state": binary[11] == "1",
    }
    logger.debug(decoded)
    return decoded


def encode(id: str, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID, a letter from A to D.
        unit: Unit code.
        state: True for on, False for off.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """
    id_parts = ["0110", "0110", "0110", "0110"]
    id_parts[min(ord(id[0]) - 65, 3)] = "0101"
    unit_pulses = "".join("0101" if bit == "1" else "0110" for bit in f"{unit:03b}")
    encoded = "".join(id_parts)
    encoded += unit_pulses
    encoded += "0110011001100110"
    encoded += "1010" if state else "0101"
    encoded += "02"
    logger.debug(encoded)
    return encoded
