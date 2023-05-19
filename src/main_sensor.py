import Adafruit_DHT
from google.cloud import pubsub_v1
import json
import time
import RPi.GPIO as GPIO

# Configuration variables
project_id = 'capstone-terrratech'
registry_id = 'YOUR_REGISTRY_ID'
device_id = 'YOUR_DEVICE_ID'
private_key_file = 'path/to/private_key.pem'
algorithm = 'ES256'
root_cert_file = 'path/to/roots.pem'
mqtt_bridge_hostname = 'mqtt.googleapis.com'
mqtt_bridge_port = 8883
relay_pin = 2  # GPIO pin connected to the relay

# GPIO setup function
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin, GPIO.OUT)

# Initialize Google Cloud Pub/Sub client
client = pubsub_v1.PublisherClient()

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
    topic_path = client.topic_path(project_id, 'YOUR_TOPIC_NAME')

    payload = {
        'humidity': humidity,
        'temperature': temperature,
        'moisture': moisture
    }

    client.publish(topic_path, json.dumps(payload).encode('utf-8'))
    print('Data published to GCP Pub/Sub.')

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

    client.subscribe('YOUR_SUBSCRIPTION_NAME', receive_commands)

    while True:
        humidity, temperature = read_sensor_data()
        moisture = read_soil_moisture()
        publish_sensor_data(humidity, temperature, moisture)
        time.sleep(60)

if __name__ == '__main__':
    main()
