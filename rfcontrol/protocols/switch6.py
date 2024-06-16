# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0101", "1"],  # Binary 1
    ["1010", "1"],  # Binary 1
    ["0110", "0"],  # Binary 0
    ["02", ""],  # Footer
]

# Mappings for encoding.
binary2pulses_mapping = {
    "0": "0110",
    "1": "1010",
}

binary2pulses_mapping2 = {"0": "0110", "1": "0101"}

name = "switch6"
type = RFControlProtocolTypes.SWITCH
brands = ["Impuls"]
pulse_lengths = [150, 453, 4733]
pulse_count = 50


def decode(pulses):
    # Pulses is something like:
    # 10010101101010010110010110101001010101011010101002

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 011100011011000111110000

    # Now we extract the data from that string.
    # | 01110      | 01000       | 0              | 1
    # | SystemCode | ProgramCode | invertes state | state
    decoded = {
        "id": int(binary[:5][::-1], 2),
        "unit": int(binary[5:10][::-1], 2),
        "state": binary[11] == "1",
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, state: bool, all: bool = False):
    encoded = binary2pulses(f"{id:05b}"[::-1], binary2pulses_mapping)
    encoded += binary2pulses(f"{unit:05b}"[::-1], binary2pulses_mapping2)
    encoded += binary2pulses_mapping2["0"] if state else binary2pulses_mapping2["1"]
    encoded += binary2pulses_mapping2["1"] if state else binary2pulses_mapping2["0"]
    encoded += "02"
    logger.debug(encoded)
    return encoded
