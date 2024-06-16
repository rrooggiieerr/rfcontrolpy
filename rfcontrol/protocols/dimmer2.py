"""
Support for LightwaveRF dimmers

http://www.benjiegillam.com/2013/02/lightwaverf-rf-protocol/
https://old-wiki.somakeit.org.uk/index.php/LightwaveRF_RF_Protocol
"""

# pylint: disable=duplicate-code
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "1"],  # Binary 1
    ["02", "0"],  # Binary 0
    ["03", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "02", "1": "01"}

name = "dimmer2"
type = RFControlProtocolTypes.DIMMER
brands = ["LightwaveRF"]
pulse_lengths = [204, 328, 1348, 10320]
pulse_count = 144


def nibble_to_number(nibble):
    return {
        0x7A: 0x00,
        0x76: 0x01,
        0x75: 0x02,
        0x73: 0x03,
        0x6E: 0x04,
        0x6D: 0x05,
        0x6B: 0x06,
        0x5E: 0x07,
        0x5D: 0x08,
        0x5B: 0x09,
        0x57: 0x0A,
        0x3E: 0x0B,
        0x3D: 0x0C,
        0x3B: 0x0D,
        0x37: 0x0E,
        0x2F: 0x0F,
    }[nibble]


def number_to_nibble(number):
    return (
        0x7A,
        0x76,
        0x75,
        0x73,
        0x6E,
        0x6D,
        0x6B,
        0x5E,
        0x5D,
        0x5B,
        0x57,
        0x3E,
        0x3D,
        0x3B,
        0x37,
        0x2F,
    )[number]


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
    dimlevel = nibble_to_number(int(binary[1:8], 2)) * 16
    dimlevel += nibble_to_number(int(binary[8:15], 2))

    unit_code = nibble_to_number(int(binary[15:22], 2))

    nstate = nibble_to_number(int(binary[22:29], 2))
    state = bool(nstate)

    remote_code = nibble_to_number(int(binary[29:36], 2)) * 1048576
    remote_code += nibble_to_number(int(binary[36:43], 2)) * 65536
    remote_code += nibble_to_number(int(binary[43:50], 2)) * 4096
    remote_code += nibble_to_number(int(binary[50:57], 2)) * 256
    remote_code += nibble_to_number(int(binary[57:64], 2)) * 16
    remote_code += nibble_to_number(int(binary[64:71], 2))

    decoded = {
        "id": remote_code,
        "unit": unit_code,
        "state": state,
        "dimlevel": dimlevel,
    }
    logger.debug(decoded)
    return decoded


def encode(
    id: int, unit: int, state: bool = None, dimlevel: int = None, all: bool = False
):
    if 0 < dimlevel <= 31:
        _level = dimlevel + 0x80
        state = binary2pulses(f"{0x76:07b}", binary2pulses_mapping)
    else:
        _level = 0
        state = binary2pulses(f"{0x7A:07b}", binary2pulses_mapping)

    level1 = binary2pulses(
        f"{number_to_nibble((_level//16) & 0x0F):07b}", binary2pulses_mapping
    )
    level2 = binary2pulses(
        f"{number_to_nibble(_level & 0x0F):07b}", binary2pulses_mapping
    )

    unit_code = binary2pulses(f"{number_to_nibble(unit):07b}", binary2pulses_mapping)

    id1 = binary2pulses(
        f"{number_to_nibble((id//1048576) & 0x0F):07b}",
        binary2pulses_mapping,
    )
    id2 = binary2pulses(
        f"{number_to_nibble((id//65536) & 0x0F):07b}",
        binary2pulses_mapping,
    )
    id3 = binary2pulses(
        f"{number_to_nibble((id//4096) & 0x0F):07b}",
        binary2pulses_mapping,
    )
    id4 = binary2pulses(
        f"{number_to_nibble((id//256) & 0x0F):07b}",
        binary2pulses_mapping,
    )
    id5 = binary2pulses(
        f"{number_to_nibble((id//16) & 0x0F):07b}",
        binary2pulses_mapping,
    )
    id6 = binary2pulses(f"{number_to_nibble(id & 0x0F):07b}", binary2pulses_mapping)

    encoded = f"01{level1}{level2}{unit_code}{state}{id1}{id2}{id3}{id4}{id5}{id6}03"
    return encoded
