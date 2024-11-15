import os
# Example of creating a path
base_path = "your_directory"
sub_folder = "subfolder"
filename = "file.txt"

# Join paths
path = os.path.join(base_path, sub_folder, filename)
print(path)

# Normalize and replace backslashes with forward slashes
normalized_path = os.path.normpath(os.path.join(base_path, sub_folder, filename)).replace("\\", "/")
print(normalized_path)