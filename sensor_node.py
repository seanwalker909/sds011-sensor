#!/usr/bin/env python3
import time
import requests
from sds011lib.sds011 import SDS011

# --- CONFIGURATION ---
# IP address of the Display Pi (the receiver)
RECEIVER_IP = "172.16.0.208" 
# The serial port of your sensor (usually /dev/ttyUSB0 for USB or /dev/ttyAMA0 for GPIO)
SERIAL_PORT = "/dev/ttyUSB0" 
# ---------------------

def main():
    try:
        sensor = SDS011(SERIAL_PORT)
        print(f"Starting sensor loop. Sending to {RECEIVER_IP}")

        while True:
            data = sensor.read()
            if data:
                print(f"Readings: {data}")
                try:
                    response = requests.post(
                        f"http://{RECEIVER_IP}:5000/update", 
                        json=data,
                        timeout=2
                    )
                    if response.status_code != 200:
                        print(f"Failed to send: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Network Error: {e}")

            time.sleep(10)

    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ kind="main":
    main()
