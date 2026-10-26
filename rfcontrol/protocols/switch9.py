"""Switch9 protocol: heater switches.

Brands: DRU Heaters.
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
    ["12", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "10", "1": "01"}

name = "switch9"
type = RFControlProtocolTypes.SWITCH
brands = ["DRU Heaters"]
pulse_lengths = [300, 600, 23000]
pulse_count = 46


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"0110100101100110011010101001101010101001011012"``.

    Returns:
        Dict with ``id``, ``unit`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 21:
        return None

    # Now we extract the data from that string.
    # | 12 bits | 8 bits | 1 bit | 1 bit |
    # | ID      | Unit   | State | ?     |
    decoded = {
        "id": int(binary[0:12], 2),
        "unit": int(binary[12:20], 2),
        "state": binary[20] == "1",
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
    encoded = binary2pulses(f"{id:012b}", binary2pulses_mapping)
    encoded += binary2pulses(f"{unit:08b}", binary2pulses_mapping)
    encoded += binary2pulses_mapping["1"] if state else binary2pulses_mapping["0"]
    encoded += "1012"
    logger.debug(encoded)
    return encoded
