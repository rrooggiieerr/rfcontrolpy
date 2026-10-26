"""Switch20 protocol: switches with a 4-bit unit code.

Brands: MBO International Electronic GmbH.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0101", "1"],  # Binary 1
    ["0110", "0"],  # Binary 0
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "0110", "1": "0101"}

name = "switch20"
type = RFControlProtocolTypes.SWITCH
brands = ["MBO International Electronic GmbH"]
pulse_lengths = [128, 400, 4152]
pulse_count = 50


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01100110010101100110011001100110011001100110011002"``.

    Returns:
        Dict with ``unit`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 8:
        return None

    # Binary is now something like:
    # 001000000000

    # Now we extract the data from that string.
    # | 001    | 0000      | 0              | 00   | 0              | 0    |
    # | header | Unit code | inverted state | zero | inverted state | zero |
    # The unit code is LSB first.
    decoded = {
        "unit": int(binary[3:7][::-1], 2),
        "state": binary[7] != "1",
    }
    logger.debug(decoded)
    return decoded


def encode(unit: int, state: bool, id: int = 0, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        unit: Unit code.
        state: True for on, False for off.
        id: Ignored by this protocol.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """
    zero = binary2pulses_mapping["0"]
    one = binary2pulses_mapping["1"]
    inverse_state = zero if state else one
    encoded = f"{zero}{zero}{one}"
    encoded += binary2pulses(f"{unit:04b}"[::-1], binary2pulses_mapping)
    encoded += f"{inverse_state}{zero}{zero}{inverse_state}{zero}02"
    logger.debug(encoded)
    return encoded
