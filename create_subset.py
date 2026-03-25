import os
import shutil
import random
from pathlib import Path


def create_subset_dataset(src, percentage, dest="subset_dataset"):
    src_path = Path(src)
    dest_path = Path(dest)

    # Define the subfolders we need to process
    splits = ['train', 'test', 'val']

    for split in splits:
        print(f"Processing {split} split...")

        img_dir = src_path / "images" / split
        lbl_dir = src_path / "labels" / split

        # Check if directory exists (some datasets might skip 'test')
        if not img_dir.exists():
            continue

        # Get all image files
        images = [f for f in img_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']]

        # Calculate sample size
        sample_size = max(1, int(len(images) * percentage))
        subset_images = random.sample(images, sample_size)

        # Create destination directories
        (dest_path / "images" / split).mkdir(parents=True, exist_ok=True)
        (dest_path / "labels" / split).mkdir(parents=True, exist_ok=True)

        for img_path in subset_images:
            # Copy image
            shutil.copy2(img_path, dest_path / "images" / split / img_path.name)

            # Find and copy corresponding label (.txt)
            label_name = img_path.stem + ".txt"
            src_label = lbl_dir / label_name

            if src_label.exists():
                shutil.copy2(src_label, dest_path / "labels" / split / label_name)
            else:
                print(f"Warning: Missing label for {img_path.name}")

    print(f"\nDone! Subset dataset created at: {dest_path.absolute()}")


if __name__ == "__main__":
    # --- Configuration ---
    SOURCE_DIRECTORY = "./output/IdCardV0.7"
    DEST_DIRECTORY = "./output/subsetIdCardV0.7"
    SAMPLE_PERCENTAGE = 0.05  # 5%
    # ---------------------

    create_subset_dataset(SOURCE_DIRECTORY, SAMPLE_PERCENTAGE, DEST_DIRECTORY)