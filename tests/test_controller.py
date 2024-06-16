# Original testdata
# https://raw.githubusercontent.com/pimatic/rfcontroljs/master/test/lib-controller.coffee
# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-lines
# pylint: disable=too-many-public-methods

import logging
import unittest

from rfcontrol import controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestControler(unittest.TestCase):
    def test_does_protocol_match_matching(self) -> None:
        # pylint: disable=no-member
        result = controller.does_protocol_match(
            [671, 2051, 4346, 10220],
            "020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201010203",
            controller.generic,
        )
        self.assertTrue(result)

    def test_does_protocol_match_not_matching(self) -> None:
        # pylint: disable=no-member
        result = controller.does_protocol_match(
            [671, 2051, 4346, 10220],
            "020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201010203",
            controller.switch1,
        )
        self.assertFalse(result)

    def test_sort_indices_1(self) -> None:
        result = controller.sort_indices((1, 3, 2, 7, 6, 5, 4, 8))
        self.assertSequenceEqual([0, 2, 1, 6, 5, 4, 3, 7], result)

    def test_sort_indices_2(self) -> None:
        result = controller.sort_indices((1, 2, 3, 4, 5, 6, 7, 8))
        self.assertSequenceEqual(
            [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
            ],
            result,
        )

    def test_sort_indices_3(self) -> None:
        result = controller.sort_indices((8, 7, 6, 5, 4, 3, 2, 1))
        self.assertSequenceEqual(
            [
                7,
                6,
                5,
                4,
                3,
                2,
                1,
                0,
            ],
            result,
        )

    def test_prepare_compressed_pulses(self) -> None:
        result = controller.prepare_compressed_pulses(
            "268 2632 1282 10168 0 0 0 0 010002000202000002000200020200020002"
        )
        self.assertSequenceEqual(
            (
                [268, 1282, 2632, 10168],
                "020001000101000001000100010100010001",
            ),
            result,
        )

    def test_decode_pulses_generic_1(self) -> None:
        results = controller.decode_pulses(
            [671, 2051, 4346, 10220],
            "020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201010203",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "generic", results))

        self.assertEqual(1, len(results))
        self.assertEqual("generic", results[0]["protocol"])
        self.assertDictEqual(
            {
                "id": 1000,
                "type": 10,
                "positive": True,
                "value": 1,
            },
            results[0]["values"],
        )

    def test_decode_pulses_generic_2(self) -> None:
        results = controller.decode_pulses(
            [671, 2051, 4346, 10220],
            "020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010102020102010102010201020201010202010201010203",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "generic", results))

        self.assertEqual(1, len(results))
        self.assertEqual("generic", results[0]["protocol"])
        self.assertDictEqual(
            {
                "id": 1000,
                "type": 10,
                "positive": True,
                "value": 1257,
            },
            results[0]["values"],
        )

    def test_decode_pulses_generic_3(self) -> None:
        results = controller.decode_pulses(
            [671, 2051, 4346, 10220],
            "020102010201020101020102010201020102010202010201010201020102020101020201010202010201020102010201020102010201020102010201020102010102020102010201020102010102010202010201020101020102010202010201010203",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "generic", results))

        self.assertEqual(1, len(results))
        self.assertEqual("generic", results[0]["protocol"])
        self.assertDictEqual(
            {
                "id": 1011,
                "type": 10,
                "positive": True,
                "value": 67129,
            },
            results[0]["values"],
        )

    def test_decode_pulses_generic_4(self) -> None:
        results = controller.decode_pulses(
            [671, 2051, 4346, 10220],
            "020102010201020101020102010201020102020101020201020102010102020101020201020102010201020102010201020102010201020102010201020102010102020102010201020102010102010202010201020101020102010202010201010203",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "generic", results))

        self.assertEqual(1, len(results))
        self.assertEqual("generic", results[0]["protocol"])
        self.assertDictEqual(
            {
                "id": 1000,
                "type": 10,
                "positive": False,
                "value": 67129,
            },
            results[0]["values"],
        )

    def test_decode_pulses_generic_5(self) -> None:
        results = controller.decode_pulses(
            [671, 2051, 4346, 10220],
            "020102010201020101020102010201020102020101020201020102010102020101020201010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010203",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "generic", results))

        self.assertEqual(1, len(results))
        self.assertEqual("generic", results[0]["protocol"])
        self.assertDictEqual(
            {
                "id": 1000,
                "type": 10,
                "positive": True,
                "value": 1073741823,
            },
            results[0]["values"],
        )

    def test_decode_pulses_generic2_1(self) -> None:
        results = controller.decode_pulses(
            [480, 1320, 13320],
            "011010101010101001011010101010101010101010010101101001101010100102",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "generic2", results))

        self.assertEqual(1, len(results))
        self.assertEqual("generic2", results[0]["protocol"])
        self.assertDictEqual(
            {
                "id": 123,
                "type": 1,
                "value": 1023,
                "freq": 3,
                "battery": 99,
                "checksum": True,
            },
            results[0]["values"],
        )

    def test_decode_pulses_generic2_2(self) -> None:
        results = controller.decode_pulses(
            [480, 1320, 13320],
            "010110101010101001011010101010101010101010010101101001101010100102",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "generic2", results))

        self.assertEqual(1, len(results))
        self.assertEqual("generic2", results[0]["protocol"])
        self.assertDictEqual(
            {
                "id": 123,
                "type": 1,
                "value": 1023,
                "freq": 3,
                "battery": 99,
                "checksum": False,
            },
            results[0]["values"],
        )

    # def test_decode_pulses_alarm3_1(self) -> None:
    #     results = controller.decode_pulses([472, 1236, 11688], '100101010101100101011010010101101010101001011010000102')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('alarm3', results[0]['protocol'])
    #     self.assertDictEqual({'id': 9787738, 'state': True}, results[0]['values'])
    #
    # def test_decode_pulses_alarm3_2(self) -> None:
    #     results = controller.decode_pulses([472, 1236, 11688], '011001100110011001100110011001100110011001100110000002')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('alarm3', results[0]['protocol'])
    #     self.assertDictEqual({'id': 6710886, 'state': True}, results[0]['values'])
    #
    # def test_decode_pulses_alarm3_3(self) -> None:
    #     results = controller.decode_pulses([472, 1236, 11688], '011010101001010110010110100110101010101010100101111112')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('alarm3', results[0]['protocol'])
    #     self.assertDictEqual({'id': 6985110, 'state': True}, results[0]['values'])
    #
    # def test_decode_pulses_alarm3_4(self) -> None:
    #     results = controller.decode_pulses([472, 1236, 11688], '011010101001001110010110100110101010101010100101111112')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('alarm3', results[0]['protocol'])
    #     self.assertDictEqual({'id': 6986089, 'state': True}, results[0]['values'])
    #
    # def test_decode_pulses_alarm3_5(self) -> None:
    #     results = controller.decode_pulses([472, 1236, 11688], '101010100110100110100110010110100110101001011010000002')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('alarm3', results[0]['protocol'])
    #     self.assertDictEqual({'id': 11168166, 'state': True}, results[0]['values'])

    # def test_decode_pulses_pir1_1(self) -> None:
    #     results = controller.decode_pulses([358, 1095, 11244], '01100101011001100110011001100110011001010110011002')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('pir1', results[0]['protocol'])
    #     self.assertDictEqual({'unit': 8, 'id': 1, 'presence': True}, results[0]['values'])
    #
    # def test_decode_pulses_pir1_2(self) -> None:
    #     results = controller.decode_pulses([358, 1095, 11244], '01100110011001100110010101100110011001010110011002')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('pir1', results[0]['protocol'])
    #     self.assertDictEqual({'unit': 0, 'id': 17, 'presence': True}, results[0]['values'])
    #
    # def test_decode_pulses_pir1_3(self) -> None:
    #     results = controller.decode_pulses([358, 1095, 11244], '01100110011001010110011001100110010101100110011002')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('pir1', results[0]['protocol'])
    #     self.assertDictEqual({'unit': 2, 'id': 2, 'presence': True}, results[0]['values'])

    # def test_decode_pulses_pir2(self) -> None:
    #     results = controller.decode_pulses([451, 1402, 14356], '01100110010110011001010110100101010101011010010102')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('pir2', results[0]['protocol'])
    #     self.assertDictEqual({'unit': 21, 'id': 21, 'presence': True}, results[0]['values'])

    # def test_decode_pulses_pir4(self) -> None:
    #     results = controller.decode_pulses([371, 1081, 5803], '110100110101001101010011001010101012')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('pir4', results[0]['protocol'])
    #     self.assertDictEqual({'id': 54099, 'unit': 21290, 'presence': True}, results[0]['values'])

    # def test_decode_pulses_pir6_1(self) -> None:
    #     results = controller.decode_pulses([288, 864, 8964], '01011010010101011010100110010101101001010101101002')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('pir6', results[0]['protocol'])
    #     self.assertDictEqual({'id': 6410630, 'presence': True}, results[0]['values'])
    #
    # def test_decode_pulses_pir6_2(self) -> None:
    #     results = controller.decode_pulses([288, 864, 8964], '01011010010101011010100110010101101001010110010102')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('pir6', results[0]['protocol'])
    #     self.assertDictEqual({'id': 6410632, 'presence': True}, results[0]['values'])
    #
    # def test_decode_pulses_pir6_3(self) -> None:
    #     results = controller.decode_pulses([288, 864, 8964], '01011010010101011010100110010101101001011001010102')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('pir6', results[0]['protocol'])
    #     self.assertDictEqual({'id': 6410640, 'presence': True}, results[0]['values'])

    # def test_decode_pulses_weather1_1(self) -> None:
    #     results = controller.decode_pulses([456, 1990, 3940, 9236], '01020102020201020101010101010102010101010202020102010101010102010101020103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather1', results[0]['protocol'])
    #     self.assertDictEqual({'id': 208, 'channel': 2, 'lowBattery': True, 'temperature': 23.2, 'humidity': 34}, results[0]['values'])
    #
    # def test_decode_pulses_weather1_2(self) -> None:
    #     results = controller.decode_pulses([456, 1990, 3940, 9236], '01020102010201010101020202020101010101020101010101020101010102020202010203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather1', results[0]['protocol'])
    #     self.assertDictEqual({'id': 67, 'channel': 1, 'lowBattery': False, 'temperature': 26.0, 'humidity': 61}, results[0]['values'])
    #
    # def test_decode_pulses_weather1_3(self) -> None:
    #     results = controller.decode_pulses([456, 1990, 3940, 9236], '01020102020201010102020102020101010101020101010101010101010102020202010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather1', results[0]['protocol'])
    #     self.assertDictEqual({'id': 198, 'channel': 1, 'lowBattery': False, 'temperature': 25.6, 'humidity': 60}, results[0]['values'])
    #
    # def test_decode_pulses_weather1_4(self) -> None:
    #     results = controller.decode_pulses([456, 1990, 3940, 9236], '01020102010102020102020102020201010101010202020201020101010201010101020203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather1', results[0]['protocol'])
    #     self.assertDictEqual({'id': 54, 'channel': 3, 'lowBattery': False, 'temperature': 24.4, 'humidity': 67}, results[0]['values'])

    # def test_decode_pulses_weather2_1(self) -> None:
    #     results = controller.decode_pulses([492, 969, 1948, 4004], '01010102020202010201010101010101020202010201020102020202010101010101010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather2', results[0]['protocol'])
    #     self.assertDictEqual({'temperature': 23.4}, results[0]['values'])
    #
    # def test_decode_pulses_weather2_2(self) -> None:
    #     results = controller.decode_pulses([492, 969, 1948, 4004], '01010102020202010201010101010101020202010201010202020202010101010101010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather2', results[0]['protocol'])
    #     self.assertDictEqual({'temperature': 23.3}, results[0]['values'])
    #
    # def test_decode_pulses_weather2_3(self) -> None:
    #     results = controller.decode_pulses([492, 969, 1948, 4004], '01010102020202010201010101010101020202010201010102020202010101010101010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather2', results[0]['protocol'])
    #     self.assertDictEqual({'temperature': 23.2}, results[0]['values'])
    #
    # def test_decode_pulses_weather2_4(self) -> None:
    #     results = controller.decode_pulses([492, 969, 1948, 4004], '01010101020201020201010101010102010101010202010102020202010101010101010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather2', results[0]['protocol'])
    #     self.assertDictEqual({'temperature': 26.8}, results[0]['values'])
    #
    # def test_decode_pulses_weather2_5(self) -> None:
    #     results = controller.decode_pulses([492, 969, 1948, 4004], '01010101020201020201010101010102010101010201010102020202010101010101010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather2', results[0]['protocol'])
    #     self.assertDictEqual({'temperature': 26.4}, results[0]['values'])
    #
    # def test_decode_pulses_weather2_6(self) -> None:
    #     results = controller.decode_pulses([492, 969, 1948, 4004], '02010102010102020201010102020202020102020102020102020202010101010202020103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather2', results[0]['protocol'])
    #     self.assertDictEqual({'temperature': -7.4}, results[0]['values'])

    # def test_decode_pulses_weather3_1(self) -> None:
    #     results = controller.decode_pulses([508, 2012, 3908, 7726], '01010202020201020201010102010102020201020202010202010201010101010202010201010101020103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather3', results[0]['protocol'])
    #     self.assertDictEqual({'id': 246, 'channel': 3, 'temperature': 24.2, 'humidity': 56}, results[0]['values'])
    #
    # def test_decode_pulses_weather3_2(self) -> None:
    #     results = controller.decode_pulses([508, 2012, 3908, 7726], '01010202020201020201010102010201020201020202010202010201010101010202010201010202010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather3', results[0]['protocol'])
    #     self.assertDictEqual({'id': 246, 'channel': 3, 'temperature': 24.4, 'humidity': 56}, results[0]['values'])
    #
    # def test_decode_pulses_weather3_3(self) -> None:
    #     results = controller.decode_pulses([508, 2012, 3908, 7726], '01010201020102020102010101010101010101020101010202010101010201020101010101010102010203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather3', results[0]['protocol'])
    #     self.assertDictEqual({'id': 173, 'channel': 1, 'temperature': 21.1, 'humidity': 65}, results[0]['values'])
    #
    # def test_decode_pulses_weather3_4(self) -> None:
    #     results = controller.decode_pulses([508, 2012, 3908, 7726], '01010201020102020102010101010102020201020101010202010101010201020101010101010102010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather3', results[0]['protocol'])
    #     self.assertDictEqual({'id': 173, 'channel': 1, 'temperature': 21.5, 'humidity': 65}, results[0]['values'])
    #
    # def test_decode_pulses_weather3_5(self) -> None:
    #     results = controller.decode_pulses([508, 2012, 3908, 7726], '01010101010202020201010101020201010201010101010202010202020101010202010201010101010203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather3', results[0]['protocol'])
    #     self.assertDictEqual({'id': 30,  'channel': 2, 'temperature': 18.1, 'humidity': 62}, results[0]['values'])
    #
    # def test_decode_pulses_weather3_6(self) -> None:
    #     results = controller.decode_pulses([508, 2012, 3908, 7726], '01010101010202020201010101020102010201010102010202010202020201010202010101010202010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather3', results[0]['protocol'])
    #     self.assertDictEqual({'id': 30,  'channel': 2, 'temperature': 18.7, 'humidity': 63}, results[0]['values'])

    # def test_decode_pulses_weather4(self) -> None:
    #     results = controller.decode_pulses([526, 990, 1903, 4130, 7828, 16076], '11111111040303030203030302020302030203020302030302020202030302020202030303020202030202020305')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather4', results[0]['protocol'])
    #     self.assertDictEqual({'id': 238, 'channel':1, 'temperature': 18.9, 'humidity': 71, 'lowBattery': False}, results[0]['values'])

    # def test_decode_pulses_weather5_1(self) -> None:
    #     results = controller.decode_pulses([534, 2000, 4000, 9120], '01020101010201020102010101020202020202010101010102020201010202010202020203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather5', results[0]['protocol'])
    #     self.assertDictEqual({'id': 162, 'temperature': 12.6, 'humidity': 67, 'lowBattery': False}, results[0]['values'])
    #
    # def test_decode_pulses_weather5_2(self) -> None:
    #     results = controller.decode_pulses([534, 2000, 4000, 9120], '01010101010101010102020102020101020202010201010101010101010101010101010203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather5', results[0]['protocol'])
    #     self.assertDictEqual({'id': 0, 'rain': 5.75, 'lowBattery': False}, results[0]['values'])
    #
    # def test_decode_pulses_weather5_3(self) -> None:
    #     results = controller.decode_pulses([534, 2000, 4000, 9120], '01020202010101020102020102020101020102020202010101010101010101010102020103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather5', results[0]['protocol'])
    #     self.assertDictEqual({'id: 142, ': 15.25, 'lowBattery': False}, results[0]['values'])
    #
    # def test_decode_pulses_weather5_4(self) -> None:
    #     results = controller.decode_pulses([534, 2000, 4000, 9120], '01020202010202020101010102010201020202010101010102010102020101020201020103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather5', results[0]['protocol'])
    #     self.assertDictEqual({'id': 238, 'temperature': 11.7, 'humidity': 99,  'lowBattery': False}, results[0]['values'])
    #
    # def test_decode_pulses_weather5_5(self) -> None:
    #     results = controller.decode_pulses([534, 2000, 4000, 9120], '01020202010202020101020101020101020202020202020202010102010202010101010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather5', results[0]['protocol'])
    #     self.assertDictEqual({'id': 238, 'temperature': -1.4, 'humidity': 69,  'lowBattery': False}, results[0]['values'])

    def test_decode_pulses_weather7(self) -> None:
        results = controller.decode_pulses(
            [444, 1992, 3955, 9330],
            "010202010201010202010101010101010101010202020102020202010202010103",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "weather7", results))

        self.assertEqual(1, len(results))
        self.assertEqual("weather7", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 105,
                "temperature": 2.9,
                "humidity": 59,
                "channel": 0,
                "lowBattery": False,
            },
            results[0]["values"],
        )

    # def test_decode_pulses_weather11(self) -> None:
    #     results = controller.decode_pulses([544, 1056, 1984, 3880], '020202010202010102010101010101020101010202010201020202020101020201020201010101010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather11', results[0]['protocol'])
    #     self.assertDictEqual({'id': 236, 'channel': 1, 'temperature': 28.2, 'humidity': 54, 'lowBattery': False}, results[0]['values'])

    # def test_decode_pulses_weather12_1(self) -> None:
    #     results = controller.decode_pulses([516, 2048, 4076, 8976], '0102020201010102020101010101010101020202020102020201020102010202020102020103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather12', results[0]['protocol'])
    #     self.assertDictEqual({'id': 113, 'channel': 1, 'temperature': 12.3, 'humidity': 85, 'lowBattery': True}, results[0]['values'])
    #
    # def test_decode_pulses_weather12_2(self) -> None:
    #     results = controller.decode_pulses([516, 2048, 4076, 8976], '0201010202010202010101010101010101020201010202010202010202020102020201010203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather12', results[0]['protocol'])
    #     self.assertDictEqual({'id': 155, 'channel': 1, 'temperature': 10.2, 'humidity': 110, 'lowBattery': False}, results[0]['values'])
    #
    # def test_decode_pulses_weather12_3(self) -> None:
    #     results = controller.decode_pulses([516, 2048, 4076, 8976], '0201010202010202010101010101010101020202010202020201020101010102010202010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather12', results[0]['protocol'])
    #     self.assertDictEqual({'id': 155, 'channel': 1, 'temperature': 11.9, 'humidity': 80, 'lowBattery': False}, results[0]['values'])

    # def test_decode_pulses_weather13(self) -> None:
    #     results = controller.decode_pulses([492, 992, 2028, 4012], '02020202010101020201020101010101020202010202010202020202010102020101010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather13', results[0]['protocol'])
    #     self.assertDictEqual({'id': 241, 'channel': 3, 'temperature': 23.7, 'humidity': 48, 'lowBattery': False}, results[0]['values'])

    # def test_decode_pulses_weather14_1(self) -> None:
    #     results = controller.decode_pulses([480, 1960, 3908, 8784], '0102020102010202010101020202020202020202010101010102010201010202010102020203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather14', results[0]['protocol'])
    #     self.assertDictEqual({'id': 78, 'channel': 1, 'temperature': 25, 'lowBattery': True}, results[0]['values'])
    #
    # def test_decode_pulses_weather14_2(self) -> None:
    #     results = controller.decode_pulses([480, 1960, 3908, 8784], '0102020102010202010101020202020201010101010102010102020101010202010102020203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather14', results[0]['protocol'])
    #     self.assertDictEqual({'id': 78, 'channel': 1, 'temperature': -3.9, 'lowBattery': True}, results[0]['values'])
    #
    # def test_decode_pulses_weather14_3(self) -> None:
    #     results = controller.decode_pulses([480, 1960, 3908, 8784], '0201010201020102010101010102020101010102010101010202020202020101020201010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather14', results[0]['protocol'])
    #     self.assertDictEqual({'id': 175, 'channel': 3, 'temperature': -27.2, 'humidity': 51, 'lowBattery': False}, results[0]['values'])
    #
    # def test_decode_pulses_weather14_4(self) -> None:
    #     results = controller.decode_pulses([480, 1960, 3908, 8784], '0201010201020102010101010102010201010102010101010202010102020101020201010103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather14', results[0]['protocol'])
    #     self.assertDictEqual({'id': 175, 'channel': 3, 'temperature': -26.9, 'humidity': 51, 'lowBattery': True}, results[0]['values'])

    # def test_decode_pulses_weather15_1(self) -> None:
    #     results = controller.decode_pulses([480, 1960, 3908, 8784], '0201010202010102010101010102010101010101020202010101020101020101010102010203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather15', results[0]['protocol'])
    #     self.assertDictEqual({'id': 2448, 'channel': 1, 'temperature': 22.6, 'humidity': 66, 'lowBattery': False}, results[0]['values'])
    #
    # def test_decode_pulses_weather15_2(self) -> None:
    #     results = controller.decode_pulses([480, 1960, 3908, 8784], '0201010202010102010101010102010201010101020202010101020101020101010102010203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather15', results[0]['protocol'])
    #     self.assertDictEqual({'id': 2448, 'channel': 2, 'temperature': 22.6, 'humidity': 66, 'lowBattery': False}, results[0]['values'])
    #
    # def test_decode_pulses_weather15_3(self) -> None:
    #     results = controller.decode_pulses([480, 1960, 3908, 8784], '0201010202010102010101010102020101010101020202010101020101020101010102010203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather15', results[0]['protocol'])
    #     self.assertDictEqual({'id': 2448, 'channel': 3, 'temperature': 22.6, 'humidity': 66, 'lowBattery': False}, results[0]['values'])
    #
    # def test_decode_pulses_weather15_4(self) -> None:
    #     results = controller.decode_pulses([480, 1960, 3908, 8784], '0201010201010202010102020201010102020202020201020201020201010101020102010203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather15', results[0]['protocol'])
    #     self.assertDictEqual({'id': 2355, 'channel': 1, 'temperature': -3.7, 'humidity': 10, 'lowBattery': True}, results[0]['values'])

    # def test_decode_pulses_weather16_1(self) -> None:
    #     results = controller.decode_pulses([472, 1964, 4052, 8904], '02020202010202010101020101010201010101010201010101010101010102020102010203')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather16', results[0]['protocol'])
    #     self.assertDictEqual({'id': 111, 'channel': 1, 'temperature': 26, 'humidity': 36, 'lowBattery': False}, results[0]['values'])
    #
    # def test_decode_pulses_weather16_2(self) -> None:
    #     results = controller.decode_pulses([472, 1964, 4052, 8904], '02020202010202010101020101010101010101010201010102010101010102020202020103')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather16', results[0]['protocol'])
    #     self.assertDictEqual({'id': 111, 'channel': 1, 'temperature': 25.6, 'humidity': 37, 'lowBattery': False}, results[0]['values'])

    # def test_decode_pulses_weather17_1(self) -> None:
    #     results = controller.decode_pulses([444, 1160, 28580], '1111111101110111111111111111010111111111110101011111111111111101110101011111111101011112')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather17', results[0]['protocol'])
    #     self.assertDictEqual({'id': 24, 'channel': 0, 'temperature': 20.1}, results[0]['values'])
    #
    # def test_decode_pulses_weather17_2(self) -> None:
    #     results = controller.decode_pulses([444, 1160, 28580], '1111111101110111111111111111010111111101110101011111011101111111110101011111011101111112')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather17', results[0]['protocol'])
    #     self.assertDictEqual({'id': 24, 'channel': 0, 'temperature': 22.8}, results[0]['values'])
    #
    # def test_decode_pulses_weather17_3(self) -> None:
    #     results = controller.decode_pulses([444, 1160, 28580], '1111111101110111010101111111010111111101110101111111011111111111110101111111011101011112')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather17', results[0]['protocol'])
    #     self.assertDictEqual({'id': 24, 'channel': 7, 'humidity': 62}, results[0]['values'])
    #
    # def test_decode_pulses_weather17_4(self) -> None:
    #     results = controller.decode_pulses([444, 1160, 28580], '1111111101110111010101111111010111111101110101111111110111111111110101111111110101110112')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather17', results[0]['protocol'])
    #     self.assertDictEqual({'id': 24, 'channel': 7, 'humidity': 61}, results[0]['values'])

    # def test_decode_pulses_weather18_1(self) -> None:
    #     results = controller.decode_pulses([496, 960, 1940, 3904], '0101020102020102020101010101010102020201010102020202020201020202010202020003')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather18', results[0]['protocol'])
    #     self.assertDictEqual({'id': 45, 'channel': 1, 'temperature': 22.7}, results[0]['values'])
    #
    # def test_decode_pulses_weather18_2(self) -> None:
    #     results = controller.decode_pulses([496, 960, 1940, 3904], '0101020102020102020101010101010102020202010102020202020201010102020101020003')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather18', results[0]['protocol'])
    #     self.assertDictEqual({'id': 45, 'channel': 1, 'temperature': 24.3}, results[0]['values'])
    #
    # def test_decode_pulses_weather18_3(self) -> None:
    #     results = controller.decode_pulses([496, 960, 1940, 3904], '0101020102020102020101010101010201010201010101010202020202010202010202010003')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather18', results[0]['protocol'])
    #     self.assertDictEqual({'id': 45, 'channel': 1, 'temperature': 28.8}, results[0]['values'])
    #
    # def test_decode_pulses_weather18_4(self) -> None:
    #     results = controller.decode_pulses([496, 960, 1940, 3904], '0101020102020102020101010101010201010102010101010202020201010101010201010003')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather18', results[0]['protocol'])
    #     self.assertDictEqual({'id': 45, 'channel': 1, 'temperature': 27.2}, results[0]['values'])

    def test_decode_pulses_weather19_1(self) -> None:
        results = controller.decode_pulses(
            [548, 1008, 1996, 3936],
            "020202010101010101010101010101020101010102010201020101010201020203",
        )
        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("weather19", results[0]["protocol"])
        self.assertEqual(
            {"id": 56, "channel": 1, "temperature": 26.6}, results[0]["values"]
        )

    def test_decode_pulses_weather19_2(self) -> None:
        results = controller.decode_pulses(
            [548, 1008, 1996, 3936],
            "020102020102010101010101010101020101020101020201010102020201020203",
        )
        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("weather19", results[0]["protocol"])
        self.assertEqual(
            {"id": 45, "channel": 1, "temperature": 29.4}, results[0]["values"]
        )

    def test_decode_pulses_weather19_3(self) -> None:
        results = controller.decode_pulses(
            [548, 1008, 1996, 3936],
            "020102020102010101010101010101020101020201010101020102010102010203",
        )
        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("weather19", results[0]["protocol"])
        self.assertEqual(
            {"id": 45, "channel": 1, "temperature": 30.4}, results[0]["values"]
        )

    def test_decode_pulses_weather19_4(self) -> None:
        results = controller.decode_pulses(
            [548, 1008, 1996, 3936],
            "020102020102010101010101010101020202010102020101020102010101010203",
        )
        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("weather19", results[0]["protocol"])
        self.assertEqual(
            {"id": 45, "channel": 1, "temperature": 46.0}, results[0]["values"]
        )

    # def test_decode_pulses_weather20_1(self) -> None:
    #     results = controller.decode_pulses([560, 972, 1904, 3812, 8556], '0302020302020202030202020302020202020202030302020202030202020202020202020104')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather20', results[0]['protocol'])
    #     self.assertDictEqual({'id': 2312, 'channel': 1, 'temperature': 19.4, 'lowBattery': True}, results[0]['values'])
    #
    # def test_decode_pulses_weather20_2(self) -> None:
    #     results = controller.decode_pulses([560, 972, 1904, 3812, 8556], '0302020302020202030202020302020202020202030203030302030202020202020202020104')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather20', results[0]['protocol'])
    #     self.assertDictEqual({'id': 2312, 'channel': 1, 'temperature': 18.6, 'lowBattery': True}, results[0]['values'])
    #
    # def test_decode_pulses_weather20_3(self) -> None:
    #     results = controller.decode_pulses([560, 972, 1904, 3812, 8556], '0302020302020202030202020302020202020202030203030302030302020202020202020104')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather20', results[0]['protocol'])
    #     self.assertDictEqual({'id': 2312, 'channel': 1, 'temperature': 18.7, 'lowBattery': True}, results[0]['values'])
    #
    # def test_decode_pulses_weather20_4(self) -> None:
    #     results = controller.decode_pulses([560, 972, 1904, 3812, 8556], '0302020302020202030302030302020302020202030302020203030202020202020202020104')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather20', results[0]['protocol'])
    #     self.assertDictEqual({'id': 2317, 'channel': 2, 'temperature': 19.8, 'lowBattery': True}, results[0]['values'])
    #
    # def test_decode_pulses_weather20_5(self) -> None:
    #     results = controller.decode_pulses([560, 972, 1904, 3812, 8556], '0302020302020202030303020302020202020202030302020203020302020202020202020104')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather20', results[0]['protocol'])
    #     self.assertDictEqual({'id': 2318, 'channel': 1, 'temperature': 19.7, 'lowBattery': True}, results[0]['values'])
    #
    # def test_decode_pulses_weather20_6(self) -> None:
    #     results = controller.decode_pulses([560, 972, 1904, 3812, 8556], '0302020302020202030303020302020202020202030302020202020302020202020202020104')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather20', results[0]['protocol'])
    #     self.assertDictEqual({'id': 2318, 'channel': 1, 'temperature': 19.3, 'lowBattery': True}, results[0]['values'])
    #
    # def test_decode_pulses_weather20_7(self) -> None:
    #     results = controller.decode_pulses([560, 972, 1904, 3812, 8556], '0302020302020202030303020302020202020202030302020302020202020202020202020104')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather20', results[0]['protocol'])
    #     self.assertDictEqual({'id': 2318, 'channel': 1, 'temperature': 20, 'lowBattery': True}, results[0]['values'])

    # def test_decode_pulses_weather21_1(self) -> None:
    #     results = controller.decode_pulses([196, 288, 628, 61284], '1222222220122012121212201220121220121212121212121212121220122020121221212112121221121213')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather21', results[0]['protocol'])
    #     self.assertDictEqual({'id': 161, 'temperature': 17.9, 'humidity': 72, 'channel': 1, 'lowBattery': False, 'crcOk': True}, results[0]['values'])
    #
    # def test_decode_pulses_weather21_2(self) -> None:
    #     results = controller.decode_pulses([196, 288, 628, 61284], '1222222220122012121212201220121212201220121212121212121220122020122020201212121212121213')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather21', results[0]['protocol'])
    #     self.assertDictEqual({'id': 161, 'temperature': 18.3, 'humidity': 69, 'channel': 1, 'lowBattery': False, 'crcOk': True}, results[0]['values'])
    #
    # def test_decode_pulses_weather21_3(self) -> None:
    #     results = controller.decode_pulses([196, 288, 628, 61284], '1222222220122012121212201220121212122020121212121212121220201212121220122112201221122123')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather21', results[0]['protocol'])
    #     self.assertDictEqual({'id': 161, 'temperature': 19.4, 'humidity': 67, 'channel': 1, 'lowBattery': False, 'crcOk': False}, results[0]['values'])
    #
    # def test_decode_pulses_weather21_4(self) -> None:
    #     results = controller.decode_pulses([196, 288, 628, 61284], '1222222220122012121212201220121212122121121212121212121221211212121221122112211221122123')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('weather21', results[0]['protocol'])
    #     self.assertDictEqual({'id': 161, 'temperature': 19.4, 'humidity': 67, 'channel': 1, 'lowBattery': False, 'crcOk': False}, results[0]['values'])

    def test_decode_pulses_dimmer1(self) -> None:
        results = controller.decode_pulses(
            [259, 1293, 2641, 10138],
            "0200010001010000010001010000010001000101000100010001000100000101000100010000010001000100010001010001000001000101000001000100010001010001000100010003",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "dimmer1", results))

        self.assertEqual(1, len(results))
        self.assertEqual("dimmer1", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 9565958,
                "all": False,
                "unit": 0,
                "dimlevel": 15,
                "state": True,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch1_1(self) -> None:
        results = controller.decode_pulses(
            [268, 1282, 2632, 10168],
            "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010100000100010001000103",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch1", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch1", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 9390234,
                "all": False,
                "state": True,
                "unit": 0,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch1_2(self) -> None:
        results = controller.decode_pulses(
            [268, 1282, 2632, 10168],
            "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010100000100010001010003",
        )
        results = list(filter(lambda result: result["protocol"] == "switch1", results))

        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("switch1", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 9390234,
                "all": False,
                "state": True,
                "unit": 1,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch1_3(self) -> None:
        results = controller.decode_pulses(
            [268, 1282, 2632, 10168],
            "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010001000100010001010003",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch1", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch1", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 9390234,
                "all": False,
                "state": False,
                "unit": 1,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch2(self) -> None:
        results = controller.decode_pulses(
            [306, 957, 9808], "01010101011001100101010101100110011001100101011002"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch2", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch2", results[0]["protocol"])
        self.assertEqual({"id": 25, "unit": 16, "state": True}, results[0]["values"])

    def test_decode_pulses_switch4(self) -> None:
        results = controller.decode_pulses(
            [295, 1180, 11210], "01010110010101100110011001100110010101100110011002"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch4", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch4", results[0]["protocol"])
        self.assertDictEqual({"id": 2, "unit": 20, "state": True}, results[0]["values"])

    def test_decode_pulses_switch5_1(self) -> None:
        results = controller.decode_pulses(
            [295, 886, 9626], "10010101101010010110010110101001010101011010101002"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch5", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch5", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 465695,
                "unit": 1,
                "all": False,
                "state": True,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch5_2(self) -> None:
        results = controller.decode_pulses(
            [295, 886, 9626], "10010101101010010110010110101001010101011010100102"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch5", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch5", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 465695,
                "unit": 1,
                "all": False,
                "state": False,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch5_3(self) -> None:
        results = controller.decode_pulses(
            [295, 886, 9626], "10010101101010010110010110101001010101011010011002"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch5", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch5", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 465695,
                "unit": 2,
                "all": False,
                "state": True,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch5_4(self) -> None:
        results = controller.decode_pulses(
            [295, 886, 9626], "10010101101010010110010110101001010101011010010102"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch5", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch5", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 465695,
                "unit": 2,
                "all": False,
                "state": False,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch5_5(self) -> None:
        results = controller.decode_pulses(
            [295, 886, 9626], "10010101101010010110010110101001010101011001101002"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch5", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch5", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 465695,
                "unit": 3,
                "all": False,
                "state": True,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch5_6(self) -> None:
        results = controller.decode_pulses(
            [295, 886, 9626], "10010101101010010110010110101001010101011001100102"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch5", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch5", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 465695,
                "unit": 3,
                "all": False,
                "state": False,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch5_7(self) -> None:
        results = controller.decode_pulses(
            [295, 886, 9626], "10010101101010010110010110101001010101010110101002"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch5", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch5", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 465695,
                "unit": 4,
                "all": False,
                "state": True,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch5_8(self) -> None:
        results = controller.decode_pulses(
            [295, 886, 9626], "10010101101010010110010110101001010101010110100102"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch5", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch5", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 465695,
                "unit": 4,
                "all": False,
                "state": False,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch5_9(self) -> None:
        results = controller.decode_pulses(
            [295, 886, 9626], "10010101101010010110010110101001010101010101011002"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch5", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch5", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 465695,
                "unit": 0,
                "all": True,
                "state": False,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch5_10(self) -> None:
        results = controller.decode_pulses(
            [295, 886, 9626], "10010101101010010110010110101001010101010101100102"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch5", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch5", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 465695,
                "unit": 0,
                "all": True,
                "state": True,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch6_1(self) -> None:
        results = controller.decode_pulses(
            [150, 453, 4733], "10101010101010101010010101100110011001100110010102"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch6", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch6", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 31,
                "unit": 1,
                "state": True,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch6_2(self) -> None:
        results = controller.decode_pulses(
            [150, 453, 4733], "10101010101010100110011001010110011001100110010102"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch6", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch6", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 15,
                "unit": 2,
                "state": True,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch7_1(self) -> None:
        results = controller.decode_pulses(
            [307, 944, 9712], "01010101010101100110011001100110011001100110011002"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch7", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch7", results[0]["protocol"])
        self.assertDictEqual({"id": 0, "unit": 3, "state": True}, results[0]["values"])

    def test_decode_pulses_switch7_2(self) -> None:
        results = controller.decode_pulses(
            [307, 944, 9712], "01010101010101100101010101010110011001100110011002"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch7", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch7", results[0]["protocol"])
        self.assertDictEqual({"id": 7, "unit": 3, "state": True}, results[0]["values"])

    def test_decode_pulses_switch7_3(self) -> None:
        results = controller.decode_pulses(
            [307, 944, 9712], "10100101011001100101010101010110011001100110011002"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch7", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch7", results[0]["protocol"])
        self.assertDictEqual({"id": 7, "unit": 1, "state": False}, results[0]["values"])

    def test_decode_pulses_switch8_1(self) -> None:
        results = controller.decode_pulses(
            [173, 563, 5740], "01010101010101010110011001100110101001011010010102"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch8", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch8", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 30,
                "unit": "B1",
                "state": False,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch8_2(self) -> None:
        results = controller.decode_pulses(
            [173, 563, 5740], "01010101010101010110011001101010010101010101101002"
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch8", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch8", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 30,
                "unit": "C3",
                "state": True,
            },
            results[0]["values"],
        )

    # def test_decode_pulses_switch9(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([305, 615, 23020], '')
    #     self.assertIsNotNone(results)
    #     results = list(filter(lambda result: result['protocol'] == 'switch9', results))
    #
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch9', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    def test_decode_pulses_switch10(self) -> None:
        results = controller.decode_pulses(
            [271, 1254, 10092],
            "01010000000101010100000100010101010000000101010100000101000100000101000101010001000100010001010001000101000000010102",
        )
        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("switch10", results[0]["protocol"])
        self.assertEqual(
            {
                "id": 3162089194,
                "unit": 35,
                "all": False,
                "state": False,
            },
            results[0]["values"],
        )

    def test_decode_pulses_switch11_1(self) -> None:
        results = controller.decode_pulses(
            [566, 1267, 6992],
            "100101010110011010101001101001010101100110010110011010100110011002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch11", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch11", results[0]["protocol"])
        self.assertDictEqual(
            {"id": 34037, "unit": 1, "state": True}, results[0]["values"]
        )

    def test_decode_pulses_switch11_2(self) -> None:
        results = controller.decode_pulses(
            [566, 1267, 6992],
            "100101011010011010101001101001010101100110010110011010100110011002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch11", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch11", results[0]["protocol"])
        self.assertEqual({"id": 34037, "unit": 1, "state": False}, results[0]["values"])

    def test_decode_pulses_switch11_3(self) -> None:
        results = controller.decode_pulses(
            [566, 1267, 6992],
            "100101101001011010101001101001010101100110010110011010100110011002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch11", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch11", results[0]["protocol"])
        self.assertDictEqual(
            {"id": 34037, "unit": 0, "state": True}, results[0]["values"]
        )

    def test_decode_pulses_switch11_4(self) -> None:
        results = controller.decode_pulses(
            [566, 1267, 6992],
            "100101100110011010101001101001010101100110010110011010100110011002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch11", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch11", results[0]["protocol"])
        self.assertEqual({"id": 34037, "unit": 0, "state": False}, results[0]["values"])

    # def test_decode_pulses_switch12(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([564, 1307, 3237, 51535], '')
    #     self.assertIsNotNone(results)
    #     results = list(filter(lambda result: result['protocol'] == 'switch12', results))
    #
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch12', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch13(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([700, 1400, 81000], '')
    #     self.assertIsNotNone(results)
    #     results = list(filter(lambda result: result['protocol'] == 'switch13', results))
    #
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch13', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch14(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([208, 624, 6556], '')
    #     self.assertIsNotNone(results)
    #     results = list(filter(lambda result: result['protocol'] == 'switch14', results))
    #
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch14', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch15(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([300, 914, 9624], '')
    #     self.assertIsNotNone(results)
    #     results = list(filter(lambda result: result['protocol'] == 'switch15', results))
    #
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch15', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch16(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([330, 1000, 10500], '')
    #     self.assertIsNotNone(results)
    #     results = list(filter(lambda result: result['protocol'] == 'switch16', results))
    #
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch16', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch17(self) -> None:
    #     results = controller.decode_pulses([260, 2680, 1275, 10550], '010200020002000002000200020200020002000200020000020200000202000200020002000200020002000200000200020200000200020200020002000002020003')
    #     self.assertIsNotNone(results)
    #     results = list(filter(lambda result: result['protocol'] == 'switch17', results))
    #
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch17', results[0]['protocol'])
    #     self.assertDictEqual({'id': 59748338, 'unit': 13, 'all': False, 'state': True}, results[0]['values'])
    #
    # def test_decode_pulses_switch21(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([204, 328, 1348, 10320], '')
    #     self.assertIsNotNone(results)
    #     results = list(filter(lambda result: result['protocol'] == 'switch21', results))
    #
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch21', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch22(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([376, 1144, 11720], '')
    #     self.assertIsNotNone(results)
    #     results = list(filter(lambda result: result['protocol'] == 'switch22', results))
    #
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch22', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch23(self) -> None:
    #     results = controller.decode_pulses([356, 716, 15728], '01101010010101011010101010011010100101010101011002')
    #     self.assertIsNotNone(results)
    #     results = list(filter(lambda result: result['protocol'] == 'switch23', results))
    #
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch23', results[0]['protocol'])
    #     self.assertDictEqual({'id': 17, 'unit': 1, 'state': True}, results[0]['values'])
    #
    # def test_decode_pulses_switch24(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([504, 1024, 6120], '')
    #     self.assertIsNotNone(results)
    #     results = list(filter(lambda result: result['protocol'] == 'switch24', results))
    #
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch24', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    def test_decode_pulses_switch25_1(self) -> None:
        results = controller.decode_pulses(
            [350, 880, 10970],
            "101010101010101010101010101010100101010101010101011010100110011002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch25", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch25", results[0]["protocol"])
        self.assertDictEqual({"id": 0, "unit": 14, "state": True}, results[0]["values"])

    def test_decode_pulses_switch25_2(self) -> None:
        results = controller.decode_pulses(
            [350, 880, 10970],
            "101010101010101010101010101010100101010101010101011010100101101002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch25", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch25", results[0]["protocol"])
        self.assertDictEqual(
            {"id": 0, "state": False, "unit": 14}, results[0]["values"]
        )

    def test_decode_pulses_switch25_3(self) -> None:
        results = controller.decode_pulses(
            [350, 880, 10970],
            "101010101010101010101010101010100101010101010101011001101010011002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch25", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch25", results[0]["protocol"])
        self.assertDictEqual({"id": 0, "state": True, "unit": 11}, results[0]["values"])

    def test_decode_pulses_switch25_4(self) -> None:
        results = controller.decode_pulses(
            [350, 880, 10970],
            "101010101010101010101010101010100101010101010101011001101001101002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch25", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch25", results[0]["protocol"])
        self.assertDictEqual(
            {"id": 0, "state": False, "unit": 11}, results[0]["values"]
        )

    def test_decode_pulses_switch25_5(self) -> None:
        results = controller.decode_pulses(
            [350, 880, 10970],
            "101010101010101010101010101010100101010101010101010110101010011002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch25", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch25", results[0]["protocol"])
        self.assertDictEqual({"id": 0, "state": True, "unit": 7}, results[0]["values"])

    def test_decode_pulses_switch25_6(self) -> None:
        results = controller.decode_pulses(
            [350, 880, 10970],
            "101010101010101010101010101010100101010101010101010110101001101002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch25", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch25", results[0]["protocol"])
        self.assertDictEqual({"id": 0, "state": False, "unit": 7}, results[0]["values"])

    def test_decode_pulses_switch25_7(self) -> None:
        results = controller.decode_pulses(
            [350, 880, 10970],
            "101010101010101010101010101010100101010101010101011010011010011002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch25", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch25", results[0]["protocol"])
        self.assertDictEqual({"id": 0, "state": True, "unit": 13}, results[0]["values"])

    def test_decode_pulses_switch25_8(self) -> None:
        results = controller.decode_pulses(
            [350, 880, 10970],
            "101010101010101010101010101010100101010101010101011010011001101002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch25", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch25", results[0]["protocol"])
        self.assertDictEqual(
            {"id": 0, "state": False, "unit": 13}, results[0]["values"]
        )

    def test_decode_pulses_switch25_9(self) -> None:
        results = controller.decode_pulses(
            [350, 880, 10970],
            "101010101010101010101010101010100101010101010101010101010110011002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch25", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch25", results[0]["protocol"])
        self.assertDictEqual({"id": 0, "state": True, "unit": 0}, results[0]["values"])

    def test_decode_pulses_switch25_10(self) -> None:
        results = controller.decode_pulses(
            [350, 880, 10970],
            "101010101010101010101010101010100101010101010101010101010101101002",
        )
        self.assertIsNotNone(results)
        results = list(filter(lambda result: result["protocol"] == "switch25", results))

        self.assertEqual(1, len(results))
        self.assertEqual("switch25", results[0]["protocol"])
        self.assertDictEqual({"id": 0, "state": False, "unit": 0}, results[0]["values"])

    # def test_decode_pulses_switch26(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([480, 1476, 15260], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch26', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch27(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([325, 972, 10130], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch27', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch28(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([310, 524, 1287, 13042], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch28', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch29(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([404, 804, 4028], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch29', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch30(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([520, 1468, 13312], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch30', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch31(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([452, 1336, 3392, 10124], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch31', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch32(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([440, 1300, 13488], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch32', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch33(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([700, 1340, 15000], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch33', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])
    #
    # def test_decode_pulses_switch34(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([316, 844, 10360], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('switch34', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    # def test_decode_pulses_rolling1(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([500, 1000, 3000, 7250], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('rolling1', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    # def test_decode_pulses_doorbell1(self) -> None:
    #     results = controller.decode_pulses([217, 648, 6696], '01101010011001100110011010101010101010101010101002')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('doorbell1', results[0]['protocol'])
    #     self.assertDictEqual({'id': 1361, 'unit': 0, 'state': True}, results[0]['values'])

    # def test_decode_pulses_doorbell3(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([300, 580, 10224], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('doorbell3', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    # def test_decode_pulses_contact1(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([268, 1282, 2632, 10168], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('contact1', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    # def test_decode_pulses_contact2(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([295, 886, 9626], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('contact2', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    # def test_decode_pulses_contact4(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([468, 1364, 14096], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('contact4', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    # def test_decode_pulses_led1(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([350, 1056, 10904], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('led1', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    # def test_decode_pulses_led2(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([434, 1227, 13016], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('led2', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    # def test_decode_pulses_led4(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([346, 966, 9476], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('led4', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    # def test_decode_pulses_shutter3(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([366, 736, 1600, 5204, 10896], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('shutter3', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    # def test_decode_pulses_shutter4(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([352, 712, 1476, 5690], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('shutter4', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    # def test_decode_pulses_shutter5(self) -> None:
    #     assert False, 'Not implemented'
    #     results = controller.decode_pulses([160, 270, 665, 6856], '')
    #     self.assertIsNotNone(results)
    #     self.assertEqual(1, len(results))
    #     self.assertEqual('shutter5', results[0]['protocol'])
    #     self.assertDictEqual({}, results[0]['values'])

    def test_decode_pulses_fixable(self) -> None:
        # Should decode fixable pulses.
        results = controller.decode_pulses(
            [258, 401, 1339, 2715, 10424],
            "030002000202000200000202000002020000020002020000020002020000020201020000020200020000020201020002000200000200020002000200020002000204",
        )
        self.assertLessEqual(1, len(results), "Fixable pulses should be fixed.")

    def test_compress_timings_1(self) -> None:
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
        self.assertIsNotNone(result)
        self.assertEqual([304, 959, 9808], result[0])
        self.assertEqual(
            "01010101011001100101010101100110011001100101011002", result[1]
        )

    def test_compress_timings_2(self) -> None:
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
        self.assertIsNotNone(result)
        self.assertEqual([304, 959, 9808], result[0])
        self.assertEqual(
            "01010101011001100101010101100110011001100101011002", result[1]
        )

    def test_compress_timings_3(self) -> None:
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
        self.assertIsNotNone(result)
        self.assertEqual([304, 957, 9804], result[0])
        self.assertEqual(
            "01010101011001100101010101100110011001100101011002", result[1]
        )

    def test_compress_timings_4(self) -> None:
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
        self.assertIsNotNone(result)
        self.assertEqual([304, 959, 9808], result[0])
        self.assertEqual(
            "01010101011001100101010101100110011001100101011002", result[1]
        )

    def test_compress_timings_5(self) -> None:
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
        self.assertIsNotNone(result)
        self.assertEqual([295, 1180, 11210], result[0])
        self.assertEqual(
            "01010110010101100110011001100110010101100110011002", result[1]
        )

    def test_encode_message_switch1(self) -> None:
        results = controller.encode_pulses(
            "switch1", {"id": 9390234, "all": False, "state": True, "unit": 0}
        )
        self.assertIsNotNone(results)
        self.assertEqual(
            "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010100000100010001000103",
            results["pulses"],
        )

    def test_encode_message_switch2(self) -> None:
        results = controller.encode_pulses(
            "switch2", {"id": 25, "unit": 16, "state": True}
        )
        self.assertIsNotNone(results)
        self.assertEqual(
            "01010101011001100101010101100110011001100101011002", results["pulses"]
        )

    def test_encode_message_switch5(self) -> None:
        results = controller.encode_pulses(
            "switch5", {"id": 465695, "unit": 2, "all": False, "state": True}
        )
        self.assertIsNotNone(results)
        self.assertEqual(
            "10010101101010010110010110101001010101011010011002", results["pulses"]
        )

    def test_encode_message_switch6(self) -> None:
        results = controller.encode_pulses(
            "switch6", {"id": 15, "unit": 2, "state": True}
        )
        self.assertIsNotNone(results)
        self.assertEqual(
            "10101010101010100110011001010110011001100110010102", results["pulses"]
        )

    def test_encode_message_switch7(self) -> None:
        results = controller.encode_pulses(
            "switch7", {"id": 7, "unit": 3, "state": True}
        )
        self.assertIsNotNone(results)
        self.assertEqual(
            "01010101010101100101010101010110011001100110011002", results["pulses"]
        )

    def test_encode_message_switch8(self) -> None:
        results = controller.encode_pulses(
            "switch8", {"id": 30, "unit": "C3", "state": True}
        )
        self.assertIsNotNone(results)
        self.assertEqual(
            "01010101010101010110011001101010010101010101101002", results["pulses"]
        )

    # def test_encode_message_switch9(self) -> None:
    #     results = controller.encode_pulses('switch9', {'id': 2472, 'unit': 65, 'state': True})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('0110100101100110011010101001101010101001011012', results['pulses'])

    def test_encode_message_switch10(self) -> None:
        results = controller.encode_pulses(
            "switch10", {"id": 3162089194, "unit": 35, "all": False, "state": False}
        )
        self.assertIsNotNone(results)
        self.assertEqual(
            "01010000000101010100000100010101010000000101010100000101000100000101000101010001000100010001010001000101000000010102",
            results["pulses"],
        )

    # def test_encode_message_switch12(self) -> None:
    #     results = controller.encode_pulses('switch12', {'id': 9983, 'unit': 1, 'state': True})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('1202021212021212121212121212021212121212121212121203', results['pulses'])
    #
    # def test_encode_message_switch13(self) -> None:
    #     results = controller.encode_pulses('switch13', {'id': 1472, 'unit': 0, 'all': False, 'state': True, 'dimm': False})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('001100110101001010101010101010110010101102', results['pulses'])
    #
    # def test_encode_message_switch14(self) -> None:
    #     results = controller.encode_pulses('switch14', {'id': 0, 'unit': 4, 'all': False, 'state': False})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('01010101010101010101010101010101010101010101100102', results['pulses'])
    #
    # def test_encode_message_switch15(self) -> None:
    #     results = controller.encode_pulses('switch15', {'id': 414908, 'unit': 1, 'all': False, 'state': True})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('01101001011001100110010110011010101001011010101002', results['pulses'])
    #
    # def test_encode_message_switch16(self) -> None:
    #     results = controller.encode_pulses('switch16', {'id': 'A', 'unit': 2, 'state': False})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('01010110011001100110010101100110011001100110010102', results['pulses'])
    #
    # def test_encode_message_switch21(self) -> None:
    #     results = controller.encode_pulses('switch21', {'remoteCode': 0xF150FC, 'unit': 0, 'state': True})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('010101010102010201010101020102010101010201020101010201010202010201010101010101020101020101020101020101010101020102020102010101010201010101020103', results['pulses'])
    #
    # def test_encode_message_switch24(self) -> None:
    #     results = controller.encode_pulses('switch24', {'id': 17, 'unit': 1, 'state': True})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('01101010010101011010100110010110100101010101011002', results['pulses'])

    def test_encode_message_switch25(self) -> None:
        results = controller.encode_pulses(
            "switch25", {"id": 0, "unit": 14, "state": True}
        )
        self.assertIsNotNone(results)
        self.assertEqual(
            "101010101010101010101010101010100101010101010101011010100110011002",
            results["pulses"],
        )

    # def test_encode_message_switch29(self) -> None:
    #     results = controller.encode_pulses('switch29', {'id': 5723557, 'unit': 5621333, 'command': 'panic'})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('00101011101010101101001010101010111000110010101010101011001011001010110012', results['pulses'])
    #
    # def test_encode_message_switch30(self) -> None:
    #     results = controller.encode_pulses('switch30', {'id': 21850, 'unit': 23118, 'command': 'arm'})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('01010101010110100101101001001110101001010101010102', results['pulses'])
    #
    # def test_encode_message_switch31(self) -> None:
    #     results = controller.encode_pulses('switch31', {'all': False, 'channel': 1, 'id': 47333, 'state': True})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('0000220100010101000000010101000001000100010000000101010000000101000100010000000001010103', results['pulses'])
    #
    # def test_encode_message_switch32(self) -> None:
    #     results = controller.encode_pulses('switch32', {'systemCode': 1, 'programCode': 1, 'state': True})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('01010110011001100101011001100110011001100110011002', results['pulses'])

    # def test_encode_message_led3(self) -> None:
    #     results = controller.encode_pulses('led3', {'id': 14152, 'command': 'cyan'})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('01011010011010100110010110010101010101100110010102', results['pulses'])
    #
    # def test_encode_message_led4(self) -> None:
    #     results = controller.encode_pulses('led4', {'id':796, 'command': 'on/off'})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('', results['pulses'])

    # def test_encode_message_doorbell1(self) -> None:
    #     results = controller.encode_pulses('doorbell1', {'id': 1361, 'unit': 0, 'state': True})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('01101010011001100110011010101010101010101010101002', results['pulses'])

    # def test_encode_message_rolling1(self) -> None:
    #     results = controller.encode_pulses('rolling1', {
    #         'codeOn': [
    #             '011111110000111001011100',
    #             '011101101101100010101100',
    #             '011111011110001001101100',
    #             '011110011010111100011100'
    #         ],
    #         'codeOff': [
    #             '011110001011100110111100',
    #             '011110101001110001111100',
    #             '011100010001011100101100',
    #             '011101110011101010001100'
    #         ],
    #         'state': True })
    #     self.assertIsNotNone(results)
    #     self.assertEqual('01101010101010100101010110101001011001101010010123', results['pulses'])

    # def test_encode_message_shutter3(self) -> None:
    #     results = controller.encode_pulses('shutter3', {'id': 151368466, 'channel': 9, 'command': 'program'})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('3210010110010101010110011010011010010110100101011001011001100101101010010110100104', results['pulses'])
    #
    # def test_encode_message_shutter4(self) -> None:
    #     results = controller.encode_pulses('', {'id': 17959394, 'channel': 0, 'all': True, 'command': 'up'})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('3201010110010101100101100101010101100101101010100101011001010101010101011001010113', results['pulses'])
    #
    # def test_encode_message_shutter5(self) -> None:
    #     results = controller.encode_pulses('shutter5', {'id': 281971, 'command': 'down'})
    #     self.assertIsNotNone(results)
    #     self.assertEqual('02210202022102022121022102212121020221210221020203', results['pulses'])

    def test_fix_pulses_1(self) -> None:
        # Should fix the pulses.
        result = controller.fix_pulses(
            [258, 401, 1339, 2715, 10424],
            "030002000202000200000202000002020000020002020000020002020000020201020000020200020000020201020002000200000200020002000200020002000204",
        )
        self.assertIsNotNone(result)
        self.assertEqual(
            [
                329,
                1339,
                2715,
                10424,
            ],
            result[0],
        )
        self.assertEqual(
            "020001000101000100000101000001010000010001010000010001010000010100010000010100010000010100010001000100000100010001000100010001000103",
            result[1],
        )

    def test_fix_pulses_2(self) -> None:
        # Should fix the pulses.
        result = controller.fix_pulses(
            [239, 320, 1337, 2717, 10359],
            "030002000202000201010202010002020101020102020101020102020101020201020101020201020101020201020102010201010201020102010201020112000204",
        )
        self.assertIsNotNone(result)
        self.assertEqual(
            [
                279,
                1337,
                2717,
                10359,
            ],
            result[0],
        )
        self.assertEqual(
            "020001000101000100000101000001010000010001010000010001010000010100010000010100010000010100010001000100000100010001000100010001000103",
            result[1],
        )

    def test_fix_pulses_3(self) -> None:
        # Should not change correct pulses.
        result = controller.fix_pulses(
            [279, 1337, 2717, 10359],
            "020001000101000100000101000001010000010001010000010001010000010100010000010100010000010100010001000100000100010001000100010001000103",
        )
        self.assertIsNone(result)
