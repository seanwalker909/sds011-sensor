# SDS011 Sensor (Sender)

This script runs on the **Sensor Pi** (the one with the USB sensor) and sends air quality data to the **Display Pi** over the LAN.

## Setup

1. Clone this repo:
   `git clone https://github.com/seanwalker909/sds011-sensor.git`
2. Navigate to folder:
   `cd sds011-sensor`
3. Create and use a virtual environment:

   **Standard Way:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   **⚠️ Raspberry Pi Workaround (If the standard way hangs):**
   ```bash
   # 1. Create the environment without pip
   python3 -m venv venv --without-pip
   
   # 2. Activate it
   source venv/bin/activate
   
   # 3. Manually install pip
   curl https://bootstrap.pypa.io/get-pip.py | python3
   
   # 4. Install dependencies
   pip install -r requirements.txt
   ```

## Running as a Service

1. Move the service file to the systemd directory:
   `sudo cp sds011-sensor.service /etc/systemd/system/`
2. Reload the systemd daemon:
   `sudo systemctl daemon-reload`
3. Enable and start the service:
   `sudo systemctl enable sds011-sensor.service`
   `sudo systemctl start sds011-sensor.service`
