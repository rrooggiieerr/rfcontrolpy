"""Switch14 protocol: switches with units 1 to 4.

Brands: UNITEC.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["10", "1"],  # Binary 1
    ["01", "0"],  # Binary 0
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "switch14"
type = RFControlProtocolTypes.SWITCH
brands = ["UNITEC"]
pulse_lengths = [209, 623, 6288]
pulse_count = 50


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01010101010101010101010101010101010101011010010102"``.

    Returns:
        Dict with ``id``, ``unit``, ``all`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Binary is now something like:
    # 000000000000000000001100

    # Now we extract the data from that string.
    # | 00000000000000000000 | 11 | 0            | 0     |
    # | ID                   | U  | inverted All | State |
    # U: 4 - unit, LSB first
    return {
        "id": int(binary[0:20], 2),
        "unit": 4 - int(binary[20:22][::-1], 2),
        "all": binary[22] != "1",
        "state": binary[23] == "1",
    }


def encode(id: int, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code, 1-4.
        state: True for on, False for off.
        all: Address all units.

    Returns:
        Pulse sequence string.
    """
    binary = f"{id:020b}"
    binary += f"{4 - unit:02b}"[::-1]
    binary += "0" if all is True else "1"
    binary += "1" if state else "0"
    return binary2pulses(binary, binary2pulses_mapping) + "02"
