# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather13"
type = RFControlProtocolTypes.WEATHER
brands = []
pulse_lengths = [492, 992, 2028, 4012]
pulse_count = 74

# Bit positions (named for clarity)
ID_START, ID_END = 0, 7
LOW_BATTERY_BIT = 8
UNIT_START, UNIT_END = 10, 11
TEMP_START, TEMP_END = 12, 23
HUMIDITY_START, HUMIDITY_END = 28, 35


def decode(pulses):
    """Decode raw pulse data into weather sensor readings."""

    def binary_to_signed_number(bit_string, start, end):
        """
        Convert binary substring [start:end] to signed integer.
        Assumes MSB is the sign bit.
        """
        bit_segment = bit_string[start : end + 1]
        sign_bit = int(bit_segment[0])
        value_bits = bit_segment[1:]
        value = int(value_bits, 2)

        if sign_bit == 1:
            # Two's complement correction
            bit_length = len(value_bits)
            value -= 1 << bit_length

        return value

    # Convert pulses to binary
    # pulses is something like: '02020202010101020201020101010101020202010202010202020202010102020101010103'
    # we first map the pulse sequences to binary
    binary = pulses2binary(pulses, pulses2binary_mapping)
    if binary is None:
        logger.debug("Failed to convert pulses to binary.")
        return None

    # binary is now something like: '11000111000000010010101011110011100100000'
    # now we extract the temperature and humidity from that string
    # 1100 0111 0000 0001 0010 1010 1111 0011 1001 0
    # IIII IIII BxCC TTTT TTTT TTTT xxxx HHHH HHHH x
    # 0    4    8    12   16   20   24   28   32
    # I: Device ID, 8-bit unsigned Int
    # B: Low-Battery Flag (1-bit, 0=Battery OK, 1=Battery Low)
    # T: Temperature Value, 12-bit signed Int (divide decimal by 10)
    # H: Humidity, 8-bit unsigned Int
    # C: Channel (2 bits + 1, 00=1, 01=2, 10=3)
    # x: Unused

    try:
        # Decode fields
        device_id = int(binary[ID_START : ID_END + 1], 2)
        low_battery = binary[LOW_BATTERY_BIT] == "1"
        unit = int(binary[UNIT_START : UNIT_END + 1], 2) + 1
        temperature = binary_to_signed_number(binary, TEMP_START, TEMP_END) / 10
        humidity = int(binary[HUMIDITY_START : HUMIDITY_END + 1], 2)

        decoded = {
            "id": device_id,
            "unit": unit,
            "temperature": temperature,
            "humidity": humidity,
            "lowBattery": low_battery,
        }

        logger.debug(f"Decoded weather13: {decoded}")
        return decoded

    except (ValueError, IndexError) as e:
        logger.exception(f"Error decoding weather13: {e}")
        return None
