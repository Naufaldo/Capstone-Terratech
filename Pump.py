from google.cloud import pubsub_v1
import RPi.GPIO as GPIO
import os
# Configure the GPIO pin connected to the relay
relay_pin = 2
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'json/credentials.json'
# Create a callback function to process incoming messages
def callback(message):
    if message.data == b'activate':
        GPIO.output(relay_pin, GPIO.HIGH)  # Activate the relay
    elif message.data == b'deactivate':
        GPIO.output(relay_pin, GPIO.LOW)  # Deactivate the relay
    message.ack()

# Create a subscriber client
subscriber = pubsub_v1.SubscriberClient()

# Define your subscription path
subscription_path = subscriber.subscription_path('capstone-terrratech', 'Relay-sub')

# Start the subscriber and listen for messages
subscriber.subscribe(subscription_path, callback=callback)

# Keep the program running to continuously receive messages
while True:
    pass
