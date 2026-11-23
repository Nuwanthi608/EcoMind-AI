
import tensorflow as tf
from pathlib import Path

# Dataset path
DATASET_DIR = Path("dataset/processed")

# Image settings
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

# Class names
CLASS_NAMES = [
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash"
]

# Load training dataset
train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR / "train",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_names=CLASS_NAMES,
    shuffle=True,
    seed=SEED
)

# Load validation dataset
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR / "validation",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_names=CLASS_NAMES,
    shuffle=False
)

# Load testing dataset
test_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR / "test",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_names=CLASS_NAMES,
    shuffle=False
)

# Normalize pixel values
normalization_layer = tf.keras.layers.Rescaling(1.0 / 255)

train_dataset = train_dataset.map(
    lambda images, labels: (
        normalization_layer(images), labels
    )
)

validation_dataset = validation_dataset.map(
    lambda images, labels: (
        normalization_layer(images), labels
    )
)

test_dataset = test_dataset.map(
    lambda images, labels: (
        normalization_layer(images), labels
    )
)

# Improve data loading performance
AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    buffer_size=AUTOTUNE
)

test_dataset = test_dataset.prefetch(
    buffer_size=AUTOTUNE
)

# Display dataset information
print("\nDataset Pipeline Ready!")

print("Class names:", CLASS_NAMES)
print("Image size:", IMAGE_SIZE)
print("Batch size:", BATCH_SIZE)

for images, labels in train_dataset.take(1):
    print("Image batch shape:", images.shape)
    print("Label batch shape:", labels.shape)
    print("Pixel value range:",
          float(tf.reduce_min(images)),
          "to",
          float(tf.reduce_max(images)))
