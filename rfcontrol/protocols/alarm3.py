"""Alarm3 protocol: smoke alarms (provisional).

Brands: Smartwares RM174RF (provisional).

The original implementation's encoder never worked (it returns the literal
string ``"{unit}000102"``), so this protocol only supports decoding.
"""

import logging
from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["10", "10"],  # Binary 0
    ["01", "01"],  # Binary 1
    ["02", ""],  # Footer
    ["12", ""],  # Footer
    ["00", ""],  # Footer
    ["11", ""],  # Footer
]

name = "alarm3"
type = RFControlProtocolTypes.ALARM
brands = ["Smartwares RM174RF (provisional)"]
pulse_lengths = [472, 1236, 11688]
pulse_count = 54


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"100101010101100101011010010101101010101001011010000102"``.

    Returns:
        Dict with ``id`` and ``state``; ``state`` is always True,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary. Every pulse pair maps to itself.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Now we extract the data from that string.
    # The ID is the first 24 bits.
    decoded = {
        "id": int(binary[0:24], 2),
        "state": True,
    }
    logger.debug(decoded)
    return decoded
