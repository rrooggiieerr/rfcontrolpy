# Original testdata
# https://raw.githubusercontent.com/pimatic/rfcontroljs/master/test/lib-controller.coffee

import logging

import pytest

from rfcontrol import controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_does_protocol_match_matching() -> None:
    result = controller.does_protocol_match(
        [671, 2051, 4346, 10220],
        "020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201010203",
        controller.generic,
    )
    assert result


def test_does_protocol_match_not_matching() -> None:
    result = controller.does_protocol_match(
        [671, 2051, 4346, 10220],
        "020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201010203",
        controller.switch1,
    )
    assert not result


def test_sort_indices_1() -> None:
    result = controller.sort_indices((1, 3, 2, 7, 6, 5, 4, 8))
    assert result == [0, 2, 1, 6, 5, 4, 3, 7]


def test_sort_indices_2() -> None:
    result = controller.sort_indices((1, 2, 3, 4, 5, 6, 7, 8))
    assert result == [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
    ]


def test_sort_indices_3() -> None:
    result = controller.sort_indices((8, 7, 6, 5, 4, 3, 2, 1))
    assert result == [
        7,
        6,
        5,
        4,
        3,
        2,
        1,
        0,
    ]


def test_prepare_compressed_pulses() -> None:
    result = controller.prepare_compressed_pulses(
        "268 2632 1282 10168 0 0 0 0 010002000202000002000200020200020002"
    )
    assert result == (
        [268, 1282, 2632, 10168],
        "020001000101000001000100010100010001",
    )


def test_decode_pulses_generic_1() -> None:
    results = controller.decode_pulses(
        [671, 2051, 4346, 10220],
        "020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "generic", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "generic"
    assert results[0]["values"] == {
        "id": 1000,
        "type": 10,
        "positive": True,
        "value": 1,
    }


def test_decode_pulses_generic_2() -> None:
    results = controller.decode_pulses(
        [671, 2051, 4346, 10220],
        "020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010102020102010102010201020201010202010201010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "generic", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "generic"
    assert results[0]["values"] == {
        "id": 1000,
        "type": 10,
        "positive": True,
        "value": 1257,
    }


def test_decode_pulses_generic_3() -> None:
    results = controller.decode_pulses(
        [671, 2051, 4346, 10220],
        "020102010201020101020102010201020102010202010201010201020102020101020201010202010201020102010201020102010201020102010201020102010102020102010201020102010102010202010201020101020102010202010201010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "generic", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "generic"
    assert results[0]["values"] == {
        "id": 1011,
        "type": 10,
        "positive": True,
        "value": 67129,
    }


def test_decode_pulses_generic_4() -> None:
    results = controller.decode_pulses(
        [671, 2051, 4346, 10220],
        "020102010201020101020102010201020102020101020201020102010102020101020201020102010201020102010201020102010201020102010201020102010102020102010201020102010102010202010201020101020102010202010201010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "generic", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "generic"
    assert results[0]["values"] == {
        "id": 1000,
        "type": 10,
        "positive": False,
        "value": 67129,
    }


def test_decode_pulses_generic_5() -> None:
    results = controller.decode_pulses(
        [671, 2051, 4346, 10220],
        "020102010201020101020102010201020102020101020201020102010102020101020201010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "generic", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "generic"
    assert results[0]["values"] == {
        "id": 1000,
        "type": 10,
        "positive": True,
        "value": 1073741823,
    }


def test_decode_pulses_generic2_1() -> None:
    results = controller.decode_pulses(
        [480, 1320, 13320],
        "011010101010101001011010101010101010101010010101101001101010100102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "generic2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "generic2"
    assert results[0]["values"] == {
        "id": 123,
        "type": 1,
        "value": 1023,
        "freq": 3,
        "battery": 99,
        "checksum": True,
    }


def test_decode_pulses_generic2_2() -> None:
    results = controller.decode_pulses(
        [480, 1320, 13320],
        "010110101010101001011010101010101010101010010101101001101010100102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "generic2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "generic2"
    assert results[0]["values"] == {
        "id": 123,
        "type": 1,
        "value": 1023,
        "freq": 3,
        "battery": 99,
        "checksum": False,
    }


def test_decode_pulses_alarm3_1() -> None:
    results = controller.decode_pulses(
        [472, 1236, 11688], "100101010101100101011010010101101010101001011010000102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "alarm3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "alarm3"
    assert results[0]["values"] == {"id": 9787738, "state": True}


def test_decode_pulses_alarm3_2() -> None:
    results = controller.decode_pulses(
        [472, 1236, 11688], "011001100110011001100110011001100110011001100110000002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "alarm3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "alarm3"
    assert results[0]["values"] == {"id": 6710886, "state": True}


def test_decode_pulses_alarm3_3() -> None:
    results = controller.decode_pulses(
        [472, 1236, 11688], "011010101001010110010110100110101010101010100101111112"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "alarm3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "alarm3"
    assert results[0]["values"] == {"id": 6985110, "state": True}


def test_decode_pulses_alarm3_4() -> None:
    results = controller.decode_pulses(
        [472, 1236, 11688], "011010101001001110010110100110101010101010100101111112"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "alarm3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "alarm3"
    assert results[0]["values"] == {"id": 6986089, "state": True}


def test_decode_pulses_alarm3_5() -> None:
    results = controller.decode_pulses(
        [472, 1236, 11688], "101010100110100110100110010110100110101001011010000002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "alarm3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "alarm3"
    assert results[0]["values"] == {"id": 11168166, "state": True}


def test_decode_pulses_pir1_1() -> None:
    results = controller.decode_pulses(
        [358, 1095, 11244],
        "01100101011001100110011001100110011001010110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "pir1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "pir1"
    assert results[0]["values"] == {"unit": 8, "id": 1, "state": True}


def test_decode_pulses_pir1_2() -> None:
    results = controller.decode_pulses(
        [358, 1095, 11244], "01100110011001100110010101100110011001010110011002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "pir1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "pir1"
    assert results[0]["values"] == {"unit": 0, "id": 17, "state": True}


def test_decode_pulses_pir1_3() -> None:
    results = controller.decode_pulses(
        [358, 1095, 11244], "01100110011001010110011001100110010101100110011002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "pir1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "pir1"
    assert results[0]["values"] == {"unit": 2, "id": 2, "state": True}


def test_decode_pulses_pir2() -> None:
    results = controller.decode_pulses(
        [451, 1402, 14356], "01100110010110011001010110100101010101011010010102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "pir2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "pir2"
    assert results[0]["values"] == {"unit": 21, "id": 21, "state": True}


def test_decode_pulses_pir4() -> None:
    results = controller.decode_pulses(
        [371, 1081, 5803], "110100110101001101010011001010101012"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "pir4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "pir4"
    assert results[0]["values"] == {"id": 54099, "unit": 21290, "state": True}


def test_decode_pulses_pir6_1() -> None:
    results = controller.decode_pulses(
        [288, 864, 8964], "01011010010101011010100110010101101001010101101002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "pir6", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "pir6"
    assert results[0]["values"] == {"id": 6410630, "state": True}


def test_decode_pulses_pir6_2() -> None:
    results = controller.decode_pulses(
        [288, 864, 8964], "01011010010101011010100110010101101001010110010102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "pir6", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "pir6"
    assert results[0]["values"] == {"id": 6410632, "state": True}


def test_decode_pulses_pir6_3() -> None:
    results = controller.decode_pulses(
        [288, 864, 8964], "01011010010101011010100110010101101001011001010102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "pir6", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "pir6"
    assert results[0]["values"] == {"id": 6410640, "state": True}


def test_decode_pulses_weather1_1() -> None:
    results = controller.decode_pulses(
        [456, 1990, 3940, 9236],
        "01020102020201020101010101010102010101010202020102010101010102010101020103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather1"
    assert results[0]["values"] == {
        "id": 208,
        "unit": 2,
        "lowBattery": True,
        "temperature": 23.2,
        "humidity": 34,
    }


def test_decode_pulses_weather1_2() -> None:
    results = controller.decode_pulses(
        [456, 1990, 3940, 9236],
        "01020102010201010101020202020101010101020101010101020101010102020202010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather1"
    assert results[0]["values"] == {
        "id": 67,
        "unit": 1,
        "lowBattery": False,
        "temperature": 26.0,
        "humidity": 61,
    }


def test_decode_pulses_weather1_3() -> None:
    results = controller.decode_pulses(
        [456, 1990, 3940, 9236],
        "01020102020201010102020102020101010101020101010101010101010102020202010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather1"
    assert results[0]["values"] == {
        "id": 198,
        "unit": 1,
        "lowBattery": False,
        "temperature": 25.6,
        "humidity": 60,
    }


def test_decode_pulses_weather1_4() -> None:
    results = controller.decode_pulses(
        [456, 1990, 3940, 9236],
        "01020102010102020102020102020201010101010202020201020101010201010101020203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather1"
    assert results[0]["values"] == {
        "id": 54,
        "unit": 3,
        "lowBattery": False,
        "temperature": 24.4,
        "humidity": 67,
    }


def test_decode_pulses_weather2_1() -> None:
    results = controller.decode_pulses(
        [492, 969, 1948, 4004],
        "01010102020202010201010101010101020202010201020102020202010101010101010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather2"
    assert results[0]["values"] == {"temperature": 23.4}


def test_decode_pulses_weather2_2() -> None:
    results = controller.decode_pulses(
        [492, 969, 1948, 4004],
        "01010102020202010201010101010101020202010201010202020202010101010101010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather2"
    assert results[0]["values"] == {"temperature": 23.3}


def test_decode_pulses_weather2_3() -> None:
    results = controller.decode_pulses(
        [492, 969, 1948, 4004],
        "01010102020202010201010101010101020202010201010102020202010101010101010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather2"
    assert results[0]["values"] == {"temperature": 23.2}


def test_decode_pulses_weather2_4() -> None:
    results = controller.decode_pulses(
        [492, 969, 1948, 4004],
        "01010101020201020201010101010102010101010202010102020202010101010101010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather2"
    assert results[0]["values"] == {"temperature": 26.8}


def test_decode_pulses_weather2_5() -> None:
    results = controller.decode_pulses(
        [492, 969, 1948, 4004],
        "01010101020201020201010101010102010101010201010102020202010101010101010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather2"
    assert results[0]["values"] == {"temperature": 26.4}


def test_decode_pulses_weather2_6() -> None:
    results = controller.decode_pulses(
        [492, 969, 1948, 4004],
        "02010102010102020201010102020202020102020102020102020202010101010202020103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather2"
    assert results[0]["values"] == {"temperature": -7.4}


def test_decode_pulses_weather3_1() -> None:
    results = controller.decode_pulses(
        [508, 2012, 3908, 7726],
        "01010202020201020201010102010102020201020202010202010201010101010202010201010101020103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather3"
    assert results[0]["values"] == {
        "id": 246,
        "unit": 3,
        "temperature": 24.2,
        "humidity": 56,
    }


def test_decode_pulses_weather3_2() -> None:
    results = controller.decode_pulses(
        [508, 2012, 3908, 7726],
        "01010202020201020201010102010201020201020202010202010201010101010202010201010202010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather3"
    assert results[0]["values"] == {
        "id": 246,
        "unit": 3,
        "temperature": 24.4,
        "humidity": 56,
    }


def test_decode_pulses_weather3_3() -> None:
    results = controller.decode_pulses(
        [508, 2012, 3908, 7726],
        "01010201020102020102010101010101010101020101010202010101010201020101010101010102010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather3"
    assert results[0]["values"] == {
        "id": 173,
        "unit": 1,
        "temperature": 21.1,
        "humidity": 65,
    }


def test_decode_pulses_weather3_4() -> None:
    results = controller.decode_pulses(
        [508, 2012, 3908, 7726],
        "01010201020102020102010101010102020201020101010202010101010201020101010101010102010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather3"
    assert results[0]["values"] == {
        "id": 173,
        "unit": 1,
        "temperature": 21.5,
        "humidity": 65,
    }


def test_decode_pulses_weather3_5() -> None:
    results = controller.decode_pulses(
        [508, 2012, 3908, 7726],
        "01010101010202020201010101020201010201010101010202010202020101010202010201010101010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather3"
    assert results[0]["values"] == {
        "id": 30,
        "unit": 2,
        "temperature": 18.1,
        "humidity": 62,
    }


def test_decode_pulses_weather3_6() -> None:
    results = controller.decode_pulses(
        [508, 2012, 3908, 7726],
        "01010101010202020201010101020102010201010102010202010202020201010202010101010202010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather3"
    assert results[0]["values"] == {
        "id": 30,
        "unit": 2,
        "temperature": 18.7,
        "humidity": 63,
    }


def test_decode_pulses_weather4() -> None:
    results = controller.decode_pulses(
        [526, 990, 1903, 4130, 7828, 16076],
        "11111111040303030203030302020302030203020302030302020202030302020202030303020202030202020305",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather4"
    assert results[0]["values"] == {
        "id": 238,
        "unit": 1,
        "temperature": 18.9,
        "humidity": 71,
        "lowBattery": False,
    }


def test_decode_pulses_weather5_1() -> None:
    results = controller.decode_pulses(
        [534, 2000, 4000, 9120],
        "01020101010201020102010101020202020202010101010102020201010202010202020203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather5"
    assert results[0]["values"] == {
        "id": 162,
        "temperature": 12.6,
        "humidity": 67,
        "lowBattery": False,
    }


def test_decode_pulses_weather5_2() -> None:
    results = controller.decode_pulses(
        [534, 2000, 4000, 9120],
        "01010101010101010102020102020101020202010201010101010101010101010101010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather5"
    assert results[0]["values"] == {"id": 0, "rain": 5.75, "lowBattery": False}


def test_decode_pulses_weather5_3() -> None:
    results = controller.decode_pulses(
        [534, 2000, 4000, 9120],
        "01020202010101020102020102020101020102020202010101010101010101010102020103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather5"
    assert results[0]["values"] == {"id": 142, "rain": 15.25, "lowBattery": False}


def test_decode_pulses_weather5_4() -> None:
    results = controller.decode_pulses(
        [534, 2000, 4000, 9120],
        "01020202010202020101010102010201020202010101010102010102020101020201020103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather5"
    assert results[0]["values"] == {
        "id": 238,
        "temperature": 11.7,
        "humidity": 99,
        "lowBattery": False,
    }


def test_decode_pulses_weather5_5() -> None:
    results = controller.decode_pulses(
        [534, 2000, 4000, 9120],
        "01020202010202020101020101020101020202020202020202010102010202010101010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather5"
    assert results[0]["values"] == {
        "id": 238,
        "temperature": -1.4,
        "humidity": 69,
        "lowBattery": False,
    }


def test_decode_pulses_weather7() -> None:
    results = controller.decode_pulses(
        [444, 1992, 3955, 9330],
        "010202010201010202010101010101010101010202020102020202010202010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather7", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather7"
    assert results[0]["values"] == {
        "id": 105,
        "temperature": 2.9,
        "humidity": 59,
        "unit": 0,
        "lowBattery": False,
    }


def test_decode_pulses_weather11() -> None:
    results = controller.decode_pulses(
        [544, 1056, 1984, 3880],
        "020202010202010102010101010101020101010202010201020202020101020201020201010101010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather11", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather11"
    assert results[0]["values"] == {
        "id": 236,
        "unit": 1,
        "temperature": 28.2,
        "humidity": 54,
        "lowBattery": False,
    }


def test_decode_pulses_weather12_1() -> None:
    results = controller.decode_pulses(
        [516, 2048, 4076, 8976],
        "0102020201010102020101010101010101020202020102020201020102010202020102020103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather12", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather12"
    assert results[0]["values"] == {
        "id": 113,
        "unit": 1,
        "temperature": 12.3,
        "humidity": 85,
        "lowBattery": True,
    }


def test_decode_pulses_weather12_2() -> None:
    results = controller.decode_pulses(
        [516, 2048, 4076, 8976],
        "0201010202010202010101010101010101020201010202010202010202020102020201010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather12", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather12"
    assert results[0]["values"] == {
        "id": 155,
        "unit": 1,
        "temperature": 10.2,
        "humidity": 110,
        "lowBattery": False,
    }


def test_decode_pulses_weather12_3() -> None:
    results = controller.decode_pulses(
        [516, 2048, 4076, 8976],
        "0201010202010202010101010101010101020202010202020201020101010102010202010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather12", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather12"
    assert results[0]["values"] == {
        "id": 155,
        "unit": 1,
        "temperature": 11.9,
        "humidity": 80,
        "lowBattery": False,
    }


# The original implementation inverts the low battery bit and expects False here.
# The Python port follows the documented bit (1 = battery low)
def test_decode_pulses_weather13() -> None:
    results = controller.decode_pulses(
        [492, 992, 2028, 4012],
        "02020202010101020201020101010101020202010202010202020202010102020101010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather13", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather13"
    assert results[0]["values"] == {
        "id": 241,
        "unit": 3,
        "temperature": 23.7,
        "humidity": 48,
        "lowBattery": True,
    }


def test_decode_pulses_weather14_1() -> None:
    results = controller.decode_pulses(
        [480, 1960, 3908, 8784],
        "0102020102010202010101020202020202020202010101010102010201010202010102020203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather14", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather14"
    assert results[0]["values"] == {
        "id": 78,
        "unit": 1,
        "temperature": 25,
        "lowBattery": True,
    }


def test_decode_pulses_weather14_2() -> None:
    results = controller.decode_pulses(
        [480, 1960, 3908, 8784],
        "0102020102010202010101020202020201010101010102010102020101010202010102020203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather14", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather14"
    assert results[0]["values"] == {
        "id": 78,
        "unit": 1,
        "temperature": -3.9,
        "lowBattery": True,
    }


def test_decode_pulses_weather14_3() -> None:
    results = controller.decode_pulses(
        [480, 1960, 3908, 8784],
        "0201010201020102010101010102020101010102010101010202020202020101020201010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather14", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather14"
    assert results[0]["values"] == {
        "id": 175,
        "unit": 3,
        "temperature": -27.2,
        "humidity": 51,
        "lowBattery": False,
    }


def test_decode_pulses_weather14_4() -> None:
    results = controller.decode_pulses(
        [480, 1960, 3908, 8784],
        "0201010201020102010101010102010201010102010101010202010102020101020201010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather14", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather14"
    assert results[0]["values"] == {
        "id": 175,
        "unit": 3,
        "temperature": -26.9,
        "humidity": 51,
        "lowBattery": True,
    }


def test_decode_pulses_weather15_1() -> None:
    results = controller.decode_pulses(
        [480, 1960, 3908, 8784],
        "0201010202010102010101010102010101010101020202010101020101020101010102010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather15", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather15"
    assert results[0]["values"] == {
        "id": 2448,
        "unit": 1,
        "temperature": 22.6,
        "humidity": 66,
        "lowBattery": False,
    }


def test_decode_pulses_weather15_2() -> None:
    results = controller.decode_pulses(
        [480, 1960, 3908, 8784],
        "0201010202010102010101010102010201010101020202010101020101020101010102010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather15", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather15"
    assert results[0]["values"] == {
        "id": 2448,
        "unit": 2,
        "temperature": 22.6,
        "humidity": 66,
        "lowBattery": False,
    }


def test_decode_pulses_weather15_3() -> None:
    results = controller.decode_pulses(
        [480, 1960, 3908, 8784],
        "0201010202010102010101010102020101010101020202010101020101020101010102010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather15", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather15"
    assert results[0]["values"] == {
        "id": 2448,
        "unit": 3,
        "temperature": 22.6,
        "humidity": 66,
        "lowBattery": False,
    }


def test_decode_pulses_weather15_4() -> None:
    results = controller.decode_pulses(
        [480, 1960, 3908, 8784],
        "0201010201010202010102020201010102020202020201020201020201010101020102010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather15", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather15"
    assert results[0]["values"] == {
        "id": 2355,
        "unit": 1,
        "temperature": -3.7,
        "humidity": 10,
        "lowBattery": True,
    }


def test_decode_pulses_weather16_1() -> None:
    results = controller.decode_pulses(
        [472, 1964, 4052, 8904],
        "02020202010202010101020101010201010101010201010101010101010102020102010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather16"
    assert results[0]["values"] == {
        "id": 111,
        "unit": 1,
        "temperature": 26,
        "humidity": 36,
        "lowBattery": False,
    }


def test_decode_pulses_weather16_2() -> None:
    results = controller.decode_pulses(
        [472, 1964, 4052, 8904],
        "02020202010202010101020101010101010101010201010102010101010102020202020103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather16"
    assert results[0]["values"] == {
        "id": 111,
        "unit": 1,
        "temperature": 25.6,
        "humidity": 37,
        "lowBattery": False,
    }


def test_decode_pulses_weather17_1() -> None:
    results = controller.decode_pulses(
        [444, 1160, 28580],
        "1111111101110111111111111111010111111111110101011111111111111101110101011111111101011112",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather17", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather17"
    assert results[0]["values"] == {"id": 24, "temperature": 20.1}


def test_decode_pulses_weather17_2() -> None:
    results = controller.decode_pulses(
        [444, 1160, 28580],
        "1111111101110111111111111111010111111101110101011111011101111111110101011111011101111112",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather17", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather17"
    assert results[0]["values"] == {"id": 24, "temperature": 22.8}


def test_decode_pulses_weather17_3() -> None:
    results = controller.decode_pulses(
        [444, 1160, 28580],
        "1111111101110111010101111111010111111101110101111111011111111111110101111111011101011112",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather17", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather17"
    assert results[0]["values"] == {"id": 24, "humidity": 62}


def test_decode_pulses_weather17_4() -> None:
    results = controller.decode_pulses(
        [444, 1160, 28580],
        "1111111101110111010101111111010111111101110101111111110111111111110101111111110101110112",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather17", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather17"
    assert results[0]["values"] == {"id": 24, "humidity": 61}


def test_decode_pulses_weather18_1() -> None:
    results = controller.decode_pulses(
        [496, 960, 1940, 3904],
        "0101020102020102020101010101010102020201010102020202020201020202010202020003",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather18", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather18"
    assert results[0]["values"] == {"id": 45, "unit": 1, "temperature": 22.7}


def test_decode_pulses_weather18_2() -> None:
    results = controller.decode_pulses(
        [496, 960, 1940, 3904],
        "0101020102020102020101010101010102020202010102020202020201010102020101020003",
    )
    assert results is not None
    assert len(results) == 1
    results = list(filter(lambda result: result["protocol"] == "weather18", results))

    assert results[0]["protocol"] == "weather18"
    assert results[0]["values"] == {"id": 45, "unit": 1, "temperature": 24.3}


def test_decode_pulses_weather18_3() -> None:
    results = controller.decode_pulses(
        [496, 960, 1940, 3904],
        "0101020102020102020101010101010201010201010101010202020202010202010202010003",
    )
    assert results is not None
    assert len(results) == 1
    results = list(filter(lambda result: result["protocol"] == "weather18", results))

    assert results[0]["protocol"] == "weather18"
    assert results[0]["values"] == {"id": 45, "unit": 1, "temperature": 28.8}


def test_decode_pulses_weather18_4() -> None:
    results = controller.decode_pulses(
        [496, 960, 1940, 3904],
        "0101020102020102020101010101010201010102010101010202020201010101010201010003",
    )
    assert results is not None
    assert len(results) == 1
    results = list(filter(lambda result: result["protocol"] == "weather18", results))

    assert results[0]["protocol"] == "weather18"
    assert results[0]["values"] == {"id": 45, "unit": 1, "temperature": 27.2}


def test_decode_pulses_weather19_1() -> None:
    results = controller.decode_pulses(
        [548, 1008, 1996, 3936],
        "020202010101010101010101010101020101010102010201020101010201020203",
    )
    assert results is not None
    assert len(results) == 1
    results = list(filter(lambda result: result["protocol"] == "weather19", results))

    assert results[0]["protocol"] == "weather19"
    assert results[0]["values"] == {"id": 56, "unit": 1, "temperature": 26.6}


def test_decode_pulses_weather19_2() -> None:
    results = controller.decode_pulses(
        [548, 1008, 1996, 3936],
        "020102020102010101010101010101020101020101020201010102020201020203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather19", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather19"
    assert results[0]["values"] == {"id": 45, "unit": 1, "temperature": 29.4}


def test_decode_pulses_weather19_3() -> None:
    results = controller.decode_pulses(
        [548, 1008, 1996, 3936],
        "020102020102010101010101010101020101020201010101020102010102010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather19", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather19"
    assert results[0]["values"] == {"id": 45, "unit": 1, "temperature": 30.4}


def test_decode_pulses_weather19_4() -> None:
    results = controller.decode_pulses(
        [548, 1008, 1996, 3936],
        "020102020102010101010101010101020202010102020101020102010101010203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather19", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather19"
    assert results[0]["values"] == {"id": 45, "unit": 1, "temperature": 46.0}


def test_decode_pulses_weather20_1() -> None:
    results = controller.decode_pulses(
        [560, 972, 1904, 3812, 8556],
        "0302020302020202030202020302020202020202030302020202030202020202020202020104",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather20", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather20"
    assert results[0]["values"] == {
        "id": 2312,
        "unit": 1,
        "temperature": 19.4,
        "lowBattery": True,
    }


def test_decode_pulses_weather20_2() -> None:
    results = controller.decode_pulses(
        [560, 972, 1904, 3812, 8556],
        "0302020302020202030202020302020202020202030203030302030202020202020202020104",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather20", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather20"
    assert results[0]["values"] == {
        "id": 2312,
        "unit": 1,
        "temperature": 18.6,
        "lowBattery": True,
    }


def test_decode_pulses_weather20_3() -> None:
    results = controller.decode_pulses(
        [560, 972, 1904, 3812, 8556],
        "0302020302020202030202020302020202020202030203030302030302020202020202020104",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather20", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather20"
    assert results[0]["values"] == {
        "id": 2312,
        "unit": 1,
        "temperature": 18.7,
        "lowBattery": True,
    }


def test_decode_pulses_weather20_4() -> None:
    results = controller.decode_pulses(
        [560, 972, 1904, 3812, 8556],
        "0302020302020202030302030302020302020202030302020203030202020202020202020104",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather20", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather20"
    assert results[0]["values"] == {
        "id": 2317,
        "unit": 2,
        "temperature": 19.8,
        "lowBattery": True,
    }


def test_decode_pulses_weather20_5() -> None:
    results = controller.decode_pulses(
        [560, 972, 1904, 3812, 8556],
        "0302020302020202030303020302020202020202030302020203020302020202020202020104",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather20", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather20"
    assert results[0]["values"] == {
        "id": 2318,
        "unit": 1,
        "temperature": 19.7,
        "lowBattery": True,
    }


def test_decode_pulses_weather20_6() -> None:
    results = controller.decode_pulses(
        [560, 972, 1904, 3812, 8556],
        "0302020302020202030303020302020202020202030302020202020302020202020202020104",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather20", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather20"
    assert results[0]["values"] == {
        "id": 2318,
        "unit": 1,
        "temperature": 19.3,
        "lowBattery": True,
    }


def test_decode_pulses_weather20_7() -> None:
    results = controller.decode_pulses(
        [560, 972, 1904, 3812, 8556],
        "0302020302020202030303020302020202020202030302020302020202020202020202020104",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather20", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather20"
    assert results[0]["values"] == {
        "id": 2318,
        "unit": 1,
        "temperature": 20,
        "lowBattery": True,
    }


def test_decode_pulses_weather21_1() -> None:
    results = controller.decode_pulses(
        [196, 288, 628, 61284],
        "1222222220122012121212201220121220121212121212121212121220122020121221212112121221121213",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather21", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather21"
    assert results[0]["values"] == {
        "crcOk": True,
        "id": 161,
        "humidity": 72,
        "lowBattery": False,
        "unit": 1,
        "temperature": 17.9,
    }


def test_decode_pulses_weather21_2() -> None:
    results = controller.decode_pulses(
        [196, 288, 628, 61284],
        "1222222220122012121212201220121212201220121212121212121220122020122020201212121212121213",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather21", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather21"
    assert results[0]["values"] == {
        "crcOk": True,
        "id": 161,
        "humidity": 69,
        "lowBattery": False,
        "unit": 1,
        "temperature": 18.3,
    }


def test_decode_pulses_weather21_3() -> None:
    results = controller.decode_pulses(
        [196, 288, 628, 61284],
        "1222222220122012121212201220121212122020121212121212121220201212121220122112201221122123",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather21", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather21"
    assert results[0]["values"] == {
        "crcOk": False,
        "id": 161,
        "humidity": 67,
        "lowBattery": False,
        "unit": 1,
        "temperature": 19.4,
    }


def test_decode_pulses_weather21_4() -> None:
    results = controller.decode_pulses(
        [196, 288, 628, 61284],
        "1222222220122012121212201220121212122121121212121212121221211212121221122112211221122123",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "weather21", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "weather21"
    assert results[0]["values"] == {
        "crcOk": False,
        "id": 161,
        "humidity": 67,
        "lowBattery": False,
        "unit": 1,
        "temperature": 19.4,
    }


def test_decode_pulses_dimmer1() -> None:
    results = controller.decode_pulses(
        [259, 1293, 2641, 10138],
        "0200010001010000010001010000010001000101000100010001000100000101000100010000010001000100010001010001000001000101000001000100010001010001000100010003",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "dimmer1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "dimmer1"
    assert results[0]["values"] == {
        "id": 9565958,
        "all": False,
        "unit": 0,
        "dimlevel": 15,
        "state": True,
    }


def test_decode_pulses_switch1_1() -> None:
    results = controller.decode_pulses(
        [268, 1282, 2632, 10168],
        "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010100000100010001000103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch1"
    assert results[0]["values"] == {
        "id": 9390234,
        "all": False,
        "state": True,
        "unit": 0,
    }


def test_decode_pulses_switch1_2() -> None:
    results = controller.decode_pulses(
        [268, 1282, 2632, 10168],
        "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010100000100010001010003",
    )
    results = list(filter(lambda result: result["protocol"] == "switch1", results))

    assert results is not None
    assert len(results) == 1
    assert results[0]["protocol"] == "switch1"
    assert results[0]["values"] == {
        "id": 9390234,
        "all": False,
        "state": True,
        "unit": 1,
    }


def test_decode_pulses_switch1_3() -> None:
    results = controller.decode_pulses(
        [268, 1282, 2632, 10168],
        "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010001000100010001010003",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch1"
    assert results[0]["values"] == {
        "id": 9390234,
        "all": False,
        "state": False,
        "unit": 1,
    }


def test_decode_pulses_switch2() -> None:
    results = controller.decode_pulses(
        [306, 957, 9808], "01010101011001100101010101100110011001100101011002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch2"
    assert results[0]["values"] == {"id": 25, "unit": 16, "state": True}


def test_decode_pulses_switch4() -> None:
    results = controller.decode_pulses(
        [295, 1180, 11210], "01010110010101100110011001100110010101100110011002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch4"
    assert results[0]["values"] == {"id": 2, "unit": 20, "state": True}


def test_decode_pulses_switch5_1() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626], "10010101101010010110010110101001010101011010101002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch5"
    assert results[0]["values"] == {
        "id": 465695,
        "unit": 1,
        "all": False,
        "state": True,
    }


def test_decode_pulses_switch5_2() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626], "10010101101010010110010110101001010101011010100102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch5"
    assert results[0]["values"] == {
        "id": 465695,
        "unit": 1,
        "all": False,
        "state": False,
    }


def test_decode_pulses_switch5_3() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626], "10010101101010010110010110101001010101011010011002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch5"
    assert results[0]["values"] == {
        "id": 465695,
        "unit": 2,
        "all": False,
        "state": True,
    }


def test_decode_pulses_switch5_4() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626], "10010101101010010110010110101001010101011010010102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch5"
    assert results[0]["values"] == {
        "id": 465695,
        "unit": 2,
        "all": False,
        "state": False,
    }


def test_decode_pulses_switch5_5() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626], "10010101101010010110010110101001010101011001101002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch5"
    assert results[0]["values"] == {
        "id": 465695,
        "unit": 3,
        "all": False,
        "state": True,
    }


def test_decode_pulses_switch5_6() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626], "10010101101010010110010110101001010101011001100102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch5"
    assert results[0]["values"] == {
        "id": 465695,
        "unit": 3,
        "all": False,
        "state": False,
    }


def test_decode_pulses_switch5_7() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626], "10010101101010010110010110101001010101010110101002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch5"
    assert results[0]["values"] == {
        "id": 465695,
        "unit": 4,
        "all": False,
        "state": True,
    }


def test_decode_pulses_switch5_8() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626], "10010101101010010110010110101001010101010110100102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch5"
    assert results[0]["values"] == {
        "id": 465695,
        "unit": 4,
        "all": False,
        "state": False,
    }


def test_decode_pulses_switch5_9() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626], "10010101101010010110010110101001010101010101011002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch5"
    assert results[0]["values"] == {
        "id": 465695,
        "unit": 0,
        "all": True,
        "state": False,
    }


def test_decode_pulses_switch5_10() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626], "10010101101010010110010110101001010101010101100102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch5"
    assert results[0]["values"] == {
        "id": 465695,
        "unit": 0,
        "all": True,
        "state": True,
    }


def test_decode_pulses_switch6_1() -> None:
    results = controller.decode_pulses(
        [150, 453, 4733], "10101010101010101010010101100110011001100110010102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch6", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch6"
    assert results[0]["values"] == {
        "id": 31,
        "unit": 1,
        "state": True,
    }


def test_decode_pulses_switch6_2() -> None:
    results = controller.decode_pulses(
        [150, 453, 4733], "10101010101010100110011001010110011001100110010102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch6", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch6"
    assert results[0]["values"] == {
        "id": 15,
        "unit": 2,
        "state": True,
    }


def test_decode_pulses_switch7_1() -> None:
    results = controller.decode_pulses(
        [307, 944, 9712], "01010101010101100110011001100110011001100110011002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch7", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch7"
    assert results[0]["values"] == {"id": 0, "unit": 3, "state": True}


def test_decode_pulses_switch7_2() -> None:
    results = controller.decode_pulses(
        [307, 944, 9712], "01010101010101100101010101010110011001100110011002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch7", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch7"
    assert results[0]["values"] == {"id": 7, "unit": 3, "state": True}


def test_decode_pulses_switch7_3() -> None:
    results = controller.decode_pulses(
        [307, 944, 9712], "10100101011001100101010101010110011001100110011002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch7", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch7"
    assert results[0]["values"] == {"id": 7, "unit": 1, "state": False}


def test_decode_pulses_switch8_1() -> None:
    results = controller.decode_pulses(
        [173, 563, 5740], "01010101010101010110011001100110101001011010010102"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch8", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch8"
    assert results[0]["values"] == {
        "id": 30,
        "unit": "B1",
        "state": False,
    }


def test_decode_pulses_switch8_2() -> None:
    results = controller.decode_pulses(
        [173, 563, 5740], "01010101010101010110011001101010010101010101101002"
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch8", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch8"
    assert results[0]["values"] == {
        "id": 30,
        "unit": "C3",
        "state": True,
    }


def test_decode_pulses_switch9_1() -> None:
    results = controller.decode_pulses(
        [305, 615, 23020],
        "0110100101100110011010101001101010101001011012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch9", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch9"
    assert results[0]["values"] == {"id": 2472, "unit": 65, "state": True}


def test_decode_pulses_switch9_2() -> None:
    results = controller.decode_pulses(
        [305, 615, 23020],
        "0110100101100110011010101001101010101001101012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch9", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch9"
    assert results[0]["values"] == {"id": 2472, "unit": 65, "state": False}


def test_decode_pulses_switch9_3() -> None:
    results = controller.decode_pulses(
        [305, 615, 23020],
        "0110100101100110011010101001101010101010011012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch9", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch9"
    assert results[0]["values"] == {"id": 2472, "unit": 64, "state": True}


def test_decode_pulses_switch9_4() -> None:
    results = controller.decode_pulses(
        [305, 615, 23020],
        "0110100101100110011010101001101010010101100112",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch9", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch9"
    assert results[0]["values"] == {"id": 2472, "unit": 71, "state": False}


def test_decode_pulses_switch10() -> None:
    results = controller.decode_pulses(
        [271, 1254, 10092],
        "01010000000101010100000100010101010000000101010100000101000100000101000101010001000100010001010001000101000000010102",
    )
    assert results is not None
    assert len(results) == 1
    assert results[0]["protocol"] == "switch10"
    assert results[0]["values"] == {
        "id": 3162089194,
        "unit": 35,
        "all": False,
        "state": False,
    }


def test_decode_pulses_switch11_1() -> None:
    results = controller.decode_pulses(
        [566, 1267, 6992],
        "100101010110011010101001101001010101100110010110011010100110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch11", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch11"
    assert results[0]["values"] == {"id": 34037, "unit": 1, "state": True}


def test_decode_pulses_switch11_2() -> None:
    results = controller.decode_pulses(
        [566, 1267, 6992],
        "100101011010011010101001101001010101100110010110011010100110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch11", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch11"
    assert results[0]["values"] == {"id": 34037, "unit": 1, "state": False}


def test_decode_pulses_switch11_3() -> None:
    results = controller.decode_pulses(
        [566, 1267, 6992],
        "100101101001011010101001101001010101100110010110011010100110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch11", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch11"
    assert results[0]["values"] == {"id": 34037, "unit": 0, "state": True}


def test_decode_pulses_switch11_4() -> None:
    results = controller.decode_pulses(
        [566, 1267, 6992],
        "100101100110011010101001101001010101100110010110011010100110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch11", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch11"
    assert results[0]["values"] == {"id": 34037, "unit": 0, "state": False}


def test_decode_pulses_switch12_1() -> None:
    results = controller.decode_pulses(
        [564, 1307, 3237, 51535],
        "1202021212021212121212121212021212121212121212121203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch12", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch12"
    assert results[0]["values"] == {"id": 9983, "unit": 1, "state": True}


def test_decode_pulses_switch12_2() -> None:
    results = controller.decode_pulses(
        [564, 1307, 3237, 51535],
        "1202021212021212121212121212121212121202121202021203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch12", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch12"
    assert results[0]["values"] == {"id": 9983, "unit": 1, "state": False}


def test_decode_pulses_switch12_3() -> None:
    results = controller.decode_pulses(
        [564, 1307, 3237, 51535],
        "1202021212021212121212121212121212021212121202120213",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch12", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch12"
    assert results[0]["values"] == {"id": 9983, "unit": 2, "state": True}


def test_decode_pulses_switch12_4() -> None:
    results = controller.decode_pulses(
        [564, 1307, 3237, 51535],
        "1202021212021212121212121212121202121212121202120203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch12", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch12"
    assert results[0]["values"] == {"id": 9983, "unit": 3, "state": True}


def test_decode_pulses_switch13_1() -> None:
    results = controller.decode_pulses(
        [700, 1400, 81000],
        "001100110101001010101010101010110010101102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch13", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch13"
    assert results[0]["values"] == {
        "id": 1472,
        "unit": 0,
        "all": False,
        "state": True,
        "dimm": False,
    }


def test_decode_pulses_switch13_2() -> None:
    results = controller.decode_pulses(
        [700, 1400, 81000],
        "001100110101001010101010101010101010101012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch13", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch13"
    assert results[0]["values"] == {
        "id": 1472,
        "unit": 0,
        "all": False,
        "state": False,
        "dimm": False,
    }


def test_decode_pulses_switch13_3() -> None:
    results = controller.decode_pulses(
        [700, 1400, 81000],
        "001100110101001010101010101010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch13", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch13"
    assert results[0]["values"] == {
        "id": 1472,
        "unit": 0,
        "all": False,
        "state": False,
        "dimm": True,
    }


def test_decode_pulses_switch13_4() -> None:
    results = controller.decode_pulses(
        [700, 1400, 81000],
        "001100110101001010101010101010110100110102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch13", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch13"
    assert results[0]["values"] == {
        "id": 1472,
        "unit": 0,
        "all": False,
        "state": True,
        "dimm": True,
    }


def test_decode_pulses_switch14_1() -> None:
    results = controller.decode_pulses(
        [208, 624, 6556],
        "01010101010101010101010101010101010101011010101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch14", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch14"
    assert results[0]["values"] == {"id": 0, "unit": 1, "all": False, "state": True}


def test_decode_pulses_switch14_2() -> None:
    results = controller.decode_pulses(
        [208, 624, 6556],
        "01010101010101010101010101010101010101011010100102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch14", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch14"
    assert results[0]["values"] == {"id": 0, "unit": 1, "all": False, "state": False}


def test_decode_pulses_switch14_3() -> None:
    results = controller.decode_pulses(
        [208, 624, 6556],
        "01010101010101010101010101010101010101010110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch14", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch14"
    assert results[0]["values"] == {"id": 0, "unit": 2, "all": False, "state": True}


def test_decode_pulses_switch14_4() -> None:
    results = controller.decode_pulses(
        [208, 624, 6556],
        "01010101010101010101010101010101010101011010010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch14", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch14"
    assert results[0]["values"] == {"id": 0, "unit": 1, "all": True, "state": False}


def test_decode_pulses_switch15_1() -> None:
    results = controller.decode_pulses(
        [300, 914, 9624],
        "01101001011001100110010110011010101001011010101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch15", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch15"
    assert results[0]["values"] == {
        "id": 414908,
        "unit": 1,
        "state": True,
        "all": False,
    }


def test_decode_pulses_switch15_2() -> None:
    results = controller.decode_pulses(
        [300, 914, 9624],
        "01101001011001100110010110011010101001010110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch15", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch15"
    assert results[0]["values"] == {
        "id": 414908,
        "unit": 1,
        "state": False,
        "all": False,
    }


def test_decode_pulses_switch15_3() -> None:
    results = controller.decode_pulses(
        [300, 914, 9624],
        "01101001011001100110010110011010101001011001101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch15", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch15"
    assert results[0]["values"] == {
        "id": 414908,
        "unit": 2,
        "state": True,
        "all": False,
    }


def test_decode_pulses_switch15_4() -> None:
    results = controller.decode_pulses(
        [300, 914, 9624],
        "01101001011001100110010110011010101001011001010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch15", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch15"
    assert results[0]["values"] == {
        "id": 414908,
        "unit": 0,
        "state": False,
        "all": True,
    }


def test_decode_pulses_switch16_1() -> None:
    results = controller.decode_pulses(
        [330, 1000, 10500],
        "01010110011001100101011001100110011001100110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch16"
    assert results[0]["values"] == {"id": "A", "unit": 1, "state": True}


def test_decode_pulses_switch16_2() -> None:
    results = controller.decode_pulses(
        [330, 1000, 10500],
        "01010110011001100101011001100110011001100110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch16"
    assert results[0]["values"] == {"id": "A", "unit": 1, "state": False}


def test_decode_pulses_switch16_3() -> None:
    results = controller.decode_pulses(
        [330, 1000, 10500],
        "01010110011001100110010101100110011001100110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch16"
    assert results[0]["values"] == {"id": "A", "unit": 2, "state": True}


def test_decode_pulses_switch16_4() -> None:
    results = controller.decode_pulses(
        [330, 1000, 10500],
        "01010110011001100110010101100110011001100110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch16"
    assert results[0]["values"] == {"id": "A", "unit": 2, "state": False}


def test_decode_pulses_switch16_5() -> None:
    results = controller.decode_pulses(
        [330, 1000, 10500],
        "01010110011001100110011001100110011001100110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch16"
    assert results[0]["values"] == {"id": "A", "unit": 3, "state": True}


def test_decode_pulses_switch16_6() -> None:
    results = controller.decode_pulses(
        [330, 1000, 10500],
        "01010110011001100110011001010110011001100110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch16"
    assert results[0]["values"] == {"id": "A", "unit": 3, "state": False}


def test_decode_pulses_switch16_7() -> None:
    results = controller.decode_pulses(
        [330, 1000, 10500],
        "01100101011001100101011001100110011001100110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch16"
    assert results[0]["values"] == {"id": "B", "unit": 1, "state": True}


def test_decode_pulses_switch16_8() -> None:
    results = controller.decode_pulses(
        [330, 1000, 10500],
        "01100101011001100101011001100110011001100110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch16"
    assert results[0]["values"] == {"id": "B", "unit": 1, "state": False}


def test_decode_pulses_switch16_9() -> None:
    results = controller.decode_pulses(
        [330, 1000, 10500],
        "01100101011001100110011001100110011001100110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch16"
    assert results[0]["values"] == {"id": "B", "unit": 3, "state": True}


def test_decode_pulses_switch16_10() -> None:
    results = controller.decode_pulses(
        [330, 1000, 10500],
        "01100101011001100110011001010110011001100110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch16", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch16"
    assert results[0]["values"] == {"id": "B", "unit": 3, "state": False}


def test_decode_pulses_switch17() -> None:
    results = controller.decode_pulses(
        [260, 2680, 1275, 10550],
        "010200020002000002000200020200020002000200020000020200000202000200020002000200020002000200000200020200000200020200020002000002020003",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch17", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch17"
    assert results[0]["values"] == {
        "id": 59748338,
        "all": False,
        "state": True,
        "unit": 13,
    }


def test_decode_pulses_switch21_1() -> None:
    results = controller.decode_pulses(
        [204, 328, 1348, 10320],
        "010201010101010202010201010101010101010201020101010201010202010201010101010101020101020101020101020101010101020102020102010101010201010101020103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch21", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch21"
    assert results[0]["values"] == {"id": 15814908, "unit": 0, "state": True}


def test_decode_pulses_switch21_2() -> None:
    results = controller.decode_pulses(
        [204, 328, 1348, 10320],
        "010101020101010201010101020102010101010201020101010102010202010201010101010101020101020101020101020101010101020102020102010101010201010101020103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch21", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch21"
    assert results[0]["values"] == {"id": 15814908, "unit": 0, "state": False}


def test_decode_pulses_switch22_1() -> None:
    results = controller.decode_pulses(
        [376, 1144, 11720],
        "01100110101010101001100101010101101010010101011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch22", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch22"
    assert results[0]["values"] == {"id": 656881, "command": "A"}


def test_decode_pulses_switch22_2() -> None:
    results = controller.decode_pulses(
        [376, 1144, 11720],
        "01100110101010101001100101010101101010010101100102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch22", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch22"
    assert results[0]["values"] == {"id": 656881, "command": "B"}


def test_decode_pulses_switch22_3() -> None:
    results = controller.decode_pulses(
        [376, 1144, 11720],
        "01100110101010101001100101010101101010010110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch22", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch22"
    assert results[0]["values"] == {"id": 656881, "command": "C"}


def test_decode_pulses_switch22_4() -> None:
    results = controller.decode_pulses(
        [376, 1144, 11720],
        "01100110101010101001100101010101101010011001010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch22", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch22"
    assert results[0]["values"] == {"id": 656881, "command": "D"}


def test_decode_pulses_switch23_1() -> None:
    results = controller.decode_pulses(
        [356, 716, 15728],
        "00110011001100110011010100110011001012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch23", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch23"
    assert results[0]["values"] == {"id": 10914, "command": "C"}


def test_decode_pulses_switch23_2() -> None:
    results = controller.decode_pulses(
        [356, 716, 15728],
        "00110011001100110011010100110011010012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch23", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch23"
    assert results[0]["values"] == {"id": 10914, "command": "D"}


def test_decode_pulses_switch23_3() -> None:
    results = controller.decode_pulses(
        [356, 716, 15728],
        "00110011001100110011010100110010101102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch23", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch23"
    assert results[0]["values"] == {"id": 10914, "command": "A"}


def test_decode_pulses_switch23_4() -> None:
    results = controller.decode_pulses(
        [356, 716, 15728],
        "00110011001100110011010100110010110102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch23", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch23"
    assert results[0]["values"] == {"id": 10914, "command": "B"}


def test_decode_pulses_switch24() -> None:
    results = controller.decode_pulses(
        [504, 1024, 6120],
        "01101010010101011010101010011010100101010101011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch24", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch24"
    assert results[0]["values"] == {"id": 17, "unit": 1, "state": True}


def test_decode_pulses_switch25_1() -> None:
    results = controller.decode_pulses(
        [350, 880, 10970],
        "101010101010101010101010101010100101010101010101011010100110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch25", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch25"
    assert results[0]["values"] == {"id": 0, "unit": 14, "state": True}


def test_decode_pulses_switch25_2() -> None:
    results = controller.decode_pulses(
        [350, 880, 10970],
        "101010101010101010101010101010100101010101010101011010100101101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch25", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch25"
    assert results[0]["values"] == {"id": 0, "state": False, "unit": 14}


def test_decode_pulses_switch25_3() -> None:
    results = controller.decode_pulses(
        [350, 880, 10970],
        "101010101010101010101010101010100101010101010101011001101010011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch25", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch25"
    assert results[0]["values"] == {"id": 0, "state": True, "unit": 11}


def test_decode_pulses_switch25_4() -> None:
    results = controller.decode_pulses(
        [350, 880, 10970],
        "101010101010101010101010101010100101010101010101011001101001101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch25", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch25"
    assert results[0]["values"] == {"id": 0, "state": False, "unit": 11}


def test_decode_pulses_switch25_5() -> None:
    results = controller.decode_pulses(
        [350, 880, 10970],
        "101010101010101010101010101010100101010101010101010110101010011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch25", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch25"
    assert results[0]["values"] == {"id": 0, "state": True, "unit": 7}


def test_decode_pulses_switch25_6() -> None:
    results = controller.decode_pulses(
        [350, 880, 10970],
        "101010101010101010101010101010100101010101010101010110101001101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch25", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch25"
    assert results[0]["values"] == {"id": 0, "state": False, "unit": 7}


def test_decode_pulses_switch25_7() -> None:
    results = controller.decode_pulses(
        [350, 880, 10970],
        "101010101010101010101010101010100101010101010101011010011010011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch25", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch25"
    assert results[0]["values"] == {"id": 0, "state": True, "unit": 13}


def test_decode_pulses_switch25_8() -> None:
    results = controller.decode_pulses(
        [350, 880, 10970],
        "101010101010101010101010101010100101010101010101011010011001101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch25", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch25"
    assert results[0]["values"] == {"id": 0, "state": False, "unit": 13}


def test_decode_pulses_switch25_9() -> None:
    results = controller.decode_pulses(
        [350, 880, 10970],
        "101010101010101010101010101010100101010101010101010101010110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch25", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch25"
    assert results[0]["values"] == {"id": 0, "state": True, "unit": 0}


def test_decode_pulses_switch25_10() -> None:
    results = controller.decode_pulses(
        [350, 880, 10970],
        "101010101010101010101010101010100101010101010101010101010101101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch25", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch25"
    assert results[0]["values"] == {"id": 0, "state": False, "unit": 0}


def test_decode_pulses_switch26_1() -> None:
    results = controller.decode_pulses(
        [480, 1476, 15260],
        "01010110011001100110010101100110011001100110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch26", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch26"
    assert results[0]["values"] == {"id": "A", "unit": 3, "state": True}


def test_decode_pulses_switch26_2() -> None:
    results = controller.decode_pulses(
        [480, 1476, 15260],
        "01010110011001100110011001010110011001100110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch26", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch26"
    assert results[0]["values"] == {"id": "A", "unit": 4, "state": True}


def test_decode_pulses_switch26_3() -> None:
    results = controller.decode_pulses(
        [480, 1476, 15260],
        "01010110011001100110011001010110011001100110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch26", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch26"
    assert results[0]["values"] == {"id": "A", "unit": 4, "state": False}


def test_decode_pulses_switch27_1() -> None:
    results = controller.decode_pulses(
        [325, 972, 10130],
        "01100110011001100101011001100110011001100110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch27", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch27"
    assert results[0]["values"] == {"id": "A", "unit": 1, "state": True}


def test_decode_pulses_switch27_2() -> None:
    results = controller.decode_pulses(
        [325, 972, 10130],
        "01100110010101100101011001100110011001100110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch27", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch27"
    assert results[0]["values"] == {"id": "C", "unit": 1, "state": True}


def test_decode_pulses_switch27_3() -> None:
    results = controller.decode_pulses(
        [325, 972, 10130],
        "01100110011001010101011001100110011001100110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch27", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch27"
    assert results[0]["values"] == {"id": "D", "unit": 1, "state": True}


def test_decode_pulses_switch28_1() -> None:
    results = controller.decode_pulses(
        [417, 1287, 13042],
        "01010110010101100101011001100110011001010101101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch28", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch28"
    assert results[0]["values"] == {
        "id": 11316396,
        "unit": 26213,
        "state": True,
        "all": False,
    }


def test_decode_pulses_switch28_2() -> None:
    results = controller.decode_pulses(
        [310, 524, 1287, 13042],
        "02020221020202210202022102210221022102020202212103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch28", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch28"
    assert results[0]["values"] == {
        "id": 11316396,
        "unit": 26213,
        "state": True,
        "all": False,
    }


def test_decode_pulses_switch28_3() -> None:
    results = controller.decode_pulses(
        [417, 1287, 13042],
        "01010110010101100101011001100110011001011010010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch28", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch28"
    assert results[0]["values"] == {
        "id": 11316396,
        "unit": 26213,
        "state": False,
        "all": False,
    }


def test_decode_pulses_switch28_4() -> None:
    results = controller.decode_pulses(
        [310, 524, 1287, 13042],
        "02020221020202210202022102210221022102022121020203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch28", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch28"
    assert results[0]["values"] == {
        "id": 11316396,
        "unit": 26213,
        "state": False,
        "all": False,
    }


def test_decode_pulses_switch28_5() -> None:
    results = controller.decode_pulses(
        [417, 1287, 13042],
        "01010110010101100101011001100110011001010101010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch28", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch28"
    assert results[0]["values"] == {
        "id": 11316396,
        "unit": 26213,
        "state": None,
        "all": True,
    }


def test_decode_pulses_switch28_6() -> None:
    results = controller.decode_pulses(
        [310, 524, 1287, 13042],
        "02020221020202210202022102210221022102020202020203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch28", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch28"
    assert results[0]["values"] == {
        "id": 11316396,
        "unit": 26213,
        "state": None,
        "all": True,
    }


def test_decode_pulses_switch29_1() -> None:
    results = controller.decode_pulses(
        [404, 804, 4028],
        "00101011101010101101001010101010111000110010101010110010101011001011010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch29", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch29"
    assert results[0]["values"] == {"id": 5723557, "unit": 5621333, "command": "arm"}


def test_decode_pulses_switch29_2() -> None:
    results = controller.decode_pulses(
        [404, 804, 4028],
        "00101011101010101101001010101010111000110010101010101011001011001010110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch29", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch29"
    assert results[0]["values"] == {"id": 5723557, "unit": 5621333, "command": "panic"}


def test_decode_pulses_switch29_3() -> None:
    results = controller.decode_pulses(
        [404, 804, 4028],
        "00101011101010101101001010101010111000110010101011001010101011001100110102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch29", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch29"
    assert results[0]["values"] == {"id": 5723557, "unit": 5621333, "command": "disarm"}


def test_decode_pulses_switch29_4() -> None:
    results = controller.decode_pulses(
        [404, 804, 4028],
        "00101011101010101101001010101010111000110010101010101100101011001010101102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch29", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch29"
    assert results[0]["values"] == {"id": 5723557, "unit": 5621333, "command": "home"}


def test_decode_pulses_switch29_5() -> None:
    results = controller.decode_pulses(
        [404, 804, 4028],
        "00101011101010101101001010101010111000110010101011010010101011001101010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch29", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch29"
    assert results[0]["values"] == {"id": 5723557, "unit": 5621333, "command": "grp1"}


def test_decode_pulses_switch29_6() -> None:
    results = controller.decode_pulses(
        [404, 804, 4028],
        "00101011101010101101001010101010111000110010101011001100101011001100101102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch29", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch29"
    assert results[0]["values"] == {"id": 5723557, "unit": 5621333, "command": "grp2"}


def test_decode_pulses_switch29_7() -> None:
    results = controller.decode_pulses(
        [404, 804, 4028],
        "00101011101010101101001010101010111000110010101011010100101011001101001102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch29", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch29"
    assert results[0]["values"] == {"id": 5723557, "unit": 5621333, "command": "grp3"}


def test_decode_pulses_switch30_1() -> None:
    results = controller.decode_pulses(
        [520, 1468, 13312],
        "01010101010110100101101001001110101001010101010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch30", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch30"
    assert results[0]["values"] == {"id": 21850, "unit": 23118, "command": "arm"}


def test_decode_pulses_switch30_2() -> None:
    results = controller.decode_pulses(
        [520, 1468, 13312],
        "01010101010110100101101001001110010101011010010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch30", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch30"
    assert results[0]["values"] == {"id": 21850, "unit": 23118, "command": "dis"}


def test_decode_pulses_switch30_3() -> None:
    results = controller.decode_pulses(
        [520, 1468, 13312],
        "01010101010110100101101001001110010101010101101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch30", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch30"
    assert results[0]["values"] == {"id": 21850, "unit": 23118, "command": "byp"}


def test_decode_pulses_switch30_4() -> None:
    results = controller.decode_pulses(
        [520, 1468, 13312],
        "01010101010110100101101001001110010110100101010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch30", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch30"
    assert results[0]["values"] == {"id": 21850, "unit": 23118, "command": "sos"}


def test_decode_pulses_switch31_1() -> None:
    results = controller.decode_pulses(
        [452, 1336, 3392, 10124],
        "0000220100010101000000010101000001000100010000000101010000000101000100010000000001010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch31", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch31"
    assert results[0]["values"] == {"id": 47333, "unit": 1, "state": True, "all": False}


def test_decode_pulses_switch31_2() -> None:
    results = controller.decode_pulses(
        [452, 1336, 3392, 10124],
        "0000220100010101000000010101000001000100010000000101010000000101000100000101010100000003",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch31", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch31"
    assert results[0]["values"] == {
        "id": 47333,
        "unit": 1,
        "state": False,
        "all": False,
    }


def test_decode_pulses_switch31_3() -> None:
    results = controller.decode_pulses(
        [452, 1336, 3392, 10124],
        "0000220100010101000000010101000001000100010000000101010000000101000100000100000100010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch31", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch31"
    assert results[0]["values"] == {"id": 47333, "unit": 2, "state": True, "all": False}


def test_decode_pulses_switch31_4() -> None:
    results = controller.decode_pulses(
        [452, 1336, 3392, 10124],
        "0000220100010101000000010101000001000100010000000101010000000101000100010001010001000003",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch31", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch31"
    assert results[0]["values"] == {
        "id": 47333,
        "unit": 2,
        "state": False,
        "all": False,
    }


def test_decode_pulses_switch31_5() -> None:
    results = controller.decode_pulses(
        [452, 1336, 3392, 10124],
        "0000220100010101000000010101000001000100010000000101010000000101000100010100000000010103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch31", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch31"
    assert results[0]["values"] == {"id": 47333, "unit": 3, "state": True, "all": False}


def test_decode_pulses_switch31_6() -> None:
    results = controller.decode_pulses(
        [452, 1336, 3392, 10124],
        "0000220100010101000000010101000001000100010000000101010000000101000100000001010101000003",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch31", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch31"
    assert results[0]["values"] == {
        "id": 47333,
        "unit": 3,
        "state": False,
        "all": False,
    }


def test_decode_pulses_switch31_7() -> None:
    results = controller.decode_pulses(
        [452, 1336, 3392, 10124],
        "0000220100010101000000010101000001000100010000000101010000000101000100000001000101000103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch31", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch31"
    assert results[0]["values"] == {"id": 47333, "unit": 4, "state": True, "all": False}


def test_decode_pulses_switch31_8() -> None:
    results = controller.decode_pulses(
        [452, 1336, 3392, 10124],
        "0000220100010101000000010101000001000100010000000101010000000101000100010100010000010003",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch31", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch31"
    assert results[0]["values"] == {
        "id": 47333,
        "unit": 4,
        "state": False,
        "all": False,
    }


def test_decode_pulses_switch31_9() -> None:
    results = controller.decode_pulses(
        [452, 1336, 3392, 10124],
        "0000220100010101000000010101000001000100010000000101010000000101000100010001000001000103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch31", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch31"
    assert results[0]["values"] == {"id": 47333, "unit": 5, "state": True, "all": True}


def test_decode_pulses_switch31_10() -> None:
    results = controller.decode_pulses(
        [452, 1336, 3392, 10124],
        "0000220100010101000000010101000001000100010000000101010000000101000100000100010100010003",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch31", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch31"
    assert results[0]["values"] == {"id": 47333, "unit": 5, "state": False, "all": True}


def test_decode_pulses_switch32_1() -> None:
    results = controller.decode_pulses(
        [440, 1300, 13488],
        "01010110011001100101011001100110011001100110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch32", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch32"
    assert results[0]["values"] == {"id": 1, "unit": 1, "state": True}


def test_decode_pulses_switch32_2() -> None:
    results = controller.decode_pulses(
        [440, 1300, 13488],
        "01010110011001100101011001100110011001100110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch32", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch32"
    assert results[0]["values"] == {"id": 1, "unit": 1, "state": False}


def test_decode_pulses_switch32_3() -> None:
    results = controller.decode_pulses(
        [440, 1300, 13488],
        "01010110011001100110010101100110011001100110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch32", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch32"
    assert results[0]["values"] == {"id": 1, "unit": 2, "state": True}


def test_decode_pulses_switch32_4() -> None:
    results = controller.decode_pulses(
        [440, 1300, 13488],
        "01010110011001100110010101100110011001100110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch32", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch32"
    assert results[0]["values"] == {"id": 1, "unit": 2, "state": False}


def test_decode_pulses_switch32_5() -> None:
    results = controller.decode_pulses(
        [440, 1300, 13488],
        "01010110011001100110011001010110011001100110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch32", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch32"
    assert results[0]["values"] == {"id": 1, "unit": 3, "state": True}


def test_decode_pulses_switch32_6() -> None:
    results = controller.decode_pulses(
        [440, 1300, 13488],
        "01010110011001100110011001010110011001100110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch32", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch32"
    assert results[0]["values"] == {"id": 1, "unit": 3, "state": False}


def test_decode_pulses_switch32_7() -> None:
    results = controller.decode_pulses(
        [440, 1300, 13488],
        "01010110011001100110011001100101011001100110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch32", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch32"
    assert results[0]["values"] == {"id": 1, "unit": 4, "state": True}


def test_decode_pulses_switch32_8() -> None:
    results = controller.decode_pulses(
        [440, 1300, 13488],
        "01010110011001100110011001100101011001100110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch32", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch32"
    assert results[0]["values"] == {"id": 1, "unit": 4, "state": False}


def test_decode_pulses_switch32_9() -> None:
    results = controller.decode_pulses(
        [440, 1300, 13488],
        "01100101011001100101011001100110011001100110011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch32", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch32"
    assert results[0]["values"] == {"id": 2, "unit": 1, "state": True}


def test_decode_pulses_switch33_1() -> None:
    results = controller.decode_pulses(
        [700, 1340, 15000],
        "010011010010101010101010101100110010101012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch33", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch33"
    assert results[0]["values"] == {
        "id": 2816,
        "unit": 1,
        "all": False,
        "state": True,
        "dimm": False,
    }


def test_decode_pulses_switch33_2() -> None:
    results = controller.decode_pulses(
        [700, 1340, 15000],
        "010011010010101010101010110010110010110102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch33", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch33"
    assert results[0]["values"] == {
        "id": 2816,
        "unit": 2,
        "all": False,
        "state": True,
        "dimm": False,
    }


def test_decode_pulses_switch33_3() -> None:
    results = controller.decode_pulses(
        [700, 1340, 15000],
        "010011010010101010101010110010101010110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch33", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch33"
    assert results[0]["values"] == {
        "id": 2816,
        "unit": 2,
        "all": False,
        "state": False,
        "dimm": False,
    }


def test_decode_pulses_switch33_4() -> None:
    results = controller.decode_pulses(
        [700, 1340, 15000],
        "010011010010101010101010110100110010110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch33", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch33"
    assert results[0]["values"] == {
        "id": 2816,
        "unit": 3,
        "all": False,
        "state": True,
        "dimm": False,
    }


def test_decode_pulses_switch33_5() -> None:
    results = controller.decode_pulses(
        [700, 1340, 15000],
        "010011010010101010101010110100101010110102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch33", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch33"
    assert results[0]["values"] == {
        "id": 2816,
        "unit": 3,
        "all": False,
        "state": False,
        "dimm": False,
    }


def test_decode_pulses_switch33_6() -> None:
    results = controller.decode_pulses(
        [700, 1340, 15000],
        "010011010010101010101010110101010010101012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch33", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch33"
    assert results[0]["values"] == {
        "id": 2816,
        "unit": 3,
        "all": True,
        "state": True,
        "dimm": False,
    }


def test_decode_pulses_switch33_7() -> None:
    results = controller.decode_pulses(
        [700, 1340, 15000],
        "010011010010101010101010110101001010101102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch33", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch33"
    assert results[0]["values"] == {
        "id": 2816,
        "unit": 3,
        "all": True,
        "state": False,
        "dimm": False,
    }


def test_decode_pulses_switch33_8() -> None:
    results = controller.decode_pulses(
        [700, 1340, 15000],
        "010011010010101010101010110101010100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch33", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch33"
    assert results[0]["values"] == {
        "id": 2816,
        "unit": 3,
        "all": True,
        "state": True,
        "dimm": True,
    }


def test_decode_pulses_switch33_9() -> None:
    results = controller.decode_pulses(
        [700, 1340, 15000],
        "010011010010101010101010110101001100110102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch33", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch33"
    assert results[0]["values"] == {
        "id": 2816,
        "unit": 3,
        "all": True,
        "state": False,
        "dimm": True,
    }


def test_decode_pulses_switch34() -> None:
    results = controller.decode_pulses(
        [316, 844, 10360],
        "01010101101010011001010101011010010101011001010110010101010110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "switch34", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "switch34"
    assert results[0]["values"] == {
        "bits": "000011101000001100001000100000100",
        "bytes": [14, 131, 8, 130],
        "id": 7430,
        "unit": 8,
        "all": True,
        "state": True,
    }


def test_decode_pulses_rolling1_1() -> None:
    results = controller.decode_pulses(
        [500, 1000, 3000, 7250],
        "01101010100101011001101010010110100110100101100123",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "rolling1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "rolling1"
    assert results[0]["values"] == {"code": "011110001011100110110010"}


def test_decode_pulses_rolling1_2() -> None:
    results = controller.decode_pulses(
        [500, 1000, 3000, 7250],
        "01101010011010011010011010010101100110011010100123",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "rolling1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "rolling1"
    assert results[0]["values"] == {"code": "011101101101100010101110"}


def test_decode_pulses_rolling1_3() -> None:
    results = controller.decode_pulses(
        [500, 1000, 3000, 7250],
        "01101010011010011010011010010101100110011010010123",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "rolling1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "rolling1"
    assert results[0]["values"] == {"code": "011101101101100010101100"}


def test_decode_pulses_doorbell1() -> None:
    results = controller.decode_pulses(
        [217, 648, 6696],
        "01101010011001100110011010101010101010101010101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell1"
    assert results[0]["values"] == {"id": 1361, "unit": 0, "state": True}


def test_decode_pulses_doorbell3_1() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "00101010101010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 0, "unit": 10}


def test_decode_pulses_doorbell3_2() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "01010010101010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 12, "unit": 10}


def test_decode_pulses_doorbell3_3() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "00110010101010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 4, "unit": 10}


def test_decode_pulses_doorbell3_4() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "01010101001010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 15, "unit": 10}


def test_decode_pulses_doorbell3_5() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "00110101001010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 7, "unit": 10}


def test_decode_pulses_doorbell3_6() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "01001101001010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 11, "unit": 10}


def test_decode_pulses_doorbell3_7() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "00101101001010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 3, "unit": 10}


def test_decode_pulses_doorbell3_8() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "01001100101010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 10, "unit": 10}


def test_decode_pulses_doorbell3_9() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "00101100101010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 2, "unit": 10}


def test_decode_pulses_doorbell3_10() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "01010100101010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 14, "unit": 10}


def test_decode_pulses_doorbell3_11() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "00110100101010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 6, "unit": 10}


def test_decode_pulses_doorbell3_12() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "01010011001010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 13, "unit": 10}


def test_decode_pulses_doorbell3_13() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "00110011001010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 5, "unit": 10}


def test_decode_pulses_doorbell3_14() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "01001011001010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 9, "unit": 10}


def test_decode_pulses_doorbell3_15() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "00101011001010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 1, "unit": 10}


def test_decode_pulses_doorbell3_16() -> None:
    results = controller.decode_pulses(
        [300, 580, 10224],
        "01001010101010101100110012",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "doorbell3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "doorbell3"
    assert results[0]["values"] == {"id": 8, "unit": 10}


def test_decode_pulses_contact1_1() -> None:
    results = controller.decode_pulses(
        [268, 1282, 2632, 10168],
        "0200010001010001000001000100010100010000010100010001000100010000010100000100010001010001000001010001000001000101000100000100010100000101000001000103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "contact1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "contact1"
    assert results[0]["values"] == {
        "id": 13040182,
        "all": False,
        "state": False,
        "unit": 9,
    }


def test_decode_pulses_contact1_2() -> None:
    results = controller.decode_pulses(
        [268, 1282, 2632, 10168],
        "020001000101000100000100010001010001000001010001000100010001000001010000010001000101000100000101000100000100010001010000010001010003",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "contact1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "contact1"
    assert results[0]["values"] == {
        "id": 13040182,
        "all": False,
        "state": True,
        "unit": 9,
    }


def test_decode_pulses_contact2_1() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626],
        "10010110100101011010101010011001010101011001010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "contact2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "contact2"
    assert results[0]["values"] == {"id": 421983, "state": False}


def test_decode_pulses_contact2_2() -> None:
    results = controller.decode_pulses(
        [295, 886, 9626],
        "10010110100110011010010101101001010101011001010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "contact2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "contact2"
    assert results[0]["values"] == {"id": 414623, "state": False}


def test_decode_pulses_contact4_1() -> None:
    results = controller.decode_pulses(
        [468, 1364, 14096],
        "10101001100110011001011010100101010101011001100102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "contact4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "contact4"
    assert results[0]["values"] == {"id": 960960, "state": False, "lowBattery": False}


def test_decode_pulses_contact4_2() -> None:
    results = controller.decode_pulses(
        [468, 1364, 14096],
        "10101001100110011001011010100101010101011010100102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "contact4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "contact4"
    assert results[0]["values"] == {"id": 960960, "state": True, "lowBattery": False}


def test_decode_pulses_contact4_3() -> None:
    results = controller.decode_pulses(
        [468, 1364, 14096],
        "10101001100110011001011010100101010101010110100102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "contact4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "contact4"
    assert results[0]["values"] == {"id": 960960, "state": True, "lowBattery": True}


def test_decode_pulses_led1_1() -> None:
    results = controller.decode_pulses(
        [350, 1056, 10904],
        "01100110100101011001100110101001010110010101011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led1"
    assert results[0]["values"] == {"id": 22702, "command": "on/off"}


def test_decode_pulses_led1_2() -> None:
    results = controller.decode_pulses(
        [350, 1056, 10904],
        "01011010010101100110011010101001010110010101011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led1"
    assert results[0]["values"] == {"id": 12638, "command": "on/off"}


def test_decode_pulses_led1_3() -> None:
    results = controller.decode_pulses(
        [350, 1056, 10904],
        "01100110100101011001100110101001010110010110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led1"
    assert results[0]["values"] == {"id": 22702, "command": "up"}


def test_decode_pulses_led1_4() -> None:
    results = controller.decode_pulses(
        [350, 1056, 10904],
        "01100110100101011001100110101001010110010101100102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led1", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led1"
    assert results[0]["values"] == {"id": 22702, "command": "down"}


def test_decode_pulses_led2_1() -> None:
    results = controller.decode_pulses(
        [434, 1227, 13016],
        "01010110101001101010100110011001010101100101011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led2"
    assert results[0]["values"] == {"id": 7658, "command": "mode-"}


def test_decode_pulses_led2_2() -> None:
    results = controller.decode_pulses(
        [434, 1227, 13016],
        "01010110101001101010100110011001010101011001011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led2"
    assert results[0]["values"] == {"id": 7658, "command": "25%"}


def test_decode_pulses_led2_3() -> None:
    results = controller.decode_pulses(
        [434, 1227, 13016],
        "01010110101001101010100110011001010101010110101002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led2"
    assert results[0]["values"] == {"id": 7658, "command": "100%"}


def test_decode_pulses_led2_4() -> None:
    results = controller.decode_pulses(
        [434, 1227, 13016],
        "01010110101001101010100110011001010101010101011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led2"
    assert results[0]["values"] == {"id": 7658, "command": "on/off"}


def test_decode_pulses_led2_5() -> None:
    results = controller.decode_pulses(
        [434, 1227, 13016],
        "01010110101001101010100110011001010110010101011002",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led2", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led2"
    assert results[0]["values"] == {"id": 7658, "command": "code:00100001"}


def test_decode_pulses_led4_1() -> None:
    results = controller.decode_pulses(
        [346, 966, 9476],
        "01010101010110100101011010100101100101010110011102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led4"
    assert results[0]["values"] == {"id": 796, "command": "on/off"}


def test_decode_pulses_led4_2() -> None:
    results = controller.decode_pulses(
        [346, 966, 9476],
        "01010101010110100101011010100101100101010101101102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led4"
    assert results[0]["values"] == {"id": 796, "command": "bright+"}


def test_decode_pulses_led4_3() -> None:
    results = controller.decode_pulses(
        [346, 966, 9476],
        "01010101010110100101011010100101100101010110100102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led4"
    assert results[0]["values"] == {"id": 796, "command": "color+"}


def test_decode_pulses_led4_4() -> None:
    results = controller.decode_pulses(
        [346, 966, 9476],
        "01010101010110100101011010100101010101101010011102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led4"
    assert results[0]["values"] == {"id": 796, "command": "code:00011101"}


def test_decode_pulses_led4_5() -> None:
    results = controller.decode_pulses(
        [346, 966, 9476],
        "01010101010110100101011010100101010101010110010102",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "led4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "led4"
    assert results[0]["values"] == {"id": 796, "command": "code:00000100"}


def test_decode_pulses_shutter3_1() -> None:
    results = controller.decode_pulses(
        [366, 736, 1600, 5204, 10896],
        "3210010110010101010110011010011010010110100101011001011001100101101010010110100104",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "shutter3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "shutter3"
    assert results[0]["values"] == {"id": 151368466, "unit": 9, "command": "program"}


def test_decode_pulses_shutter3_2() -> None:
    results = controller.decode_pulses(
        [366, 736, 1600, 5204, 10896],
        "3210011010100110010101101001010110011010011001100110010101010101101010010110100104",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "shutter3", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "shutter3"
    assert results[0]["values"] == {"id": 195237544, "unit": 1, "command": "program"}


def test_decode_pulses_shutter4_1() -> None:
    results = controller.decode_pulses(
        [352, 712, 1476, 5690],
        "3201010110010101100101100101010101100101101010100101011001010101010101011001010113",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "shutter4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "shutter4"
    assert results[0]["values"] == {
        "id": 17959394,
        "unit": 0,
        "all": True,
        "command": "up",
    }


def test_decode_pulses_shutter4_2() -> None:
    results = controller.decode_pulses(
        [352, 712, 1476, 5690],
        "3201010110010101100101100101010101100101101010100101011001010110100110011001100113",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "shutter4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "shutter4"
    assert results[0]["values"] == {
        "id": 17959394,
        "unit": 3,
        "all": False,
        "command": "stop",
    }


def test_decode_pulses_shutter4_3() -> None:
    results = controller.decode_pulses(
        [352, 712, 1476, 5690],
        "3201010110010101100101100101010101100101101010100101011001011001100101101010100103",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "shutter4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "shutter4"
    assert results[0]["values"] == {
        "id": 17959394,
        "unit": 5,
        "all": False,
        "command": "down",
    }


def test_decode_pulses_shutter4_4() -> None:
    results = controller.decode_pulses(
        [352, 712, 1476, 5690],
        "3201011001010101010110010101010101010110100101011001100101100101100101011001010113",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "shutter4", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "shutter4"
    assert results[0]["values"] == {
        "id": 33817364,
        "unit": 9,
        "all": False,
        "command": "up",
    }


def test_decode_pulses_shutter5_1() -> None:
    results = controller.decode_pulses(
        [160, 270, 665, 6856],
        "02210202022102022121022102212121020221212102020203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "shutter5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "shutter5"
    assert results[0]["values"] == {"id": 281971, "command": "stop"}


def test_decode_pulses_shutter5_2() -> None:
    results = controller.decode_pulses(
        [160, 270, 665, 6856],
        "02210202022102022121022102212121020221210202210203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "shutter5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "shutter5"
    assert results[0]["values"] == {"id": 281971, "command": "up"}


def test_decode_pulses_shutter5_3() -> None:
    results = controller.decode_pulses(
        [160, 270, 665, 6856],
        "02210202022102022121022102212121020221210221020203",
    )
    assert results is not None
    results = list(filter(lambda result: result["protocol"] == "shutter5", results))

    assert len(results) == 1
    assert results[0]["protocol"] == "shutter5"
    assert results[0]["values"] == {"id": 281971, "command": "down"}


def test_decode_pulses_fixable() -> None:
    # Should decode fixable pulses.
    results = controller.decode_pulses(
        [258, 401, 1339, 2715, 10424],
        "030002000202000200000202000002020000020002020000020002020000020201020000020200020000020201020002000200000200020002000200020002000204",
    )
    assert len(results) >= 1, "Fixable pulses should be fixed."


def test_decode_pulses_unknown_pulse_length() -> None:
    # Index 3 refers to a fourth pulse length that doesn't exist.
    results = controller.decode_pulses([300, 900, 9000], "01010123")
    assert results == []


def test_decode_pulses_invalid_character() -> None:
    results = controller.decode_pulses([300, 900, 9000], "0101x2")
    assert results == []


def test_decode_pulses_zero_pulse_length_not_at_end() -> None:
    # Filtering the 0 leaves 2 pulse lengths, so index 2 no longer exists.
    results = controller.decode_pulses([300, 0, 900], "0202")
    assert results == []


def test_compress_timings_1() -> None:
    # Should compress the timings.
    result = controller.compress_timings(
        [
            288,
            972,
            292,
            968,
            292,
            972,
            292,
            968,
            292,
            972,
            920,
            344,
            288,
            976,
            920,
            348,
            284,
            976,
            288,
            976,
            284,
            976,
            288,
            976,
            288,
            976,
            916,
            348,
            284,
            980,
            916,
            348,
            284,
            976,
            920,
            348,
            284,
            976,
            920,
            348,
            284,
            980,
            280,
            980,
            284,
            980,
            916,
            348,
            284,
            9808,
        ]
    )
    assert result is not None
    assert result[0] == [304, 959, 9808]
    assert result[1] == "01010101011001100101010101100110011001100101011002"


def test_compress_timings_2() -> None:
    # Should compress the timings.
    result = controller.compress_timings(
        [
            292,
            968,
            292,
            972,
            292,
            972,
            292,
            976,
            288,
            976,
            920,
            344,
            288,
            976,
            920,
            348,
            284,
            976,
            288,
            976,
            288,
            976,
            284,
            980,
            284,
            976,
            920,
            348,
            284,
            976,
            916,
            352,
            280,
            980,
            916,
            352,
            280,
            980,
            916,
            348,
            284,
            980,
            284,
            976,
            284,
            984,
            912,
            352,
            280,
            9808,
        ]
    )
    assert result is not None
    assert result[0] == [304, 959, 9808]
    assert result[1] == "01010101011001100101010101100110011001100101011002"


def test_compress_timings_3() -> None:
    # Should compress the timings.
    result = controller.compress_timings(
        [
            292,
            976,
            288,
            972,
            292,
            972,
            292,
            920,
            288,
            976,
            920,
            344,
            288,
            980,
            916,
            344,
            288,
            980,
            284,
            980,
            284,
            972,
            288,
            980,
            284,
            976,
            920,
            344,
            288,
            976,
            916,
            352,
            280,
            980,
            916,
            348,
            284,
            980,
            916,
            348,
            284,
            980,
            284,
            976,
            288,
            976,
            916,
            352,
            280,
            9804,
        ]
    )
    assert result is not None
    assert result[0] == [304, 957, 9804]
    assert result[1] == "01010101011001100101010101100110011001100101011002"


def test_compress_timings_4() -> None:
    # Should compress the timings.
    result = controller.compress_timings(
        [
            288,
            972,
            292,
            968,
            296,
            972,
            296,
            976,
            288,
            976,
            920,
            344,
            288,
            976,
            920,
            344,
            292,
            972,
            288,
            976,
            288,
            976,
            284,
            976,
            288,
            976,
            920,
            344,
            288,
            976,
            920,
            344,
            284,
            980,
            916,
            348,
            284,
            980,
            916,
            348,
            284,
            980,
            284,
            976,
            288,
            980,
            912,
            352,
            280,
            9808,
        ]
    )
    assert result is not None
    assert result[0] == [304, 959, 9808]
    assert result[1] == "01010101011001100101010101100110011001100101011002"


def test_compress_timings_5() -> None:
    # Should compress the timings.
    result = controller.compress_timings(
        [
            295,
            1180,
            295,
            1180,
            295,
            1180,
            1180,
            295,
            295,
            1180,
            295,
            1180,
            295,
            1180,
            1180,
            295,
            295,
            1180,
            1180,
            295,
            295,
            1180,
            1180,
            295,
            295,
            1180,
            1180,
            295,
            295,
            1180,
            1180,
            295,
            295,
            1180,
            295,
            1180,
            295,
            1180,
            1180,
            295,
            295,
            1180,
            1180,
            295,
            295,
            1180,
            1180,
            295,
            295,
            11210,
        ]
    )
    assert result is not None
    assert result[0] == [295, 1180, 11210]
    assert result[1] == "01010110010101100110011001100110010101100110011002"


def test_encode_message_switch1() -> None:
    results = controller.encode_pulses(
        "switch1", {"id": 9390234, "all": False, "state": True, "unit": 0}
    )
    assert results is not None
    assert (
        results["pulses"]
        == "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010100000100010001000103"
    )


def test_encode_message_switch2() -> None:
    results = controller.encode_pulses("switch2", {"id": 25, "unit": 16, "state": True})
    assert results is not None
    assert results["pulses"] == "01010101011001100101010101100110011001100101011002"


def test_encode_message_switch5() -> None:
    results = controller.encode_pulses(
        "switch5", {"id": 465695, "unit": 2, "all": False, "state": True}
    )
    assert results is not None
    assert results["pulses"] == "10010101101010010110010110101001010101011010011002"


def test_encode_message_switch6() -> None:
    results = controller.encode_pulses("switch6", {"id": 15, "unit": 2, "state": True})
    assert results is not None
    assert results["pulses"] == "10101010101010100110011001010110011001100110010102"


def test_encode_message_switch7() -> None:
    results = controller.encode_pulses("switch7", {"id": 7, "unit": 3, "state": True})
    assert results is not None
    assert results["pulses"] == "01010101010101100101010101010110011001100110011002"


def test_encode_message_switch8() -> None:
    results = controller.encode_pulses(
        "switch8", {"id": 30, "unit": "C3", "state": True}
    )
    assert results is not None
    assert results["pulses"] == "01010101010101010110011001101010010101010101101002"


def test_encode_message_switch9() -> None:
    results = controller.encode_pulses(
        "switch9", {"id": 2472, "unit": 65, "state": True}
    )
    assert results is not None
    assert results["pulses"] == "0110100101100110011010101001101010101001011012"


def test_encode_message_switch10() -> None:
    results = controller.encode_pulses(
        "switch10", {"id": 3162089194, "unit": 35, "all": False, "state": False}
    )
    assert results is not None
    assert (
        results["pulses"]
        == "01010000000101010100000100010101010000000101010100000101000100000101000101010001000100010001010001000101000000010102"
    )


def test_encode_message_switch12() -> None:
    results = controller.encode_pulses(
        "switch12", {"id": 9983, "unit": 1, "state": True}
    )
    assert results is not None
    assert results["pulses"] == "1202021212021212121212121212021212121212121212121203"


def test_encode_message_switch13() -> None:
    results = controller.encode_pulses(
        "switch13", {"id": 1472, "unit": 0, "all": False, "state": True, "dimm": False}
    )
    assert results is not None
    assert results["pulses"] == "001100110101001010101010101010110010101102"


def test_encode_message_switch14() -> None:
    results = controller.encode_pulses(
        "switch14", {"id": 0, "unit": 4, "all": False, "state": False}
    )
    assert results is not None
    assert results["pulses"] == "01010101010101010101010101010101010101010101100102"


def test_encode_message_switch15() -> None:
    results = controller.encode_pulses(
        "switch15", {"id": 414908, "unit": 1, "all": False, "state": True}
    )
    assert results is not None
    assert results["pulses"] == "01101001011001100110010110011010101001011010101002"


def test_encode_message_switch16() -> None:
    results = controller.encode_pulses(
        "switch16", {"id": "A", "unit": 2, "state": False}
    )
    assert results is not None
    assert results["pulses"] == "01010110011001100110010101100110011001100110010102"


def test_encode_message_switch21() -> None:
    results = controller.encode_pulses(
        "switch21", {"id": 15814908, "unit": 0, "state": True}
    )
    assert results is not None
    assert (
        results["pulses"]
        == "010101010102010201010101020102010101010201020101010201010202010201010101010101020101020101020101020101010101020102020102010101010201010101020103"
    )


def test_encode_message_switch24() -> None:
    results = controller.encode_pulses("switch24", {"id": 17, "unit": 1, "state": True})
    assert results is not None
    assert results["pulses"] == "01101010010101011010100110010110100101010101011002"


def test_encode_message_switch25() -> None:
    results = controller.encode_pulses("switch25", {"id": 0, "unit": 14, "state": True})
    assert results is not None
    assert (
        results["pulses"]
        == "101010101010101010101010101010100101010101010101011010100110011002"
    )


def test_encode_message_unknown_protocol() -> None:
    with pytest.raises(controller.RFControlProtocolNotFoundError):
        controller.encode_pulses("unknown", {"id": 0})


def test_encode_message_decode_only_protocol() -> None:
    # pir1 can only be received, it has no encode function.
    with pytest.raises(controller.RFControlSendNotSupportedError):
        controller.encode_pulses("pir1", {"id": 1, "unit": 1, "state": True})


def test_encode_message_switch29() -> None:
    results = controller.encode_pulses(
        "switch29", {"id": 5723557, "unit": 5621333, "command": "panic"}
    )
    assert results is not None
    assert (
        results["pulses"]
        == "00101011101010101101001010101010111000110010101010101011001011001010110012"
    )


def test_encode_message_switch30() -> None:
    results = controller.encode_pulses(
        "switch30", {"id": 21850, "unit": 23118, "command": "arm"}
    )
    assert results is not None
    assert results["pulses"] == "01010101010110100101101001001110101001010101010102"


def test_encode_message_switch31() -> None:
    results = controller.encode_pulses(
        "switch31", {"all": False, "unit": 1, "id": 47333, "state": True}
    )
    assert results is not None
    assert (
        results["pulses"]
        == "0000220100010101000000010101000001000100010000000101010000000101000100010000000001010103"
    )


def test_encode_message_switch32() -> None:
    results = controller.encode_pulses("switch32", {"id": 1, "unit": 1, "state": True})
    assert results is not None
    assert results["pulses"] == "01010110011001100101011001100110011001100110011002"


def test_encode_message_led3() -> None:
    results = controller.encode_pulses("led3", {"id": 14152, "command": "cyan"})
    assert results is not None
    assert results["pulses"] == "01011010011010100110010110010101010101100110010102"


def test_encode_message_led4() -> None:
    results = controller.encode_pulses("led4", {"id": 796, "command": "on/off"})
    assert results is not None
    assert results["pulses"] == "01010101010110100101011010100101100101010110011002"


def test_encode_message_doorbell1() -> None:
    results = controller.encode_pulses(
        "doorbell1", {"id": 1361, "unit": 0, "state": True}
    )
    assert results is not None
    assert results["pulses"] == "01101010011001100110011010101010101010101010101002"


def test_encode_message_rolling1() -> None:
    results = controller.encode_pulses(
        "rolling1",
        {
            "code_on": [
                "011111110000111001011100",
                "011101101101100010101100",
                "011111011110001001101100",
                "011110011010111100011100",
            ],
            "code_off": [
                "011110001011100110111100",
                "011110101001110001111100",
                "011100010001011100101100",
                "011101110011101010001100",
            ],
            "state": True,
        },
    )
    assert results is not None
    assert results["pulses"] == "01101010101010100101010110101001011001101010010123"


def test_encode_message_shutter3() -> None:
    results = controller.encode_pulses(
        "shutter3", {"id": 151368466, "unit": 9, "command": "program"}
    )
    assert results is not None
    assert (
        results["pulses"]
        == "3210010110010101010110011010011010010110100101011001011001100101101010010110100104"
    )


def test_encode_message_shutter4() -> None:
    results = controller.encode_pulses(
        "shutter4", {"id": 17959394, "unit": 0, "all": True, "command": "up"}
    )
    assert results is not None
    assert (
        results["pulses"]
        == "3201010110010101100101100101010101100101101010100101011001010101010101011001010113"
    )


def test_encode_message_shutter5() -> None:
    results = controller.encode_pulses("shutter5", {"id": 281971, "command": "down"})
    assert results is not None
    assert results["pulses"] == "02210202022102022121022102212121020221210221020203"


def test_fix_pulses_1() -> None:
    # Should fix the pulses.
    result = controller.fix_pulses(
        [258, 401, 1339, 2715, 10424],
        "030002000202000200000202000002020000020002020000020002020000020201020000020200020000020201020002000200000200020002000200020002000204",
    )
    assert result is not None
    assert result[0] == [
        329,
        1339,
        2715,
        10424,
    ]
    assert (
        result[1]
        == "020001000101000100000101000001010000010001010000010001010000010100010000010100010000010100010001000100000100010001000100010001000103"
    )


def test_fix_pulses_2() -> None:
    # Should fix the pulses.
    result = controller.fix_pulses(
        [239, 320, 1337, 2717, 10359],
        "030002000202000201010202010002020101020102020101020102020101020201020101020201020101020201020102010201010201020102010201020112000204",
    )
    assert result is not None
    assert result[0] == [
        279,
        1337,
        2717,
        10359,
    ]
    assert (
        result[1]
        == "020001000101000100000101000001010000010001010000010001010000010100010000010100010000010100010001000100000100010001000100010001000103"
    )


def test_fix_pulses_3() -> None:
    # Should not change correct pulses.
    result = controller.fix_pulses(
        [279, 1337, 2717, 10359],
        "020001000101000100000101000001010000010001010000010001010000010100010000010100010000010100010001000100000100010001000100010001000103",
    )
    assert result is None


def test_sort_compressed_pulses() -> None:
    result = controller.sort_compressed_pulses(
        [480, 1988, 1020, 3976],
        "01020102020102020202020202020202010202010102010201010101020102020101020103",
    )
    assert result == (
        [480, 1020, 1988, 3976],
        "02010201010201010101010101010101020101020201020102020202010201010202010203",
    )


def test_get_protocol() -> None:
    protocol = controller.get_protocol("switch1")
    assert protocol is not None
    assert protocol.name == "switch1"


def test_get_protocol_unknown() -> None:
    assert controller.get_protocol("unknown") is None


def test_get_protocol_not_a_protocol() -> None:
    # Other names in the rfcontrol.protocols package are not protocols.
    assert controller.get_protocol("RFControlProtocolTypes") is None
    assert controller.get_protocol("Path") is None
