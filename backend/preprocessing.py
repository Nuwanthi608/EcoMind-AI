
from pathlib import Path
from PIL import Image

# Dataset location
dataset_dir = Path("dataset/processed")

# Image size required by our model
IMAGE_SIZE = (224, 224)

# Dataset categories
categories = [
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash"
]

# Check images
for split in ["train", "validation", "test"]:

    print(f"\nProcessing {split} dataset")

    for category in categories:

        category_path = dataset_dir / split / category

        image_count = 0

        for image_path in category_path.iterdir():

            if image_path.suffix.lower() not in [
                ".jpg", ".jpeg", ".png"
            ]:
                continue

            try:
                with Image.open(image_path) as img:

                    # Convert image to RGB
                    img = img.convert("RGB")

                    # Resize image
                    img = img.resize(IMAGE_SIZE)

                    image_count += 1

            except Exception as error:
                print("Error:", image_path, error)

        print(f"{category}: {image_count} images checked")

print("\nImage preprocessing check completed!")
