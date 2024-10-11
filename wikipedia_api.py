# Python 3
# Get information about this day in history from English Wikipedia

import datetime
import requests
import json
import time
import os

# Wikimedia API URL for "On This Day" data
base_url = 'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/'

# Headers with authentication token and user agent
headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJiYTAwMDZmMzNjM2U1OWJjMWRhZWZmNmNmZDY1MTQwZSIsImp0aSI6ImIyZTlkZGNjYmM0OTUxNDA3OTQwOWViNjRlNmNkMzczMDdjYTY3NjZjNzQwNjU2MDZlNmQwZTA2ZmE4ZmY3YTJhNDRkMDA2YWEzZDFjZWI4IiwiaWF0IjoxNzI4NDcwODQ4LjEwMDg0MSwibmJmIjoxNzI4NDcwODQ4LjEwMDg0NCwiZXhwIjozMzI4NTM3OTY0OC4wOTc5NDYsInN1YiI6Ijc2Njc2ODU0IiwiaXNzIjoiaHR0cHM6Ly9tZXRhLndpa2ltZWRpYS5vcmciLCJyYXRlbGltaXQiOnsicmVxdWVzdHNfcGVyX3VuaXQiOjUwMDAsInVuaXQiOiJIT1VSIn0sInNjb3BlcyI6WyJiYXNpYyJdfQ.HytyfR4avX0sH4cea-sZjs-um9QqclKGxLSKSQnyCVurK85e-BvEbU0g0291tPEFv3xS11nqVwqfwMxC4KHmr348eYGOTm0TMBVrbroQL3B3jKWeIfVt33JAqb-jmgKfd-eGhqFfhCMCZ0Ustse-KuxUjn_IxT4pm787FIdndLLx7Dt7sBLboNl2YxDUWKwD6woeubPRYTE1lv47CjXoSuSlsEYCgOuzmKM_Vz1xSZYAvX6VOV4-r2Ew8bfCt7_MMxLgB-1aPlwW8VlNVTUH3mc1h4w5kcfvit0EWPq4LbL27JaNXumVsRqjZ1Zen2wO2HybNLAoTmX3Hnir3OkcrmlRp1C84SPBZQcBVFLwjptk7mS4UvKSxcDgNxsc222Fueu82liy6VUR2t9318std3A1acLZe2KGYwrJMvk3ghWibP9fkLhUkhdfsLDefvmVw2_GJAjc_wjfZGrnqRp8jrZWRPAln_m0jAdGXlKSw4cqNa2TJjWUN_dLggAeXUGQrs4cS14Xo5p8G303TQ-QhDk06nBql_ZDhAarNWNJogoWWKKkrRjmesBy5P-3fc-JBpNmSCzgHax8iB84c7Dk1Kx1-h3sFLD2CG5DuM4YvyCQJIaMnUOi1tYwCB-JGHQuOYojt_fEuw46JjN5lq5G9a4IFQ1MOwvfQ-_vftZ9Jo8',
  'User-Agent': 'HistoryMeetsAI (blah2652@gmail.com)'
}

# Create a directory named "Data" if it doesn't exist
output_dir = "Data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def fetch_and_save_data(month, day, retries=3):
    # Format the date as MM/DD
    date = f"{month:02d}/{day:02d}"
    
    print(f"For {date}")

    # Construct the URL for the specific day
    url = base_url + date
    
    attempt = 0
    while attempt < retries:
        try:
            # Send request to Wikimedia API
            response = requests.get(url, headers=headers)
            
            # Check if the response is successful (status code 200)
            if response.status_code == 200:
                print(f"200 for {date}")
                # Parse the JSON response
                data = response.json()
                
                # Define the filename using the date (MM-DD.json)
                filename = f"{output_dir}/{month:02d}-{day:02d}.json"
                
                # Save the JSON response to the "Data" directory
                with open(filename, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                
                print(f"Data saved to {filename}")
                return  # Exit the function if successful
            elif response.status_code == 500:
                # Log the retry attempt for error 500
                print(f"Encountered 500 error for {date}. Retrying {attempt+1}/{retries}...")
                attempt += 1
                time.sleep(1)  # Delay before retrying to avoid hammering the server
            else:
                # If the error code is not 500, log and skip
                print(f"Skipping {date}, response code: {response.status_code}")
                return
        
        except Exception as e:
            # Handle other types of errors (e.g., connection issues)
            print(f"Error for {date}: {e}")
            return
        
        if attempt >= retries:
            print(f"Skipped {date}")

# Iterate through all months and days of the year
for month in range(1, 3):  # Loop over months from 1 to 12
    for day in range(1, 32):  # Loop over days from 1 to 31
        try:
            # Fetch and save data for the given month and day
            fetch_and_save_data(month, day)
        
        except Exception as e:
            # Handle any unexpected errors during the iteration
            print(f"Unexpected error for {month:02d}/{day:02d}: {e}")
