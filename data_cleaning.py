import json
import os
import csv

output_dir = "CleanedData"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load Data from JSON Files
def load_data_from_json(data_dir):
    data_list = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)
                data_list.append((filename, data))  # Storing the filename with the data
    return data_list

# Extract and Clean Event Data, Including Article Link
def clean_events(data_list):
    cleaned_data = []
    for filename, data in data_list:
        for event in data.get("events", []):
            year = event.get("year")
            text = event.get("text") 
            pages = event.get("pages", [])
            
            # Get the first related page if available
            if pages:
                title = pages[0].get("title", "Unknown")
                description = pages[0].get("description", "No description available")
                article_url = pages[0].get("content_urls", {}).get("desktop", {}).get("page", "No URL available")
            else:
                title = "Unknown"
                description = "No description available"
                article_url = "No URL available"
            
            # Only add the event if year and text are available
            if year and text:
                cleaned_data.append({
                    "date": filename.replace(".json", ""),  # Use the filename as the date
                    "year": year,
                    "event": text,
                    "title": title,
                    "description": description, 
                    "article_url": article_url  
                })
    return cleaned_data

# Remove Duplicates
def remove_duplicates(cleaned_data):
    seen_events = set()
    unique_data = []
    for entry in cleaned_data:
        event_key = (entry['year'], entry['event'])
        if event_key not in seen_events:
            seen_events.add(event_key)
            unique_data.append(entry)
    return unique_data

# Standardize Text Formatting (title case)
def standardize_text(cleaned_data):
    for entry in cleaned_data:
        entry['event'] = entry['event'].title()
        entry['description'] = entry['description'].capitalize()
    return cleaned_data

# Filter Out Entries with Missing Data
def filter_missing_data(cleaned_data):
    return [entry for entry in cleaned_data if entry.get('year') and entry.get('event')]

# Save Cleaned Data as JSON
def save_to_json(cleaned_data, output_filename):
    with open(output_filename, 'w') as output_file:
        json.dump(cleaned_data, output_file, indent=4)

# Save Cleaned Data to CSV
def save_to_csv(cleaned_data, output_filename):
    fieldnames = ['date', 'year', 'event', 'title', 'description', 'article_url']
    with open(output_filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in cleaned_data:
            writer.writerow(row)

# Main function to execute the data cleaning pipeline
def main():
    data_dir = "Data"  # Directory with JSON files
    json_output_file = "CleanedData/cleaned_data.json"
    csv_output_file = "CleanedData/cleaned_data.csv"
    
    #Load data from JSON files
    data_list = load_data_from_json(data_dir)
    
    # Clean and extract relevant fields (events with detailed info)
    cleaned_data = clean_events(data_list)
    
    # Remove duplicate entries
    cleaned_data = remove_duplicates(cleaned_data)
    
    # Standardize text (e.g., title case for event descriptions)
    cleaned_data = standardize_text(cleaned_data)
    
    # Filter out entries with missing data (year, event)
    cleaned_data = filter_missing_data(cleaned_data)
    
    # Save the cleaned data to a new JSON file
    save_to_json(cleaned_data, json_output_file)
    
    # Save the cleaned data to a CSV file for analysis
    save_to_csv(cleaned_data, csv_output_file)
    
    print("Data cleaning complete. Cleaned data with article links saved to JSON and CSV.")

if __name__ == "__main__":
    main()
