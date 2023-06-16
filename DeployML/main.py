import tensorflow as tf
from tensorflow import keras
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Inisialisasi Firebase
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ml-test-terra.asia-southeast1.firebasedatabase.app/'
})

# Mengunduh model .hdf5 dari Google Cloud Storage
def download_model_from_gcs(bucket_name, model_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(model_name)
    blob.download_to_filename(model_name)

# Memuat model .hdf5 ke dalam TensorFlow-Keras
def load_model_from_hdf5(model_name):
    model = keras.models.load_model(model_name)
    return model

# Melakukan prediksi pada gambar yang ingin diuji
def predict_image(model, image_path):
    # Lakukan prediksi
    prediction = model.predict(image)
    return prediction

# Menyimpan hasil prediksi di Firebase Realtime Database
def save_prediction_to_realtime_db(prediction):
    ref = db.reference('predictions')
    new_prediction_ref = ref.push()
    new_prediction_ref.set({
        'prediction': prediction.tolist()
    })
def main():
    # Mengunduh model .hdf5 dari Google Cloud Storage
    bucket_name = 'tstrr'
    model_name = 'trainmy_modelaug.hdf5'
    download_model_from_gcs(bucket_name, model_name)

    # Memuat model .hdf5 ke dalam TensorFlow-Keras
    model = load_model_from_hdf5(model_name)

    # Prediksi gambar dan simpan hasilnya di Firebase Realtime Database
    image_path = 'path/to/uploaded/image.jpg'
    prediction = predict_image(model, image_path)
    save_prediction_to_realtime_db(prediction)

# Menjalankan program utama
if __name__ == '__main__':
    main()