# Python library rfcontrolpy

![Python][python-shield]
[![GitHub Release][releases-shield]][releases]
[![Licence][license-shield]][license]
[![Maintainer][maintainer-shield]][maintainer]  
[![Github Sponsors][github-shield]][github]
[![PayPal][paypal-shield]][paypal]
[![BuyMeCoffee][buymecoffee-shield]][buymecoffee]
[![Patreon][patreon-shield]][patreon]

## Introduction

rfcontrolpy is a Python library and port of the node.js [rfcontroljs](https://github.com/pimatic/rfcontroljs)
module for parsing and constructing 433mhz On-Off Keying (OOK) signals for various devices,
switches and weather stations.

It works together with the [RFControl](https://github.com/pimatic/RFControl) Arduino library
for receiving the signals.

The Python port now contains a working controller and a dozen of protocols. Not all protocols are
ported yet due to low demand or lack of hardware.

You can find a list of all supported protocols [here](protocols.md).

## The Processing Pipeline

### Receiving

The arduino is connected via serial bus to the processing computer (for example a raspberry pi)
and waits for rf signal. 

> Mostly all 433mhzw OOK signals from devices are send multiple times directly in row and have a
> longer footer pulse in between. They differ by the pulse lengths used to encode the data and footer 
> and the pulse count.

[RFControl](https://github.com/rrooggiieerr/RFControl) running on the Arduino detects the start of a 
signal by its longer footer pulse and verifies it one time by comparing it with the next signal. 
It is unaware of the specific protocol, it just uses the stated fact above. Also we are 
not interested in it if the pulse was a high or low pulse (presence or absence of a carrier wave), 
because the information is decoded in the pulse lengths.

We will call the received sequence of pulse lengths now **timings sequence**. For example a timing
sequence in microseconds could look like this:

```
288  972  292  968  292  972  292  968  292  972  920  344  288  976  920  348  
284  976  288  976  284  976  288  976  288  976  916  348  284  980  916  348  
284  976  920  348  284  976  920  348  284  980  280  980  284  980  916  348  
284  9808
```

You can clearly see the two different pulse lengths (around 304 and 959 microseconds) for the data
encoding and the longer footer pulse (9808 microseconds). 

All observed protocols have less than 8 different pulse length and all pulse length do differ by at 
least a factor of 2. This makes a further compression and simplification possible: We map each 
pulse length to a number from 0 to 7 (a bucket) and calculate for a better accuracy the average of 
all timings mapped to each of the bucket. The result is something like that:

```
buckets: 304, 959, 9808
pulses: 01010101011001100101010101100110011001100101011002
```

To make the representation unique, we choose the buckets in ascending order (respectively we are
sorting it after receiving from the Arduino).

We call the sorted buckets **pulse lengths**, the compressed timings **pulse sequence** and the 
length of the pulse sequence (inclusive footer) **pulse count**.

### Protocol Matching

We detect possible protocols by two criteria. The pulse length must match with a small tolerance
and the pulse count must match. 

### Protocol Parsing

If a protocol matches, its `parse` function is called with the pulse sequence. Most protocols are
parsed almost the same way. First the pulse sequence must be converted to a binary representation.

In almost all cases there exist a mapping from pulse sequences to a binary `0` and `1`. In this
example the pulse sequence `0110` represents a binary `0` and `0101` maps to a binary `1`:

```Python
pulses2binary_mapping = {
  ["0110": "0"], # Binary 0
  ["0101": "1"], # Binary 1 
  ["02": ""]     # Footer
}
binary = helpers.pulses2binary(pulses, pulses2binary_mapping)
```

The binary representation now looks like this:

```
110011000010
```

As last step the protocol dependent information must be extracted from the binary representation:

```Python
decoded = {
  "id": int(binary[:6], 2),
  "unit": int(binary[6:11], 2),
  "state": binary[12] == "1"
}
```

## Details

RFControl is more sensitive than needed for most protocols. 
So we get sometimes, depending of the accuracy of the sender/remote, different bucket counts. 

This is by design, to catch up further protocols that maybe need a higher sensitivity. The specific
protocol has not to deal with this issue, because `rfcontrolpy` auto merges similar buckets before
calling the `decodePulses` function of each protocol.

The algorithm is the following:

1. Record the (maybe to many) buckets and compressed pulses with [RFControl](https://github.com/pimatic/RFControl) (Arduino / c++)
2. Sort the buckets in `rfcontrolpy` `prepare_compressed_pulses`
3. Try to find a matching protocol in rfcontrolpy `decode_pulses`
4. If we have more than 3 buckets and two of the buckets are similar (`b1*2 < b2`) we merge them to just one bucket by averaging and adapting the pulses in rfcontrolpy `fix_pulses`
5. Go to step 3

## Adding a new Protocol

### Preparation

1. Fork the rfcontrolpy repository and clone your fork into a local directory.
2. We are using [unittest](https://docs.python.org/3/library/unittest.html) for automating tests.
3. You should be able to run the tests with `python3 -m unittest discover`.
5. Running `python3 -m build` let it compile all files and whats for changes.

### Protocol development

1. Create a new protocol file (like the others) in `rfcontrol/protocols/`.
2. Add a test case in `tests/protocols` with the data from the Arduino.
3. Adapt the protocol file, so that the test get passed.

## Support my work

Do you enjoy using this Python library? Then consider supporting my work using one of the following
platforms, your donation is greatly appreciated and keeps me motivated:

[![Github Sponsors][github-shield]][github]
[![PayPal][paypal-shield]][paypal]
[![BuyMeCoffee][buymecoffee-shield]][buymecoffee]
[![Patreon][patreon-shield]][patreon]

## Hire me

If you're in need for a freelance Python developer for your project please contact me, you can find
my email address on [my GitHub profile](https://github.com/rrooggiieerr).

---

[python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[releases]: https://github.com/rrooggiieerr/rfcontrolpy/releases
[releases-shield]: https://img.shields.io/github/v/release/rrooggiieerr/rfcontrolpy?style=for-the-badge
[license]: ./LICENSE
[license-shield]: https://img.shields.io/github/license/rrooggiieerr/rfcontrolpy?style=for-the-badge
[maintainer]: https://github.com/rrooggiieerr
[maintainer-shield]: https://img.shields.io/badge/MAINTAINER-%40rrooggiieerr-41BDF5?style=for-the-badge
[paypal]: https://paypal.me/seekingtheedge
[paypal-shield]: https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white
[buymecoffee]: https://www.buymeacoffee.com/rrooggiieerr
[buymecoffee-shield]: https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black
[github]: https://github.com/sponsors/rrooggiieerr
[github-shield]: https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=ea4aaa
[patreon]: https://www.patreon.com/seekingtheedge/creators
[patreon-shield]: https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white
