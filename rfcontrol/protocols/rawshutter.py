"""Rawshutter protocol: replay recorded pulse sequences of any shutter.

Brands: RAW.

Only sending is supported. ``encode()`` sets the module's ``pulse_lengths`` to
the recorded ones, so read them after encoding.
"""

from typing import Any

from rfcontrol.protocols import RFControlProtocolTypes

name = "rawshutter"
type = RFControlProtocolTypes.SHUTTER
brands = ["RAW"]
pulse_lengths: list[int] = []
pulse_count = 0


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Raw protocols can't be received.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes.

    Returns:
        Always None.
    """
    return None


def encode(
    pulse_lengths: list[int],  # pylint: disable=redefined-outer-name
    pulses_up: str,
    pulses_down: str,
    pulses_stop: str,
    command: str = "",
) -> str:
    """Encode a message into a pulse sequence.

    Args:
        pulse_lengths: Pulse lengths of the recorded signals.
        pulses_up: Recorded pulse sequence for up.
        pulses_down: Recorded pulse sequence for down.
        pulses_stop: Recorded pulse sequence for stop.
        command: ``up``, ``down`` or ``stop``; anything else sends nothing.

    Returns:
        Pulse sequence string.
    """
    # Like the original implementation, remember the recorded pulse lengths.
    globals()["pulse_lengths"] = list(pulse_lengths)
    return {"up": pulses_up, "down": pulses_down, "stop": pulses_stop}.get(command, "")
