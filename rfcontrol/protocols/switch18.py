"""Switch18 protocol: switches with a 28-bit ID.

Brands: Otio, Advisen.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["02", ""],  # Footer
    ["01", "1"],  # Binary 1
    ["10", "0"],  # Binary 0
    ["03", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "10", "1": "01"}

name = "switch18"
type = RFControlProtocolTypes.SWITCH
brands = ["Otio", "Advisen"]
pulse_lengths = [600, 1200, 3500, 7000]
pulse_count = 68


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"10011001010110101010011001011010100101010110010101010101101001010203"``.

    Returns:
        Dict with ``id`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 32:
        return None

    # Binary is now something like:
    # 01011100001011000111101111110011

    # Now we extract the data from that string.
    # | 01 | 01    | 1100001011000111101111110 |
    # | 01 | State | ID                        |
    return {
        "id": int(binary[4:32], 2),
        "state": binary[2] == "1",
    }


def encode(id: int, state: bool, unit: int = 0, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        state: True for on, False for off.
        unit: Ignored by this protocol.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """
    encoded = "1001"
    encoded += "1001" if state else "0110"
    encoded += binary2pulses(f"{id:028b}", binary2pulses_mapping)
    encoded += "03"
    return encoded
