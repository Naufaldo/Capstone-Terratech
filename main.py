import Adafruit_DHT
import RPi.GPIO as GPIO
from google.cloud import pubsub
import os

# Set the path to the JSON key file
keyfile_path = '/home/pi/Capstone/json/capstone-terrratech-9782ae376611.json'

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = keyfile_path

# Set up Google Cloud Pub/Sub client
publisher = pubsub.PublisherClient()

# Set your GCP project ID and topic name
project_id = "capstone-terrratech"
topic_name = "projects/capstone-terrratech/topics/Sensor"

# Format the topic path
topic_path = publisher.topic_path(project_id, topic_name)

# Set up DHT22 sensor
dht_pin = 17  # GPIO pin number where DHT22 is connected
dht_sensor = Adafruit_DHT.DHT22

# Set up soil moisture sensor
moisture_pin = 14  # GPIO pin number where soil moisture sensor is connected
GPIO.setmode(GPIO.BCM)
GPIO.setup(moisture_pin, GPIO.IN)

# Read data from sensors
humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
moisture = GPIO.input(moisture_pin)

# Check if sensor readings are valid
if humidity is not None and temperature is not None:
    # Define the sensor data
    sensor_data = {
        "temperature": temperature,
        "humidity": humidity,
        "moisture": moisture
    }

    # Convert the sensor data to bytes
    message_data = str(sensor_data).encode("utf-8")

    # Publish the message to Pub/Sub
    future = publisher.publish(topic_path, data=message_data)
    print(f"Published message ID: {future.result()}")
else:
    print("Failed to read data from sensors.")

# Clean up the Pub/Sub client
publisher.close()
