import json
from datetime import datetime

def load_events(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def find_most_significant_event(events, input_date):
    matching_events = [event for event in events if event['date'] == input_date]
    if not matching_events:
        return None
    return max(matching_events, key=lambda x: x['significance_factor'])

def display_event(event):
    if event is None:
        print("No events found for the given date.")
    else:
        print(f"Date: {event['date']}-{event['year']}")
        print(f"Event: {event['event']}")
        print(f"Title: {event['title']}")
        print(f"Description: {event['description']}")
        print(f"Article URL: {event['article_url']}")
        print(f"Significance Factor: {event['significance_factor']}")

def main():
    file_path = 'CleanedData/cleaned_data.json'  # Update this with the actual path to your JSON file
    events = load_events(file_path)

    while True:
        input_date = input("Enter a date in MM-DD format (or 'q' to quit): ")
        if input_date.lower() == 'q':
            break

        try:
            datetime.strptime(input_date, "%m-%d")
        except ValueError:
            print("Invalid date format. Please use MM-DD.")
            continue

        most_significant_event = find_most_significant_event(events, input_date)
        display_event(most_significant_event)
        print()

if __name__ == "__main__":
    main()