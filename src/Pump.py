from google.cloud import pubsub_v1
import RPi.GPIO as GPIO
import time
import os

# Configuration variables
project_id = 'capstone-terrratech'
subscription_name = 'Relay-sub'
relay_pin = 2  # GPIO pin connected to the relay

# Set environment variable for service account credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'json/credentials.json'

# Initialize Google Cloud Pub/Sub client
subscriber = pubsub_v1.SubscriberClient()

# GPIO setup function
def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin, GPIO.OUT)

# Function to control the relay
def control_relay(on):
    # Control the relay based on the value of 'on'
    # Adjust the code based on the specific relay module and pin configuration you're using
    if on:
        GPIO.output(relay_pin, GPIO.HIGH)  # Turn on the relay
    else:
        GPIO.output(relay_pin, GPIO.LOW)   # Turn off the relay

# Function to receive commands from the mobile device and control the relay
def receive_commands(message):
    command = message.data.decode('utf-8')  
    if command == 'on':
        control_relay(True)
    elif command == 'off':
        control_relay(False)
    message.ack()

# Main function
def main():
    setup_gpio()

    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    subscriber.subscribe(subscription_path, callback=receive_commands)

    # Keep the program running to continuously listen for commands
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
