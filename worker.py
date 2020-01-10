from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import pika
import json
import yaml
import os
import sys

if ('AMQP_URL' in os.environ):
    connection = pika.BlockingConnection(pika.URLParameters(os.environ['AMQP_URL']))
else:
    sys.exit("\nRequired ENV var AMQP_URL is not set, please run the worker by exporting it.\n")

# Init RGB Matrix configuration
options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat-pwm'
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.multiplexing = 0
options.pwm_bits = 11
options.brightness = 100
options.pwm_lsb_nanoseconds = 130
options.led_rgb_sequence = 'RGB'
options.gpio_slowdown = 2

channel = connection.channel()

channel.queue_declare(queue='display_queue')

def current_time_millis():
    return str(time.time())

def DisplayText(text):
    matrix = RGBMatrix(options = options)
    canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("../../../fonts/7x13.bdf")
    textColor = graphics.Color(100, 100, 100)

    pos = canvas.width

    while True:
        canvas.Clear()
        len = graphics.DrawText(canvas, font, pos, 10, textColor, text)
        pos -= 1
        if (pos + len < 0):
            return
            
        time.sleep(0.05)
        canvas = matrix.SwapOnVSync(canvas)

def DisplayDrawing(data):
    matrix = RGBMatrix(options = options)
    canvas = matrix.CreateFrameCanvas()
    
    for pixel in data:
        canvas.SetPixel(pixel['x'], pixel['y'], pixel['r'], pixel['g'], pixel['b'])
    
    canvas = matrix.SwapOnVSync(canvas)
    time.sleep(8)

    canvas.Clear()


# Messages in the queue are fetched here, then sent to the appropriate method for display
def callback(ch, method, properties, body):
    j = json.loads(body)

    if (j['type'] == 'text'):
        print(current_time_millis() + " - running job " + j['jobId'])
        DisplayText(j['text'])
    
    if (j['type'] == 'drawing'):
        print(current_time_millis() + " - running job " + j['jobId'])
        DisplayDrawing(yaml.safe_load(j['drawing']))



channel.basic_consume(queue='display_queue', auto_ack=True, on_message_callback=callback)

print(' Listening for tasks...')
channel.start_consuming()