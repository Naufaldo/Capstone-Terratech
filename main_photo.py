import subprocess
from datetime import datetime

# Authenticate with Google Cloud
subprocess.run(['gcloud', 'auth', 'login'])

# Set the Google Cloud project ID
subprocess.run(['gcloud', 'config', 'set', 'project', 'capstone-terrratech'])

# Generate the current date and time
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Set the image file name using the current date and time
image_file_name = f'{current_datetime}.jpg'

# Capture an image using fswebcam
subprocess.run(['fswebcam', '-r', '1280x720', '--no-banner', image_file_name])

# Upload the image to Google Cloud Storage using gsutil
subprocess.run(['gsutil', 'cp', image_file_name, 'gs://sky-photo/'])
