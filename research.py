import os
# # Example of creating a path
# base_path = "your_directory"
# sub_folder = "subfolder"
# filename = "file.txt"

# # Join paths
# path = os.path.join(base_path, sub_folder, filename)
# print(path)

# # Normalize and replace backslashes with forward slashes
# normalized_path = os.path.normpath(os.path.join(base_path, sub_folder, filename)).replace("\\", "/")
# print(normalized_path)

import os
import re

def latest_model():
    metrices_path = "D:/Project/NeuroScan/runs/detect"
    
    # Check if the path exists
    if not os.path.exists(metrices_path):
        print(f"Error: The path {metrices_path} does not exist.")
        return None
    
    # List all subdirectories inside the 'detect' folder
    all_folders = [f for f in os.listdir(metrices_path) if os.path.isdir(os.path.join(metrices_path, f))]
    
    # Sort the folders based on the numeric value at the end of the folder name
    def extract_numeric_part(folder_name):
        match = re.search(r'(\d+)$', folder_name)
        return int(match.group(1)) if match else 0
    
    all_folders.sort(key=extract_numeric_part)
    print(all_folders)
    
    if all_folders:
        # Get the most recent model folder (the last one after sorting)
        latest_folder = all_folders[-1]
        print(f"Latest model folder: {latest_folder}")
        return latest_folder

# Test the function
latest_model()
