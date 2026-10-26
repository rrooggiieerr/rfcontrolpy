"""PIR5 protocol: motion sensors.

Brands: Trust SmartHome, COCO Technologies, KlikAanKlikUit.

Same frame as switch1. Messages can be 132 or 148 pulses long.
"""

import logging
from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["02", ""],  # Header
    ["0100", "1"],  # Binary 1
    ["0001", "0"],  # Binary 0
    ["03", ""],  # Footer
]

name = "pir5"
type = RFControlProtocolTypes.PIR
brands = ["Trust SmartHome", "COCO Technologies", "KlikAanKlikUit"]
pulse_lengths = [268, 1282, 2632, 10168]
pulse_counts = [132, 148]


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"0200010001010001000001000100010100010000010100010001000100010000010100000100010001010001000001010001000001000101000100000100010100000101000001000103"``.

    Returns:
        Dict with ``id``, ``all``, ``state`` and ``unit``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 32:
        return None

    # Binary is now something like:
    # 001100011011111010001101100110010100

    # Now we extract the data from that string.
    # | 00110001101111101000110110 |   0 |     1 | 1001 | [0100] |
    # | ID                         | All | State | Unit | ?      |
    decoded = {
        "id": int(binary[0:26], 2),
        "all": binary[26] == "1",
        "state": binary[27] == "1",
        "unit": int(binary[28:32], 2),
    }
    logger.debug(decoded)
    return decoded
