import requests

# Define the Wikipedia article title and the date range
article_title = 'Python_(programming_language)'
start_date = '20230901'  # Format: YYYYMMDD
end_date = '20230930'    # Format: YYYYMMDD

headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJiYTAwMDZmMzNjM2U1OWJjMWRhZWZmNmNmZDY1MTQwZSIsImp0aSI6ImIyZTlkZGNjYmM0OTUxNDA3OTQwOWViNjRlNmNkMzczMDdjYTY3NjZjNzQwNjU2MDZlNmQwZTA2ZmE4ZmY3YTJhNDRkMDA2YWEzZDFjZWI4IiwiaWF0IjoxNzI4NDcwODQ4LjEwMDg0MSwibmJmIjoxNzI4NDcwODQ4LjEwMDg0NCwiZXhwIjozMzI4NTM3OTY0OC4wOTc5NDYsInN1YiI6Ijc2Njc2ODU0IiwiaXNzIjoiaHR0cHM6Ly9tZXRhLndpa2ltZWRpYS5vcmciLCJyYXRlbGltaXQiOnsicmVxdWVzdHNfcGVyX3VuaXQiOjUwMDAsInVuaXQiOiJIT1VSIn0sInNjb3BlcyI6WyJiYXNpYyJdfQ.HytyfR4avX0sH4cea-sZjs-um9QqclKGxLSKSQnyCVurK85e-BvEbU0g0291tPEFv3xS11nqVwqfwMxC4KHmr348eYGOTm0TMBVrbroQL3B3jKWeIfVt33JAqb-jmgKfd-eGhqFfhCMCZ0Ustse-KuxUjn_IxT4pm787FIdndLLx7Dt7sBLboNl2YxDUWKwD6woeubPRYTE1lv47CjXoSuSlsEYCgOuzmKM_Vz1xSZYAvX6VOV4-r2Ew8bfCt7_MMxLgB-1aPlwW8VlNVTUH3mc1h4w5kcfvit0EWPq4LbL27JaNXumVsRqjZ1Zen2wO2HybNLAoTmX3Hnir3OkcrmlRp1C84SPBZQcBVFLwjptk7mS4UvKSxcDgNxsc222Fueu82liy6VUR2t9318std3A1acLZe2KGYwrJMvk3ghWibP9fkLhUkhdfsLDefvmVw2_GJAjc_wjfZGrnqRp8jrZWRPAln_m0jAdGXlKSw4cqNa2TJjWUN_dLggAeXUGQrs4cS14Xo5p8G303TQ-QhDk06nBql_ZDhAarNWNJogoWWKKkrRjmesBy5P-3fc-JBpNmSCzgHax8iB84c7Dk1Kx1-h3sFLD2CG5DuM4YvyCQJIaMnUOi1tYwCB-JGHQuOYojt_fEuw46JjN5lq5G9a4IFQ1MOwvfQ-_vftZ9Jo8',
  'User-Agent': 'HistoryMeetsAI (blah2652@gmail.com)'
}

# Construct the URL for the Pageviews API
url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start_date}/{end_date}'

# Send the GET request to the API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Print total page views for each day
    for item in data['items']:
        date = item['timestamp']
        views = item['views']
        print(f"Date: {date[:4]}-{date[4:6]}-{date[6:8]}, Pageviews: {views}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
