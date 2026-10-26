"""PIR2 protocol: motion sensor.

Brands: Multi Kon Trade B00RTDMC4S.
"""

from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["10", "0"],  # Binary 0
    ["01", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping: dict[str, str] = {}

name = "pir2"
type = RFControlProtocolTypes.PIR
brands = ["Multi Kon Trade B00RTDMC4S"]
pulse_lengths = [451, 1402, 14356]
pulse_count = 50


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01100110010110011001010110100101010101011010010102"``.

    Returns:
        Dict with ``id``, ``unit`` and ``state``; ``state`` is always True,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 10:
        return None

    # Binary is now something like:
    # 101011010111001111110011

    # Now we extract the data from that string.
    # | 10101 | 10101 | 11001111110011 |
    # |  Unit |    ID | fixed          |
    return {
        "unit": int(binary[0:5], 2),
        "id": int(binary[5:10], 2),
        "state": True,
    }
