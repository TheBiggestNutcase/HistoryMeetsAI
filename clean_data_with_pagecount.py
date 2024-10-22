import json
import os
import requests
import urllib.parse
from datetime import datetime, timedelta

output_dir = "CleanedData"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJiYTAwMDZmMzNjM2U1OWJjMWRhZWZmNmNmZDY1MTQwZSIsImp0aSI6ImIyZTlkZGNjYmM0OTUxNDA3OTQwOWViNjRlNmNkMzczMDdjYTY3NjZjNzQwNjU2MDZlNmQwZTA2ZmE4ZmY3YTJhNDRkMDA2YWEzZDFjZWI4IiwiaWF0IjoxNzI4NDcwODQ4LjEwMDg0MSwibmJmIjoxNzI4NDcwODQ4LjEwMDg0NCwiZXhwIjozMzI4NTM3OTY0OC4wOTc5NDYsInN1YiI6Ijc2Njc2ODU0IiwiaXNzIjoiaHR0cHM6Ly9tZXRhLndpa2ltZWRpYS5vcmciLCJyYXRlbGltaXQiOnsicmVxdWVzdHNfcGVyX3VuaXQiOjUwMDAsInVuaXQiOiJIT1VSIn0sInNjb3BlcyI6WyJiYXNpYyJdfQ.HytyfR4avX0sH4cea-sZjs-um9QqclKGxLSKSQnyCVurK85e-BvEbU0g0291tPEFv3xS11nqVwqfwMxC4KHmr348eYGOTm0TMBVrbroQL3B3jKWeIfVt33JAqb-jmgKfd-eGhqFfhCMCZ0Ustse-KuxUjn_IxT4pm787FIdndLLx7Dt7sBLboNl2YxDUWKwD6woeubPRYTE1lv47CjXoSuSlsEYCgOuzmKM_Vz1xSZYAvX6VOV4-r2Ew8bfCt7_MMxLgB-1aPlwW8VlNVTUH3mc1h4w5kcfvit0EWPq4LbL27JaNXumVsRqjZ1Zen2wO2HybNLAoTmX3Hnir3OkcrmlRp1C84SPBZQcBVFLwjptk7mS4UvKSxcDgNxsc222Fueu82liy6VUR2t9318std3A1acLZe2KGYwrJMvk3ghWibP9fkLhUkhdfsLDefvmVw2_GJAjc_wjfZGrnqRp8jrZWRPAln_m0jAdGXlKSw4cqNa2TJjWUN_dLggAeXUGQrs4cS14Xo5p8G303TQ-QhDk06nBql_ZDhAarNWNJogoWWKKkrRjmesBy5P-3fc-JBpNmSCzgHax8iB84c7Dk1Kx1-h3sFLD2CG5DuM4YvyCQJIaMnUOi1tYwCB-JGHQuOYojt_fEuw46JjN5lq5G9a4IFQ1MOwvfQ-_vftZ9Jo8',
  'User-Agent': 'HistoryMeetsAI (blah2652@gmail.com)'
}

# Load Data from JSON Files
def load_data_from_json(data_dir):
    data_list = []
    # Sorted list of JSON files
    json_files = sorted([f for f in os.listdir(data_dir) if f.endswith(".json")])
    for filename in json_files:
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
            data_list.append((filename, data))
    return data_list

# Extract and Clean Event Data, Including Pageview-based Significance Factor
def clean_events(data_list):
    cleaned_data = []
    for filename, data in data_list:
        # Extract the date from the filename
        date_str = filename.replace(".json", "")
        day, month = date_str.split("-")

        print(f"{day}-{month} is being processed...")

        for category in ["selected", "events", "births", "deaths", "holidays"]:
            for item in data.get(category, []):
                year = item.get("year")
                text = item.get("text")
                pages = item.get("pages", [])
                
                if pages:
                    title = pages[0].get("title", "Unknown")
                    description = pages[0].get("description", "No description available")
                    article_url = pages[0].get("content_urls", {}).get("desktop", {}).get("page", "No URL available")
                    significance_factor = get_pageviews(title)
                else:
                    title = "Unknown"
                    description = "No description available"
                    article_url = "No URL available"
                    significance_factor = 0  # Default significance if no article is available
                
                # Only add the item if year and text are available
                if year and text:
                    cleaned_data.append({
                        "date": date_str,
                        "year": year,
                        "event": text,
                        "category": category,
                        "title": title,
                        "description": description,
                        "article_url": article_url,
                        "significance_factor": significance_factor
                    })

        print(f"{day}-{month} done processing")

    return cleaned_data

# Function to Get Pageviews from Wikipedia's Pageview API
def get_pageviews(article_title):
    """
    Uses the Wikimedia Pageview API to get the total views for an article in the last 30 days.
    You can adjust the start and end dates as needed.
    """
    base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
    
    # Parameters
    project = "en.wikipedia"
    access = "all-access"
    agent = "all-agents"
    granularity = "monthly"
    
    # URL encode the article title
    encoded_title = urllib.parse.quote(article_title)
    
    # Set the date range
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now().replace(day=1) - timedelta(days=30)).strftime('%Y%m%d')
    
    # Build the API URL
    url = f"{base_url}{project}/{access}/{agent}/{encoded_title}/{granularity}/{start_date}/{end_date}"
    
    try:
        # API request
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Get the total views from the response
        total_views = 0
        for item in data.get("items", []):
            total_views += item.get("views", 0)
        
        return total_views  # Return total pageviews as the significance factor
    except Exception as e:
        print(f"Error fetching pageviews for {article_title}: {e}")
        return 0  # Return 0 if there's an error

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

# Main function
def main():
    data_dir = "IndiaData"  # Directory with JSON files
    json_output_file = "CleanedData/cleaned_data.json"
    
    data_list = load_data_from_json(data_dir)
    cleaned_data = clean_events(data_list)
    cleaned_data = remove_duplicates(cleaned_data)
    cleaned_data = standardize_text(cleaned_data)
    cleaned_data = filter_missing_data(cleaned_data)
    save_to_json(cleaned_data, json_output_file)
    
    print("Data cleaning complete. Cleaned data with pageviews and categories saved to JSON.")

if __name__ == "__main__":
    main()
