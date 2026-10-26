"""Switch15 protocol: switches with units 1 to 4.

Brands: Daycom Switches.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["10", "1"],  # Binary 1
    ["01", "0"],  # Binary 0
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "switch15"
type = RFControlProtocolTypes.SWITCH
brands = ["Daycom Switches"]
pulse_lengths = [300, 914, 9624]
pulse_count = 50

# Unit code (LSB first) for each unit; any other code addresses all units.
_unit_codes = {1: 7, 2: 6, 3: 5, 4: 3}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01101001011001100110010110011010101001011010101002"``.

    Returns:
        Dict with ``id``, ``unit``, ``state`` and ``all``; for all units ``unit`` is 0,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Binary is now something like:
    # 011001010100101111001111

    # Now we extract the data from that string.
    # | 01100101010010111100 | 1     | 111       |
    # | ID                   | State | Unit code |
    # The unit code is LSB first. For all units the state is inverted.
    unit_code = int(binary[21:24][::-1], 2)
    state = binary[20] == "1"
    unit = next((u for u, code in _unit_codes.items() if code == unit_code), 0)
    all_units = unit == 0
    if all_units:
        state = not state
    decoded = {
        "id": int(binary[0:20], 2),
        "unit": unit,
        "state": state,
        "all": all_units,
    }
    logger.debug(decoded)
    return decoded


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
    if all:
        unit_code = 0
        state = not state
    else:
        unit_code = _unit_codes.get(unit, 0)
    binary = f"{id:020b}"
    binary += "1" if state else "0"
    binary += f"{unit_code:03b}"[::-1]
    encoded = binary2pulses(binary, binary2pulses_mapping) + "02"
    logger.debug(encoded)
    return encoded
