"""Weather4 protocol: Auriol temperature and humidity sensor.

The sensor sends the temperature in °F; it is converted to °C.
"""

from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["1111111104", ""],  # Header
    ["02", "0"],  # Binary 0
    ["03", "1"],  # Binary 1
    ["05", ""],  # Footer
]

name = "weather4"
type = RFControlProtocolTypes.WEATHER
brands = ["Auriol"]
pulse_lengths = [526, 990, 1903, 4130, 7828, 16076]
pulse_count = 92


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"11111111040203020202020202030202020203020302030203030303020303020303020202020302020202020305"``.

    Returns:
        Dict with ``id``, ``unit``, ``temperature``, ``humidity`` and
        ``lowBattery``, or None if the pulses don't match the protocol.
    """
    # We first map the pulse sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 40:
        return None

    # Binary is now something like:
    # 0110001100000000011000011101011100110001

    # Based on this example : T18,8 H71 :1110111001010101011000011000011100010001
    # 11101110-0101-0101-011000011000-0111-0001-0001
    # 11101110 : Station ID (random after restart)
    # 0101 : Check Sum
    # 0101 : Battery 0000=full(3V) 0100=2,6V
    # 0100 0000 0110 : temperature is sent by the sensor in °F and not °C
    # 0111-0001 : humidity first nibble is the tens, second nibble the units {0111=7  0001=1}= 71%H
    # 0001 : Channel (0001 = 1, xxxx = ?, xxxx = ?)
    # The lowest value that the protocol support is 90°F (000000000000).
    # In our example it give us 0110 0001 1000
    # which is 1560 in decimal
    # So the rule is 1560/10 - 90 = 66 °F (18,8 °C) (this rule works fine for all temp
    # positive/negative)

    t0 = int(binary[16:28], 2)
    temperature = round((t0 * 10 - 12200) / 18) / 10

    h0 = int(binary[28:32], 2)
    h1 = int(binary[32:36], 2)
    humidity = h0 * 10 + h1
    low_battery = (3 - (int(binary[12:16], 2) / 10)) < 2.5

    return {
        "id": int(binary[:8], 2),
        "unit": int(binary[36:40], 2),
        "temperature": temperature,
        "humidity": humidity,
        "lowBattery": low_battery,
    }
