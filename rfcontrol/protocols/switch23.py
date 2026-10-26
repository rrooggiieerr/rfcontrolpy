"""Switch23 protocol: remotes with four buttons A to D.

Brands: Atag Cooking hood, TXS4 Transmitter.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["10", "0"],  # Binary 0
    ["01", "1"],  # Binary 1
    ["2", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "10", "1": "01"}

name = "switch23"
type = RFControlProtocolTypes.SWITCH
brands = ["Atag Cooking hood", "TXS4 Transmitter"]
commands = ["A", "B", "C", "D"]
pulse_lengths = [350, 720, 16000]
pulse_count = 38

_command_codes = {
    "A": "1110",
    "B": "1100",
    "C": "1011",
    "D": "1001",
}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"00110011001100110011010100110011001012"``.

    Returns:
        Dict with ``id`` and ``command``; ``command`` is None for an unknown command code,
        or None if the pulses don't match the protocol.
    """
    # The first pulse is a header and is skipped.
    # We first map the sequences to binary.
    binary = pulses2binary(pulses[1:38], pulses2binary_mapping)

    if binary is None or len(binary) < 18:
        return None

    # Now we extract the data from that string.
    # | 14 bits | 4 bits  |
    # | ID      | Command |
    command_code = binary[14:18]
    return {
        "id": int(binary[0:14], 2),
        "command": next(
            (c for c, code in _command_codes.items() if code == command_code), None
        ),
    }


def encode(id: int, command: str) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        command: ``A``, ``B``, ``C`` or ``D``; anything else sends ``A``.

    Returns:
        Pulse sequence string.
    """
    command_code = _command_codes.get(command, _command_codes["A"])
    encoded = "0"
    encoded += binary2pulses(f"{id:014b}", binary2pulses_mapping)
    encoded += binary2pulses(command_code, binary2pulses_mapping)
    encoded += "2"
    return encoded
