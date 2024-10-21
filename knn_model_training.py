import json
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def load_cleaned_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
        return []

def prepare_data(data):
    X = []
    y = []
    significance_factors = []
    
    for entry in data:
        # Input: date in dd-mm format
        X.append(entry['date'])
        
        # Output: event description (as labels)
        y.append(entry['event'])
        
        # Store the significance factor for ranking later
        significance_factors.append(entry['significance_factor'])
    
    return X, y, significance_factors

def preprocess_data(X, y):
    label_encoder_X = LabelEncoder()
    label_encoder_y = LabelEncoder()
    
    X_encoded = label_encoder_X.fit_transform(X)
    y_encoded = label_encoder_y.fit_transform(y)
    
    return X_encoded, y_encoded, label_encoder_X, label_encoder_y

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X.reshape(-1, 1), y, test_size=0.2, random_state=42)
    
    knn = KNeighborsClassifier(n_neighbors=5)
    
    knn.fit(X_train, y_train)
    
    return knn, X_test, y_test

def predict_events(date, knn, label_encoder_X, label_encoder_y, significance_factors, data):
    try:
        encoded_date = label_encoder_X.transform([date])[0]
    except ValueError:
        print(f"Error: The date '{date}' is not recognized.")
        return []

    event_indices = knn.kneighbors([[encoded_date]], n_neighbors=5, return_distance=False)[0]
    
    predicted_events = []
    for index in event_indices:
        event = data[index]
        predicted_events.append({
            'event': event['event'],
            'year': event['year'],
            'description': event['description'],
            'significance_factor': event['significance_factor'],
            'article_url': event['article_url']
        })
    
    ranked_events = sorted(predicted_events, key=lambda x: x['significance_factor'], reverse=True)
    
    return ranked_events

def main():
    data_filename = "CleanedData/cleaned_data.json"
    data = load_cleaned_data(data_filename)
    
    if not data:
        return  # Exit if no data is loaded
    
    X, y, significance_factors = prepare_data(data)
    
    X_encoded, y_encoded, label_encoder_X, label_encoder_y = preprocess_data(X, y)
    
    knn, X_test, y_test = train_model(X_encoded, y_encoded)
    
    while True:
        input_date = input("Enter a date (mm-dd) or 'quit' to quit: ")
        if input_date.lower() == 'quit':
            break
        predicted_events = predict_events(input_date, knn, label_encoder_X, label_encoder_y, significance_factors, data)
        
        if predicted_events:
            for event in predicted_events:
                print("-------------------------")
                print(f"Event: {event['event']}")
                print(f"Year: {event['year']}")
                print(f"Description: {event['description']}")
                print(f"Significance Factor: {event['significance_factor']}")
                print(f"Article URL: {event['article_url']}")
                print("-------------------------")
        else:
            print(f"No events found for the date '{input_date}'.")

if __name__ == "__main__":
    main()
