"""Shutter5 protocol: shutter motors.

Brands: eSmart.

Commands: ``up``, ``down`` and ``stop``.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["02", "0"],  # Binary 0
    ["21", "1"],  # Binary 1
    ["03", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "02", "1": "21"}

name = "shutter5"
type = RFControlProtocolTypes.SHUTTER
brands = ["eSmart"]
commands = ["up", "down", "stop"]
pulse_lengths = [160, 270, 665, 6856]
pulse_count = 50

_command_codes = {"up": "001", "down": "010", "stop": "100"}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"02210202022102022121022102212121020221210221020203"``.

    Returns:
        Dict with ``id`` and ``command``; ``command`` is None for an unknown command code,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 23:
        return None

    # Binary is now something like:
    # 010001001101011100110100

    # Now we extract the data from that string.
    # | 01000100110101110011 | 010     | 0 |
    # | ID                   | Command | ? |
    command_code = binary[20:23]
    return {
        "id": int(binary[0:20], 2),
        "command": next(
            (c for c, code in _command_codes.items() if code == command_code), None
        ),
    }


def encode(id: int, command: str) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        command: ``up``, ``down`` or ``stop``.

    Returns:
        Pulse sequence string.
    """
    encoded = binary2pulses(f"{id:020b}", binary2pulses_mapping)
    encoded += binary2pulses(_command_codes[command], binary2pulses_mapping)
    encoded += "0203"
    return encoded
