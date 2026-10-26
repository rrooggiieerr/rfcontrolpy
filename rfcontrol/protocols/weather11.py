"""Weather11 protocol: temperature and humidity sensor."""

import logging
from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather11"
type = RFControlProtocolTypes.WEATHER
brands = ["Xiron Temperature & Humidity Sensor"]
pulse_lengths = [544, 1056, 1984, 3880]
pulse_count = 84


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"020201010102020201010101010101020101020102010201020202020101020202010102010101010103"``.

    Returns:
        Dict with ``id``, ``unit``, ``temperature``, ``humidity`` and ``lowBattery``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 36:
        return None

    # Binary is now something like:
    # 11000111000000010010101011110011100100000

    # Now we extract the data from that string.
    # 1100 0111 0000 0001 0010 1010 1111 0011 1001 0000 0
    # IIII IIII BxUU TTTT TTTT TTTT xxxx HHHH HHHH xxxx x
    # 0    4    8    12   16   20   24   28   32   36
    # I: Device ID, 8-bit unsigned Int
    # B: Battery flag (1-bit, 1=Battery OK, 0=Battery Low)
    # U: Unit, the channel (2 bits + 1, 00=1, 01=2, 10=3)
    # T: Temperature Value, 12-bit signed Int (divide decimal by 10)
    # H: Humidity, 8-bit unsigned Int
    # x: Unused
    decoded = {
        "id": int(binary[0:8], 2),
        "unit": int(binary[10:12], 2) + 1,
        "temperature": binary2signed(binary[12:24]) / 10,
        "humidity": int(binary[28:36], 2),
        "lowBattery": binary[8] != "1",
    }
    logger.debug(decoded)
    return decoded
