import json
import os
from typing import Dict, Any, List

output_dir = "ExtractedData"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def extract_event_details(directory_path: str) -> List[Dict[str, Any]]:
    all_events = []

    try:
        # Iterate through all files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith('.json'):
                file_path = os.path.join(directory_path, filename)
                
                # Read the JSON data from the file
                with open(file_path, 'r') as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file: {filename}")
                        continue

                # Process each event in the 'selected' array
                for event in data.get("selected", []):
                    year = event.get("year")
                    event_text = event.get("text")
                    
                    if year is None or event_text is None:
                        print(f"Missing year or text in an event in file: {filename}")
                        continue

                    # Extract information from related pages
                    related_pages = []
                    for page in event.get("pages", []):
                        page_info = {
                            "title": page.get("title", "No title"),
                            "description": page.get("description", "No description available"),
                            "extract": page.get("extract", "No extract available")
                        }
                        related_pages.append(page_info)

                    # Construct the event dictionary
                    event_dict = {
                        "year": year,
                        "event_text": event_text,
                        "related_pages": related_pages,
                        "source_file": filename
                    }

                    all_events.append(event_dict)
                    
                # Process each event in the 'births' array
                for event in data.get("births", []):
                    year = event.get("year")
                    event_text = event.get("text")
                    
                    if year is None or event_text is None:
                        print(f"Missing year or text in an event in file: {filename}")
                        continue

                    # Extract information from related pages
                    related_pages = []
                    for page in event.get("pages", []):
                        page_info = {
                            "title": page.get("title", "No title"),
                            "description": page.get("description", "No description available"),
                            "extract": page.get("extract", "No extract available")
                        }
                        related_pages.append(page_info)

                    # Construct the event dictionary
                    event_dict = {
                        "year": year,
                        "event_text": event_text,
                        "related_pages": related_pages,
                        "source_file": filename
                    }

                    all_events.append(event_dict)

                # Process each event in the 'deaths' array
                for event in data.get("deaths", []):
                    year = event.get("year")
                    event_text = event.get("text")
                    
                    if year is None or event_text is None:
                        print(f"Missing year or text in an event in file: {filename}")
                        continue

                    # Extract information from related pages
                    related_pages = []
                    for page in event.get("pages", []):
                        page_info = {
                            "title": page.get("title", "No title"),
                            "description": page.get("description", "No description available"),
                            "extract": page.get("extract", "No extract available")
                        }
                        related_pages.append(page_info)

                    # Construct the event dictionary
                    event_dict = {
                        "year": year,
                        "event_text": event_text,
                        "related_pages": related_pages,
                        "source_file": filename
                    }

                    all_events.append(event_dict)
                    
                # Process each event in the 'events' array
                for event in data.get("events", []):
                    year = event.get("year")
                    event_text = event.get("text")
                    
                    if year is None or event_text is None:
                        print(f"Missing year or text in an event in file: {filename}")
                        continue

                    # Extract information from related pages
                    related_pages = []
                    for page in event.get("pages", []):
                        page_info = {
                            "title": page.get("title", "No title"),
                            "description": page.get("description", "No description available"),
                            "extract": page.get("extract", "No extract available")
                        }
                        related_pages.append(page_info)

                    # Construct the event dictionary
                    event_dict = {
                        "year": year,
                        "event_text": event_text,
                        "related_pages": related_pages,
                        "source_file": filename
                    }

                    all_events.append(event_dict)

                # Process each event in the 'holidays' array
                for event in data.get("holidays", []):
                    # year = event.get("year")
                    event_text = event.get("text")
                    
                    if event_text is None:
                        print(f"Missing year or text in an event in file: {filename}")
                        continue

                    # Extract information from related pages
                    related_pages = []
                    for page in event.get("pages", []):
                        page_info = {
                            "title": page.get("title", "No title"),
                            "description": page.get("description", "No description available"),
                            "extract": page.get("extract", "No extract available")
                        }
                        related_pages.append(page_info)

                    # Construct the event dictionary
                    event_dict = {
                        # "year": year,
                        "event_text": event_text,
                        "related_pages": related_pages,
                        "source_file": filename
                    }

                    all_events.append(event_dict)

        return all_events

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def save_to_json(data: List[Dict[str, Any]], output_file: str):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

# Example usage
if __name__ == "__main__":
    directory_path = 'Data'  # Replace with your actual directory path
    output_file = 'ExtractedData/extracted_events.json'  # Name of the output file

    extracted_data = extract_event_details(directory_path)
    
    if extracted_data:
        save_to_json(extracted_data, output_file)
        print(f"Extracted {len(extracted_data)} events. Data saved to {output_file}")
    else:
        print("No data was extracted.")

    # # Print the first event as an example
    # if extracted_data:
    #     print("\nExample of extracted event:")
    #     print(json.dumps(extracted_data[0], indent=2))