
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split

# Original dataset location
source_dir = Path(
    "dataset/raw/trashnet/data/extracted/dataset-resized"
)

# New dataset location
output_dir = Path("dataset/processed")

# Waste categories
categories = [
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash"
]

# Dataset split ratios
train_ratio = 0.70
validation_ratio = 0.15
test_ratio = 0.15

for category in categories:

    print(f"\nProcessing: {category}")

    # Get image paths
    category_path = source_dir / category

    images = [
        image for image in category_path.iterdir()
        if image.suffix.lower() in [".jpg", ".jpeg", ".png"]
    ]

    # First split: 70% training, 30% temporary
    train_images, temp_images = train_test_split(
        images,
        test_size=0.30,
        random_state=42
    )

    # Second split: 15% validation, 15% testing
    validation_images, test_images = train_test_split(
        temp_images,
        test_size=0.50,
        random_state=42
    )

    # Create destination folders and copy images
    splits = {
        "train": train_images,
        "validation": validation_images,
        "test": test_images
    }

    for split_name, split_images in splits.items():

        destination = output_dir / split_name / category
        destination.mkdir(parents=True, exist_ok=True)

        for image in split_images:
            shutil.copy2(image, destination / image.name)

        print(f"{split_name}: {len(split_images)} images")

print("\nDataset splitting completed successfully!")
