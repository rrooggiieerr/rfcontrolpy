"""PIR4 protocol: SelectPlus doorbell, handled as a PIR sensor."""

import logging
from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0", "0"],  # Binary 0
    ["1", "1"],  # Binary 1
    ["2", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping: dict[str, str] = {}

name = "pir4"
type = RFControlProtocolTypes.PIR
brands = ["SelectPlus Doorbell"]
pulse_lengths = [371, 1081, 5803]
pulse_count = 36


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"110100110101001101010011001010101012"``.

    Returns:
        Dict with ``id``, ``unit`` and ``state``; ``state`` is always True,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 11010011010100110101001100101010101

    # Now we extract the data from that string.
    decoded = {
        "id": int(binary[0:16], 2),
        "unit": int(binary[16:32], 2),
        "state": True,
    }
    logger.debug(decoded)
    return decoded
