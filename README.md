# rgb-panel-worker

Worker component of the RGB Panel projet.

Connects to a [RabbitMQ](https://rabbitmq.com) queue and reads items added by [`rgb-panel-api`](https://github.com/agence-webup/rgb-panel-api).

This Python worker has a few dependencies, namely [`Pika`](https://github.com/pika/pika) and the Python bindings from [`rpi-rgb-led-matrix`](https://github.com/hzeller/rpi-rgb-led-matrix/).


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

In order to run in the background you might want to use [screen](https://linux.die.net/man/1/screen)