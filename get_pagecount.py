import json
import os
import csv
import requests
import urllib.parse
from datetime import datetime, timedelta

headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJiYTAwMDZmMzNjM2U1OWJjMWRhZWZmNmNmZDY1MTQwZSIsImp0aSI6ImIyZTlkZGNjYmM0OTUxNDA3OTQwOWViNjRlNmNkMzczMDdjYTY3NjZjNzQwNjU2MDZlNmQwZTA2ZmE4ZmY3YTJhNDRkMDA2YWEzZDFjZWI4IiwiaWF0IjoxNzI4NDcwODQ4LjEwMDg0MSwibmJmIjoxNzI4NDcwODQ4LjEwMDg0NCwiZXhwIjozMzI4NTM3OTY0OC4wOTc5NDYsInN1YiI6Ijc2Njc2ODU0IiwiaXNzIjoiaHR0cHM6Ly9tZXRhLndpa2ltZWRpYS5vcmciLCJyYXRlbGltaXQiOnsicmVxdWVzdHNfcGVyX3VuaXQiOjUwMDAsInVuaXQiOiJIT1VSIn0sInNjb3BlcyI6WyJiYXNpYyJdfQ.HytyfR4avX0sH4cea-sZjs-um9QqclKGxLSKSQnyCVurK85e-BvEbU0g0291tPEFv3xS11nqVwqfwMxC4KHmr348eYGOTm0TMBVrbroQL3B3jKWeIfVt33JAqb-jmgKfd-eGhqFfhCMCZ0Ustse-KuxUjn_IxT4pm787FIdndLLx7Dt7sBLboNl2YxDUWKwD6woeubPRYTE1lv47CjXoSuSlsEYCgOuzmKM_Vz1xSZYAvX6VOV4-r2Ew8bfCt7_MMxLgB-1aPlwW8VlNVTUH3mc1h4w5kcfvit0EWPq4LbL27JaNXumVsRqjZ1Zen2wO2HybNLAoTmX3Hnir3OkcrmlRp1C84SPBZQcBVFLwjptk7mS4UvKSxcDgNxsc222Fueu82liy6VUR2t9318std3A1acLZe2KGYwrJMvk3ghWibP9fkLhUkhdfsLDefvmVw2_GJAjc_wjfZGrnqRp8jrZWRPAln_m0jAdGXlKSw4cqNa2TJjWUN_dLggAeXUGQrs4cS14Xo5p8G303TQ-QhDk06nBql_ZDhAarNWNJogoWWKKkrRjmesBy5P-3fc-JBpNmSCzgHax8iB84c7Dk1Kx1-h3sFLD2CG5DuM4YvyCQJIaMnUOi1tYwCB-JGHQuOYojt_fEuw46JjN5lq5G9a4IFQ1MOwvfQ-_vftZ9Jo8',
  'User-Agent': 'HistoryMeetsAI (blah2652@gmail.com)'
}

# 1. Load Data from JSON Files
def load_data_from_json(data_dir):
    data_list = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)
                data_list.append((filename, data))  # Storing the filename with the data
    return data_list

# 2. Extract and Clean Event Data, Including Pageview-based Significance Factor
def clean_events(data_list):
    cleaned_data = []
    for filename, data in data_list:
        # Extract the date from the filename
        date_str = filename.replace(".json", "")
        day, month = date_str.split("-")

        # Print message that the date is being processed
        print(f"{day}-{month} is being processed...")

        for event in data.get("events", []):
            year = event.get("year")
            text = event.get("text")  # The main event description
            pages = event.get("pages", [])
            
            # Get the first related page if available
            if pages:
                title = pages[0].get("title", "Unknown")
                description = pages[0].get("description", "No description available")
                article_url = pages[0].get("content_urls", {}).get("desktop", {}).get("page", "No URL available")
                
                # Call the function to get the pageview count from Wikimedia Pageview API
                significance_factor = get_pageviews(title)
            else:
                title = "Unknown"
                description = "No description available"
                article_url = "No URL available"
                significance_factor = 0  # Default significance if no article is available
            
            # Only add the event if year and text are available
            if year and text:
                cleaned_data.append({
                    "date": filename.replace(".json", ""),  # Use the filename as the date
                    "year": year,
                    "event": text,
                    "title": title,
                    "description": description,  # Include detailed event information
                    "article_url": article_url,  # Include article URL
                    "significance_factor": significance_factor  # Include significance factor based on pageviews
                })

        # Print message that the date has been processed
        print(f"{day}-{month} done processing")

    return cleaned_data

# 3. Function to Get Pageviews from Wikipedia's Pageview API
def get_pageviews(article_title):
    """
    Uses the Wikimedia Pageview API to get the total views for an article in the last 30 days.
    You can adjust the start and end dates as needed.
    """
    base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
    
    # Define parameters
    project = "en.wikipedia"
    access = "all-access"
    agent = "all-agents"
    granularity = "monthly"
    
    # URL encode the article title
    encoded_title = urllib.parse.quote(article_title)
    
    # Set the date range (adjust as needed)
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now().replace(day=1) - timedelta(days=30)).strftime('%Y%m%d')
    
    # Build the API URL
    url = f"{base_url}{project}/{access}/{agent}/{encoded_title}/{granularity}/{start_date}/{end_date}"
    
    try:
        # Make the API request
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

# 4. Remove Duplicates
def remove_duplicates(cleaned_data):
    seen_events = set()
    unique_data = []
    for entry in cleaned_data:
        event_key = (entry['year'], entry['event'])
        if event_key not in seen_events:
            seen_events.add(event_key)
            unique_data.append(entry)
    return unique_data

# 5. Standardize Text Formatting (title case)
def standardize_text(cleaned_data):
    for entry in cleaned_data:
        entry['event'] = entry['event'].title()
        entry['description'] = entry['description'].capitalize()
    return cleaned_data

# 6. Filter Out Entries with Missing Data
def filter_missing_data(cleaned_data):
    return [entry for entry in cleaned_data if entry.get('year') and entry.get('event')]

# 7. Save Cleaned Data as JSON
def save_to_json(cleaned_data, output_filename):
    with open(output_filename, 'w') as output_file:
        json.dump(cleaned_data, output_file, indent=4)

# 8. Save Cleaned Data to CSV
def save_to_csv(cleaned_data, output_filename):
    fieldnames = ['date', 'year', 'event', 'title', 'description', 'article_url', 'significance_factor']
    with open(output_filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in cleaned_data:
            writer.writerow(row)

# Main function to execute the data cleaning pipeline
def main():
    data_dir = "Data"  # Directory with JSON files
    json_output_file = "PageViews/pageviews.json"
    csv_output_file = "PageViews/pageviews.csv"
    
    # Step 1: Load data from JSON files
    data_list = load_data_from_json(data_dir)
    
    # Step 2: Clean and extract relevant fields (events with detailed info)
    cleaned_data = clean_events(data_list)
    
    # Step 3: Remove duplicate entries
    cleaned_data = remove_duplicates(cleaned_data)
    
    # Step 4: Standardize text (e.g., title case for event descriptions)
    cleaned_data = standardize_text(cleaned_data)
    
    # Step 5: Filter out entries with missing data (year, event)
    cleaned_data = filter_missing_data(cleaned_data)
    
    # Step 6: Save the cleaned data to a new JSON file
    save_to_json(cleaned_data, json_output_file)
    
    # Step 7: Save the cleaned data to a CSV file for analysis
    save_to_csv(cleaned_data, csv_output_file)
    
    print("Data cleaning complete. Cleaned data with pageviews saved to JSON and CSV.")

# Run the main function
if __name__ == "__main__":
    main()
