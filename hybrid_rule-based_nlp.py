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

def find_events_by_category(events, input_date):
    matching_events = {
        "events": None,
        "births": None,
        "deaths": None,
        "holidays": None
    }
    
    for event in events:
        if event['date'] == input_date:
            category = event['category']
            if category in matching_events and (matching_events[category] is None or 
                                                event['significance_factor'] > matching_events[category]['significance_factor']):
                matching_events[category] = event
    
    return matching_events

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
        print("No event found for this category.")
    else:
        print(f"Date: {event['date']}-{event['year']}")
        print(f"Event: {event['event']}")
        print(f"Title: {event['title']}")
        print(f"Description: {event['description']}")
        print(f"Article URL: {event['article_url']}")
        print(f"Category: {event['category']}")
        print(f"Significance Factor: {event['significance_factor']}")
        print("Entities:")
        for entity_type, entity_text in event.get('entities', {}).items():
            print(f"  {entity_type}: {entity_text}")
    print()

def main():
    file_path = 'CleanedData/cleaned_data.json'  # Path to JSON file
    events = load_events(file_path)
    processed_events = preprocess_events(events)

    while True:
        query = input("Enter a date (MM-DD) or a question (or 'q' to quit): ")
        if query.lower() == 'q':
            break

        try:
            # Try to parse as date
            date = datetime.strptime(query, "%m-%d")
            events_by_category = find_events_by_category(processed_events, query)
            
            print("Events for this date:")
            for category in ["events", "births", "deaths", "holidays"]:
                print(f"\n{category.capitalize()}:")
                display_event(events_by_category[category])
        
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