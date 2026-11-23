
import tensorflow as tf
from pathlib import Path

# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

IMAGE_SIZE = (224, 224)
NUM_CLASSES = 6

CLASS_NAMES = [
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash"
]

MODEL_DIR = PROJECT_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "ecomind_mobilenetv2.keras"


# ==========================================
# 2. BUILD MODEL FUNCTION
# ==========================================

def build_model():

    print("\nBuilding EcoMind AI model...")

    # Data augmentation
    data_augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
        ],
        name="data_augmentation"
    )

    # Load pretrained MobileNetV2
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet"
    )

    # Freeze pretrained layers
    base_model.trainable = False

    # Input image
    inputs = tf.keras.Input(
        shape=(224, 224, 3),
        name="input_image"
    )

    # Apply augmentation
    x = data_augmentation(inputs)

    # Convert pixel range 0-1 into -1 to 1
    x = tf.keras.layers.Rescaling(
        scale=2.0,
        offset=-1.0,
        name="mobilenet_preprocessing"
    )(x)

    # Feature extraction
    x = base_model(x, training=False)

    # Classification layers
    x = tf.keras.layers.GlobalAveragePooling2D()(x)

    x = tf.keras.layers.Dropout(0.3)(x)

    outputs = tf.keras.layers.Dense(
        NUM_CLASSES,
        activation="softmax",
        name="waste_predictions"
    )(x)

    # Create complete model
    model = tf.keras.Model(
        inputs=inputs,
        outputs=outputs,
        name="EcoMind_AI_MobileNetV2"
    )

    # Compile model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.0001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    print("Model built successfully!")
    print("Architecture: MobileNetV2")
    print("Input size:", IMAGE_SIZE)
    print("Number of classes:", NUM_CLASSES)

    return model


# ==========================================
# 3. RUN ONLY WHEN EXECUTED DIRECTLY
# ==========================================

if __name__ == "__main__":

    model = build_model()

    model.summary()

    model.save(MODEL_PATH)

    print("\nModel architecture saved!")
    print("Location:", MODEL_PATH)
