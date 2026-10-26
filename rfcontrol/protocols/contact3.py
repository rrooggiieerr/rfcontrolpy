"""Contact3 protocol: door/window contacts.

Brands: Home Easy HE852.
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

name = "contact3"
type = RFControlProtocolTypes.CONTACT
brands = ["Home Easy HE852"]
pulse_lengths = [310, 950, 9644]
pulse_count = 50


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes.

    Returns:
        Dict with ``id`` and ``state``; ``state`` is True when the contact is closed,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Now we extract the data from that string.
    # | 20 bits | 3 bits | 1 bit |
    # | ID      | ?      | State |
    return {
        "id": int(binary[0:20], 2),
        "state": binary[23] == "1",
    }
