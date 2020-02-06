# rgb-panel-worker

Worker component of the RGB Panel projet.

Runs on a Raspberry Pi 3 or newer. Tested and working on a Raspberry Pi 3 Model B+.

Connects to a [RabbitMQ](https://rabbitmq.com) queue and reads items added by [`rgb-panel-api`](https://github.com/agence-webup/rgb-panel-api).

This Python worker has a few dependencies, namely [`Pika`](https://github.com/pika/pika) and the Python bindings from [`rpi-rgb-led-matrix`](https://github.com/hzeller/rpi-rgb-led-matrix/).

For improved performance, we recommend running the [DietPi]("https://dietpi.com") distribution rather than the official [Raspbian]("https://www.raspberrypi.org/downloads/raspbian/") distro.

## Installation instructions

### Requirements
- Raspberry Pi
- Python
- pip

### Install rpi-rgb-led-matrix

Follow the installation instructions for [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix/), while making sure to compile for the right hardware.

### Clone this repo

First, move to the directory containing samples for the Python bindings in the previously installed `rpi-rgb-led-matrix`.

```bash
cd bindings/python/samples/
```

Now you can clone this repo

```bash
git clone git@github.com:agence-webup/rgb-panel-worker.git
```

### Install dependencies with pip

```bash
pip install -r requirements.txt
```

### Make sure your RGB Panel is connected and sufficiently powered

Just in case.

### Run the worker

You will need so specify your AMQP endpoint as an environment variable passed to the worker

```bash
AMQP_URL="AMQP://YOUR_AMQP_ENDPOINT" sudo worker.py
```

In order to run in the background you might want to use [screen](https://linux.die.net/man/1/screen) or simply use:

```bash
AMQP_URL="AMQP://YOUR_AMQP_ENDPOINT" sudo worker.py &
```

## Optional: Run the worker as a systemd service

This part is completely optional but is more convenient than running the worker manually each time. In addition, you won't have to manage how to run it in the background, since that's systemd's job!

First, create a bash script wherever you like. For this example we're adding it to `root`'s home.

```bash
touch /root/runworker.sh
```

Add the following to your new file, replacing the directory with wherever your worker is located, and the AMQP_URL with your AMQP endpoint.

```bash
#!/usr/bin/env bash

cd /root/matrixpython/bindings/python/samples

AMQP_URL=amqp://YOUR_AMQP_URL python worker.py
```

Once that's done, you can create a file defining the service

```bash
touch /lib/systemd/system/pythonworker.service
```

Then add the following to your file in order to define the service. Remember to replace the script location with your own if it's different.

```s
[Unit]
Description=Worker for webup-rgb project
After=multi-user.target

[Service]
Type=idle
ExecStart=/bin/bash /root/runworker.sh
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Now we need to set permissions. You can omit the `sudo` if you're running as `root`.

```bash
sudo chmod 644 /lib/systemd/system/pythonworker.service
```

We're almost done. Now we need to reload systemd and enable the service to make sure it runs on boot.

```bash
sudo systemctl daemon-reload
```

```bash
sudo systemctl enable pythonworker.service
```

Now you can reboot

```bash
sudo reboot
```

Upon rebooting, you can check the status of your newly created service, which will now run automatically on boot and will restart if ever it crashes.

```bash
sudo systemctl status pythonworker.service
```