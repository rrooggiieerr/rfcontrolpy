# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

# Supported stations
# - Auriol H13726
# - Ventus WS155
# - Hama EWS 1500
# - Meteoscan W155/W160
# - Alecto WS4500
# - Alecto WS3500
# - Ventus W044
# - Balance RF-WS105
#
# pulses could be:
# '01020101010201020102010101020202020202010101010102020201010202010202020203'
# we first map the pulse sequences to binary
# binary is now something like: '01000101 0100 011111100000 11100110 1111'
# based on this example : T12,6 H65
# 01000101 0100 011111100000 11100110 1111
# 01000101 : Station ID (random after restart)
# 0100 : states
# 01111110000011100110 : data
# 1111 : check sum (n8 = ( 0xf - n0 - n1 - n2 - n3 - n4 - n5 - n6 - n7) & 0xf)
# the states showing which data is transmitted
# 0  1  0  0
# |  |  |  |-> 0: Scheduled transmission.
# |  |  |  |-> 1: The transmission was initiated by pressing the button inside the sensor unit
# |  |--|----> 00,01,10: Temperature and Humidity is transmitted. 11: Non temp/hum data
# |----------> 0: Sensor's battery voltage is normal. 1: Battery voltage is below ~2.6 V.


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
            temp_raw -= 1 << n
        temperature = temp_raw / 10.0

        h0 = int(binary[28:32][::-1], 2)
        h1 = int(binary[24:28][::-1], 2)
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
