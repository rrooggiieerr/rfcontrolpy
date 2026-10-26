"""Switch21 protocol: LightwaveRF switches.

Brands: LightwaveRF.

Uses the same frame and nibble encoding as dimmer2, with the dim level 0.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes
from rfcontrol.protocols.dimmer2 import nibble_to_number, number_to_nibble

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "1"],  # Binary 1
    ["02", "0"],  # Binary 0
    ["03", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "02", "1": "01"}

name = "switch21"
type = RFControlProtocolTypes.SWITCH
brands = ["LightwaveRF"]
pulse_lengths = [204, 328, 1348, 10320]
pulse_count = 144


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"010201010101010202010201010101010101010201020101010201010202010201010101010101020101020101020101020101010101020102020102010101010201010101020103"``.

    Returns:
        Dict with ``id``, ``unit`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 71:
        return None

    # Now we extract the data from that string. Every value is a 7-bit
    # LightwaveRF nibble code:
    # | 1 | 2 x level | Unit | State | 6 x ID |
    try:
        unit = nibble_to_number(int(binary[15:22], 2))
        state = bool(nibble_to_number(int(binary[22:29], 2)))
        remote_code = 0
        for i in range(6):
            start = 29 + i * 7
            remote_code = remote_code * 16 + nibble_to_number(
                int(binary[start : start + 7], 2)
            )
    except KeyError:
        logger.debug("Unknown nibble code")
        return None
    return {
        "id": remote_code,
        "unit": unit,
        "state": state,
    }


def encode(id: int, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Remote ID.
        unit: Unit code.
        state: True for on, False for off.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """

    def _nibble(number: int) -> str:
        return binary2pulses(f"{number_to_nibble(number):07b}", binary2pulses_mapping)

    # The level is 0 when switching on or off.
    level = binary2pulses(f"{0x7A:07b}", binary2pulses_mapping)
    state_pulses = binary2pulses(
        f"{0x76 if state else 0x7A:07b}", binary2pulses_mapping
    )
    encoded = f"01{level}{level}{_nibble(unit)}{state_pulses}"
    for shift in (20, 16, 12, 8, 4, 0):
        encoded += _nibble((id >> shift) & 0x0F)
    encoded += "03"
    return encoded
