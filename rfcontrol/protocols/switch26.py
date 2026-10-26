"""Switch26 protocol: tri-state switches with a channel letter and a unit.

Brands: Chacon EMW200TC.

Channel and unit are strings. Unknown codes are returned as their raw bits,
and raw bits can also be sent.
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

name = "switch26"
type = RFControlProtocolTypes.SWITCH
brands = ["Chacon EMW200TC"]
pulse_lengths = [480, 1476, 15260]
pulse_count = 50

_channel_codes = {"A": "011", "B": "101", "C": "110"}
_unit_codes = {"1": "0111", "2": "1011", "3": "1101", "4": "1110"}
# Unit code followed by the constant bits.
_unit_and_constant_codes = {
    "1": "01111111",
    "2": "10111111",
    "3": "11011111",
    "4": "11101111",
}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01010110011001100110011001010110011001100110101002"``.

    Returns:
        Dict with ``channel``, ``unit`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 12:
        return None

    # Now we extract the data from that string.
    # | 3 bits  | 4 bits | constant | 1 symbol |
    # | Channel | Unit   | constant | Command  |
    # A command of 2 means on.
    channel_code = binary[0:3]
    unit_code = binary[3:7]
    decoded = {
        "channel": next(
            (c for c, code in _channel_codes.items() if code == channel_code),
            channel_code,
        ),
        "unit": next(
            (u for u, code in _unit_codes.items() if code == unit_code),
            unit_code + binary[7:11],
        ),
        "state": binary[11] == "2",
    }
    logger.debug(decoded)
    return decoded


def encode(channel: str, unit: str, state: bool) -> str:
    """Encode a message into a pulse sequence.

    Args:
        channel: Channel letter, or raw channel bits.
        unit: Unit as a string, or raw unit and constant bits.
        state: True for on, False for off.

    Returns:
        Pulse sequence string.
    """
    encoded = binary2pulses(_channel_codes.get(channel, channel), binary2pulses_mapping)
    encoded += binary2pulses(
        _unit_and_constant_codes.get(unit, unit), binary2pulses_mapping
    )
    encoded += binary2pulses("2" if state else "0", binary2pulses_mapping)
    encoded += "02"
    logger.debug(encoded)
    return encoded
