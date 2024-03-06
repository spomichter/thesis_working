import json
import numpy as np

# Get the file name of the JSON file from the user
json_file = "testset_annotations.json"

# Read the JSON data from the file
data = None
with open(json_file, 'r') as file:
    data = json.load(file)

annotations = []
# Iterate over each image in the JSON data
for image_data in data:
    image_path = image_data['image']
    index = image_path.index("test-images")
    image_path = image_path[index:]
    image_path = image_path.replace("X", "/")
    original_width = image_data['label'][0]['original_width']
    original_height = image_data['label'][0]['original_height']
    
    # Create a dictionary to store the bounding boxes for each label
    bounding_boxes = {}
    
    # Iterate over each annotation for the current image
    for annotation in image_data['label']:
        label = annotation['rectanglelabels'][0]
        
        # Extract the bounding box coordinates
        x = annotation['x']
        y = annotation['y']
        width = annotation['width']
        height = annotation['height']
        
        # Scale the coordinates to the original image dimensions
        x_scaled = int(x * original_width / 100)
        y_scaled = int(y * original_height / 100)
        width_scaled = int(width * original_width / 100)
        height_scaled = int(height * original_height / 100)
        
        # Calculate the xyxy coordinates
        x1 = x_scaled
        y1 = y_scaled
        x2 = x_scaled + width_scaled
        y2 = y_scaled + height_scaled
        
        # Add the bounding box coordinates to the dictionary
        if label not in bounding_boxes:
            bounding_boxes[label] = []
        bounding_boxes[label].append([x1, y1, x2, y2])
    
    annotations.append((image_path, bounding_boxes))
    # Print the bounding boxes for the current image
    print(f"Bounding Boxes for {image_path}:")
    for label, boxes in bounding_boxes.items():
        print(f"Label: {label}")
        for box in boxes:
            print(f"  - Coordinates: {box}")
    print()

ann_np = np.array(annotations)