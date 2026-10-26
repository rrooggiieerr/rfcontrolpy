"""Weather13 protocol: Xiron temperature and humidity sensor 2."""

from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather13"
type = RFControlProtocolTypes.WEATHER
brands = ["Xiron Temperature & Humidity Sensor 2"]
pulse_lengths = [492, 992, 2028, 4012]
pulse_count = 74

# Bit positions (named for clarity)
ID_START, ID_END = 0, 7
LOW_BATTERY_BIT = 8
UNIT_START, UNIT_END = 10, 11
TEMP_START, TEMP_END = 12, 23
HUMIDITY_START, HUMIDITY_END = 28, 35


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"02020202010101020201020101010101020202010202010202020202010102020101010103"``.

    Returns:
        Dict with ``id``, ``unit``, ``temperature``, ``humidity`` and
        ``lowBattery``, or None if the pulses don't match the protocol.
    """
    # We first map the pulse sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 36:
        return None

    # Binary is now something like:
    # 111100011010000011101101111100110000

    # Now we extract the temperature and humidity from that string
    # 1111 0001 1010 0000 1110 1101 1111 0011 0000
    # IIII IIII BxCC TTTT TTTT TTTT xxxx HHHH HHHH
    # 0    4    8    12   16   20   24   28   32
    # I: Device ID, 8-bit unsigned Int
    # B: Low-Battery Flag (1-bit, 0=Battery OK, 1=Battery Low)
    # T: Temperature Value, 12-bit signed Int (divide decimal by 10)
    # H: Humidity, 8-bit unsigned Int
    # C: Channel (2 bits + 1, 00=1, 01=2, 10=3)
    # x: Unused

    return {
        "id": int(binary[ID_START : ID_END + 1], 2),
        "unit": int(binary[UNIT_START : UNIT_END + 1], 2) + 1,
        "temperature": binary2signed(binary[TEMP_START : TEMP_END + 1]) / 10,
        "humidity": int(binary[HUMIDITY_START : HUMIDITY_END + 1], 2),
        "lowBattery": binary[LOW_BATTERY_BIT] == "1",
    }
