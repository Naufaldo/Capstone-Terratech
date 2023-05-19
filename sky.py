import subprocess
from datetime import datetime
import os
from google.cloud import storage

# Set the path to your JSON credentials file
credentials_path = 'json/credentials.json'

# Set the Google Cloud project ID
project_id = 'capstone-terrratech'

# Set the bucket name
bucket_name = 'gs://sky-photo/'

# Authenticate with Google Cloud using the JSON credentials file
subprocess.run(['gcloud', 'auth', 'activate-service-account', '--key-file', credentials_path])

# Set the Google Cloud project ID
subprocess.run(['gcloud', 'config', 'set', 'project', project_id])

# Generate the current date and time
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Set the image file name using the current date and time
image_file_name = f'{current_datetime}.jpg'

# Capture an image using fswebcam
subprocess.run(['fswebcam', '-r', '1280x720', '--no-banner', image_file_name])

# Create a client for Google Cloud Storage
client = storage.Client(project=project_id)

# Upload the image to Google Cloud Storage
bucket = client.bucket(bucket_name)
blob = bucket.blob(image_file_name)
blob.upload_from_filename(image_file_name)

# Remove the local picture file
os.remove(image_file_name)
