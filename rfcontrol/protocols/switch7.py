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
    ["1010", "0"],  # State  0
    ["0101", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {
    "0": "0110",
    "1": "0101",
}

name = "switch7"
type = RFControlProtocolTypes.SWITCH
brands = ["eHome"]
pulse_lengths = [307, 944, 9712]
pulse_count = 50


def decode(pulses):
    # Pulses is something like:
    #

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    #

    # Now we extract the data from that string.
    decoded = {
        "id": int(binary[4:7][::-1], 2),
        "unit": int(binary[1:4][::-1], 2),
        "state": binary[0] == "1",
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, state: bool, all: bool = False):
    encoded = "0101" if state else "1010"
    encoded += binary2pulses(f"{unit:03b}"[::-1], binary2pulses_mapping)
    encoded += binary2pulses(f"{id:03b}"[::-1], binary2pulses_mapping)
    encoded += "0110011001100110011002"
    logger.debug(encoded)
    return encoded
