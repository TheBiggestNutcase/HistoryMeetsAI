import pandas as pd
import json

# Load data from JSON or CSV
def load_data(file_path):
    if file_path.endswith('.json'):
        with open(file_path, 'r') as file:
            data = json.load(file)
    elif file_path.endswith('.csv'):
        data = pd.read_csv(file_path).to_dict(orient='records')
    return data

def find_events_by_date(data, input_date):
    events = []
    for entry in data:
        if entry['date'] == input_date:
            events.append({
                "year": entry['year'],
                "event": entry['event'],
                "description": entry['description'],
                "title": entry['title']
            })
    return events

def main():
    # Load the cleaned historical event data
    file_path = 'CleanedData/cleaned_data.csv'  # or cleaned_data_with_links.csv
    data = load_data(file_path)
    
    # Input date in the format dd-mm
    input_date = input("Enter a date (dd-mm): ")
    
    # Find events for the given date
    events = find_events_by_date(data, input_date)
    
    # Display the results
    if events:
        for event in events:
            print(f"Title: {event['title']}")
            print(f"Year: {event['year']}")
            print(f"Event: {event['event']}")
            print(f"Description: {event['description']}")
            print("\n")
    else:
        print("No events found for this date.")

if __name__ == "__main__":
    main()
