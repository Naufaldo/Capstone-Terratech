import Adafruit_DHT
from google.cloud import pubsub_v1
from google.cloud import firestore
import json
import time
import RPi.GPIO as GPIO
import os

# Configuration variables
project_id = 'capstone-terrratech'
subscription_name = 'Sensor-sub'
collection_name = 'sensor_data'
relay_pin = 2  # GPIO pin connected to the relay

# Set environment variable for service account credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pi/Capstone/json/credentials.json'

# GPIO setup function
def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin, GPIO.OUT)
    

# Initialize Google Cloud Pub/Sub client
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

# Initialize Firestore client
db = firestore.Client()

# Function to read sensor data from DHT22
def read_sensor_data():
    sensor = Adafruit_DHT.DHT22
    pin = 17  # GPIO pin connected to the DHT22 sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity, temperature

# Function to read soil moisture
def read_soil_moisture():
    # Read the sensor and return the moisture level
    # Adjust the code based on the specific sensor and pin configuration you're using
    # Assuming you are using GPIO pin 14 for soil moisture sensor
    GPIO.setup(14, GPIO.IN)
    moisture_level = GPIO.input(14)
    if moisture_level:
        return "tanah basah"
    else:
        return "tanah kering"

# Function to control the relay
def control_relay(on):
    # Control the relay based on the value of 'on'
    # Adjust the code based on the specific relay module and pin configuration you're using
    if on:
        GPIO.output(relay_pin, GPIO.HIGH)  # Turn on the relay
    else:
        GPIO.output(relay_pin, GPIO.LOW)   # Turn off the relay

# Function to publish sensor data to GCP Pub/Sub
def publish_sensor_data(humidity, temperature, moisture):
    topic_path = publisher.topic_path(project_id, 'Sensor')

    payload = {
        'humidity': humidity,
        'temperature': temperature,
        'moisture': moisture
    }

    publisher.publish(topic_path, json.dumps(payload).encode('utf-8'))
    print('Data published to GCP Pub/Sub.')

    # Store data in Firestore
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(payload)
    print('Data stored in Firestore.')

# Function to receive commands from the mobile device and control the relay
def receive_commands(message):
    command = message.data.decode('utf-8')
    if command == 'on':
        control_relay(True)
    elif command == 'off':
        control_relay(False)

# Main function
def main():
    setup_gpio()

    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    subscriber.subscribe(subscription_path, callback=receive_commands)

    while True:
        humidity, temperature = read_sensor_data()
        moisture = read_soil_moisture()
        publish_sensor_data(humidity, temperature, moisture)
        time.sleep(60)

if __name__ == '__main__':
    main()
