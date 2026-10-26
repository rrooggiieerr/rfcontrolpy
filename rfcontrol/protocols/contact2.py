"""Contact2 protocol: door/window contacts.

Brands: No brand.
"""

import logging
from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["10", "0"],  # Binary 0
    ["01", "1"],  # Binary 1
    ["02", ""],  # Footer
]

name = "contact2"
type = RFControlProtocolTypes.CONTACT
brands = ["No brand"]
pulse_lengths = [295, 886, 9626]
pulse_count = 50


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"10010110100101011010101010011001010101011001010102"``.

    Returns:
        Dict with ``id`` and ``state``; ``state`` is always False,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 20:
        return None

    # Now we extract the data from that string.
    # | 20 bits | 4 bits |
    # | ID      | ?      |
    decoded = {
        "id": int(binary[0:20], 2),
        "state": False,
    }
    logger.debug(decoded)
    return decoded
