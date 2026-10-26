"""Switch17 protocol: self-learning switches.

Brands: Intertek 22541673 (e.g. Bauhaus).
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["02", ""],  # Header
    ["0100", "1"],  # Binary 1
    ["0001", "0"],  # Binary 0
    ["03", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "0001", "1": "0100"}

name = "switch17"
type = RFControlProtocolTypes.SWITCH
brands = ["Intertek 22541673 (e.g. Bauhaus)"]
# The original implementation lists the pulse lengths unsorted (260, 2680, 1275,
# 10550), so it never matches sorted receptions. Here they're sorted, with the
# pulse indexes 1 and 2 swapped accordingly; the signal is the same.
pulse_lengths = [260, 1275, 2680, 10550]
pulse_count = 132


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"020100010001000001000100010100010001000100010000010100000101000100010001000100010001000100000100010100000100010100010001000001010003"``.

    Returns:
        Dict with ``id``, ``all``, ``state`` and ``unit``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 32:
        return None

    # Binary is now something like:
    # 11100011111010111111110010011101

    # Now we extract the data from that string.
    # | 11100011111010111111110010 |   0 |     1 | 1101 |
    # | ID                         | All | State | Unit |
    return {
        "id": int(binary[0:26], 2),
        "all": binary[26] == "1",
        "state": binary[27] == "1",
        "unit": int(binary[28:32], 2),
    }


def encode(id: int, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code.
        state: True for on, False for off.
        all: Address all units.

    Returns:
        Pulse sequence string.
    """
    encoded = "02"
    encoded += binary2pulses(f"{id:026b}", binary2pulses_mapping)
    encoded += binary2pulses_mapping["1"] if all else binary2pulses_mapping["0"]
    encoded += binary2pulses_mapping["1"] if state else binary2pulses_mapping["0"]
    encoded += binary2pulses(f"{unit:04b}", binary2pulses_mapping)
    encoded += "03"
    return encoded
