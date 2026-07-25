#!/usr/bin/env python3
import time
import requests
from sds011lib import SDS011Reader
import logging

# --- CONFIGURATION ---
# IP address of the Display Pi (the receiver)
RECEIVER_IP = "172.16.0.208" 
# The serial port of your sensor (usually /dev/ttyUSB0 for USB or /dev/ttyAMA0 for GPIO)
SERIAL_PORT = "/dev/ttyUSB0" 
# Increased wait time to allow sensor more time to flush data and complete the packet.
READ_CYCLE_WAIT_TIME = 20 # Time in seconds between attempts
# ---------------------

# Set up basic logging for better debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting SDS011 Sensor Node Service.")
    try:
        # Attempt to initialize the sensor
        logging.info(f"Attempting to initialize sensor on port: {SERIAL_PORT}")
        sensor = SDS011Reader(SERIAL_PORT) 
        logging.info("Sensor initialized successfully.")
        
        while True:
            logging.info("--- Starting new sensor reading cycle ---")
            try:
                # Attempt to read data
                data = sensor.query_data()
                if data:
                    logging.info(f"Successfully read data: {data}")
                    
                    # Attempt to send data to the receiver
                    logging.info(f"Attempting to send data to receiver at {RECEIVER_IP}:5000")
                    try:
                        response = requests.post(
                            f"http://{RECEIVER_IP}:5000/update", 
                            json=data,
                            timeout=5
                        )
                        if response.status_code == 200:
                            logging.info("Data successfully sent and acknowledged by receiver.")
                        else:
                            logging.error(f"Failed to send data. Receiver returned status code: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        logging.error(f"Network Error while sending data to {RECEIVER_IP}: {e}")
                else:
                    logging.warning("sensor.query_data() returned no data.")
            except Exception as e:
                # Log the full exception string (This should capture the detail)
                logging.error(f"CRITICAL FAILURE DURING SENSOR CYCLE: {type(e).__name__} - {str(e)}")
            
            logging.info(f"--- Sensor reading cycle complete. Waiting for {READ_CYCLE_WAIT_TIME} seconds. ---")
            time.sleep(READ_CYCLE_WAIT_TIME)

    except KeyboardInterrupt:
        logging.info("Service manually stopped by user.")
    except Exception as e:
        # Log the full initialization error
        logging.critical(f"FATAL: An unrecoverable error occurred during sensor initialization: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    main()