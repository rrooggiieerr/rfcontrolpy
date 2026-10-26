"""Weather18 protocol: temperature sensor."""

from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["0003", ""],  # Footer
]

name = "weather18"
type = RFControlProtocolTypes.WEATHER
brands = ["Mebus/Renkforce E0190T"]
pulse_lengths = [496, 960, 1940, 3904]
pulse_count = 76


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"0101020102020102020101010101010102020202010102020202020201010102020101020003"``.

    Returns:
        Dict with ``id``, ``unit`` and ``temperature``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Binary is now something like:
    # 001011011000000011110011111100011001

    # Now we extract the data from that string.
    # 1100 0111 0000 0001 0010 1010 1111 0011 1001 0
    # IIII IIII xxUU TTTT TTTT TTTT xxxx xxxx xxxx xx
    # 0    4    8    12   16   20   24   28   32
    # I: Device ID, 8-bit unsigned Int
    # U: Unit, the channel (2 bits + 1, 00=1, 01=2, 10=3)
    # T: Temperature Value, 12-bit signed Int (divide decimal by 10)
    # x: Unused
    return {
        "id": int(binary[0:8], 2),
        "unit": int(binary[10:12], 2) + 1,
        "temperature": binary2signed(binary[12:24]) / 10,
    }
