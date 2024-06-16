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
    ["1010", "2"],  # Binary tri-state
    ["0110", "0"],  # Bbinary 0
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "0110", "1": "0101", "2": "1010"}

name = "switch8"
type = RFControlProtocolTypes.SWITCH
brands = ["Rev"]
pulse_lengths = [189, 547, 5720]
pulse_count = 50


def binary_to_char(data):
    character = 0
    i = len(data) - 1
    while i >= 0:
        if data[i] == "2":
            break
        i -= 1
        character += 1

    return chr(65 + character)


def decode(pulses):
    # Pulses is something like:
    # 01010101010101010110011001101010010101010101101002

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 111100021112

    # Now we extract the data from that string.
    # | 11110      | 00211       | 1              | 2
    # | SystemCode | ProgramCode | inverse state  | state

    # First we save the tri-state as a char.
    unit = binary_to_char(binary[5:10])
    state = binary[11] == "2"

    # For the rest we don't need the third state. Set all 2 to 0
    binary = binary.replace("2", "0")

    # Building the unit code to something like this 'E10'
    unit += str(int(binary[5:10], 2))

    decoded = {
        "id": int(binary[:5], 2),
        "unit": unit,
        "state": state,
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, state: bool, all: bool = False):
    encoded = binary2pulses(f"{id:05b}", binary2pulses_mapping)

    unit_char = ord(unit[0]) - 65
    unit = int(unit[1:])

    programcode1 = f"{unit:05b}"
    programcode2 = programcode1[: 4 - unit_char] + "2" + programcode1[5 - unit_char :]

    encoded += binary2pulses(programcode2, binary2pulses_mapping)

    encoded += binary2pulses_mapping["1"] if state else binary2pulses_mapping["2"]
    encoded += binary2pulses_mapping["2"] if state else binary2pulses_mapping["1"]
    encoded += "02"
    logger.debug(encoded)
    return encoded
