"""Switch13 protocol: switches with a parity bit.

Brands: Aldi Quigg GT-7000, Globaltronics GT-FSI-04a.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, parity_bit, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["10", "1"],  # Binary 1
    ["01", "0"],  # Binary 0
    ["2", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "switch13"
type = RFControlProtocolTypes.SWITCH
brands = ["Aldi Quigg GT-7000", "Globaltronics GT-FSI-04a"]
pulse_lengths = [700, 1400, 81000]
pulse_count = 42


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"001100110101001010101010101010110100110102"``.

    Returns:
        Dict with ``id``, ``unit``, ``all``, ``state`` and ``dimm``, or None if the parity bit
        doesn't match,
        or None if the pulses don't match the protocol.
    """
    # The first pulse is a header and is skipped.
    # We first map the sequences to binary.
    binary = pulses2binary(pulses[1:], pulses2binary_mapping)

    if binary is None or len(binary) < 20:
        return None

    # Binary is now something like:
    # 01011100000000011011

    # Now we extract the data from that string.
    # | 010111000000 | 00   | 0   | 1     | 1    | 0    | 1        | 1      |
    # | ID           | Unit | All | State | Dimm | zero | unit ref | parity |
    if (binary[19] == "1") != parity_bit(binary[12:19]):
        logger.debug("Parity bit doesn't match")
        return None
    decoded = {
        "id": int(binary[0:12], 2),
        "unit": int(binary[12:14], 2),
        "all": binary[14] == "1",
        "state": binary[15] == "1",
        "dimm": binary[16] == "1",
    }
    logger.debug(decoded)
    return decoded


def encode(
    id: int, unit: int, state: bool, all: bool = False, dimm: bool = False
) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code.
        state: True for on, False for off.
        all: Address all units.
        dimm: Dim command.

    Returns:
        Pulse sequence string.
    """
    unit_bits = f"{unit:02b}"
    binary = f"{id:012b}{unit_bits}"
    binary += "1" if all is True else "0"
    binary += "1" if state else "0"
    binary += "1" if dimm is True else "0"
    binary += "0" + unit_bits[0]
    binary += "1" if parity_bit(binary[12:]) else "0"
    encoded = "0" + binary2pulses(binary, binary2pulses_mapping) + "2"
    logger.debug(encoded)
    return encoded
