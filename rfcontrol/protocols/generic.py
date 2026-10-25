"""Generic protocol: homemade sensors sending a typed numeric value."""

import logging
from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0201", "0"],  # Binary 0
    ["0102", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "generic"
type = RFControlProtocolTypes.GENERIC
brands = ["homemade"]
pulse_lengths = [671, 2049, 4346, 10208]
pulse_count = 198


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Pulses could be:
    020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201010203

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201010203"``.

    Returns:
        Dict with ``id``, ``type``, ``positive`` and ``value``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 0000111110100010101000000000000000000000000000001

    # Now we extract the data from that string.
    # | 00001111101000 | 1010 |        1 | 000000000000000000000000000001 |
    # | ID             | Type | Positive | Value                          |
    decoded = {
        "id": int(binary[:14], 2),
        "type": int(binary[14:18], 2),
        "positive": binary[18] == "1",
        "value": int(binary[19:], 2),
    }
    logger.debug(decoded)
    return decoded
