# Supported protocols

rfcontrolpy supports 88 protocols, ported from the original [rfcontroljs](https://github.com/pimatic/rfcontroljs/blob/master/protocols.md) implementation.

| Protocol | Type | Brands | Encode |
| --- | --- | --- | --- |
| [alarm1](#alarm1) | alarm | FA20RF | yes |
| [alarm2](#alarm2) | alarm | FA21RF | yes |
| [alarm3](#alarm3) | alarm | Smartwares RM174RF (provisional) | no |
| [awning1](#awning1) | awning | awningCode | yes |
| [awning2](#awning2) | awning | Soluna | yes |
| [contact1](#contact1) | contact | KlikAanKlikUit | no |
| [contact2](#contact2) | contact | No brand | no |
| [contact3](#contact3) | contact | Home Easy HE852 | no |
| [contact4](#contact4) | contact | GS-IWDS07 | yes |
| [dimmer1](#dimmer1) | dimmer | CoCo Technologies, D-IO (Chacon), Intertechno, KlikAanKlikUit, Nexa | yes |
| [dimmer2](#dimmer2) | dimmer | LightwaveRF | yes |
| [doorbell1](#doorbell1) | doorbell | ADEO, ELRO/Home Easy HE-852 | yes |
| [doorbell2](#doorbell2) | doorbell | LIFETEC-MD13187 | yes |
| [doorbell3](#doorbell3) | doorbell | Smarthome WP515S | yes |
| [generic](#generic) | generic | homemade | no |
| [generic2](#generic2) | generic | homemade | no |
| [led1](#led1) | led | LED Stripe RF Dimmer (no name) | yes |
| [led2](#led2) | led | LED Controller | yes |
| [led3](#led3) | led | LED Controller | yes |
| [led4](#led4) | led | LED Controller | yes |
| [pir1](#pir1) | pir | ? | no |
| [pir2](#pir2) | pir | Multi Kon Trade B00RTDMC4S | no |
| [pir3](#pir3) | pir | Inter-Union | no |
| [pir4](#pir4) | pir | SelectPlus Doorbell | no |
| [pir5](#pir5) | pir | Trust SmartHome, COCO Technologies, KlikAanKlikUit | no |
| [pir6](#pir6) | pir | Zanbo (ZABC86-1), Unknown (OSW-1-3 and OTW-1-3) | no |
| [rawshutter](#rawshutter) | shutter | RAW | yes |
| [rawswitch](#rawswitch) | switch | RAW | yes |
| [rolling1](#rolling1) | rolling | rollingCode | yes |
| [shutter1](#shutter1) | shutter | Nobily | yes |
| [shutter3](#shutter3) | shutter | Romotec | yes |
| [shutter4](#shutter4) | shutter | ROHRMOTOR24 | yes |
| [shutter5](#shutter5) | shutter | eSmart | yes |
| [switch1](#switch1) | switch | CoCo Technologies, D-IO (Chacon), Intertechno, KlikAanKlikUit, Nexa | yes |
| [switch2](#switch2) | switch | Elro, Elro Home Easy | yes |
| [switch3](#switch3) | switch | Brennenstuhl Comfort, Elro Home Control | yes |
| [switch4](#switch4) | switch | Cogex, KlikAanKlikUit, Intertechno, Düwi Terminal | yes |
| [switch5](#switch5) | switch | Eurodomest | yes |
| [switch6](#switch6) | switch | Impuls | yes |
| [switch7](#switch7) | switch | eHome | yes |
| [switch8](#switch8) | switch | Rev | yes |
| [switch9](#switch9) | switch | DRU Heaters | yes |
| [switch10](#switch10) | switch | Easy Home Advanced | yes |
| [switch11](#switch11) | switch | McPower | yes |
| [switch12](#switch12) | switch | Europe RS-200 | yes |
| [switch13](#switch13) | switch | Aldi Quigg GT-7000, Globaltronics GT-FSI-04a | yes |
| [switch14](#switch14) | switch | UNITEC | yes |
| [switch15](#switch15) | switch | Daycom Switches | yes |
| [switch16](#switch16) | switch | Everflourish | yes |
| [switch17](#switch17) | switch | Intertek 22541673 (e.g. Bauhaus) | yes |
| [switch18](#switch18) | switch | Otio, Advisen | yes |
| [switch19](#switch19) | switch | REV Switch 008342 and Dimmer 008343 | yes |
| [switch20](#switch20) | switch | MBO International Electronic GmbH | yes |
| [switch21](#switch21) | switch | LightwaveRF | yes |
| [switch22](#switch22) | switch | Relay 4CH switch | yes |
| [switch23](#switch23) | switch | Atag Cooking hood, TXS4 Transmitter | yes |
| [switch24](#switch24) | switch | Power remote 1204380, Steffen 1204380 | yes |
| [switch25](#switch25) | switch | Lidl 0655B | yes |
| [switch26](#switch26) | switch | Chacon EMW200TC | yes |
| [switch27](#switch27) | switch | Chacon Zen (EMW200TB) | yes |
| [switch28](#switch28) | switch | oh!haus & Co. | yes |
| [switch29](#switch29) | switch | Meiantech, Atlantic, Aidebao, PB-403R | yes |
| [switch30](#switch30) | switch | JP-05 | yes |
| [switch31](#switch31) | switch | Masterplug UK | yes |
| [switch32](#switch32) | switch | Rising Sun RSL366, Conrad RSL366, PROmax | yes |
| [switch33](#switch33) | switch | Lidl Powerfix RCB-I 3600R | yes |
| [switch34](#switch34) | switch | conecto SA-CC50132 | yes |
| [weather1](#weather1) | weather | Logilink WS0002, DANIU | no |
| [weather2](#weather2) | weather | Auriol, Pollin (EWS-151) | no |
| [weather3](#weather3) | weather | TFA, Conrad Electronic | no |
| [weather4](#weather4) | weather | Auriol | no |
| [weather5](#weather5) | weather | Auriol, Ventus, Hama, Meteoscan, Alecto, Balance | no |
| [weather6](#weather6) | weather | Sempre GT-WT-02 | no |
| [weather7](#weather7) | weather | Auriol IAN 9183 | no |
| [weather8](#weather8) | weather | ? | no |
| [weather9](#weather9) | weather | TCM | no |
| [weather10](#weather10) | weather | Velleman WS8426S | no |
| [weather11](#weather11) | weather | Xiron Temperature & Humidity Sensor | no |
| [weather12](#weather12) | weather | Globaltronics GT-WT-01 | no |
| [weather13](#weather13) | weather | Xiron Temperature & Humidity Sensor 2 | no |
| [weather14](#weather14) | weather | Prologue Temperature & Humidity Sensor | no |
| [weather15](#weather15) | weather | Globaltronics GT-WT-01 variant, Freetec PT-250 | no |
| [weather16](#weather16) | weather | Ea2 labs Bl999 | no |
| [weather17](#weather17) | weather | TFA 30.3125 | no |
| [weather18](#weather18) | weather | Mebus/Renkforce E0190T | no |
| [weather19](#weather19) | weather | Landmann BBQ Thermometer | no |
| [weather20](#weather20) | weather | Freetec PT-250 variant | no |
| [weather21](#weather21) | weather | Auriol HG02832, Auriol HG05124A-DCF, Auriol IAN 321304_1901, Rubicson 48957 | no |

## alarm1

Smoke alarms.

**Type**: alarm  
**Brands**: FA20RF  
**Pulse lengths**: 800, 1423, 2760, 8040, 13000  
**Pulse count**: 52

**Decoded values**:

- `id`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `state` (default `True`): True to trigger the alarm. For False the original implementation sends ``"0"``, which is kept for compatibility.

## alarm2

Smoke alarms.

**Type**: alarm  
**Brands**: FA21RF  
**Pulse lengths**: 805, 1377, 2710, 8104, 22564  
**Pulse count**: 52

**Decoded values**:

- `id`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `state` (default `True`): True to trigger the alarm. For False the original implementation sends ``"0"``, which is kept for compatibility.

## alarm3

Smoke alarms (provisional).

**Type**: alarm  
**Brands**: Smartwares RM174RF (provisional)  
**Pulse lengths**: 472, 1236, 11688  
**Pulse count**: 54

**Decoded values**:

- `id`
- `state`

**Encode parameters**:

Encoding isn't supported.

## awning1

Awning motors.

**Type**: awning  
**Brands**: awningCode  
**Pulse lengths**: 352, 740, 1580, 4720, 7772  
**Pulse count**: 164

**Decoded values**:

- `id`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `command`: ``in``, ``out`` or ``stop``.

## awning2

Awning motors.

**Type**: awning  
**Brands**: Soluna  
**Pulse lengths**: 359, 718, 1532, 4740, 10048  
**Pulse count**: 82

**Decoded values**:

- `id`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `command`: ``in``, ``out`` or ``stop``.

## contact1

Door/window contacts.

**Type**: contact  
**Brands**: KlikAanKlikUit  
**Pulse lengths**: 268, 1282, 2632, 10168  
**Pulse count**: 132, 148

**Decoded values**:

- `id`
- `all`
- `state`
- `unit`

**Encode parameters**:

Encoding isn't supported.

## contact2

Door/window contacts.

**Type**: contact  
**Brands**: No brand  
**Pulse lengths**: 295, 886, 9626  
**Pulse count**: 50

**Decoded values**:

- `id`
- `state`

**Encode parameters**:

Encoding isn't supported.

## contact3

Door/window contacts.

**Type**: contact  
**Brands**: Home Easy HE852  
**Pulse lengths**: 310, 950, 9644  
**Pulse count**: 50

**Decoded values**:

- `id`
- `state`

**Encode parameters**:

Encoding isn't supported.

## contact4

Door/window contact sensor with low-battery flag.

**Type**: contact  
**Brands**: GS-IWDS07  
**Pulse lengths**: 468, 1364, 14096  
**Pulse count**: 50

**Decoded values**:

- `id`
- `state`
- `lowBattery`

**Encode parameters**:

- `id`: Device ID.
- `state`: Contact state.
- `low_battery` (default `False`): True if the battery is low.

## dimmer1

Self-learning dimmers.

**Type**: dimmer  
**Brands**: CoCo Technologies, D-IO (Chacon), Intertechno, KlikAanKlikUit, Nexa  
**Pulse lengths**: 260, 1300, 2700, 10400  
**Pulse count**: 148

**Decoded values**:

- `id`
- `unit`
- `all`
- `state`
- `dimlevel`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state` (default `None`): True for on, False for off, None to leave unchanged.
- `dimlevel` (default `None`): Dim level, 0-15. Without a dim level a plain on/off message is sent, which is the same as switch1.
- `all` (default `False`): Address all units in the group.

## dimmer2

Support for LightwaveRF dimmers.

**Type**: dimmer  
**Brands**: LightwaveRF  
**Pulse lengths**: 204, 328, 1348, 10320  
**Pulse count**: 144

**Decoded values**:

- `id`
- `unit`
- `state`
- `dimlevel`

**Encode parameters**:

- `id`: Remote ID.
- `unit`: Unit code.
- `state` (default `None`): Ignored; derived from ``dimlevel``.
- `dimlevel` (default `None`): Dim level, 1-31 for on, anything else for off.
- `all` (default `False`): Ignored by this protocol.

## doorbell1

Doorbells.

**Type**: doorbell  
**Brands**: ADEO, ELRO/Home Easy HE-852  
**Pulse lengths**: 217, 648, 6696  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## doorbell2

Doorbells, handled as a PIR sensor.

**Type**: doorbell  
**Brands**: LIFETEC-MD13187  
**Pulse lengths**: 491, 1491, 19270  
**Pulse count**: 48

**Decoded values**:

- `unit`
- `id`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state` (default `True`): Ignored by this protocol.
- `all` (default `False`): Ignored by this protocol.

## doorbell3

Doorbells.

**Type**: doorbell  
**Brands**: Smarthome WP515S  
**Pulse lengths**: 300, 580, 10224  
**Pulse count**: 26

**Decoded values**:

- `id`
- `unit`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state` (default `True`): Ignored by this protocol.
- `all` (default `False`): Ignored by this protocol.

## generic

Homemade sensors sending a typed numeric value.

**Type**: generic  
**Brands**: homemade  
**Pulse lengths**: 671, 2049, 4346, 10208  
**Pulse count**: 198

**Decoded values**:

- `id`
- `type`
- `positive`
- `value`

**Encode parameters**:

Encoding isn't supported.

## generic2

Homemade sensors with battery level and checksum.

**Type**: generic  
**Brands**: homemade  
**Pulse lengths**: 480, 1320, 13320  
**Pulse count**: 66

**Decoded values**:

- `id`
- `type`
- `value`
- `freq`
- `battery`
- `checksum`

**Encode parameters**:

Encoding isn't supported.

## led1

LED strip RF dimmer.

**Type**: led  
**Brands**: LED Stripe RF Dimmer (no name)  
**Pulse lengths**: 439, 1240, 12944  
**Pulse count**: 50

**Decoded values**:

- `id`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `command`: One of the commands, or ``code:<8 bits>`` for any other command code.

## led2

LED controller.

**Type**: led  
**Brands**: LED Controller  
**Pulse lengths**: 439, 1240, 12944  
**Pulse count**: 50

**Decoded values**:

- `id`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `command`: One of the commands, or ``code:<8 bits>`` for any other command code.

## led3

LED controller.

**Type**: led  
**Brands**: LED Controller  
**Pulse lengths**: 439, 1240, 12944  
**Pulse count**: 50

**Decoded values**:

- `id`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `command`: One of the commands, or ``code:<8 bits>`` for any other command code.

## led4

LED controller.

**Type**: led  
**Brands**: LED Controller  
**Pulse lengths**: 345, 967, 9484  
**Pulse count**: 50

**Decoded values**:

- `id`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `command`: One of the commands, or ``code:<8 bits>`` for any other command code.

## pir1

Motion sensor, brand unknown.

**Type**: pir  
**Brands**: ?  
**Pulse lengths**: 358, 1095, 11244  
**Pulse count**: 50

**Decoded values**:

- `unit`
- `id`
- `state`

**Encode parameters**:

Encoding isn't supported.

## pir2

Motion sensor.

**Type**: pir  
**Brands**: Multi Kon Trade B00RTDMC4S  
**Pulse lengths**: 451, 1402, 14356  
**Pulse count**: 50

**Decoded values**:

- `unit`
- `id`
- `state`

**Encode parameters**:

Encoding isn't supported.

## pir3

Motion sensor.

**Type**: pir  
**Brands**: Inter-Union  
**Pulse lengths**: 496, 1471, 6924  
**Pulse count**: 66

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

Encoding isn't supported.

## pir4

SelectPlus doorbell, handled as a PIR sensor.

**Type**: pir  
**Brands**: SelectPlus Doorbell  
**Pulse lengths**: 371, 1081, 5803  
**Pulse count**: 36

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

Encoding isn't supported.

## pir5

Motion sensors.

**Type**: pir  
**Brands**: Trust SmartHome, COCO Technologies, KlikAanKlikUit  
**Pulse lengths**: 268, 1282, 2632, 10168  
**Pulse count**: 132, 148

**Decoded values**:

- `id`
- `all`
- `state`
- `unit`

**Encode parameters**:

Encoding isn't supported.

## pir6

Motion sensor with a 24-bit ID.

**Type**: pir  
**Brands**: Zanbo (ZABC86-1), Unknown (OSW-1-3 and OTW-1-3)  
**Pulse lengths**: 288, 864, 8964  
**Pulse count**: 50

**Decoded values**:

- `id`
- `state`

**Encode parameters**:

Encoding isn't supported.

## rawshutter

Replay recorded pulse sequences of any shutter.

**Type**: shutter  
**Brands**: RAW  
**Pulse lengths**: set by encode  
**Pulse count**: set by encode

Decoding isn't supported.

**Encode parameters**:

- `pulse_lengths`: Pulse lengths of the recorded signals.
- `pulses_up`: Recorded pulse sequence for up.
- `pulses_down`: Recorded pulse sequence for down.
- `pulses_stop`: Recorded pulse sequence for stop.
- `command` (default `None`): ``up``, ``down`` or ``stop``.

## rawswitch

Replay recorded pulse sequences of any switch.

**Type**: switch  
**Brands**: RAW  
**Pulse lengths**: set by encode  
**Pulse count**: set by encode

Decoding isn't supported.

**Encode parameters**:

- `pulse_lengths`: Pulse lengths of the recorded signals.
- `pulses_on`: Recorded pulse sequence for on.
- `pulses_off`: Recorded pulse sequence for off.
- `state`: True for on, False for off.

## rolling1

Rolling code switches.

**Type**: rolling  
**Brands**: rollingCode  
**Pulse lengths**: 500, 1000, 3000, 7250  
**Pulse count**: 50

**Decoded values**:

- `code`

**Encode parameters**:

- `code_on`: Recorded binary codes for on; the first one is sent.
- `code_off`: Recorded binary codes for off; the first one is sent.
- `state`: True for on, False for off.

## shutter1

Shutter motors.

**Type**: shutter  
**Brands**: Nobily  
**Pulse lengths**: 280, 736, 1532, 4752, 7796  
**Pulse count**: 164

**Decoded values**:

- `id`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `command`: ``up``, ``down`` or ``stop``.

## shutter3

Shutter motors.

**Type**: shutter  
**Brands**: Romotec  
**Pulse lengths**: 366, 736, 1600, 5204, 10896  
**Pulse count**: 82

**Decoded values**:

- `id`
- `channel`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `channel`: Channel.
- `command`: ``up``, ``down``, ``stop`` or ``program``.

## shutter4

Shutter motors.

**Type**: shutter  
**Brands**: ROHRMOTOR24  
**Pulse lengths**: 352, 712, 1476, 5690  
**Pulse count**: 82

**Decoded values**:

- `id`
- `channel`
- `all`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `command`: ``up``, ``down`` or ``stop``.
- `channel` (default `0`): Channel, ignored when ``all`` is True.
- `all` (default `False`): Address all channels.

## shutter5

Shutter motors.

**Type**: shutter  
**Brands**: eSmart  
**Pulse lengths**: 160, 270, 665, 6856  
**Pulse count**: 50

**Decoded values**:

- `id`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `command`: ``up``, ``down`` or ``stop``.

## switch1

Self-learning switches.

**Type**: switch  
**Brands**: CoCo Technologies, D-IO (Chacon), Intertechno, KlikAanKlikUit, Nexa  
**Pulse lengths**: 268, 1282, 2632, 10168  
**Pulse count**: 132

**Decoded values**:

- `id`
- `unit`
- `all`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Address all units in the group.

## switch2

House code / unit code switches.

**Type**: switch  
**Brands**: Elro, Elro Home Easy  
**Pulse lengths**: 306, 957, 9808  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: House code.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch3

House code / unit code switches.

**Type**: switch  
**Brands**: Brennenstuhl Comfort, Elro Home Control  
**Pulse lengths**: 306, 957, 9808  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: House code.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch4

Unit / ID switches.

**Type**: switch  
**Brands**: Cogex, KlikAanKlikUit, Intertechno, Düwi Terminal  
**Pulse lengths**: 306, 957, 9808  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch5

20-bit ID switches.

**Type**: switch  
**Brands**: Eurodomest  
**Pulse lengths**: 295, 886, 9626  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `all`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code, 1-4.
- `state`: True for on, False for off.
- `all` (default `False`): Address all units in the group.

## switch6

System code / program code switches.

**Type**: switch  
**Brands**: Impuls  
**Pulse lengths**: 150, 453, 4733  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: System code.
- `unit`: Program code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch7

3-bit unit / 3-bit ID switches.

**Type**: switch  
**Brands**: eHome  
**Pulse lengths**: 307, 944, 9712  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch8

Tri-state system code / program code switches.

**Type**: switch  
**Brands**: Rev  
**Pulse lengths**: 189, 547, 5720  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: System code.
- `unit`: Unit as a letter plus number, like ``'E10'``.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch9

Heater switches.

**Type**: switch  
**Brands**: DRU Heaters  
**Pulse lengths**: 300, 600, 23000  
**Pulse count**: 46

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch10

System code / group / unit switches.

**Type**: switch  
**Brands**: Easy Home Advanced  
**Pulse lengths**: 271, 1254, 10092  
**Pulse count**: 116

**Decoded values**:

- `id`
- `unit`
- `all`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Address all units in the group.

## switch11

McPower switches.

**Type**: switch  
**Brands**: McPower  
**Pulse lengths**: 566, 1267, 6992  
**Pulse count**: 66

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch12

Switches with units 1 to 4.

**Type**: switch  
**Brands**: Europe RS-200  
**Pulse lengths**: 562, 1313, 3234, 34888  
**Pulse count**: 52

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code, 1-4.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch13

Switches with a parity bit.

**Type**: switch  
**Brands**: Aldi Quigg GT-7000, Globaltronics GT-FSI-04a  
**Pulse lengths**: 700, 1400, 81000  
**Pulse count**: 42

**Decoded values**:

- `id`
- `unit`
- `all`
- `state`
- `dimm`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Address all units.
- `dimm` (default `False`): Dim command.

## switch14

Switches with units 1 to 4.

**Type**: switch  
**Brands**: UNITEC  
**Pulse lengths**: 209, 623, 6288  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `all`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code, 1-4.
- `state`: True for on, False for off.
- `all` (default `False`): Address all units.

## switch15

Switches with units 1 to 4.

**Type**: switch  
**Brands**: Daycom Switches  
**Pulse lengths**: 300, 914, 9624  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`
- `all`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code, 1-4.
- `state`: True for on, False for off.
- `all` (default `False`): Address all units.

## switch16

Tri-state switches with letter IDs.

**Type**: switch  
**Brands**: Everflourish  
**Pulse lengths**: 330, 1000, 10500  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: Device ID, a letter from A to D.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch17

Self-learning switches.

**Type**: switch  
**Brands**: Intertek 22541673 (e.g. Bauhaus)  
**Pulse lengths**: 260, 1275, 2680, 10550  
**Pulse count**: 132

**Decoded values**:

- `id`
- `all`
- `state`
- `unit`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Address all units.

## switch18

Switches with a 28-bit ID.

**Type**: switch  
**Brands**: Otio, Advisen  
**Pulse lengths**: 600, 1200, 3500, 7000  
**Pulse count**: 68

**Decoded values**:

- `id`
- `state`

**Encode parameters**:

- `id`: Device ID.
- `state`: True for on, False for off.
- `unit` (default `0`): Ignored by this protocol.
- `all` (default `False`): Ignored by this protocol.

## switch19

Switches and dimmers with letter IDs and units 1 to 3.

**Type**: switch  
**Brands**: REV Switch 008342 and Dimmer 008343  
**Pulse lengths**: 472, 1436, 14776  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: Device ID, a letter from A to D.
- `unit`: Unit code, 1-3.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch20

Switches with a 4-bit unit code.

**Type**: switch  
**Brands**: MBO International Electronic GmbH  
**Pulse lengths**: 128, 400, 4152  
**Pulse count**: 50

**Decoded values**:

- `unit`
- `state`

**Encode parameters**:

- `unit`: Unit code.
- `state`: True for on, False for off.
- `id` (default `0`): Ignored by this protocol.
- `all` (default `False`): Ignored by this protocol.

## switch21

LightwaveRF switches.

**Type**: switch  
**Brands**: LightwaveRF  
**Pulse lengths**: 204, 328, 1348, 10320  
**Pulse count**: 144

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: Remote ID.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch22

Remotes with four buttons A to D.

**Type**: switch  
**Brands**: Relay 4CH switch  
**Pulse lengths**: 376, 1144, 11720  
**Pulse count**: 50

**Decoded values**:

- `id`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `command`: ``A``, ``B``, ``C`` or ``D``.

## switch23

Remotes with four buttons A to D.

**Type**: switch  
**Brands**: Atag Cooking hood, TXS4 Transmitter  
**Pulse lengths**: 350, 720, 16000  
**Pulse count**: 38

**Decoded values**:

- `id`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `command`: ``A``, ``B``, ``C`` or ``D``; anything else sends ``A``.

## switch24

Switches with house code and unit code.

**Type**: switch  
**Brands**: Power remote 1204380, Steffen 1204380  
**Pulse lengths**: 512, 1024, 6144  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: House code.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch25

4-key remote with a master key.

**Type**: switch  
**Brands**: Lidl 0655B  
**Pulse lengths**: 350, 880, 10970  
**Pulse count**: 66

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: Ignored; the remote has a fixed prefix.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch26

Tri-state switches with a channel letter and a unit.

**Type**: switch  
**Brands**: Chacon EMW200TC  
**Pulse lengths**: 480, 1476, 15260  
**Pulse count**: 50

**Decoded values**:

- `channel`
- `unit`
- `state`

**Encode parameters**:

- `channel`: Channel letter, or raw channel bits.
- `unit`: Unit as a string, or raw unit and constant bits.
- `state`: True for on, False for off.

## switch27

Tri-state switches with a channel letter and a unit.

**Type**: switch  
**Brands**: Chacon Zen (EMW200TB)  
**Pulse lengths**: 325, 972, 10130  
**Pulse count**: 50

**Decoded values**:

- `channel`
- `unit`
- `state`

**Encode parameters**:

- `channel`: Channel letter, or raw channel bits.
- `unit`: Unit as a string, or raw unit and constant bits.
- `state`: True for on, False for off.

## switch28

Remotes with on, off and both buttons.

**Type**: switch  
**Brands**: oh!haus & Co.  
**Pulse lengths**: 417, 1287, 13042  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `command`: ``on``, ``off`` or ``both``.

## switch29

Wireless keychain remotes.

**Type**: switch  
**Brands**: Meiantech, Atlantic, Aidebao, PB-403R  
**Pulse lengths**: 404, 804, 4028  
**Pulse count**: 74

**Decoded values**:

- `id`
- `unit`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `command`: ``arm``, ``panic``, ``disarm``, ``home``, ``grp1``, ``grp2``, ``grp3``.

## switch30

Alarm keypads.

**Type**: switch  
**Brands**: JP-05  
**Pulse lengths**: 520, 1468, 13312  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `command`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `command`: ``arm``, ``dis``, ``byp``, ``sos``.

## switch31

Sockets with channels 1 to 4.

**Type**: switch  
**Brands**: Masterplug UK  
**Pulse lengths**: 452, 1336, 3392, 10124  
**Pulse count**: 88

**Decoded values**:

- `id`
- `unit`
- `state`
- `all`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Channel, 1-4.
- `state`: True for on, False for off.
- `all` (default `False`): Address all channels.

## switch32

Switches with system code and program code positions.

**Type**: switch  
**Brands**: Rising Sun RSL366, Conrad RSL366, PROmax  
**Pulse lengths**: 440, 1300, 13488  
**Pulse count**: 50

**Decoded values**:

- `id`
- `unit`
- `state`

**Encode parameters**:

- `id`: System code, 1-4.
- `unit`: Program code, 1-4.
- `state`: True for on, False for off.
- `all` (default `False`): Ignored by this protocol.

## switch33

Switches with a parity bit.

**Type**: switch  
**Brands**: Lidl Powerfix RCB-I 3600R  
**Pulse lengths**: 700, 1340, 15000  
**Pulse count**: 42

**Decoded values**:

- `id`
- `unit`
- `all`
- `state`
- `dimm`

**Encode parameters**:

- `id`: Device ID.
- `unit`: Unit code.
- `state`: True for on, False for off.
- `all` (default `False`): Address all units.
- `dimm` (default `False`): Dim command.

## switch34

Switches (experimental).

**Type**: switch  
**Brands**: conecto SA-CC50132  
**Pulse lengths**: 316, 844, 10360  
**Pulse count**: 68

**Decoded values**:

- `bits`
- `bytes`
- `id`
- `unit`
- `all`
- `state`

**Encode parameters**:

- `id` (default `0`): Ignored, a fixed code is sent.
- `unit` (default `0`): Ignored, a fixed code is sent.
- `state` (default `True`): Ignored, a fixed code is sent.
- `all` (default `False`): Ignored, a fixed code is sent.

## weather1

Temperature and humidity sensor.

**Type**: weather  
**Brands**: Logilink WS0002, DANIU  
**Pulse lengths**: 456, 1990, 3940, 9236  
**Pulse count**: 74

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `humidity`
- `lowBattery`

**Encode parameters**:

Encoding isn't supported.

## weather2

Temperature sensor.

**Type**: weather  
**Brands**: Auriol, Pollin (EWS-151)  
**Pulse lengths**: 492, 969, 1948, 4004  
**Pulse count**: 74

**Decoded values**:

- `temperature`

**Encode parameters**:

Encoding isn't supported.

## weather3

Temperature and humidity sensor.

**Type**: weather  
**Brands**: TFA, Conrad Electronic  
**Pulse lengths**: 508, 2012, 3908, 7726  
**Pulse count**: 86

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `humidity`

**Encode parameters**:

Encoding isn't supported.

## weather4

Auriol temperature and humidity sensor.

**Type**: weather  
**Brands**: Auriol  
**Pulse lengths**: 526, 990, 1903, 4130, 7828, 16076  
**Pulse count**: 92

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `humidity`
- `lowBattery`

**Encode parameters**:

Encoding isn't supported.

## weather5

Multi-sensor weather stations.

**Type**: weather  
**Brands**: Auriol, Ventus, Hama, Meteoscan, Alecto, Balance  
**Pulse lengths**: 534, 2000, 4000, 9000  
**Pulse count**: 74

**Decoded values**:

- `id`
- `lowBattery`
- `temperature`
- `humidity`
- `avgAirspeed`
- `windDirection`
- `windGust`
- `rain`

**Encode parameters**:

Encoding isn't supported.

## weather6

Temperature and humidity sensor.

**Type**: weather  
**Brands**: Sempre GT-WT-02  
**Pulse lengths**: 552, 2089, 4137, 9032  
**Pulse count**: 80

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `humidity`
- `lowBattery`

**Encode parameters**:

Encoding isn't supported.

## weather7

Auriol IAN 9183 temperature and humidity sensor.

**Type**: weather  
**Brands**: Auriol IAN 9183  
**Pulse lengths**: 456, 1990, 3940, 9236  
**Pulse count**: 66

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `humidity`
- `lowBattery`

**Encode parameters**:

Encoding isn't supported.

## weather8

Temperature and humidity sensor.

**Type**: weather  
**Brands**: ?  
**Pulse lengths**: 200, 1000, 2000, 8000  
**Pulse count**: 74

**Decoded values**:

- `id`
- `temperature`
- `humidity`

**Encode parameters**:

Encoding isn't supported.

## weather9

Temperature and humidity sensor.

**Type**: weather  
**Brands**: TCM  
**Pulse lengths**: 412, 2075, 4115, 8070  
**Pulse count**: 86

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `humidity`
- `lowBattery`
- `sync`

**Encode parameters**:

Encoding isn't supported.

## weather10

Temperature sensor.

**Type**: weather  
**Brands**: Velleman WS8426S  
**Pulse lengths**: 492, 969, 1948, 4004  
**Pulse count**: 74

**Decoded values**:

- `id`
- `unit`
- `temperature`

**Encode parameters**:

Encoding isn't supported.

## weather11

Temperature and humidity sensor.

**Type**: weather  
**Brands**: Xiron Temperature & Humidity Sensor  
**Pulse lengths**: 544, 1056, 1984, 3880  
**Pulse count**: 84

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `humidity`
- `lowBattery`

**Encode parameters**:

Encoding isn't supported.

## weather12

Temperature and humidity sensor.

**Type**: weather  
**Brands**: Globaltronics GT-WT-01  
**Pulse lengths**: 496, 2048, 4068, 8960  
**Pulse count**: 76

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `humidity`
- `lowBattery`

**Encode parameters**:

Encoding isn't supported.

## weather13

Xiron temperature and humidity sensor 2.

**Type**: weather  
**Brands**: Xiron Temperature & Humidity Sensor 2  
**Pulse lengths**: 492, 992, 2028, 4012  
**Pulse count**: 74

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `humidity`
- `lowBattery`

**Encode parameters**:

Encoding isn't supported.

## weather14

Temperature and humidity sensor.

**Type**: weather  
**Brands**: Prologue Temperature & Humidity Sensor  
**Pulse lengths**: 480, 1960, 3908, 8784  
**Pulse count**: 76

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `lowBattery`
- `humidity`

**Encode parameters**:

Encoding isn't supported.

## weather15

Temperature and humidity sensor.

**Type**: weather  
**Brands**: Globaltronics GT-WT-01 variant, Freetec PT-250  
**Pulse lengths**: 496, 2048, 4068, 8960  
**Pulse count**: 76

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `humidity`
- `lowBattery`

**Encode parameters**:

Encoding isn't supported.

## weather16

Temperature and humidity sensor.

**Type**: weather  
**Brands**: Ea2 labs Bl999  
**Pulse lengths**: 500, 1850, 3900, 9000  
**Pulse count**: 74

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `humidity`
- `lowBattery`

**Encode parameters**:

Encoding isn't supported.

## weather17

Temperature or humidity sensor.

**Type**: weather  
**Brands**: TFA 30.3125  
**Pulse lengths**: 444, 1160, 28580  
**Pulse count**: 88

**Decoded values**:

- `id`
- `channel`
- `temperature`
- `humidity`

**Encode parameters**:

Encoding isn't supported.

## weather18

Temperature sensor.

**Type**: weather  
**Brands**: Mebus/Renkforce E0190T  
**Pulse lengths**: 496, 960, 1940, 3904  
**Pulse count**: 76

**Decoded values**:

- `id`
- `unit`
- `temperature`

**Encode parameters**:

Encoding isn't supported.

## weather19

Landmann BBQ thermometer.

**Type**: weather  
**Brands**: Landmann BBQ Thermometer  
**Pulse lengths**: 548, 1008, 1996, 3936  
**Pulse count**: 66

**Decoded values**:

- `id`
- `unit`
- `temperature`

**Encode parameters**:

Encoding isn't supported.

## weather20

Temperature sensor.

**Type**: weather  
**Brands**: Freetec PT-250 variant  
**Pulse lengths**: 560, 972, 1904, 3812, 8556  
**Pulse count**: 76

**Decoded values**:

- `id`
- `unit`
- `temperature`
- `lowBattery`

**Encode parameters**:

Encoding isn't supported.

## weather21

Temperature and humidity sensor.

**Type**: weather  
**Brands**: Auriol HG02832, Auriol HG05124A-DCF, Auriol IAN 321304_1901, Rubicson 48957  
**Pulse lengths**: 196, 288, 628, 61284  
**Pulse count**: 88

**Decoded values**:

- `crcOk`
- `id`
- `humidity`
- `lowBattery`
- `unit`
- `temperature`

**Encode parameters**:

Encoding isn't supported.
