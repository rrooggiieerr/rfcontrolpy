"""Switch30 protocol: alarm keypads.

Brands: JP-05.

Commands: ``arm``, ``dis``, ``byp``, ``sos``.
"""

import logging
from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding. The pulses are the bits.
pulses2binary_mapping = [
    ["0", "0"],  # Binary 0
    ["1", "1"],  # Binary 1
    ["2", ""],  # Footer
]

name = "switch30"
type = RFControlProtocolTypes.SWITCH
brands = ["JP-05"]
commands = ["arm", "dis", "byp", "sos"]
pulse_lengths = [520, 1468, 13312]
pulse_count = 50

_command_codes = {
    "arm": "1010010101010101",
    "dis": "0101010110100101",
    "byp": "0101010101011010",
    "sos": "0101101001010101",
}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01010101010110100101101001001110101001010101010102"``.

    Returns:
        Dict with ``id``, ``unit`` and ``command``; for an unknown command code ``command``
        is None,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 32:
        return None

    # Now we extract the data from that string.
    # | 16 bits | 16 bits | 16 bits |
    # | ID      | Unit    | Command |
    command_code = pulses[32:48]
    decoded = {
        "id": int(binary[0:16], 2),
        "unit": int(binary[16:32], 2),
        "command": next(
            (c for c, code in _command_codes.items() if code == command_code),
            None,
        ),
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, command: str) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code.
        command: ``arm``, ``dis``, ``byp``, ``sos``.

    Returns:
        Pulse sequence string.
    """
    encoded = f"{id:016b}{unit:016b}{_command_codes[command]}02"
    logger.debug(encoded)
    return encoded
