"""Doorbell3 protocol: doorbells.

Brands: Smarthome WP515S.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["10", "1"],  # Binary 1
    ["2", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "doorbell3"
type = RFControlProtocolTypes.DOORBELL
brands = ["Smarthome WP515S"]
pulse_lengths = [300, 580, 10224]
pulse_count = 26


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"00101010101010101100110012"``.

    Returns:
        Dict with ``id`` and ``unit``,
        or None if the pulses don't match the protocol.
    """
    # The first pulse is a header and is skipped.
    # We first map the sequences to binary.
    binary = pulses2binary(pulses[1:], pulses2binary_mapping)

    if binary is None or len(binary) < 12:
        return None

    # Now we extract the data from that string.
    # | 4 bits | 8 bits |
    # | ID     | Unit   |
    return {
        "id": int(binary[0:4], 2),
        "unit": int(binary[4:12], 2),
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
    encoded = "0"
    encoded += binary2pulses(f"{id:04b}", binary2pulses_mapping)
    encoded += binary2pulses(f"{unit:08b}", binary2pulses_mapping)
    encoded += "2"
    return encoded
