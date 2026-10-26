"""Weather14 protocol: temperature and humidity sensor."""

from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "1"],  # Binary 1
    ["02", "0"],  # Binary 0
    ["03", ""],  # Footer
]

name = "weather14"
type = RFControlProtocolTypes.WEATHER
brands = ["Prologue Temperature & Humidity Sensor"]
pulse_lengths = [480, 1960, 3908, 8784]
pulse_count = 76


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"0201010201020102010101010102020101010102010101010202020202020101020201010103"``.

    Returns:
        Dict with ``id``, ``unit``, ``temperature`` and ``lowBattery``, plus
        ``humidity`` when the sensor has one,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 36:
        return None

    # Binary is now something like:
    # 0110101011111001111011110000001100111

    # Now we extract the data from that string.
    # 1100 0111 0000 0001 0010 1010 1111 0011 1001 0
    # xxxx IIII IIII UUxB TTTT TTTT TTTT HHHH HHHH xx
    # 0    4    8    12   16   20   24   28   32
    # I: Device ID, 8-bit unsigned Int
    # U: Unit, the channel (2 bits, modulo 3, + 1)
    # B: Battery flag (1-bit, 1=Battery OK, 0=Battery Low)
    # T: Temperature Value, 12-bit signed Int (divide decimal by 10)
    # H: Humidity, 8-bit unsigned Int, always 11001100 without a humidity sensor
    # x: Unused
    decoded = {
        "id": int(binary[4:12], 2),
        "unit": int(binary[12:14], 2) % 3 + 1,
        "temperature": binary2signed(binary[16:28]) / 10,
        "lowBattery": binary[15] != "1",
    }
    humidity = int(binary[28:36], 2)
    if humidity != 0b11001100:
        decoded["humidity"] = humidity
    return decoded
