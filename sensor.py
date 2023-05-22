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

# GPIO pins
sensor_pin = 17  # GPIO pin connected to the DHT22 sensor
moisture_pin = 14  # GPIO pin for moisture sensor
rain_pin = 19  # GPIO pin for rain sensor

# Function to read sensor data from DHT22
def read_sensor_data():
    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
    moisture = read_soil_moisture()
    rain = read_rain_sensor()
    return humidity, temperature, moisture, rain

# Function to read soil moisture
def read_soil_moisture():
    GPIO.setup(moisture_pin, GPIO.IN)
    moisture_level = GPIO.input(moisture_pin)
    if moisture_level:
        return "tanah basah"
    else:
        return "tanah kering"

# Function to read rain sensor
def read_rain_sensor():
    GPIO.setup(rain_pin, GPIO.IN)
    rain_status = GPIO.input(rain_pin)
    if rain_status:
        return "rain detected"
    else:
        return "no rain"

# Function to publish sensor data to GCP Pub/Sub
def publish_sensor_data(humidity, temperature, moisture, rain):
    topic_path = publisher.topic_path(project_id, topic_name)

    payload = {
        'humidity': humidity,
        'temperature': temperature,
        'moisture': moisture,
        'rain': rain
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
        humidity, temperature, moisture, rain = read_sensor_data()
        publish_sensor_data(humidity, temperature, moisture, rain)

        time.sleep(60)

if __name__ == '__main__':
    main()
