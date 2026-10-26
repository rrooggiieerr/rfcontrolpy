"""Switch19 protocol: switches and dimmers with letter IDs and units 1 to 3.

Brands: REV Switch 008342 and Dimmer 008343.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["10", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "switch19"
type = RFControlProtocolTypes.SWITCH
brands = ["REV Switch 008342 and Dimmer 008343"]
pulse_lengths = [472, 1436, 14776]
pulse_count = 50

_id_codes = {"A": "11010", "B": "01110", "C": "01011", "D": "01010"}
_unit_codes = {1: "11010100", 2: "01110100", 3: "01010111"}
_state_codes = {False: "0011", True: "1100"}


def _lookup[K](codes: dict[K, str], code: str) -> K | None:
    return next((key for key, value in codes.items() if value == code), None)


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"10010101101010010110010110101001010101011010101002"``.

    Returns:
        Dict with ``id`` (a letter), ``unit`` and ``state``; unknown codes are None,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Now we extract the data from that string.
    # | 5 bits | 3 bits | 8 bits | 4 bits | 4 bits |
    # | ID     | fixed  | Unit   | fixed  | State  |
    decoded = {
        "id": _lookup(_id_codes, binary[0:5]),
        "unit": _lookup(_unit_codes, binary[8:16]),
        "state": _lookup(_state_codes, binary[20:24]),
    }
    logger.debug(decoded)
    return decoded


def encode(id: str, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID, a letter from A to D.
        unit: Unit code, 1-3.
        state: True for on, False for off.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """
    encoded = binary2pulses(_id_codes[id], binary2pulses_mapping)
    encoded += "100110"
    encoded += binary2pulses(_unit_codes[unit], binary2pulses_mapping)
    encoded += "01010101"
    encoded += binary2pulses(_state_codes[state], binary2pulses_mapping)
    encoded += "02"
    logger.debug(encoded)
    return encoded
