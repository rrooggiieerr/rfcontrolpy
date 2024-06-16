"""
Use this skeleton protocol to implement new protocols
"""

# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = []

# Mapping for encoding
binary2pulses_mapping = {}

name = "skeleton"
type = RFControlProtocolTypes.DIMMER
brands = []
pulse_lengths = []
pulse_count = 0


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
    decoded = {}
    logger.debug(decoded)
    return decoded


def encode(id: int, unit: int):
    encoded = ""
    logger.debug(encoded)
    return encoded
