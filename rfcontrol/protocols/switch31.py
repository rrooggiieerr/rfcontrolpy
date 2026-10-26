"""Switch31 protocol: sockets with channels 1 to 4.

Brands: Masterplug UK.

The ID and channel are each followed by their inverse, which is used to
validate a message.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["000022", ""],  # Header
    ["00", "0"],  # Binary 0
    ["01", "1"],  # Binary 1
    ["03", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "00", "1": "01"}

name = "switch31"
type = RFControlProtocolTypes.SWITCH
brands = ["Masterplug UK"]
pulse_lengths = [452, 1336, 3392, 10124]
pulse_count = 88

# Channel 5 addresses all channels.
_ALL_CHANNELS = 5


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"0000220100010101000000010101000001000100010000000101010000000101000100010000000001010103"``.

    Returns:
        Dict with ``id``, ``unit`` (the channel), ``state`` and ``all``, or None if the
        inverted ID or channel doesn't match,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 40:
        return None

    # Binary is now something like:
    # 1011100011100101010001110001101010000111

    # Now we extract the data from that string.
    # | 1011100011100101 | 0100011100011010 | 1000    | 0111             |
    # | ID               | inverted ID      | Channel | inverted channel |
    # The channel is sent in reverse bit order and the last bit is the state.
    # For off, the channel is inverted.
    id_ = int(binary[0:16], 2)
    if id_ != int(binary[16:32], 2) ^ 0xFFFF:
        logger.debug("ID validation failed")
        return None
    channel_bits = binary[32:36]
    if int(channel_bits, 2) != int(binary[36:40], 2) ^ 0xF:
        logger.debug("Channel validation failed")
        return None
    channel = int(channel_bits[::-1], 2)
    state = binary[39] == "1"
    if not state:
        channel ^= 0xF
    return {
        "id": id_,
        "unit": channel,
        "state": state,
        "all": channel == _ALL_CHANNELS,
    }


def encode(id: int, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Channel, 1-4.
        state: True for on, False for off.
        all: Address all channels.

    Returns:
        Pulse sequence string.
    """
    # The ID followed by the inverted ID.
    id_bits = f"{((id << 16) + (id ^ 0xFFFF)) & 0xFFFFFFFF:032b}"
    channel = _ALL_CHANNELS if all is True else unit
    if state is False:
        channel ^= 0xF
    # The inverted channel followed by the channel, then reversed.
    channel_bits = f"{(((channel ^ 0xFF) << 4) + channel) & 0xFF:08b}"[::-1]
    encoded = "000022"
    encoded += binary2pulses(id_bits, binary2pulses_mapping)
    encoded += binary2pulses(channel_bits, binary2pulses_mapping)
    encoded += "03"
    return encoded
