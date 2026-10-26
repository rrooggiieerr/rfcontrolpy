"""Shutter1 protocol: shutter motors.

Brands: Nobily.

Commands: ``up``, ``down`` and ``stop``.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["32", ""],  # Header
    ["01", "0"],  # Binary 0
    ["10", "1"],  # Binary 1
    ["14", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "shutter1"
type = RFControlProtocolTypes.SHUTTER
brands = ["Nobily"]
commands = ["up", "down", "stop"]
pulse_lengths = [280, 736, 1532, 4752, 7796]
pulse_count = 164

_command_codes = {"up": "1000", "down": "1001", "stop": "1010"}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"32010110010101011001010101010101100110101001011010100101100101011001010110010101103201011001010101100101010101010110011010100101101010010110010101100101011001010114"``.

    Returns:
        Dict with ``id`` and ``command``; ``command`` is None for an unknown
        command code, or None if the pulses don't match the protocol.
    """
    # The message is sent twice, separated by a fixed 1:
    # 32 <ID> <command> <command> 10 32 <ID> <command> <command> 14
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 35:
        return None

    # Binary is now something like:
    # 0010000100000001011100111001000100010001001000010000000101110011100100010001000

    # Now we extract the data from that string.
    # | 0010000100000001011100111001000 | 1000    | 1000    | 1     |
    # | ID                              | command | command | fixed |
    command_code = binary[31:35]
    command = next(
        (c for c, code in _command_codes.items() if code == command_code), None
    )
    decoded = {
        "id": int(binary[0:31], 2),
        "command": command,
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, command: str) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        command: ``up``, ``down`` or ``stop``.

    Returns:
        Pulse sequence string.
    """
    id_pulses = binary2pulses(f"{id:031b}", binary2pulses_mapping)
    command_pulses = binary2pulses(_command_codes[command], binary2pulses_mapping)
    message = f"{id_pulses}{command_pulses}{command_pulses}"
    encoded = f"32{message}1032{message}14"
    logger.debug(encoded)
    return encoded
