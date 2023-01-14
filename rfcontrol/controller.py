"""
Python port of the original CoffeeScript/nodejs code
"""
import logging

from rfcontrol import helpers
from rfcontrol.protocols import (
    dimmer1,
    generic,
    generic2,
    switch1,
    switch2,
    switch3,
    switch4,
    switch5,
    switch6,
    switch7,
    switch8,
    switch10,
    switch11,
    switch25,
    weather7,
    weather19,
)

protocols = (
    # weather1, weather2, weather3, weather4, weather5, weather6,
    weather7,
    # weather8, weather9, weather10, weather11, weather12, weather13, weather14,
    # weather15, weather16, weather17, weather18,
    weather19,  # weather20, weather21
    switch1,
    switch2,
    switch3,
    switch4,
    switch5,
    switch6,
    switch7,
    switch8,
    # switch9,
    switch10,
    switch11,
    # switch12, switch13, switch14, switch15, switch16,
    # switch17, switch18, switch19, switch20, switch21, switch22, switch23, switch24,
    switch25,
    # switch26, switch27, switch28, switch29, switch30, switch31, switch32
    # switch33, switch34
    # rolling1
    dimmer1,
    # dimmer2
    # pir1, pir2, pir3, pir4, pir5, pir6
    # contact1, contact2, contact3, contact4
    generic,
    generic2,
    # alarm1, alarm2, alarm3
    # led1, led2, led3, led4
    # doorbell1, doorbell2, doorbell3,
    # awning1, awning2
    # shutter1, shutter3, shutter4, shutter5
    # rawswitch, rawshutter
)

logger = logging.getLogger(__name__)


def does_protocol_match(pulse_lengths, pulse_sequence, protocol: str) -> bool:
    """
    Test if a protocol matches the pulse lengths and pulse sequence
    """
    if protocol.pulse_count != len(pulse_sequence):
        return False

    if len(protocol.pulse_lengths) != len(pulse_lengths):
        return False

    for i, pulse_length in enumerate(pulse_lengths):
        max_delta = pulse_length * 0.4
        if abs(protocol.pulse_lengths[i] - pulse_length) > max_delta:
            return False

    return True


def sort_indices(array: []):
    """
    Sort the indexes of an array by order of element value.
    """
    element_index_map = []
    for i, element in enumerate(array):
        element_index_map.append([element, i])
    element_index_map.sort()

    indices = []
    for item in element_index_map:
        indices.append(item[1])

    return indices


def compress_timings(timings: []):
    """ """
    pulses = ""
    buckets = []
    sums = []
    counts = []

    for timing in timings:
        # Search for a bucket.
        has_match = False
        for j, bucket in enumerate(buckets):
            if abs(bucket - timing) < bucket * 0.5:
                pulses += str(j)
                sums[j] += timing
                counts[j] += 1
                has_match = True
        if not has_match:
            # Create new bucket.
            pulses += str(len(buckets))
            buckets.append(timing)
            sums.append(timing)
            counts.append(1)

    for j, _bucket in enumerate(buckets):
        buckets[j] = round(sums[j] / counts[j])

    return (buckets, pulses)


def prepare_compressed_pulses(input: str):
    """ """
    # Input is something like:
    # 268 2632 1282 10168 0 0 0 0 010002000202000002000200020200020002...
    # The first 8 numbers are the pulse length and the last string is the pulse sequence
    parts = input.split(" ")
    pulse_lengths = [int(i) for i in parts[0:7]]
    pulses = parts[8]

    # Now lets filter out 0 pulses
    pulse_lengths = list(filter(lambda pulse_length: pulse_length > 0, pulse_lengths))

    # Next sort the pulses from short to long and update indices in pulses.
    return sort_compressed_pulses(pulse_lengths, pulses)


def sort_compressed_pulses(pulse_lengths: [], pulses: str):
    """
    Sort the pulses from short to long and updates indices in pulses.
    """
    sorted_indices = sort_indices(pulse_lengths)
    pulse_lengths.sort()
    pulses = helpers.map_by_array(pulses, sorted_indices)

    return (pulse_lengths, pulses)


def fix_pulses(pulse_lengths: [], pulse_sequence: str):
    """
    Merge pulse timings with similar length.

    Timings are considered the same if they differ less then a factor of 2.
    """
    # If we have less then 3 different pulseLenght there is nothing to fix.
    if len(pulse_lengths) <= 3:
        return None

    # Consider timing as the same if they differ less then a factor of 2.
    i = 1
    while i < len(pulse_lengths):
        if pulse_lengths[i - 1] * 2 < pulse_lengths[i]:
            i += 1
            continue
        # Merge pulseLengths[i-1] and pulseLengths[i]
        new_pulse_length = int((pulse_lengths[i - 1] + pulse_lengths[i]) / 2)
        # Replace the old two pulse length with the new one
        new_pulse_lengths = pulse_lengths[: i - 1]
        new_pulse_lengths.append(new_pulse_length)
        new_pulse_lengths.extend(pulse_lengths[i + 1 :])
        break

    # Nothing to do...
    if i is len(pulse_lengths):
        return None

    # Adapt pulses
    new_pulse_sequence = pulse_sequence
    while i < len(pulse_lengths):
        new_pulse_sequence = new_pulse_sequence.replace(f"{i}", f"{i-1}")
        i += 1
    return (new_pulse_lengths, new_pulse_sequence)


def decode_pulses(pulse_lengths: [], pulse_sequence: str):
    """
    Decode pulse sequence to protocol
    """
    results = []
    for protocol in protocols:
        if does_protocol_match(pulse_lengths, pulse_sequence, protocol):
            decoded = protocol.decode(pulse_sequence)
            if decoded is not None:
                logger.debug("Protocol %s matches", protocol.name)
                logger.debug("Decoded reception: %s", decoded)
                results.append({"protocol": protocol.name, "values": decoded})

    # Try to fix pulses.
    fixed_pulses = fix_pulses(pulse_lengths, pulse_sequence)
    if fixed_pulses is not None:
        # We have fixes so try again with the fixed pulse lengths...
        results.extend(decode_pulses(fixed_pulses[0], fixed_pulses[1]))

    return results


def encode_pulses(protocol_name: str, message: str):
    """
    Encode protocol to pulse sequence
    """
    protocol = get_protocol(protocol_name)

    if protocol is None:
        raise Exception(f"Could not find a protocol named {protocol_name}")

    if protocol.encode is None:
        raise Exception("The protocol has no send report")

    return {
        "pulses": protocol.encode(**message),
        "pulse_lengths": protocol.pulse_lengths,
    }


def get_all_protocols() -> []:
    """
    Get all implemented protocols.
    """
    return protocols


def get_protocol(protocol_name: str) -> str | None:
    """
    Get protocol with given name.
    """
    for _protocol in protocols:
        if _protocol.name is protocol_name:
            return _protocol

    return None
