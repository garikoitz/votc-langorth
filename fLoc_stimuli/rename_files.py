import os
import re

# Define the folder containing the images
folder_path = '/Users/tiger/Desktop/CN_word2'

# Regex pattern to find files with "CN_word2-<number>.jpg" format
pattern = re.compile(r"CN_word2-(\d+)\.jpg")

# Iterate over files in the folder
for filename in os.listdir(folder_path):
    match = pattern.match(filename)
    if match:
        # Extract the original number
        original_number = int(match.group(1))
        
        # Subtract 20 from the original number
        new_number = original_number - 80
        
        # Construct the new filename
        new_filename = f"CN_word2-{new_number}.jpg"
        
        # Rename the file
        original_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        os.rename(original_file, new_file)
        print(f"Renamed '{filename}' to '{new_filename}'")