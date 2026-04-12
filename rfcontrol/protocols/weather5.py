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
brands = ["Auriol IAN 9183"]
pulse_lengths = [534, 2000, 4000, 9000]
pulse_count = 74


def decode(pulses):
    binary = pulses2binary(pulses, pulses2binary_mapping)
    if binary is None:
        return None

    # id (bits 0..7) LSB-first
    id_ = int(binary[0:8][::-1], 2)
    # battery (bit 8)
    low_battery = int(binary[8], 2) != 0
    # states (bits 9..10) LSB-first
    states = int(binary[9:11][::-1], 2)

    if states in (0, 1, 2):
        # temperature (bits 12..23) LSB-first, signed two's complement
        temp_raw = int(binary[12:24][::-1], 2)
        n = 12  # number of bits
        if temp_raw >= (1 << (n - 1)):
            temp_raw -= (1 << n)
        temperature = temp_raw / 10.0

        # humidity: bits 24..29 MSB-first (6 bits)
        humidity = int(binary[24:30], 2)

        decoded = {
            "id": id_,
            "lowBattery": low_battery,
            "temperature": temperature,
            "humidity": humidity,
        }
        logger.debug(decoded)
        return decoded

    if states == 3:
        # substate (bits 12..14) LSB-first
        substate = int(binary[12:15][::-1], 2)

        if substate == 1:
            avg_airspeed = int(binary[24:32][::-1], 2) / 5.0
            decoded = {
                "id": id_,
                "lowBattery": low_battery,
                "avgAirspeed": avg_airspeed,
            }
            logger.debug(decoded)
            return decoded

        if substate == 7:
            wind_direction = int(binary[15:24][::-1], 2)
            wind_gust = int(binary[24:32][::-1], 2) / 5.0
            decoded = {
                "id": id_,
                "lowBattery": low_battery,
                "windDirection": wind_direction,
                "windGust": wind_gust,
            }
            logger.debug(decoded)
            return decoded

        if substate == 3:
            rain = int(binary[16:32][::-1], 2) / 4.0
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
