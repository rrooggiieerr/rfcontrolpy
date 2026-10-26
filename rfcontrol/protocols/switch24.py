"""Switch24 protocol: switches with house code and unit code.

Brands: Power remote 1204380, Steffen 1204380.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["10", "1"],  # Binary 1
    ["01", "0"],  # Binary 0
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "switch24"
type = RFControlProtocolTypes.SWITCH
brands = ["Power remote 1204380", "Steffen 1204380"]
pulse_lengths = [512, 1024, 6144]
pulse_count = 50


def _invert(bits: str) -> str:
    return bits.translate(str.maketrans("01", "10"))


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01101010010101011010100110010110100101010101011002"``.

    Returns:
        Dict with ``id`` (house code), ``unit`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Binary is now something like:
    # 011100001110100110000001

    # Now we extract the data from that string. The house code is sent inverted.
    # |     01110 | 00011 | 101001 |     1 | 00 |    00001 |
    # | HouseCode | ????? | ?????? | State | ?? | UnitCode |
    return {
        "id": int(_invert(binary[0:5]), 2),
        "unit": int(binary[19:24], 2),
        "state": binary[16] == "1",
    }


def encode(id: int, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: House code.
        unit: Unit code.
        state: True for on, False for off.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """
    encoded = binary2pulses(_invert(f"{id:05b}"), binary2pulses_mapping)
    encoded += "0101011010100110010110"
    encoded += binary2pulses_mapping["1"] if state else binary2pulses_mapping["0"]
    encoded += "0101"
    encoded += binary2pulses(f"{unit:05b}", binary2pulses_mapping)
    encoded += "02"
    return encoded
