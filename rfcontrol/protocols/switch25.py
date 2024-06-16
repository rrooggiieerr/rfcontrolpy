# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [["10", "1"], ["01", "0"], ["02", ""]]

# Mapping for encoding
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "switch25"
type = RFControlProtocolTypes.SWITCH
brands = ["Lidl 0655B"]
pulse_lengths = [350, 880, 10970]
pulse_count = 66


def decode(pulses):
    # Pulses is something like:
    # 101010101010101010101010101010100101010101010101011010100110011002

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 10101010101010101010101010101010010101010101010101

    # Now we extract the data from that string.
    # 1111111111111111000000000 | 1110 | 10    | 1
    # prefix                    | unit | state | postfix
    # after the prefix there is the 4 digit unit code, the state and inverse state and a final 1
    # the keys on the remote map to the unit code in the following way:
    # key '1' => 1110 which is a decimal 14
    # key '2' => 1011 which is a decimal 11
    # key '3' => 0111 which is a decimal 7
    # key '4' => 1101 which is a decimal 13
    # key 'master' => 0000 which is a decimal 0
    decoded = {"id": 0, "unit": int(binary[25:29], 2), "state": binary[29] == "1"}
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, state: bool, all: bool = False):
    encoded = "10101010101010101010101010101010010101010101010101"
    encoded += binary2pulses(f"{unit:04b}", binary2pulses_mapping)
    encoded += binary2pulses_mapping["1"] if state else binary2pulses_mapping["0"]
    encoded += binary2pulses_mapping["0"] if state else binary2pulses_mapping["1"]
    encoded += "1002"
    logger.debug(encoded)
    return encoded
