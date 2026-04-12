#!/usr/bin/env python3
import time
import json
import logging
import serial
from collections import defaultdict

# In order to find new sensors or just to monitor the output of this library, 
# you can use this script:

# first be sure to have the correct BAUDRATE (actually 115200)
# and be sure to have access to /dev/ttyUSB0 or the port where homeduino is attached.
# If this is not the case (because homeassistant is running)
# you can add a PTY-bridge:
####  sudo socat -d -d /dev/ttyUSB0,raw,echo=0,nonblock PTY,raw,echo=0,link=/tmp/ttyRF &
# and change SERIAL_PORT to /tmp/ttyRF

# start this script on terminal by 
# python -m rfcontrol_monitor


from rfcontrol import controller  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rfmonitor")

SERIAL_PORT = "/dev/ttyUSB0"
# SERIAL_PORT = "/tmp/ttyRF"  # if socat is used

BAUDRATE = 115200  # anpassen falls nötig
DEBOUNCE_SECONDS = 3
MIN_CONFIRM = 2  # Anzahl gleicher Decodes bevor als "verified" markiert

seen = {}  # key -> {protocol, id, first, last, count, verified, last_values, raw_examples}
pending_counts = defaultdict(int)

def parse_line(line: str):
    # Lines from homeduino look like: "RF receive 1368 460 14056 0 0 0 0 0 0110..."
    parts = line.strip().split()
    if len(parts) < 10:
        return None
    # last part is the pulse sequence string
    pulse_sequence = parts[-1]
    # first 8 numeric fields are pulse lengths (some zero)
    try:
        pulse_lengths = [int(x) for x in parts[2:10]]
    except ValueError:
        return None
    # filter zeros like controller.prepare_compressed_pulses does
    pulse_lengths = [p for p in pulse_lengths if p > 0]
    # sort/reindex like controller.prepare_compressed_pulses -> controller.sort_compressed_pulses
    pulse_lengths, pulse_sequence = controller.sort_compressed_pulses(pulse_lengths, pulse_sequence)
    return pulse_lengths, pulse_sequence

def handle_decode(results):
    now = time.time()
    for r in results:
        proto = r["protocol"]
        vals = r["values"]
        sensor_id = f"{proto}:{vals.get('id')}"
        entry = seen.get(sensor_id)
        if entry is None:
            seen[sensor_id] = {
                "protocol": proto,
                "id": vals.get("id"),
                "first": now,
                "last": now,
                "count": 1,
                "verified": False,
                "last_values": vals,
                "raw_examples": [r],
            }
            pending_counts[sensor_id] = 1
        else:
            # debounce counting
            if now - entry["last"] > DEBOUNCE_SECONDS:
                entry["count"] += 1
            entry["last"] = now
            entry["last_values"] = vals
            entry["raw_examples"].append(r)
            pending_counts[sensor_id] += 1
            # verify after MIN_CONFIRM consistent receptions
            if not entry["verified"] and pending_counts[sensor_id] >= MIN_CONFIRM:
                entry["verified"] = True

def main():
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    logger.info("Listening on %s", SERIAL_PORT)
    try:
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue
            # quick filter: only process RF receive lines
            if "RF receive" not in line:
                continue
            parsed = parse_line(line)
            if parsed is None:
                continue
            pulse_lengths, pulse_sequence = parsed
            # controller.decode_pulses returns list of results
            results = controller.decode_pulses(pulse_lengths, pulse_sequence)
            if results:
                handle_decode(results)
                logger.info("Decoded: %s", results)
            # periodically dump inventory
            if int(time.time()) % 30 == 0:
                with open("rf_sensors.json", "w") as f:
                    json.dump(seen, f, default=str, indent=2)
            time.sleep(0.01)
    except KeyboardInterrupt:
        logger.info("Stopping, writing final inventory")
        with open("rf_sensors.json", "w") as f:
            json.dump(seen, f, default=str, indent=2)
    finally:
        ser.close()

if __name__ == "__main__":
    main()
