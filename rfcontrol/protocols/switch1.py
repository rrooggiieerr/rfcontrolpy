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
    ["02", ""],  # Header
    ["0001", "0"],  # Binary 0
    ["0100", "1"],  # Binary 1
    ["03", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {
    "0": "0001",
    "1": "0100",
}

name = "switch1"
type = RFControlProtocolTypes.SWITCH
brands = ["CoCo Technologies", "D-IO (Chacon)", "Intertechno", "KlikAanKlikUit", "Nexa"]
pulse_lengths = [268, 1282, 2632, 10168]
pulse_count = 132


def decode(pulses):
    # Pulses is something like:
    # 020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010100000100010001000103

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 00100011110100100010011010010000

    # Now we extract the data from that string.
    # | 00100011110100100010011010 |   0 |     1 | 0000 |
    # | ID                         | All | State | Unit |
    # logger.debug(f'{binary[0:26]} {binary[26]} {binary[27]} {binary[28:]}')
    decoded = {
        "id": int(binary[:26], 2),
        "unit": int(binary[28:], 2),
        "all": binary[26] == "1",
        "state": binary[27] == "1",
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int, state: bool, all: bool = False):
    encoded = "02"
    encoded += binary2pulses(f"{id:026b}", binary2pulses_mapping)
    encoded += binary2pulses_mapping["1"] if all else binary2pulses_mapping["0"]
    encoded += binary2pulses_mapping["1"] if state else binary2pulses_mapping["0"]
    encoded += binary2pulses(f"{unit:04b}", binary2pulses_mapping)
    encoded += "03"
    logger.debug(encoded)
    return encoded
