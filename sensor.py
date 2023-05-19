import Adafruit_DHT
from google.cloud import pubsub_v1
from google.cloud import firestore
import json
import time
import os
import datetime
import RPi.GPIO as GPIO

# Configuration variables
project_id = 'capstone-terrratech'
topic_name = 'Sensor'
collection_name = 'sensor_data'

# Set environment variable for service account credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'json/credentials.json'

# Initialize Google Cloud Pub/Sub client
publisher = pubsub_v1.PublisherClient()
db = firestore.Client()

# GPIO pin for moisture sensor
moisture_pin = 14

# Function to read sensor data from DHT22
def read_sensor_data():
    sensor = Adafruit_DHT.DHT22
    pin = 17  # GPIO pin connected to the DHT22 sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    moisture = read_soil_moisture()
    return humidity, temperature, moisture

# Function to read soil moisture
def read_soil_moisture():
    GPIO.setup(moisture_pin, GPIO.IN)
    moisture_level = GPIO.input(moisture_pin)
    if moisture_level:
        return "tanah basah"
    else:
        return "tanah kering"

# Function to publish sensor data to GCP Pub/Sub
def publish_sensor_data(humidity, temperature, moisture):
    topic_path = publisher.topic_path(project_id, topic_name)

    payload = {
        'humidity': humidity,
        'temperature': temperature,
        'moisture': moisture
    }

    publisher.publish(topic_path, json.dumps(payload).encode('utf-8'))
    print('Data published to GCP Pub/Sub.')

    # Store data in Firestore with the document ID as the timestamp
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    doc_ref = db.collection(collection_name).document(timestamp)
    doc_ref.set(payload)
    print('Data stored in Firestore with document ID:', timestamp)

# Main function
def main():
    # GPIO setup
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    while True:
        humidity, temperature, moisture = read_sensor_data()
        publish_sensor_data(humidity, temperature, moisture)

        time.sleep(60)

if __name__ == '__main__':
    main()
