#use post.zip from the burn intensity dataset from Hugging face
import os
import shutil
from sklearn.model_selection import train_test_split

# Define the source directory and the new base directory
source_dir = "/Users/priyanjaligoel/Downloads/post"
base_dir = "/Users/priyanjaligoel/Downloads/organized_data"

# Create base directory and subdirectories
os.makedirs(os.path.join(base_dir, "images"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "labels"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "train_images"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "test_images"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "validation_images"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "train_labels"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "test_labels"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "validation_labels"), exist_ok=True)

# Separate files into images and labels
for file in os.listdir(source_dir):
    file_path = os.path.join(source_dir, file)
    if os.path.isfile(file_path):  # Only process files
        if file.startswith("BS_"):  # Move BS_ files to labels folder
            shutil.move(file_path, os.path.join(base_dir, "labels", file))
        elif file.startswith("HLS_"):  # Move HLS_ files to images folder
            shutil.move(file_path, os.path.join(base_dir, "images", file))

# List all image and label files
image_files = sorted(os.listdir(os.path.join(base_dir, "images")))
label_files = sorted(os.listdir(os.path.join(base_dir, "labels")))

# Split images into train, test, validation (80%, 10%, 10%)
train_images, test_images = train_test_split(image_files, test_size=0.2, random_state=42)
val_images, test_images = train_test_split(test_images, test_size=0.5, random_state=42)

# Function to move files with error handling
def move_file(src, dst):
    if os.path.exists(src):
        shutil.copy(src, dst)
    else:
        print(f"File not found: {src}")

# Move train, test, validation files
for image in train_images:
    move_file(os.path.join(base_dir, "images", image), os.path.join(base_dir, "train_images", image))
    label = image.replace("HLS_", "BS_")  # Match label file to image
    move_file(os.path.join(base_dir, "labels", label), os.path.join(base_dir, "train_labels", label))

for image in test_images:
    move_file(os.path.join(base_dir, "images", image), os.path.join(base_dir, "test_images", image))
    label = image.replace("HLS_", "BS_")  # Match label file to image
    move_file(os.path.join(base_dir, "labels", label), os.path.join(base_dir, "test_labels", label))

for image in val_images:
    move_file(os.path.join(base_dir, "images", image), os.path.join(base_dir, "validation_images", image))
    label = image.replace("HLS_", "BS_")  # Match label file to image
    move_file(os.path.join(base_dir, "labels", label), os.path.join(base_dir, "validation_labels", label))

print("Files successfully organized into respective directories.")

import os

# Define the folder containing the files
folder = "/Users/priyanjaligoel/Downloads/organized_data/validation_images" # Update this to your folder path

# List all files in the folder
all_files = [f for f in os.listdir(folder) if f.endswith(".tiff")]

# Rename files by moving the prefix to the end
for file in all_files:
    # Separate the filename and extension
    file_name, file_extension = os.path.splitext(file)  # Splits into 'name' and '.tiff'

    # Split the filename into prefix and the rest
    parts = file_name.split("_", 1)  # Split only on the first underscore
    if len(parts) == 2:  # Ensure there is a prefix and a rest
        prefix, rest = parts
        # Construct the new filename
        new_name = f"{rest}_{prefix}{file_extension}"  # Add back the correct extension
        # Rename the file in place
        old_path = os.path.join(folder, file)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {file} -> {new_name}")

print("All files have been renamed in the same folder.")
