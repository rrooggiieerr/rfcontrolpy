"""Switch27 protocol: tri-state switches with a channel letter and a unit.

Brands: Chacon Zen (EMW200TB).

The id is the channel letter. An unknown channel code is returned as its raw
bits, and raw bits can also be sent; an unknown unit code is returned as None.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0110", "1"],  # Binary 1
    ["0101", "0"],  # Binary 0
    ["1010", "2"],  # Binary 2
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "0101", "1": "0110", "2": "1010"}

name = "switch27"
type = RFControlProtocolTypes.SWITCH
brands = ["Chacon Zen (EMW200TB)"]
pulse_lengths = [325, 972, 10130]
pulse_count = 50

_channel_codes = {"A": "1111", "B": "1011", "C": "1101", "D": "1110"}
_unit_codes = {"1": "01111", "2": "10111", "3": "11011"}
# Unit code followed by the constant bits.
_unit_and_constant_codes = {"1": "0111111", "2": "1011111", "3": "1101111"}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01100110011001100101011001100110011001100110101002"``.

    Returns:
        Dict with ``id`` (the channel letter), ``unit`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 12:
        return None

    # Now we extract the data from that string.
    # | 4 bits  | 5 bits | constant | 1 symbol |
    # | Channel | Unit   | constant | Command  |
    # A command of 2 means on.
    channel_code = binary[0:4]
    unit_code = binary[4:9]
    unit = next((u for u, code in _unit_codes.items() if code == unit_code), None)
    decoded = {
        "id": next(
            (c for c, code in _channel_codes.items() if code == channel_code),
            channel_code,
        ),
        "unit": None if unit is None else int(unit),
        "state": binary[11] == "2",
    }
    logger.debug(decoded)
    return decoded


def encode(id: str, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Channel letter, or raw channel bits.
        unit: Unit code.
        state: True for on, False for off.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """
    encoded = binary2pulses(_channel_codes.get(id, id), binary2pulses_mapping)
    encoded += binary2pulses(_unit_and_constant_codes[str(unit)], binary2pulses_mapping)
    encoded += binary2pulses("2" if state else "0", binary2pulses_mapping)
    encoded += "02"
    logger.debug(encoded)
    return encoded
