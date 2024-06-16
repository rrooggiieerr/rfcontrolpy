# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long

import logging

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["00", "0"],  # binary 0
    ["01", "1"],  # binary 1
    ["02", ""],  # footer
]

# Mapping for encoding
binary2pulses_mapping = {
    "0": "00",
    "1": "01",
}

name = "switch10"
type = RFControlProtocolTypes.SWITCH
brands = ["Easy Home Advanced"]
pulse_lengths = [271, 1254, 10092]
pulse_count = 116


def decode(pulses):
    # Pulses is something like:
    # 01010000000101010100000100010101010000000101010100000101000100000101000101010001000100010001010001000101000000010102

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)
    logger.debug(binary)

    if binary is None:
        return None

    # Binary is now something like:
    # 11000111100 1011110001111001101001101110101010110101100011

    # Now we extract the data from that string.
    # | 11000111100 10111100011110011010011011101010   1011    01       01      100011
    # | ?          |     systemcode                  | Group | State | group2 |  Unit
    groupcode1 = int(binary[43:47], 2)
    groupcode2 = int(binary[49:51], 2)

    group_res = True
    if groupcode1 == 11 and groupcode2 == 1:
        group_res = False
    elif groupcode1 == 12 and groupcode2 == 3:
        group_res = True

    decoded = {
        "id": int(binary[11:43], 2),
        "unit": int(binary[51:57], 2),
        "all": group_res,
        "state": binary[47] == "1",
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, state: bool, all: bool = False):
    if all:
        groupcode1 = binary2pulses(f"{12:04b}", binary2pulses_mapping)
        groupcode2 = binary2pulses(f"{3:02b}", binary2pulses_mapping)
    else:
        groupcode1 = binary2pulses(f"{11:04b}", binary2pulses_mapping)
        groupcode2 = binary2pulses(f"{1:02b}", binary2pulses_mapping)

    encoded = "0101000000010101010000"
    encoded += binary2pulses(f"{id:032b}", binary2pulses_mapping)
    encoded += groupcode1
    if state:
        encoded += binary2pulses("10", binary2pulses_mapping)
    else:
        encoded += binary2pulses("01", binary2pulses_mapping)
    encoded += groupcode2
    encoded += binary2pulses(f"{unit:06b}", binary2pulses_mapping)
    encoded += "02"
    logger.debug(encoded)
    return encoded
