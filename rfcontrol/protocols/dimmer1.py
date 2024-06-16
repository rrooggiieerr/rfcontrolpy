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
    ["0000", "N"],  # State = don't change
    ["03", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {
    "0": "0001",
    "1": "0100",
    "N": "0000",
}

name = "dimmer1"
type = RFControlProtocolTypes.DIMMER
brands = ["CoCo Technologies", "D-IO (Chacon)", "Intertechno", "KlikAanKlikUit", "Nexa"]
pulse_lengths = [260, 1300, 2700, 10400]
pulse_count = 148


def decode(pulses: str):
    # Pulses is something like:
    # 0200010001010000010001010000010001000101000100010001000100000101000100010000010001000100010001010001000001000100000001000100010001010001000100010003

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 001000111101001000100110100100000001

    # Now we extract the data from that string.
    # | 00100100011111011100000110 |   0 |     N | 0000 |  1111 |
    # | 00100011110100100010011010 |   0 |     1 | 0000 |  0001 |
    # | ID                         | All | State | unit | level |
    state = None
    if binary[27] != "N":
        state = binary[27] == "1"

    decoded = {
        "id": int(binary[:26], 2),
        "unit": int(binary[28:32], 2),
        "all": binary[26] == "1",
        "state": state,
        "dimlevel": int(binary[32:36], 2),
    }
    logger.debug(decoded)
    return decoded


def encode(
    id: int, unit: int, state: bool = None, dimlevel: int = None, all: bool = False
):
    encoded = "02"
    encoded += binary2pulses(f"{id:026b}", binary2pulses_mapping)
    encoded += binary2pulses_mapping["1"] if all else binary2pulses_mapping["0"]
    if state is None:
        encoded += binary2pulses_mapping["N"]
    else:
        encoded += binary2pulses_mapping["1"] if state else binary2pulses_mapping["0"]
    encoded += binary2pulses(f"{unit:04b}", binary2pulses_mapping)
    encoded += binary2pulses(f"{dimlevel:04b}", binary2pulses_mapping)
    encoded += "03"
    logger.debug(encoded)
    return encoded
