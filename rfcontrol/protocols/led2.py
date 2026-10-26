"""Led2 protocol: LED controller.

Brands: LED Controller.

Commands: ``on/off``, ``light``, ``bright+``, ``bright-``, ``100%``, ``50%``, ``25%``, ``mode+``, ``mode-``, ``speed+``, ``speed-``.
Other command codes are decoded and can be sent as ``code:<8 bits>``.
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

name = "led2"
type = RFControlProtocolTypes.LED
brands = ["LED Controller"]
commands = [
    "on/off",
    "light",
    "bright+",
    "bright-",
    "100%",
    "50%",
    "25%",
    "mode+",
    "mode-",
    "speed+",
    "speed-",
]
pulse_lengths = [439, 1240, 12944]
pulse_count = 50

_command_codes = {
    "on/off": "00000001",
    "light": "00000100",
    "bright+": "00000101",
    "bright-": "00000110",
    "100%": "00000111",
    "50%": "00001000",
    "25%": "00001001",
    "mode+": "00001011",
    "mode-": "00010001",
    "speed+": "00001111",
    "speed-": "00001101",
}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01011010011010100110010110010101010101010101011002"``.

    Returns:
        Dict with ``id`` and ``command``; an unknown command code is returned
        as ``code:<8 bits>``, or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Now we extract the data from that string.
    # | 16 bits | 8 bits  |
    # | ID      | Command |
    command_code = binary[16:24]
    command = next(
        (c for c, code in _command_codes.items() if code == command_code),
        f"code:{command_code}",
    )
    decoded = {
        "id": int(binary[0:16], 2),
        "command": command,
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, command: str) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        command: One of the commands, or ``code:<8 bits>`` for any other
            command code.

    Returns:
        Pulse sequence string.

    Raises:
        ValueError: If the command is unknown.
    """
    if command in _command_codes:
        command_code = _command_codes[command]
    elif command.startswith("code:"):
        command_code = command[5:]
    else:
        raise ValueError(f"Unknown command {command}")
    encoded = binary2pulses(f"{id:016b}", binary2pulses_mapping)
    encoded += binary2pulses(command_code, binary2pulses_mapping)
    encoded += "02"
    logger.debug(encoded)
    return encoded
