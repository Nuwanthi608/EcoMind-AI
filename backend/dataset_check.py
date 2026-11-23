from pathlib import Path
from PIL import Image

dataset_path = Path(
    "dataset/raw/trashnet/data/extracted/dataset-resized"
)

categories = [
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash"
]

for category in categories:

    category_path = dataset_path / category

    images = list(category_path.glob("*"))

    valid_images = 0

    for image_path in images:

        try:
            with Image.open(image_path) as img:
                img.verify()
                valid_images += 1

        except Exception:
            print("Invalid image:", image_path)

    print(f"{category}: {valid_images} valid images")

print("\nDataset checking completed!")