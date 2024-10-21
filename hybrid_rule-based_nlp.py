import json
from datetime import datetime
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def load_events(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def preprocess_events(events):
    for event in events:
        # Use NER to extract entities
        doc = nlp(event['event'])
        event['entities'] = {ent.label_: ent.text for ent in doc.ents}
        
        # Combine all text fields for better text matching
        event['full_text'] = f"{event['event']} {event['title']} {event['description']}"
    return events

def find_most_significant_event(events, input_date):
    matching_events = [event for event in events if event['date'] == input_date]
    if not matching_events:
        return None
    return max(matching_events, key=lambda x: x['significance_factor'])

def find_similar_events(events, query, top_n=5):
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    event_vectors = vectorizer.fit_transform([event['full_text'] for event in events])
    query_vector = vectorizer.transform([query])
    
    # Calculate cosine similarity
    similarities = cosine_similarity(query_vector, event_vectors).flatten()
    
    # Get top N similar events
    top_indices = similarities.argsort()[-top_n:][::-1]
    return [events[i] for i in top_indices]

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
        print("Entities:")
        for entity_type, entity_text in event.get('entities', {}).items():
            print(f"  {entity_type}: {entity_text}")

def main():
    file_path = 'CleanedData/cleaned_data.json'  # Update this with the actual path to your JSON file
    events = load_events(file_path)
    processed_events = preprocess_events(events)

    while True:
        query = input("Enter a date (MM-DD) or a question (or 'q' to quit): ")
        if query.lower() == 'q':
            break

        try:
            # Try to parse as date
            date = datetime.strptime(query, "%m-%d")
            most_significant_event = find_most_significant_event(processed_events, query)
            if most_significant_event:
                print("Most significant event for this date:")
                display_event(most_significant_event)
            else:
                print("No events found for the given date.")
        except ValueError:
            # If not a date, treat as a text query
            similar_events = find_similar_events(processed_events, query)
            print(f"Top {len(similar_events)} events related to your query:")
            for event in similar_events:
                display_event(event)
                print()

        print()

if __name__ == "__main__":
    main()