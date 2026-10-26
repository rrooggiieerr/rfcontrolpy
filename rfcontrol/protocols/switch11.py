"""Switch11 protocol: McPower switches."""

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
binary2pulses_mapping = {"1": "01", "0": "10"}

name = "switch11"
type = RFControlProtocolTypes.SWITCH
brands = ["McPower"]
pulse_lengths = [566, 1267, 6992]
pulse_count = 66


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"100101010110011010101001101001010101100110010110011010100110011002"``.

    Returns:
        Dict with ``id``, ``unit`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 22:
        return None

    # Binary is now something like:
    # 01111010000100111101011010001010

    # Now we extract the data from that string.
    # | 011 |    1 | 1  | 0  | 1000010011110101 | 1010001010 |
    # | ?   | Unit | S4 | S5 | ID               | ?          |
    # Unit 1: S4 is the state, S5 is always 0.
    # Unit 0: S5 is the state, S4 is the inverted state.
    unit = int(binary[3], 2)
    state = binary[4] == "1" if unit == 1 else binary[5] == "1"
    decoded = {"id": int(binary[6:22], 2), "unit": unit, "state": state}
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
    encoded = "100101"
    encoded += binary2pulses(f"{unit:1b}", binary2pulses_mapping)

    state_str = binary2pulses(f"{state:1b}", binary2pulses_mapping)
    inv_state_str = binary2pulses(f"{not state:1b}", binary2pulses_mapping)
    # Bits 4 and 5, see the layout in decode().
    if unit == 1:
        encoded += state_str + binary2pulses("0", binary2pulses_mapping)
    else:
        encoded += inv_state_str + state_str

    encoded += binary2pulses(f"{id:016b}", binary2pulses_mapping)
    encoded += "01100110101001100110"
    encoded += "02"
    logger.debug(encoded)
    return encoded
