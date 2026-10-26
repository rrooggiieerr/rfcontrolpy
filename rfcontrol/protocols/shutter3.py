"""Shutter3 protocol: shutter motors.

Brands: Romotec.

Commands: ``up``, ``down``, ``stop`` and ``program``.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["32", ""],  # Header
    ["01", "0"],  # Binary 0
    ["10", "1"],  # Binary 1
    ["04", ""],  # Footer 1
    ["14", ""],  # Footer 2
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "shutter3"
type = RFControlProtocolTypes.SHUTTER
brands = ["Romotec"]
commands = ["up", "down", "stop", "program"]
pulse_lengths = [366, 736, 1600, 5204, 10896]
pulse_count = 82

# The command followed by its inverse.
_command_codes = {
    "up": "001000",
    "down": "011001",
    "stop": "101010",
    "program": "100110",
}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"3210010110010101010110011010011010010110100101011001011001100101101010010110100104"``.

    Returns:
        Dict with ``id``, ``unit`` and ``command``; ``command`` is None for
        an unknown command code, or None if the pulses don't match the
        protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 36:
        return None

    # Binary is now something like:
    # 100100000101101100110001001010011100110

    # Now we extract the data from that string.
    # | 1001 0000 0101 1011 0011 0001 0010 | 1001    | 1     | 100     | 110             |
    # | ID                                 | Unit    | fixed | Command | inverse command |
    command_code = binary[33:36]
    command = next(
        (c for c, code in _command_codes.items() if code[:3] == command_code), None
    )
    return {
        "id": int(binary[0:28], 2),
        "unit": int(binary[28:32], 2),
        "command": command,
    }


def encode(id: int, unit: int, command: str) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit (channel) code.
        command: ``up``, ``down``, ``stop`` or ``program``.

    Returns:
        Pulse sequence string.
    """
    id_pulses = binary2pulses(f"{id:028b}", binary2pulses_mapping)
    unit_pulses = binary2pulses(f"{unit:04b}", binary2pulses_mapping)
    command_pulses = binary2pulses(_command_codes[command], binary2pulses_mapping)
    if command != "program":
        encoded = f"32{id_pulses}{unit_pulses}01{command_pulses}14"
    else:
        encoded = f"32{id_pulses}{unit_pulses}10{command_pulses}04"
    return encoded
