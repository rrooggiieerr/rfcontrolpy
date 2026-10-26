"""Weather21 protocol: temperature and humidity sensor."""

import logging
from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["12222222", ""],  # Header
    ["02", "0"],  # Binary 0
    ["12", "0"],  # Binary 0
    ["22", "1"],  # Binary 1
    ["20", "1"],  # Binary 1
    ["21", "1"],  # Binary 1
    ["03", ""],  # Footer
    ["13", ""],  # Footer
    ["23", ""],  # Footer
]


def _crc8_table(polynomial: int) -> list[int]:
    table = []
    for i in range(256):
        byte = i
        for _ in range(8):
            carry = byte & 0x80
            byte = (byte << 1) % 256
            if carry:
                byte ^= polynomial
        table.append(byte)
    return table


_CRC8_TABLE = _crc8_table(0x31)


def _crc8(data: list[int], init: int) -> int:
    crc = init
    for byte in data:
        crc = _CRC8_TABLE[(crc ^ byte) % 256]
    return crc


name = "weather21"
type = RFControlProtocolTypes.WEATHER
brands = [
    "Auriol HG02832",
    "Auriol HG05124A-DCF",
    "Auriol IAN 321304_1901",
    "Rubicson 48957",
]
pulse_lengths = [196, 288, 628, 61284]
pulse_count = 88


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"1222222220122012121212201220121220121212121212121212121220122020121221212112121221121213"``.

    Returns:
        Dict with ``crcOk``, ``id``, ``humidity``, ``lowBattery``, ``unit`` and ``temperature``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 32:
        return None

    # Binary is now something like:
    # 101000010100100000000000101100111000100

    # Now we extract the data from that string.
    # | 0-----7  | 8----15  | 16-19 | 20----31     | 32----39 |
    # | 10100001 | 01001000 | 0000  | 000010110011 | 1000100x |
    # | ID       | Humidity | Flags | Temperature  | Checksum |
    # Flags:
    # 16: Battery indicator, 1 = normal, 0 = low
    # 17: TX button
    # 18-19: Unit, the channel (value + 1)
    # The checksum is a CRC-8 over the XOR of the first 4 bytes.
    digest = 0
    for offset in range(0, 32, 8):
        digest ^= int(binary[offset : offset + 8], 2)
    # The binary is one bit short: the last bit of the checksum is part of the
    # footer. Like the original implementation, it's read as 0.
    checksum = int(binary[32:40].ljust(8, "0"), 2)
    decoded = {
        "crcOk": checksum == _crc8([digest], 0x53),
        "id": int(binary[0:8], 2),
        "humidity": int(binary[8:16], 2),
        "lowBattery": binary[16] == "1",
        "unit": int(binary[18:20], 2) + 1,
        "temperature": binary2signed(binary[20:32]) / 10,
    }
    logger.debug(decoded)
    return decoded
