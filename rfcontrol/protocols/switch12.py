"""Switch12 protocol: switches with units 1 to 4.

Brands: Europe RS-200.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["12", "1"],  # Binary 1
    ["02", "0"],  # Binary 0
    ["03", ""],  # Footer
    ["13", ""],  # Footer 2
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "02", "1": "12"}

name = "switch12"
type = RFControlProtocolTypes.SWITCH
brands = ["Europe RS-200"]
pulse_lengths = [562, 1313, 3234, 34888]
pulse_count = 52


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"1202021212021212121212121212021202121202121212020203"``.

    Returns:
        Dict with ``id``, ``unit`` and ``state``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 20:
        return None

    # Binary is now something like:
    # 1001101111111101011011100

    # Now we extract the data from that string.
    # | 10011011111111 | 0 | 1 | 01 | 1 | 0 | 11 | 1 | 0 | 0 |
    # | ID             | S | 1 | U  | 1 | S | 11 | s | S |   |
    # S: State, s: inverted state, U: 4 - unit
    return {
        "id": int(binary[0:14], 2),
        "unit": 4 - int(binary[16:18], 2),
        "state": binary[19] == "1",
    }


def encode(id: int, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code, 1-4.
        state: True for on, False for off.
        all: Ignored by this protocol.

    Returns:
        Pulse sequence string.
    """
    id_bits = f"{id:014b}"
    s = "1" if state else "0"
    s_inv = "0" if state else "1"
    unit_bits = f"{4 - unit:02b}"
    if unit == 1:
        binary = f"{id_bits}{s_inv}1{unit_bits}1{s}11{s}{s}1"
    else:
        binary = f"{id_bits}{s}1{unit_bits}1{s}11{s_inv}{s}0"
    encoded = binary2pulses(binary, binary2pulses_mapping)
    encoded += "13" if unit == 2 else "03"
    return encoded
