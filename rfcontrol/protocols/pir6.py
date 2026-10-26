"""PIR6 protocol: motion sensor with a 24-bit ID.

Brands: Zanbo (ZABC86-1), Unknown (OSW-1-3 and OTW-1-3).
"""

import logging
from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["10", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping: dict[str, str] = {}

name = "pir6"
type = RFControlProtocolTypes.PIR
brands = ["Zanbo (ZABC86-1)", "Unknown (OSW-1-3 and OTW-1-3)"]
pulse_lengths = [288, 864, 8964]
pulse_count = 50


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01011010010101011010100110010101101001010101101002"``.

    Returns:
        Dict with ``id`` and ``state``; ``state`` is always True,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    binary += "0"

    # Binary is now something like:
    # 001100001110100011000011

    # Now we extract the data from that string.
    # 0011 0000 1110 1000 1100 0011
    # xxII IIII IIII IIII IIII IIII
    # I: 22 bit ID (unsigned, MSB)
    # x: ignored
    # The original implementation reads one bit past the end (bits 2..24),
    # which shifts the ID left by one. A 0 is appended to stay compatible.
    decoded = {
        "id": int(binary[2:25], 2),
        "state": True,
    }
    logger.debug(decoded)
    return decoded
