import os
from glob import glob

# Define the base data directory
data_directory = "/vol/home/s4406559/UC_project/git-lfs-3.2.0/wildfires-cems/val"

# Output list to store the collected file paths and metadata
collected_data = []

# Traverse the directory structure
for root, dirs, files in os.walk(data_directory):
    # Look for GRA.tif, S2L2A.tif, and S2L2A.json files
    grading_files = [f for f in files if f.endswith("_GRA.tif")]
    sentinel_files = [f for f in files if f.endswith("_S2L2A.tif")]
    sentinel_jsons = [f for f in files if f.endswith("_S2L2A.json")]
    
    # If both grading and Sentinel-2A files are found
    if grading_files and sentinel_files and sentinel_jsons:
        for gra_file in grading_files:
            for s2_file in sentinel_files:
                for json_file in sentinel_jsons:
                    # Extract EMSR, AOI, and subfolder information
                    path_parts = root.split("/")
                    emsr_folder = path_parts[-4] if len(path_parts) > 3 else "Unknown"
                    aoi_folder = path_parts[-3] if len(path_parts) > 2 else "Unknown"
                    subfolder = path_parts[-2] if len(path_parts) > 1 else "Unknown"
                    
                    # Record file paths and metadata
                    collected_data.append({
                        "EMSR": emsr_folder,
                        "AOI": aoi_folder,
                        "Subfolder": subfolder,
                        "grading_tif": os.path.join(root, gra_file),
                        "sentinel2a_tif": os.path.join(root, s2_file),
                        "sentinel2a_json": os.path.join(root, json_file)
                    })

# Display the collected data
print(f"Collected {len(collected_data)} sets of grading, Sentinel-2A TIFF, and JSON files.")

# Example: Display the first 5 entries
# for entry in collected_data:
#     print(entry)
import os
import shutil
import pandas as pd

# Sample data dictionary (replace with your full data list)


# Destination folder
destination_folder = "organized_val"
os.makedirs(destination_folder, exist_ok=True)

# Initialize a list for CSV mapping
csv_data = []

# Iterate through the data list
for entry in collected_data:
    emsr = entry['EMSR']
    aoi = entry['AOI']
    subfolder = entry['Subfolder']

    # Create subfolder structure
    target_folder = os.path.join(destination_folder, emsr, aoi, subfolder)
    os.makedirs(target_folder, exist_ok=True)

    # Copy files
    for key in ['grading_tif', 'sentinel2a_tif', 'sentinel2a_json']:
        src = entry[key]
        dest = os.path.join(target_folder, os.path.basename(src))
        shutil.copy2(src, dest)
    
    # Add to CSV data
    csv_data.append({
        "EMSR": emsr,
        "AOI": aoi,
        "Subfolder": subfolder,
        "grading_tif": os.path.join(target_folder, os.path.basename(entry['grading_tif'])),
        "sentinel2a_tif": os.path.join(target_folder, os.path.basename(entry['sentinel2a_tif'])),
        "sentinel2a_json": os.path.join(target_folder, os.path.basename(entry['sentinel2a_json']))
    })

# Create a CSV mapping file
csv_file = os.path.join(destination_folder, "val_mapping.csv")
pd.DataFrame(csv_data).to_csv(csv_file, index=False)

print(f"Organized files are saved in: {destination_folder}")
print(f"Mapping CSV is saved at: {csv_file}")

