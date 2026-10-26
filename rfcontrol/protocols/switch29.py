"""Switch29 protocol: wireless keychain remotes.

Brands: Meiantech, Atlantic, Aidebao, PB-403R.

Commands: ``arm``, ``panic``, ``disarm``, ``home``, ``grp1``, ``grp2``, ``grp3``.
"""

from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding. The pulses are the bits.
pulses2binary_mapping = [
    ["0", "0"],  # Binary 0
    ["1", "1"],  # Binary 1
    ["2", ""],  # Footer
]

name = "switch29"
type = RFControlProtocolTypes.SWITCH
brands = ["Meiantech", "Atlantic", "Aidebao", "PB-403R"]
commands = ["arm", "panic", "disarm", "home", "grp1", "grp2", "grp3"]
pulse_lengths = [404, 804, 4028]
pulse_count = 74

_command_codes = {
    "arm": "011001010101100101101010",
    "panic": "010101100101100101011001",
    "disarm": "100101010101100110011010",
    "home": "010110010101100101010110",
    "grp1": "101001010101100110101010",
    "grp2": "100110010101100110010110",
    "grp3": "101010010101100110100110",
}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"00101011101010101101001010101010111000110010101010110010101011001011010102"``.

    Returns:
        Dict with ``id``, ``unit`` and ``command``; for an unknown command code ``command``
        is the command code as a number,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 73:
        return None

    # Now we extract the data from that string.
    # | 25 bits | 24 bits | 24 bits |
    # | ID      | Unit    | Command |
    command_code = pulses[49:73]
    return {
        "id": int(binary[0:25], 2),
        "unit": int(binary[25:49], 2),
        "command": next(
            (c for c, code in _command_codes.items() if code == command_code),
            int(binary[49:73], 2),
        ),
    }


def encode(id: int, unit: int, command: str) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code.
        command: ``arm``, ``panic``, ``disarm``, ``home``, ``grp1``, ``grp2``, ``grp3``.

    Returns:
        Pulse sequence string.
    """
    return f"{id:025b}{unit:024b}{_command_codes[command]}2"
