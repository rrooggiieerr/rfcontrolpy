"""Switch28 protocol: remotes with on, off and both buttons.

Brands: oh!haus & Co.

No mapping to binary fits all codes, so the pulses themselves are read as bits.
"""

from typing import Any

from rfcontrol.protocols import RFControlProtocolTypes

name = "switch28"
type = RFControlProtocolTypes.SWITCH
brands = ["oh!haus & Co."]
pulse_lengths = [417, 1287, 13042]
pulse_count = 50

_command_codes = {"on": "01011010", "off": "10100101", "both": "01010101"}


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01010110010101100101011001100110011001010101101002"``.

    Returns:
        Dict with ``id``, ``unit``, ``state`` and ``all``; the ``both`` command
        decodes as ``all`` with ``state`` None, an unknown command code as
        ``state`` None,
        or None if the pulses don't match the protocol.
    """
    # Now we extract the data from the pulses.
    # | 0101011001010110010101100 | 110011001100101 | 01011010 | 02     |
    # | ID                        | Unit            | Command  | footer |
    command = next(
        (c for c, code in _command_codes.items() if code == pulses[40:48]), None
    )
    try:
        decoded = {
            "id": int(pulses[0:25], 2),
            "unit": int(pulses[25:40], 2),
            "state": {"on": True, "off": False}.get(command or ""),
            "all": command == "both",
        }
    except ValueError:
        return None
    return decoded


def encode(id: int, unit: int, state: bool, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code.
        state: True for on, False for off; ignored when ``all`` is True.
        all: Send the ``both`` command.

    Returns:
        Pulse sequence string.
    """
    command = "both" if all else ("on" if state else "off")
    return f"{id:025b}{unit:015b}{_command_codes[command]}02"
