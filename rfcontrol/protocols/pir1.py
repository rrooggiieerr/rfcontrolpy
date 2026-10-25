"""PIR1 protocol: motion sensor, brand unknown."""

import logging

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0110", "0"],  # Binary 0
    ["0101", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping: dict[str, str] = {}

name = "pir1"
type = RFControlProtocolTypes.PIR
brands: list[str] = []
pulse_lengths = [358, 1095, 11244]
pulse_count = 50


def decode(pulses):
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01010110010101100110011001100110010101100110011002"``.

    Returns:
        Dict with ``id``, ``unit`` and ``state``; ``state`` is always True,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 101000001000

    # Now we extract the data from that string.
    # | 10100 | 00010 |     0 |    0 |
    # |  Unit |    ID | fixed | State|
    decoded = {
        "unit": int(binary[0:5], 2),
        "id": int(binary[5:10], 2),
        "state": True,
    }
    logger.debug(decoded)
    return decoded
