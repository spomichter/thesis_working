import os
import shutil
import re

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)

def copy_image_files():
    current_dir = "/home/yashas/Documents/thesis/test-images/"
    # current_dir = os.getcwd()
    first_images_dir = os.path.join(current_dir, "first_images")
    
    # Create the "first_images" directory if it doesn't exist
    if not os.path.exists(first_images_dir):
        os.makedirs(first_images_dir)
    
    image_dirs = []
    # Traverse the current directory and its subdirectories
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            # print(f"Checking: {file}")
            if file == "im_0.jpg":
                # Get the original path of the file
                original_path = os.path.join(root, file)

                if "images0" in original_path:
                    image_dirs.append(root)
                    print(f"Found: {original_path}")
                
                    # Replace "/" with "," in the original path to create the new file name
                    new_file_name = original_path.replace("/", ",")
                    
                    # Construct the destination path for the copied file
                    destination_path = os.path.join(first_images_dir, new_file_name)
                    
                    # Copy the file to the "first_images" directory with the new file name
                    shutil.copy2(original_path, destination_path)
                    print(f"Copied: {original_path} -> {destination_path}")
    
    print(f"Found {len(image_dirs)} images in {current_dir}")
    
    image_dirs = sorted_alphanumeric(image_dirs)
    image_dirs_path = os.path.join(current_dir, "image_dirs.txt")
    # save image_dirs to a file
    with open(image_dirs_path, 'w') as file:
        for image_dir in image_dirs:
            file.write(image_dir + "\n")

# Run the script
copy_image_files()