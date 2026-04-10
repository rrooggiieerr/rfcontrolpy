# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather5"
type = RFControlProtocolTypes.WEATHER
brands = ["Auriol", "Ventus", "Hama", "Meteoscan", "Alecto", "Balance"]
pulse_lengths = [534, 2000, 4000, 9000]
pulse_count = 74


def _binary_to_number_lsbmsb(binary, start, end):
    """Extract bits [start..end] from binary string, reverse (LSB first), convert to int."""
    bits = binary[start:end + 1]
    return int(bits[::-1], 2)


def _binary_to_signed_number_lsbmsb(binary, start, end):
    """Extract bits [start..end] LSB-first, convert to signed int (two's complement)."""
    n = end - start + 1
    value = _binary_to_number_lsbmsb(binary, start, end)
    if value >= (1 << (n - 1)):
        value -= (1 << n)
    return value


def decode(pulses):
    # Pulses mapping to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # binary is now something like: '01000101 0100 011111100000 11100110 1111'
    # 01000101 : Station ID (random after restart) - bits 0..7
    # 0100 : states - bits 8..11
    # 01111110000011100110 : data - bits 12..31
    # 1111 : check sum - bits 32..35

    # states showing which data is transmitted (bits 9..10)
    # 00,01,10: Temperature and Humidity. 11: Non temp/hum data
    # bit 8: battery (0=normal, 1=low)

    states = _binary_to_number_lsbmsb(binary, 9, 10)
    id_ = _binary_to_number_lsbmsb(binary, 0, 7)
    low_battery = _binary_to_number_lsbmsb(binary, 8, 8) != 0

    if states in (0, 1, 2):
        temperature = _binary_to_signed_number_lsbmsb(binary, 12, 23) / 10.0
        h0 = _binary_to_number_lsbmsb(binary, 28, 31)
        h1 = _binary_to_number_lsbmsb(binary, 24, 27)
        humidity = h0 * 10 + h1

        decoded = {
            "id": id_,
            "lowBattery": low_battery,
            "temperature": temperature,
            "humidity": humidity,
        }
        logger.debug(decoded)
        return decoded

    if states == 3:
        substate = _binary_to_number_lsbmsb(binary, 12, 14)

        if substate == 1:
            avg_airspeed = _binary_to_number_lsbmsb(binary, 24, 31) / 5.0
            decoded = {
                "id": id_,
                "lowBattery": low_battery,
                "avgAirspeed": avg_airspeed,
            }
            logger.debug(decoded)
            return decoded

        if substate == 7:
            wind_direction = _binary_to_number_lsbmsb(binary, 15, 23)
            wind_gust = _binary_to_number_lsbmsb(binary, 24, 31) / 5.0
            decoded = {
                "id": id_,
                "lowBattery": low_battery,
                "windDirection": wind_direction,
                "windGust": wind_gust,
            }
            logger.debug(decoded)
            return decoded

        if substate == 3:
            rain = _binary_to_number_lsbmsb(binary, 16, 31) / 4.0
            decoded = {
                "id": id_,
                "lowBattery": low_battery,
                "rain": rain,
            }
            logger.debug(decoded)
            return decoded

    decoded = {
        "id": id_,
        "lowBattery": low_battery,
    }
    logger.debug(decoded)
    return decoded
