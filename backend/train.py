
import numpy as np
import tensorflow as tf

from sklearn.utils.class_weight import compute_class_weight

from backend.data_pipeline import (
    train_dataset,
    validation_dataset,
    test_dataset,
    CLASS_NAMES
)

from backend.model import build_model, MODEL_PATH


# ==========================================
# 1. TRAINING CONFIGURATION
# ==========================================

EPOCHS = 12
SEED = 42

tf.keras.utils.set_random_seed(SEED)

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

print("\n===================================")
print("       EcoMind AI Training")
print("===================================")

print("Architecture: MobileNetV2")
print("Classes:", CLASS_NAMES)
print("Maximum epochs:", EPOCHS)


# ==========================================
# 2. CALCULATE CLASS WEIGHTS
# ==========================================

print("\nCalculating class weights...")

all_labels = np.concatenate([
    labels.numpy()
    for _, labels in train_dataset
])

class_ids = np.unique(all_labels)

class_weights_array = compute_class_weight(
    class_weight="balanced",
    classes=class_ids,
    y=all_labels
)

class_weights = {
    int(class_id): float(weight)
    for class_id, weight in zip(
        class_ids,
        class_weights_array
    )
}

print("Class weights:", class_weights)


# ==========================================
# 3. BUILD MODEL
# ==========================================

model = build_model()

print("\nModel summary:")

model.summary()


# ==========================================
# 4. TRAINING CALLBACKS
# ==========================================

callbacks = [

    # Save the best model
    tf.keras.callbacks.ModelCheckpoint(
        filepath=str(MODEL_PATH),
        monitor="val_accuracy",
        save_best_only=True,
        mode="max",
        verbose=1
    ),

    # Stop when validation accuracy stops improving
    tf.keras.callbacks.EarlyStopping(
        monitor="val_accuracy",
        patience=4,
        restore_best_weights=True,
        mode="max",
        verbose=1
    ),

    # Reduce learning rate when progress slows
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=2,
        min_lr=0.000001,
        verbose=1
    )
]


# ==========================================
# 5. TRAIN MODEL
# ==========================================

print("\nStarting model training...\n")

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks,
    verbose=2
)


# ==========================================
# 6. SAVE TRAINED MODEL
# ==========================================

model.save(MODEL_PATH)

print("\nBest trained model saved successfully!")

print("Model location:", MODEL_PATH)


# ==========================================
# 7. EVALUATE MODEL
# ==========================================

print("\n===================================")
print("       Model Evaluation")
print("===================================")

test_loss, test_accuracy = model.evaluate(
    test_dataset,
    verbose=1
)


# ==========================================
# 8. TRAINING SUMMARY
# ==========================================

best_val_accuracy = max(
    history.history["val_accuracy"]
)

print("\n===================================")
print("       Training Completed")
print("===================================")

print(
    "Best Validation Accuracy:",
    round(float(best_val_accuracy) * 100, 2),
    "%"
)

print(
    "Test Accuracy:",
    round(float(test_accuracy) * 100, 2),
    "%"
)

print(
    "Test Loss:",
    round(float(test_loss), 4)
)

print("Saved Model:", MODEL_PATH)
