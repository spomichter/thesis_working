import json

# Read the text file
with open('tokens_over_time.txt', 'r') as file:
    lines = file.readlines()

# Initialize an empty list to store the JSON objects
json_data = []

num_input_frames = 3
num_output_frames = 1
reverse = False
# Iterate through the lines using a sliding window of size 3
for i in range(len(lines) - num_input_frames-1):
    # Construct the input string with line numbers
    input_lines = []
    for j in range(num_input_frames):
        if reverse:
            k = num_input_frames- 1 - j
        else:
            k = j
        if i + j < len(lines):
            line = lines[i + k].strip().replace('"', '').replace("'", "").replace("\n", " ")
            input_lines.append(f"frame t-{num_input_frames - k - 1}: {line}")
    
    # Get the next two lines for the output
    output_lines = []
    for j in range(num_output_frames):
        if i + num_input_frames + j < len(lines):
            line = lines[i + num_input_frames + j].strip().replace('"', '').replace("'", "").replace("\n", " ")
            output_lines.append(f"frame t+{j+1}: {line}")
    
    # Create a JSON object with the current sliding window and output lines
    json_object = {
        "instruction": "Given the following few token representations of a visual frame in the following format 'frame t-0: [{{object_id, {{centroid_x, centroid_y}},num_radial_points,radial_points}}]', predict the next two frames in the following format 'frame t+0: [{{object_id, {{centroid_x, centroid_y}},num_radial_points,radial_points}}]' and 'frame t+1: [{{object_id, {{centroid_x, centroid_y}},num_radial_points,radial_points",
        "input": "\n".join(input_lines),
        "output": "\n".join(output_lines)
    }
    
    # Append the JSON object to the list
    json_data.append(json_object)

# Write the JSON data to a file
with open('input.json', 'w') as file:
    json.dump(json_data, file, indent=2)