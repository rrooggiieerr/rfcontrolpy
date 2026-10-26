"""Shutter4 protocol: shutter motors.

Brands: ROHRMOTOR24.

Commands: ``up``, ``down`` and ``stop``. Unit 0 addresses all units.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["32", ""],  # Header
    ["01", "0"],  # Binary 0
    ["10", "1"],  # Binary 1
    ["03", ""],  # Footer 1
    ["13", ""],  # Footer 2
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "shutter4"
type = RFControlProtocolTypes.SHUTTER
brands = ["ROHRMOTOR24"]
commands = ["up", "down", "stop"]
pulse_lengths = [352, 712, 1476, 5690]
pulse_count = 82

_decode_command_codes = {"001": "up", "011": "down", "101": "stop"}
# Command code and footer, for all units and for a single unit.
_all_command_codes = {"up": "001000", "down": "011001", "stop": "101010"}
_unit_command_codes = {
    "up": ("001111", "03"),
    "down": ("011110", "03"),
    "stop": ("101010", "13"),
}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"3201010110010101100101100101010101100101101010100101011001010101010101011001010113"``.

    Returns:
        Dict with ``id``, ``unit``, ``all`` and ``command``; ``command`` is None for an unknown
        command code,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 36:
        return None

    # Binary is now something like:
    # 000100010010000010011110001000000001000

    # Now we extract the data from that string.
    # | 0001 0001 0010 0000 1001 1110 0010 | 0000    | 0     | 001     | 000             |
    # | ID                                 | Unit    | fixed | Command | inverse command |
    unit = int(binary[28:32], 2)
    return {
        "id": int(binary[0:28], 2),
        "unit": unit,
        "all": unit == 0,
        "command": _decode_command_codes.get(binary[33:36]),
    }


def encode(id: int, command: str, unit: int = 0, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        command: ``up``, ``down`` or ``stop``.
        unit: Unit (channel) code, ignored when ``all`` is True.
        all: Address all units.

    Returns:
        Pulse sequence string.
    """
    if all:
        unit = 0
        command_code = _all_command_codes[command]
        footer = "13"
    else:
        command_code, footer = _unit_command_codes[command]
    encoded = "32"
    encoded += binary2pulses(f"{id:028b}", binary2pulses_mapping)
    encoded += binary2pulses(f"{unit:04b}", binary2pulses_mapping)
    encoded += "01"
    encoded += binary2pulses(command_code, binary2pulses_mapping)
    encoded += footer
    return encoded
