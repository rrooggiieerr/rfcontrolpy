"""Doorbell2 protocol: doorbells, handled as a PIR sensor.

Brands: LIFETEC-MD13187.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "1"],  # Binary 1
    ["10", "0"],  # Binary 0
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "10", "1": "01"}

name = "doorbell2"
type = RFControlProtocolTypes.DOORBELL
brands = ["LIFETEC-MD13187"]
pulse_lengths = [491, 1491, 19270]
pulse_count = 48


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes.

    Returns:
        Dict with ``unit``, ``id`` and ``state``; ``state`` is always True,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 23:
        return None

    # Now we extract the data from that string.
    # | 12 bits | 11 bits |
    # | Unit    | ID      |
    return {
        "unit": int(binary[0:12], 2),
        "id": int(binary[12:23], 2),
        "state": True,
    }


def encode(id: int, unit: int, state: bool = True, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code.
        state: Ignored by this protocol.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """
    encoded = binary2pulses(f"{unit:012b}", binary2pulses_mapping)
    encoded += binary2pulses(f"{id:011b}", binary2pulses_mapping)
    encoded += "02"
    return encoded
