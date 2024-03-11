import json
import os

def process_file(file_path, num_input_frames, num_output_frames, reverse):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    lang_prompt_loc = file_path.replace("images0/tokens_over_time.txt", "lang.txt")
    with open(lang_prompt_loc, 'r') as file:
        lang_prompt = file.read().splitlines()
    lang_prompt = lang_prompt[0]
    lang_prompt = lang_prompt.replace('"', '').replace("'", "").replace("\n", "")
    # print(lang_prompt)

    json_data = []

    for i in range(len(lines) - num_input_frames - 1):
        input_lines = []
        input_lines.append(lang_prompt)
        for j in range(num_input_frames):
            k = num_input_frames - 1 - j if reverse else j
            if i + j < len(lines):
                line = lines[i + k].strip().replace('"', '').replace("'", "").replace("\n", " ")
                input_lines.append(f"frame t-{num_input_frames - k - 1}: {line}")

        output_lines = []
        for j in range(num_output_frames):
            if i + num_input_frames + j < len(lines):
                line = lines[i + num_input_frames + j].strip().replace('"', '').replace("'", "").replace("\n", " ")
                output_lines.append(f"frame t+{j+1}: {line}")

        json_object = {
            "instruction": "Given a language description of the task in the frame sequence and the following few token representations of a visual frame in the following format 'frame t-0: [{{object_id, {{centroid_x, centroid_y}},radial_points}}]', predict the next two frames in the following format 'frame t+0: [{{object_id, {{centroid_x, centroid_y}},radial_points}}]'",
            "input": "\n".join(input_lines),
            "output": "\n".join(output_lines)
        }

        json_data.append(json_object)

    return json_data

# Read the file containing paths to tokens_over_time.txt files
with open("/home/yashas/Documents/thesis/test-images/eval_image_dirs.txt", "r") as file:
    file_paths = file.read().splitlines()

file_paths = [path + "/tokens_over_time.txt" for path in file_paths]

num_input_frames = 3
num_output_frames = 1
reverse = False

combined_json_data = []

for file_path in file_paths:
    file_path = file_path.strip()
    json_data = process_file(file_path, num_input_frames, num_output_frames, reverse)

    # Write individual JSON file for each tokens_over_time.txt file
    # output_file_name = os.path.splitext(os.path.basename(file_path))[0] + '.json'
    output_file_name = file_path.replace(".txt", ".json")
    with open(output_file_name, 'w') as file:
        json.dump(json_data, file, indent=2)

    combined_json_data.extend(json_data)

print("Number of examples:", len(combined_json_data))
print("Processed files: ", len(file_paths))

# Write the combined JSON file
with open('combined_output.json', 'w') as file:
    json.dump(combined_json_data, file, indent=2)