"""Rawswitch protocol: replay recorded pulse sequences of any switch.

Brands: RAW.

Only sending is supported. ``encode()`` sets the module's ``pulse_lengths`` to
the recorded ones, so read them after encoding.
"""

from typing import Any

from rfcontrol.protocols import RFControlProtocolTypes

name = "rawswitch"
type = RFControlProtocolTypes.SWITCH
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
    pulses_on: str,
    pulses_off: str,
    state: bool,
) -> str:
    """Encode a message into a pulse sequence.

    Args:
        pulse_lengths: Pulse lengths of the recorded signals.
        pulses_on: Recorded pulse sequence for on.
        pulses_off: Recorded pulse sequence for off.
        state: True for on, False for off.

    Returns:
        Pulse sequence string.
    """
    # Like the original implementation, remember the recorded pulse lengths.
    globals()["pulse_lengths"] = list(pulse_lengths)
    return pulses_on if state else pulses_off
