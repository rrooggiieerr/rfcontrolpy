"""Switch22 protocol: remotes with four buttons A to D.

Brands: Relay 4CH switch.
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
binary2pulses_mapping = {"0": "10", "1": "01"}

name = "switch22"
type = RFControlProtocolTypes.SWITCH
brands = ["Relay 4CH switch"]
commands = ["A", "B", "C", "D"]
pulse_lengths = [376, 1144, 11720]
pulse_count = 50

_command_codes = {
    "A": "1110",
    "B": "1101",
    "C": "1011",
    "D": "0111",
}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01100110101010101001100101010101101010010110010102"``.

    Returns:
        Dict with ``id`` and ``command``; ``command`` is None for an unknown command code,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Now we extract the data from that string.
    # | 20 bits | 4 bits  |
    # | ID      | Command |
    command_code = binary[20:24]
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
        command: ``A``, ``B``, ``C`` or ``D``.

    Returns:
        Pulse sequence string.
    """
    command_code = _command_codes[command]
    encoded = ""
    encoded += binary2pulses(f"{id:020b}", binary2pulses_mapping)
    encoded += binary2pulses(command_code, binary2pulses_mapping)
    encoded += "02"
    return encoded
