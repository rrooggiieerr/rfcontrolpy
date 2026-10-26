"""Doorbell1 protocol: doorbells.

Brands: ADEO, ELRO/Home Easy HE-852.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "1"],  # Binary 1
    ["10", "0"],  # Binary 0
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "10", "1": "01"}

name = "doorbell1"
type = RFControlProtocolTypes.DOORBELL
brands = ["ADEO", "ELRO/Home Easy HE-852"]
pulse_lengths = [217, 648, 6696]
pulse_count = 50


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01101010011001100110011010101010101010101010101002"``.

    Returns:
        Dict with ``id``, ``unit`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Now we extract the data from that string.
    # | 12 bits | 11 bits | 1 bit           |
    # | ID      | Unit    | inverted state  |
    # ID and Unit are LSB first.
    decoded = {
        "id": int(binary[0:12][::-1], 2),
        "unit": int(binary[12:23][::-1], 2),
        "state": binary[23] != "1",
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code.
        state: True for on, False for off.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """
    encoded = binary2pulses(f"{id:012b}"[::-1], binary2pulses_mapping)
    encoded += binary2pulses(f"{unit:011b}"[::-1], binary2pulses_mapping)
    encoded += binary2pulses_mapping["0"] if state else binary2pulses_mapping["1"]
    encoded += "02"
    logger.debug(encoded)
    return encoded
