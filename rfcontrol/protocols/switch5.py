"""Switch5 protocol: 20-bit ID switches.

Brands: Eurodomest.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["10", "0"],  # Binary 0
    ["01", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {
    "0": "10",
    "1": "01",
}

name = "switch5"
type = RFControlProtocolTypes.SWITCH
brands = ["Eurodomest"]
pulse_lengths = [295, 886, 9626]
pulse_count = 50


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"10010101101010010110010110101001010101011010101002"``.

    Returns:
        Dict with ``id``, ``unit``, ``state`` and ``all``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Binary is now something like:
    # 011100011011000111110000

    # Now we extract the data from that string.
    # | 01110001101100011111 | 000      | 0              |
    # | ID                   | UnitCode | inverted state |
    unit_code = int(binary[20:23], 2)
    unit = (1, 2, 3, 0, 4, 0, 0, 0)[unit_code]
    all_units = unit_code not in [0, 1, 2, 4]
    state = (binary[23] == "1") if all_units else (binary[23] == "0")

    return {
        "id": int(binary[0:20], 2),
        "unit": unit,
        "all": all_units,
        "state": state,
    }


def encode(id: int, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code, 1-4.
        state: True for on, False for off.
        all: Address all units in the group.

    Returns:
        Pulse sequence string.
    """
    unit_code: int | None
    encoded = binary2pulses(f"{id:020b}", binary2pulses_mapping)
    if all:
        unit_code = 6 if state else 7
        state = not state
    else:
        unit_code = (None, 0, 1, 2, 4)[unit]
    encoded += binary2pulses(f"{unit_code:03b}", binary2pulses_mapping)
    encoded += binary2pulses_mapping["0"] if state else binary2pulses_mapping["1"]
    encoded += "02"
    return encoded
