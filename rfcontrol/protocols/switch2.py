# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0110", "0"],  # Binary 0
    ["0101", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding
binary2pulses_mapping = {"0": "0110", "1": "0101"}

name = "switch2"
type = RFControlProtocolTypes.SWITCH
brands = ["Elro", "Elro Home Easy"]
pulse_lengths = [306, 957, 9808]
pulse_count = 50


def decode(pulses):
    # Pulses is something like:
    # 01010101011001100101010101100110011001100101011002

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 110011000010

    # Now we extract the data from that string.
    # |     11001 |    10000 |     1 |              0 |
    # | HouseCode | UnitCode | State | inverted state |
    decoded = {
        "id": int(binary[0:5], 2),
        "unit": int(binary[5:10], 2),
        "state": binary[11] == "0",
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, state: bool, all: bool = False):
    encoded = binary2pulses(f"{id:05b}", binary2pulses_mapping)
    encoded += binary2pulses(f"{unit:05b}", binary2pulses_mapping)
    encoded += binary2pulses_mapping["1"] if state else binary2pulses_mapping["0"]
    encoded += binary2pulses_mapping["0"] if state else binary2pulses_mapping["1"]
    encoded += "02"
    logger.debug(encoded)
    return encoded
