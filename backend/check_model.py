
import tensorflow as tf
from pathlib import Path

MODEL_PATH = Path("models/ecomind_mobilenetv2.keras")

print("\nLoading EcoMind AI model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("\nModel loaded successfully!")

print("\nModel Information:")
print("Model name:", model.name)
print("Input shape:", model.input_shape)
print("Output shape:", model.output_shape)

print("\nTraining Configuration:")

print("Optimizer:", model.optimizer.__class__.__name__)
print("Loss:", model.loss)

print("\nTrainable parameters:")
print(
    sum(
        tf.keras.backend.count_params(w)
        for w in model.trainable_weights
    )
)

print("\nModel check completed!")
