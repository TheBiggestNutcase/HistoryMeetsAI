import json
import os
from pathlib import Path

def filter_india_data(input_file, output_file):
    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Initialize the filtered data structure
    filtered_data = {
        "selected": [],
        "events": [],
        "births": [],
        "deaths": [],
        "holidays": []
    }
    
    # Filter the 'selected' array
    for item in data.get("selected", []):
        if "text" in item and "India" in item["text"]:
            filtered_data["selected"].append(item)
    
    # Filter the other arrays
    for key in ["events", "births", "deaths", "holidays"]:
        for item in data.get(key, []):
            if "text" in item and "India" in item["text"]:
                filtered_data[key].append(item)
    
    # Write the filtered data to the output JSON file
    with open(output_file, 'w') as f:
        json.dump(filtered_data, f, indent=2)

    print(f"Filtered data has been saved to {output_file}")

def process_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Process each JSON file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{filename}")
            filter_india_data(input_path, output_path)

# Usage
input_folder = "Data"  # Replace with your input folder path
output_folder = "IndiaData"  # Replace with your desired output folder path
process_folder(input_folder, output_folder)