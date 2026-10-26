"""Awning2 protocol: awning motors.

Brands: Soluna.

Commands: ``in``, ``out`` and ``stop``.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["32", ""],  # Header
    ["01", "0"],  # Binary 0
    ["10", "1"],  # Binary 1
    ["14", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "awning2"
type = RFControlProtocolTypes.AWNING
brands = ["Soluna"]
commands = ["in", "out", "stop"]
pulse_lengths = [359, 718, 1532, 4740, 10048]
pulse_count = 82

_command_codes = {"in": "001000", "out": "011001", "stop": "101010"}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"3210101010011010010101101001010101100101011010100110011010010101100101011001010114"``.

    Returns:
        Dict with ``id`` and ``command``; ``command`` is None for an unknown
        command code, or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 39:
        return None

    # Binary is now something like:
    # 111101100011000010001110101100010001000

    # Now we extract the data from that string.
    # | 1111011000110000100011101011000 | 10    | 001000  |
    # | ID                              | fixed | command |
    command_code = binary[33:39]
    command = next(
        (c for c, code in _command_codes.items() if code == command_code), None
    )
    return {
        "id": int(binary[0:31], 2),
        "command": command,
    }


def encode(id: int, command: str) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        command: ``in``, ``out`` or ``stop``.

    Returns:
        Pulse sequence string.
    """
    id_pulses = binary2pulses(f"{id:031b}", binary2pulses_mapping)
    command_pulses = binary2pulses(_command_codes[command], binary2pulses_mapping)
    return f"32{id_pulses}1001{command_pulses}14"
