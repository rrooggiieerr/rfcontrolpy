"""Helpers for converting between pulse sequences and binary strings.

Python port of the original CoffeeScript/Node.js rfcontroljs helpers.
"""

import logging

logger = logging.getLogger(__name__)


def pulses2binary(pulses: str, pulses2binary_mapping) -> str | None:
    """Converts a sequence of pulses to a binary value."""
    binary = ""
    pointer = 0
    while pointer < len(pulses):
        for pulse, byte in pulses2binary_mapping:
            if pulses[pointer:].startswith(pulse):
                binary += byte
                pointer += len(pulse)
                break
        else:
            logger.debug("No matching pulse sequence found")
            return None
    return binary


def binary2pulses(binary: str, binary2pulses_mapping) -> str:
    """Converts a binary value to a sequence of pulses."""
    pulses = ""
    for bit in binary:
        pulses += binary2pulses_mapping[bit]
    return pulses


def hex_checksum(data):
    """Calculates the checksum."""
    checksum = 0
    number = int(data[0:32][::-1], 2)
    while number > 0:
        checksum ^= number & 0x0F
        number >>= 4
    return checksum == 0
