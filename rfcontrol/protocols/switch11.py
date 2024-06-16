# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "1"],  # Binary 1
    ["10", "0"],  # Binary 0
    ["02", ""],  # Footer
]

# Mapping for encoding
binary2pulses_mapping = {"1": "01", "0": "10"}

name = "switch11"
type = RFControlProtocolTypes.SWITCH
brands = ["McPower"]
pulse_lengths = [566, 1267, 6992]
pulse_count = 66


def decode(pulses):
    # Pulses is something like:
    # 12021212121212121212021212121212121212121203

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 1011111111011111111110

    # Now we extract the data from that string.
    # | 1011111111|011111111|   1   |10
    # | ID?       |unit?    | State |Channel
    unit = int(binary[3], 2)
    if unit == 1:
        state = binary[4] == "1"
    else:
        state = binary[5] == "1"
    decoded = {"id": int(binary[6:22], 2), "unit": unit, "state": state}
    logger.debug(decoded)
    return decoded


# Looks like encode had never worked in the original implementation
def encode(id: int, unit: int, state: bool, all: bool = False):
    encoded = "011010"
    unit = binary2pulses(f"{unit}", binary2pulses_mapping)
    encoded += binary2pulses_mapping[str(unit)]

    state = binary2pulses_mapping["1"] if state else binary2pulses_mapping["0"]
    inv_state = binary2pulses_mapping["0"] if state else binary2pulses_mapping["1"]
    if unit == 1:
        encoded += f"{state}{inv_state}"
    else:
        encoded += f"{inv_state}{state}"

    encoded += binary2pulses(f"{id:026b}", binary2pulses_mapping)
    encoded += "02"
    logger.debug(encoded)
    return encoded
