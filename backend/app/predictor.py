from functools import lru_cache
import numpy as np
from PIL import Image
import tensorflow as tf
from .config import MODEL_PATH, CLASS_NAMES, IMAGE_SIZE

@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Trained model not found at {MODEL_PATH}. Run: python train.py from project root."
        )
    return tf.keras.models.load_model(MODEL_PATH)

def predict_image(image: Image.Image):
    image = image.convert("RGB").resize(IMAGE_SIZE)
    array = np.asarray(image, dtype=np.float32)
    batch = np.expand_dims(array, axis=0)
    model = load_model()
    probabilities = model.predict(batch, verbose=0)[0]
    index = int(np.argmax(probabilities))
    return CLASS_NAMES[index], float(probabilities[index])
