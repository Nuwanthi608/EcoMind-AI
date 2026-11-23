
import numpy as np
import tensorflow as tf

from pathlib import Path
from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

from backend.data_pipeline import (
    test_dataset,
    CLASS_NAMES
)

from backend.model import MODEL_PATH


# ==========================================
# 1. LOAD TRAINED MODEL
# ==========================================

print("\nLoading trained EcoMind AI model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully!")


# ==========================================
# 2. GENERATE PREDICTIONS
# ==========================================

print("\nGenerating predictions...")

actual_labels = []
predicted_labels = []

for images, labels in test_dataset:

    predictions = model.predict(
        images,
        verbose=0
    )

    predicted_classes = np.argmax(
        predictions,
        axis=1
    )

    actual_labels.extend(labels.numpy())
    predicted_labels.extend(predicted_classes)

actual_labels = np.array(actual_labels)
predicted_labels = np.array(predicted_labels)

print("Predictions completed!")


# ==========================================
# 3. CLASSIFICATION REPORT
# ==========================================

print("\n===================================")
print("       Classification Report")
print("===================================")

report = classification_report(
    actual_labels,
    predicted_labels,
    labels=list(range(len(CLASS_NAMES))),
    target_names=CLASS_NAMES,
    zero_division=0
)

print(report)


# ==========================================
# 4. CONFUSION MATRIX
# ==========================================

print("\n===================================")
print("       Confusion Matrix")
print("===================================")

matrix = confusion_matrix(
    actual_labels,
    predicted_labels,
    labels=list(range(len(CLASS_NAMES)))
)

print("Class order:", CLASS_NAMES)
print(matrix)


# ==========================================
# 5. SAVE EVALUATION RESULTS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

report_path = REPORT_DIR / "classification_report.txt"
matrix_path = REPORT_DIR / "confusion_matrix.csv"

with open(report_path, "w", encoding="utf-8") as file:

    file.write("EcoMind AI - Classification Report\n\n")
    file.write(report)

    file.write("\n\nConfusion Matrix:\n")
    file.write(str(matrix))

np.savetxt(
    matrix_path,
    matrix,
    delimiter=",",
    fmt="%d"
)

print("\n===================================")
print("       Evaluation Completed")
print("===================================")

print("Report saved:", report_path)
print("Confusion matrix saved:", matrix_path)
